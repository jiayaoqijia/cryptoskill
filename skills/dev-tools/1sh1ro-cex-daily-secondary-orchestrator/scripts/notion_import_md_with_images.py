#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlparse
from urllib.request import Request, urlopen

NOTION_API_BASE = "https://api.notion.com/v1"
DEFAULT_NOTION_VERSION = "2025-09-03"

IMAGE_RE = re.compile(r"^!\[(.*?)\]\((.+?)\)\s*$")
HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)$")
BULLET_RE = re.compile(r"^-\s+(.*)$")
NUMBERED_RE = re.compile(r"^\d+\.\s+(.*)$")
URL_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")


class NotionApiError(RuntimeError):
    pass


@dataclass
class MarkdownEntry:
    kind: str
    text: str = ""
    alt: str = ""
    image_path: Optional[Path] = None


@dataclass
class ParsedMarkdown:
    title: Optional[str]
    entries: List[MarkdownEntry]


def normalize_notion_id(raw: str) -> str:
    candidate = raw.strip()
    if candidate.startswith("http://") or candidate.startswith("https://"):
        parsed = urlparse(candidate)
        part = parsed.path.strip("/").split("/")[-1]
        match = re.search(r"([0-9a-fA-F]{32})", part)
        if not match:
            raise ValueError(f"URL 中未找到 Notion 页面 ID: {raw}")
        candidate = match.group(1)

    cleaned = re.sub(r"[^0-9a-fA-F]", "", candidate)
    if len(cleaned) != 32:
        raise ValueError(f"无效的 Notion ID: {raw}")
    return f"{cleaned[:8]}-{cleaned[8:12]}-{cleaned[12:16]}-{cleaned[16:20]}-{cleaned[20:]}"


def chunk_text(text: str, max_len: int = 1900) -> List[str]:
    if not text:
        return [""]
    chunks: List[str] = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + max_len])
        start += max_len
    return chunks


def split_inline_code(text: str) -> List[Tuple[bool, str]]:
    if text.count("`") % 2 == 1:
        return [(False, text)]

    segments: List[Tuple[bool, str]] = []
    in_code = False
    buf: List[str] = []
    for ch in text:
        if ch == "`":
            seg = "".join(buf)
            if seg:
                segments.append((in_code, seg))
            buf.clear()
            in_code = not in_code
            continue
        buf.append(ch)
    tail = "".join(buf)
    if tail:
        segments.append((in_code, tail))
    return segments


def build_rich_text(markdown_text: str) -> List[Dict[str, Any]]:
    rich: List[Dict[str, Any]] = []
    for is_code, seg in split_inline_code(markdown_text):
        for piece in chunk_text(seg):
            if piece == "":
                continue
            item: Dict[str, Any] = {"type": "text", "text": {"content": piece}}
            if is_code:
                item["annotations"] = {
                    "bold": False,
                    "italic": False,
                    "strikethrough": False,
                    "underline": False,
                    "code": True,
                    "color": "default",
                }
            rich.append(item)

    if not rich:
        rich.append({"type": "text", "text": {"content": " "}})
    return rich


def resolve_image_path(raw_path: str, md_path: Path, charts_dir: Optional[Path]) -> Path:
    path_token = raw_path.strip()
    if path_token.startswith("<") and path_token.endswith(">"):
        path_token = path_token[1:-1].strip()

    if URL_RE.match(path_token):
        raise ValueError(f"不支持外链图片，需为本地路径: {path_token}")

    candidates: List[Path] = []
    candidates.append((md_path.parent / path_token).resolve())
    if charts_dir is not None:
        candidates.append((charts_dir / Path(path_token).name).resolve())

    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(f"图片不存在: {raw_path}")


