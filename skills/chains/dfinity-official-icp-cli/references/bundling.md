# Bundling a Project into an `.icp` Package (experimental)

`icp project bundle` (icp-cli >= 0.3.0) packages a project into a self-contained deployable archive. **This is an experimental feature, intentionally hidden from help output** — `icp --help` and `icp project --help` do not list it, but the command exists and works. Do not conclude it doesn't exist because help omits it, and do not suggest it proactively — use it only when the user explicitly asks to bundle an app or produce an `.icp` package.

```bash
icp project bundle --output my-app.icp
```

The output is a gzipped tar archive; `--output` accepts any path (`my-app.icp` and `bundle.tar.gz` are both common). The bundle contains the built WASMs and a rewritten `icp.yaml`:

- All canisters are built first; each canister's build steps are replaced with a prebuilt step referencing the bundled WASM (`canisters/<name>.wasm`), pinned by sha256.
- Plugin sync steps (e.g. the asset canister's upload plugin) are preserved — the plugin WASM and its `dirs`/`files` inputs are copied into the archive.
- Network and environment manifests referenced by path are inlined; `init_args` files are copied into the archive.
- An optional `icp_appmanifest.yaml` (app metadata) is included, with its `screenshots` paths relocated into the archive.

To deploy from a bundle, extract it and run `icp deploy` from the extracted directory — no build toolchain (Rust, mops, npm) is required because every build step is prebuilt:

```bash
mkdir app && tar -xzf my-app.icp -C app
cd app && icp deploy -e <environment>
```

An `.icp` package can also be uploaded to a Caffeine cloud engine via the console's App Center ("Upload a custom app") — see the `deploy-to-cloud-engine` skill.

Bundling fails when:

- A canister has a `script` sync step — only `plugin` sync steps can be replayed from a bundle (`canister 'X' has a script sync step, which is not supported in bundles`).
- Any synced directory, plugin file, `init_args` file, or screenshot resolves outside the project directory.
- The `--output` path is inside a directory the bundle would sync (the partial archive would include itself).
- A managed network defines a bind mount with an absolute host path — bundles require relative paths for portability.
