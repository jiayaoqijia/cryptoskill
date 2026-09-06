#!/usr/bin/env python3
"""Kubernetes Manifest Security Auditor.

Static analysis (no cluster access) for common Kubernetes YAML security and
reliability risks.

Input is provided via --params JSON or stdin JSON; output is always JSON.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


SEVERITY_ORDER: Dict[str, int] = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
SEVERITY_WEIGHT: Dict[str, int] = {"CRITICAL": 35, "HIGH": 20, "MEDIUM": 10, "LOW": 4}


def _json_dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)


def _success(data: Dict[str, Any]) -> str:
    return _json_dumps({"ok": True, "data": data})


def _error(message: str, details: Optional[Dict[str, Any]] = None) -> str:
    payload: Dict[str, Any] = {"ok": False, "error": message}
    if details is not None:
        payload["details"] = details
    return _json_dumps(payload)


def _read_stdin_json() -> Optional[Dict[str, Any]]:
    if sys.stdin is None or sys.stdin.isatty():
        return None
    raw = sys.stdin.read().strip()
    if not raw:
        return None
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("stdin JSON must be an object")
    return parsed


def _load_yaml(manifests_yaml: str) -> List[Any]:
    try:
        import yaml  # type: ignore
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "PyYAML is required. Install with: pip install -r requirements.txt"
        ) from e

    try:
        docs = list(yaml.safe_load_all(manifests_yaml))
    except Exception as e:
        raise ValueError(f"Failed to parse YAML: {e}")

    return docs


def _get(d: Any, path: Sequence[str], default: Any = None) -> Any:
    cur = d
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            return default
        cur = cur[p]
    return cur


def _kind_pod_spec(doc: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], str]:
    kind = str(doc.get("kind") or "")

    if kind == "Pod":
        return doc.get("spec") if isinstance(doc.get("spec"), dict) else {}, "spec"

    if kind in {"Deployment", "StatefulSet", "DaemonSet", "ReplicaSet"}:
        spec = _get(doc, ["spec", "template", "spec"], {})
        return spec if isinstance(spec, dict) else {}, "spec.template.spec"

    if kind == "Job":
        spec = _get(doc, ["spec", "template", "spec"], {})
        return spec if isinstance(spec, dict) else {}, "spec.template.spec"

    if kind == "CronJob":
        spec = _get(doc, ["spec", "jobTemplate", "spec", "template", "spec"], {})
        return spec if isinstance(spec, dict) else {}, "spec.jobTemplate.spec.template.spec"

    return None, ""


def _image_tag_risky(image: str) -> bool:
    if not image:
        return False
    if "@" in image:
        # Digest pinned is best practice.
        return False

    # Handle registries with ports: "registry:5000/repo/image"
    last_slash = image.rfind("/")
    tail = image[last_slash + 1 :]
    if ":" not in tail:
        # No tag provided -> implicitly latest
        return True

    tag = tail.split(":", 1)[1]
    return tag.lower() == "latest" or tag == ""


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    resource: Dict[str, str]
    message: str
    remediation: str
    path: str
    container: Optional[str] = None

    def to_json(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "resource": self.resource,
            "message": self.message,
            "path": self.path,
            "remediation": self.remediation,
        }
        if self.container is not None:
            out["container"] = self.container
        return out


def analyze(manifests_yaml: str, *, ruleset: str, max_findings: int) -> Dict[str, Any]:
    docs = _load_yaml(manifests_yaml)

    findings: List[Finding] = []
    resources_scanned = 0

    for i, doc in enumerate(docs):
        if not isinstance(doc, dict):
            continue

        kind = str(doc.get("kind") or "")
        if not kind:
            continue

        meta = doc.get("metadata") if isinstance(doc.get("metadata"), dict) else {}
        name = str(meta.get("name") or f"<unnamed-{i}>")
        namespace = str(meta.get("namespace") or "default")

        pod_spec, pod_spec_path = _kind_pod_spec(doc)
        if pod_spec is None:
            continue

        resources_scanned += 1

        res = {"kind": kind, "name": name, "namespace": namespace}

        # Spec-level security flags
        host_network = bool(pod_spec.get("hostNetwork") is True)
        host_pid = bool(pod_spec.get("hostPID") is True)
        host_ipc = bool(pod_spec.get("hostIPC") is True)
        if host_network or host_pid or host_ipc:
            flags = []
            if host_network:
                flags.append("hostNetwork")
            if host_pid:
                flags.append("hostPID")
            if host_ipc:
                flags.append("hostIPC")
            findings.append(
                Finding(
                    rule_id="SEC_HOST_NETWORK",
                    severity="HIGH",
                    resource=res,
                    container=None,
                    message="Host namespace sharing enabled: " + ", ".join(flags),
                    path=f"{pod_spec_path}.hostNetwork/hostPID/hostIPC",
                    remediation="Disable hostNetwork/hostPID/hostIPC unless strictly required.",
                )
            )

        volumes = pod_spec.get("volumes") if isinstance(pod_spec.get("volumes"), list) else []
        for vi, v in enumerate(volumes):
            if isinstance(v, dict) and "hostPath" in v:
                findings.append(
                    Finding(
                        rule_id="SEC_HOSTPATH",
                        severity="HIGH",
                        resource=res,
                        container=None,
                        message="hostPath volume detected",
                        path=f"{pod_spec_path}.volumes[{vi}].hostPath",
                        remediation="Avoid hostPath when possible; use PVCs. If required, restrict path and readOnly.",
                    )
                )
                break

        pod_sc = pod_spec.get("securityContext") if isinstance(pod_spec.get("securityContext"), dict) else {}

        containers = pod_spec.get("containers") if isinstance(pod_spec.get("containers"), list) else []
        for ci, c in enumerate(containers):
            if not isinstance(c, dict):
                continue
            cname = str(c.get("name") or f"container-{ci}")
            cpath = f"{pod_spec_path}.containers[{ci}]"

            csc = c.get("securityContext") if isinstance(c.get("securityContext"), dict) else {}

            # privileged
            if csc.get("privileged") is True:
                findings.append(
                    Finding(
                        rule_id="SEC_PRIVILEGED",
                        severity="CRITICAL",
                        resource=res,
                        container=cname,
                        message="Container is privileged",
                        path=f"{cpath}.securityContext.privileged",
                        remediation="Set privileged: false and drop unnecessary capabilities.",
                    )
                )

            # runAsNonRoot
            effective_run_as_non_root = csc.get("runAsNonRoot")
            if effective_run_as_non_root is None:
                effective_run_as_non_root = pod_sc.get("runAsNonRoot")
            if effective_run_as_non_root is not True:
                findings.append(
                    Finding(
                        rule_id="SEC_RUN_AS_ROOT",
                        severity="MEDIUM",
                        resource=res,
                        container=cname,
                        message="runAsNonRoot is not set to true",
                        path=f"{cpath}.securityContext.runAsNonRoot",
                        remediation="Set runAsNonRoot: true and use a non-root USER in the image.",
                    )
                )

            # allowPrivilegeEscalation
            if csc.get("allowPrivilegeEscalation") is not False:
                findings.append(
                    Finding(
                        rule_id="SEC_ALLOW_PRIV_ESC",
                        severity="MEDIUM",
                        resource=res,
                        container=cname,
                        message="allowPrivilegeEscalation is not set to false",
                        path=f"{cpath}.securityContext.allowPrivilegeEscalation",
                        remediation="Set allowPrivilegeEscalation: false.",
                    )
                )

            # resource requests/limits
            resources = c.get("resources") if isinstance(c.get("resources"), dict) else {}
            req = resources.get("requests") if isinstance(resources.get("requests"), dict) else None
            lim = resources.get("limits") if isinstance(resources.get("limits"), dict) else None
            if req is None or lim is None:
                sev = "LOW" if ruleset == "baseline" else "MEDIUM"
                missing = []
                if req is None:
                    missing.append("requests")
                if lim is None:
                    missing.append("limits")
                findings.append(
                    Finding(
                        rule_id="REL_NO_LIMITS",
                        severity=sev,
                        resource=res,
                        container=cname,
                        message="Resource requests/limits missing: " + ", ".join(missing),
                        path=f"{cpath}.resources",
                        remediation="Set cpu/memory requests and limits to improve stability and scheduling.",
                    )
                )

            # latest tag
            image = str(c.get("image") or "")
            if _image_tag_risky(image):
                findings.append(
                    Finding(
                        rule_id="SUPPLY_CHAIN_LATEST_TAG",
                        severity="LOW",
                        resource=res,
                        container=cname,
                        message="Image tag is ':latest' or missing (non-reproducible deployments)",
                        path=f"{cpath}.image",
                        remediation="Pin a version tag or (preferably) an image digest.",
                    )
                )

    findings.sort(
        key=lambda f: (
            SEVERITY_ORDER.get(f.severity, 999),
            f.resource.get("kind", ""),
            f.resource.get("namespace", ""),
            f.resource.get("name", ""),
            f.container or "",
            f.rule_id,
        )
    )

    if max_findings < 1:
        max_findings = 1
    findings = findings[: max_findings]

    by_sev = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for f in findings:
        if f.severity in by_sev:
            by_sev[f.severity] += 1

    risk_score = min(100, sum(SEVERITY_WEIGHT.get(f.severity, 0) for f in findings))

    if by_sev["CRITICAL"]:
        risk_level = "CRITICAL"
    elif by_sev["HIGH"]:
        risk_level = "HIGH"
    elif by_sev["MEDIUM"]:
        risk_level = "MEDIUM"
    elif by_sev["LOW"]:
        risk_level = "LOW"
    else:
        risk_level = "LOW"

    return {
        "summary": {
            "documents": len(docs),
            "resources_scanned": resources_scanned,
            "findings_total": len(findings),
            "by_severity": by_sev,
        },
        "risk_score": int(risk_score),
        "risk_level": risk_level,
        "findings": [f.to_json() for f in findings],
    }


DEMO_YAML = """\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: nginx:latest
          securityContext:
            privileged: true
          # resources intentionally omitted