def parse_markdown(md_path: Path, charts_dir: Optional[Path]) -> ParsedMarkdown:
    entries: List[MarkdownEntry] = []
    title: Optional[str] = None
    paragraph_lines: List[str] = []

    def flush_paragraph() -> None:
        if not paragraph_lines:
            return
        text = "\n".join(paragraph_lines).strip()
        paragraph_lines.clear()
        if text:
            entries.append(MarkdownEntry(kind="paragraph", text=text))

    lines = md_path.read_text(encoding="utf-8").splitlines()
    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            continue

        image_match = IMAGE_RE.match(stripped)
        if image_match:
            flush_paragraph()
            alt = image_match.group(1).strip()
            image_path = resolve_image_path(image_match.group(2), md_path, charts_dir)
            entries.append(MarkdownEntry(kind="image", alt=alt, image_path=image_path))
            continue

        heading_match = HEADING_RE.match(stripped)
        if heading_match:
            flush_paragraph()
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            if level == 1 and title is None:
                title = text
            entries.append(MarkdownEntry(kind=f"heading_{level}", text=text))
            continue

        bullet_match = BULLET_RE.match(stripped)
        if bullet_match:
            flush_paragraph()
            entries.append(MarkdownEntry(kind="bulleted_list_item", text=bullet_match.group(1).strip()))
            continue

        numbered_match = NUMBERED_RE.match(stripped)
        if numbered_match:
            flush_paragraph()
            entries.append(MarkdownEntry(kind="numbered_list_item", text=numbered_match.group(1).strip()))
            continue

        paragraph_lines.append(line)

    flush_paragraph()
    return ParsedMarkdown(title=title, entries=entries)


def text_block(kind: str, text: str) -> Dict[str, Any]:
    payload = {"rich_text": build_rich_text(text)}
    return {"type": kind, kind: payload}


def image_block(file_upload_id: str, alt: str) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"type": "file_upload", "file_upload": {"id": file_upload_id}}
    if alt:
        payload["caption"] = build_rich_text(alt)
    return {"type": "image", "image": payload}


def markdown_entry_to_block(entry: MarkdownEntry, file_upload_id: Optional[str] = None) -> Dict[str, Any]:
    if entry.kind in {"heading_1", "heading_2", "heading_3", "paragraph", "bulleted_list_item", "numbered_list_item"}:
        return text_block(entry.kind, entry.text)
    if entry.kind == "image":
        if not file_upload_id:
            raise ValueError("image block 缺少 file_upload_id")
        return image_block(file_upload_id=file_upload_id, alt=entry.alt)
    raise ValueError(f"不支持的 markdown 结构: {entry.kind}")


def build_multipart_file_body(file_path: Path, content_type: str) -> Tuple[bytes, str]:
    boundary = f"----CodexBoundary{uuid.uuid4().hex}"
    filename = file_path.name.replace('"', "")
    file_bytes = file_path.read_bytes()

    body = bytearray()
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode("utf-8")
    )
    body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
    body.extend(file_bytes)
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    return bytes(body), f"multipart/form-data; boundary={boundary}"


class NotionClient:
    def __init__(self, token: str, notion_version: str) -> None:
        self.token = token
        self.notion_version = notion_version

    def _request(
        self,
        method: str,
        path: str,
        *,
        query: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        raw_body: Optional[bytes] = None,
        extra_headers: Optional[Dict[str, str]] = None,
        expected_codes: Tuple[int, ...] = (200,),
        timeout: int = 120,
    ) -> Dict[str, Any]:
        url = f"{NOTION_API_BASE}{path}"
        if query:
            url = f"{url}?{urlencode(query)}"

        headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": self.notion_version,
        }
        if extra_headers:
            headers.update(extra_headers)

        body = raw_body
        if json_body is not None:
            body = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"

        for attempt in range(6):
            req = Request(url=url, data=body, method=method)
            for k, v in headers.items():
                req.add_header(k, v)
            try:
                with urlopen(req, timeout=timeout) as resp:
                    status = resp.getcode()
                    payload = resp.read()
                    data = json.loads(payload.decode("utf-8")) if payload else {}
                    if status not in expected_codes:
                        raise NotionApiError(f"{method} {path} 返回状态码 {status}: {data}")
                    return data
            except HTTPError as exc:
                raw = exc.read().decode("utf-8", errors="replace")
                if exc.code == 429 and attempt < 5:
                    retry_after = exc.headers.get("Retry-After") if exc.headers else None
                    wait_sec = float(retry_after) if retry_after and retry_after.isdigit() else (1.2 * (attempt + 1))
                    time.sleep(wait_sec)
                    continue
                raise NotionApiError(f"{method} {path} 失败 HTTP {exc.code}: {raw}") from exc
            except URLError as exc:
                if attempt < 5:
                    time.sleep(1.2 * (attempt + 1))
                    continue
                raise NotionApiError(f"{method} {path} 网络错误: {exc}") from exc
        raise NotionApiError(f"{method} {path} 多次重试后失败")

    def create_page(self, parent_page_id: str, title: str) -> str:
        payload = self._request(
            "POST",
            "/pages",
            json_body={
                "parent": {"page_id": parent_page_id},
                "properties": {
                    "title": {
                        "title": [
                            {"type": "text", "text": {"content": title[:2000]}},
                        ]
                    }
                },
            },
            expected_codes=(200,),
        )
        page_id = payload.get("id")
        if not page_id:
            raise NotionApiError(f"创建页面成功但缺少 id: {payload}")
        return page_id

    def update_page_title(self, page_id: str, title: str) -> None:
        self._request(
            "PATCH",
            f"/pages/{quote(page_id)}",
            json_body={
                "properties": {
                    "title": {
                        "title": [
                            {"type": "text", "text": {"content": title[:2000]}},
                        ]
                    }
                }
            },
            expected_codes=(200,),
        )

    def list_block_children(self, block_id: str) -> List[Dict[str, Any]]:
        all_children: List[Dict[str, Any]] = []
        cursor: Optional[str] = None
        while True:
            query = {"page_size": "100"}
            if cursor:
                query["start_cursor"] = cursor
            payload = self._request(
                "GET",
                f"/blocks/{quote(block_id)}/children",
                query=query,
                expected_codes=(200,),
            )
            results = payload.get("results", [])
            if isinstance(results, list):
                all_children.extend(results)
            if not payload.get("has_more"):
                break
            cursor = payload.get("next_cursor")
            if not cursor:
                break
        return all_children

    def archive_block(self, block_id: str) -> None:
        self._request(
            "PATCH",
            f"/blocks/{quote(block_id)}",
            json_body={"archived": True},
            expected_codes=(200,),
        )

    def append_children(self, block_id: str, children: List[Dict[str, Any]]) -> None:
        if not children:
            return
        self._request(
            "PATCH",
            f"/blocks/{quote(block_id)}/children",
            json_body={"children": children},
            expected_codes=(200,),
        )

    def create_file_upload(self, filename: str, content_type: str) -> str:
        payload: Optional[Dict[str, Any]] = None
        last_error: Optional[Exception] = None
        candidates = [
            {"mode": "single_part", "filename": filename, "content_type": content_type},
            {"filename": filename, "content_type": content_type},
            {"filename": filename},
        ]
        for body in candidates:
            try:
                payload = self._request(
                    "POST",
                    "/file_uploads",
                    json_body=body,
                    expected_codes=(200, 201),
                )
                break
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                continue

        if payload is None:
            raise NotionApiError(f"创建文件上传失败: {last_error}")
        file_upload_id = payload.get("id")
        if not file_upload_id:
            raise NotionApiError(f"创建文件上传失败，响应缺少 id: {payload}")
        return file_upload_id

    def send_file_upload(self, file_upload_id: str, file_path: Path, content_type: str) -> None:
        body, form_content_type = build_multipart_file_body(file_path=file_path, content_type=content_type)
        self._request(
            "POST",
            f"/file_uploads/{quote(file_upload_id)}/send",
            raw_body=body,
            extra_headers={"Content-Type": form_content_type},
            expected_codes=(200,),
        )

    def complete_file_upload(self, file_upload_id: str) -> None:
        self._request(
            "POST",
            f"/file_uploads/{quote(file_upload_id)}/complete",
            json_body={},
            expected_codes=(200,),
        )

    def upload_local_file(self, file_path: Path) -> str:
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        file_upload_id = self.create_file_upload(filename=file_path.name, content_type=content_type)
        self.send_file_upload(file_upload_id=file_upload_id, file_path=file_path, content_type=content_type)
        self.complete_file_upload(file_upload_id=file_upload_id)
        return file_upload_id


def clear_page_children(client: NotionClient, page_id: str) -> int:
    children = client.list_block_children(page_id)
    count = 0
    for child in children:
        block_id = child.get("id")
        if not block_id:
            continue
        client.archive_block(block_id)
        count += 1
    return count


def ensure_token(raw_token: Optional[str], env_name: str) -> str:
    if raw_token:
        return raw_token.strip()
    env_token = os.environ.get(env_name)
    if env_token:
        return env_token.strip()
    raise SystemExit(f"未找到 Notion token。请传 --token 或设置环境变量 {env_name}")