---
apiVersion: v1
kind: Pod
metadata:
  name: debug-pod
spec:
  hostNetwork: true
  containers:
    - name: shell
      image: alpine
      command: ["sh", "-c", "sleep 3600"]
      securityContext:
        allowPrivilegeEscalation: true
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: file-writer
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: file-writer
    spec:
      volumes:
        - name: host
          hostPath:
            path: /var/log
      containers:
        - name: writer
          image: alpine:3.19
          command: ["sh", "-c", "echo hi > /mnt/host/test && sleep 3600"]
          volumeMounts:
            - name: host
              mountPath: /mnt/host
          resources:
            requests:
              cpu: "50m"
              memory: "64Mi"
            limits:
              cpu: "200m"
              memory: "256Mi"
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint Kubernetes YAML manifests for security risks")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")
    parser.add_argument("--params", type=str, help="JSON parameters")
    args = parser.parse_args()

    try:
        if args.demo:
            report = analyze(DEMO_YAML, ruleset="restricted", max_findings=200)
            report["demo"] = True
            print(_success(report))
            return 0

        if args.params:
            params = json.loads(args.params)
            if not isinstance(params, dict):
                raise ValueError("--params JSON must be an object")
        else:
            stdin_params = _read_stdin_json()
            if stdin_params is None:
                print(_error("Either --demo, --params, or stdin JSON must be provided"))
                return 2
            params = stdin_params

        ruleset = params.get("ruleset", "baseline")
        if ruleset not in {"baseline", "restricted"}:
            raise ValueError("ruleset must be one of: baseline, restricted")

        max_findings_raw = params.get("max_findings", 200)
        if not isinstance(max_findings_raw, int):
            raise ValueError("max_findings must be an integer")
        max_findings = max_findings_raw

        manifests_yaml = params.get("manifests_yaml")
        manifest_path = params.get("manifest_path")

        if isinstance(manifests_yaml, str):
            yaml_text = manifests_yaml
        elif isinstance(manifest_path, str):
            yaml_text = Path(manifest_path).read_text(encoding="utf-8")
        else:
            raise ValueError("One of manifests_yaml or manifest_path is required")

        report = analyze(yaml_text, ruleset=ruleset, max_findings=max_findings)
        report["demo"] = False
        print(_success(report))
        return 0

    except json.JSONDecodeError as e:
        print(_error("Invalid JSON", {"message": str(e)}))
        return 1
    except FileNotFoundError as e:
        print(_error("Manifest file not found", {"path": str(e)}))
        return 1
    except ValueError as e:
        print(_error(str(e)))
        return 1
    except RuntimeError as e:
        print(_error(str(e)))
        return 1
    except Exception as e:
        print(_error("Unexpected error", {"message": str(e)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