def build_final_blocks(client: NotionClient, entries: List[MarkdownEntry]) -> List[Dict[str, Any]]:
    blocks: List[Dict[str, Any]] = []
    uploaded_map: Dict[Path, str] = {}

    for entry in entries:
        if entry.kind != "image":
            blocks.append(markdown_entry_to_block(entry))
            continue

        if entry.image_path is None:
            raise ValueError("image entry 缺少 image_path")
        image_path = entry.image_path.resolve()
        upload_id = uploaded_map.get(image_path)
        if upload_id is None:
            upload_id = client.upload_local_file(image_path)
            uploaded_map[image_path] = upload_id
        blocks.append(markdown_entry_to_block(entry, file_upload_id=upload_id))
    return blocks


def append_blocks_in_batches(client: NotionClient, page_id: str, blocks: List[Dict[str, Any]]) -> None:
    batch_size = 50
    for i in range(0, len(blocks), batch_size):
        client.append_children(page_id, blocks[i : i + batch_size])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="将本地 markdown + 本地图表导入 Notion（图片走 Notion 内部 file_upload）。")
    parser.add_argument("--md", required=True, help="本地 markdown 文件路径。")
    parser.add_argument("--charts-dir", default="", help="图表目录（可选，默认尝试 md 同级相对路径）。")
    parser.add_argument("--page-id", default="", help="目标 Notion 页面 ID（存在时默认清空后重写）。")
    parser.add_argument("--parent-page-id", default="", help="父页面 ID（用于新建子页面）。")
    parser.add_argument("--title", default="", help="页面标题（新建页面时可选；更新页面时可用于改标题）。")
    parser.add_argument("--token", default="", help="Notion Internal Integration Token（可选，优先于环境变量）。")
    parser.add_argument("--token-env", default="NOTION_API_TOKEN", help="token 环境变量名，默认 NOTION_API_TOKEN。")
    parser.add_argument("--notion-version", default=DEFAULT_NOTION_VERSION, help=f"Notion-Version header，默认 {DEFAULT_NOTION_VERSION}。")
    parser.add_argument("--dry-run", action="store_true", help="仅解析 markdown，不调用 Notion API。")
    parser.add_argument(
        "--no-clear-existing",
        action="store_true",
        help="page-id 模式下不清空旧内容，改为直接追加。",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    md_path = Path(args.md).expanduser().resolve()
    if not md_path.exists():
        raise SystemExit(f"markdown 文件不存在: {md_path}")

    charts_dir: Optional[Path] = None
    if args.charts_dir.strip():
        charts_dir = Path(args.charts_dir).expanduser().resolve()
        if not charts_dir.exists():
            raise SystemExit(f"charts 目录不存在: {charts_dir}")

    if not args.page_id and not args.parent_page_id:
        raise SystemExit("请提供 --page-id 或 --parent-page-id 其一。")

    parsed = parse_markdown(md_path=md_path, charts_dir=charts_dir)
    image_count = sum(1 for e in parsed.entries if e.kind == "image")
    print(f"[info] Parsed entries: {len(parsed.entries)} (images={image_count})")
    if parsed.title:
        print(f"[info] Markdown title: {parsed.title}")

    if args.dry_run:
        print("[ok] Dry-run 完成，未调用 Notion API。")
        return

    token = ensure_token(args.token, args.token_env)
    client = NotionClient(token=token, notion_version=args.notion_version)

    page_id = args.page_id.strip()
    parent_page_id = args.parent_page_id.strip()
    normalized_page_id: Optional[str] = normalize_notion_id(page_id) if page_id else None
    normalized_parent_id: Optional[str] = normalize_notion_id(parent_page_id) if parent_page_id else None

    target_page_id: str
    if normalized_page_id:
        target_page_id = normalized_page_id
        clear_existing = not args.no_clear_existing
        if clear_existing:
            removed = clear_page_children(client, target_page_id)
            print(f"[info] Cleared blocks: {removed}")
        if args.title.strip():
            client.update_page_title(target_page_id, args.title.strip())
    else:
        assert normalized_parent_id is not None
        title = args.title.strip() or parsed.title or md_path.stem
        target_page_id = client.create_page(parent_page_id=normalized_parent_id, title=title)
        print(f"[info] Created page: {target_page_id}")

    blocks = build_final_blocks(client=client, entries=parsed.entries)
    append_blocks_in_batches(client=client, page_id=target_page_id, blocks=blocks)

    notion_url = f"https://www.notion.so/{target_page_id.replace('-', '')}"
    print(f"[ok] Imported blocks: {len(blocks)}")
    print(f"[ok] Notion page: {notion_url}")


if __name__ == "__main__":
    main()
