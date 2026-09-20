# Vendored tools

Third-party tools committed into this repository rather than pulled in at install time.

## `godot-mcp/`

The Godot MCP server the Executor Agent drives for every `.tscn`/`.tres` operation and all
live-editor introspection.

| | |
| :--- | :--- |
| **Upstream** | https://github.com/tugcantopaloglu/godot-mcp |
| **License** | MIT — see `godot-mcp/LICENSE`, retained in full |
| **How it is tracked** | **Vendored**, not a git submodule. Its source files are committed directly into this repository. |

### It is not a submodule

This is worth stating plainly, because it used to be described as one. There is no `.gitmodules`
entry and no gitlink for this path — `git ls-files docs/tools/godot-mcp` lists ordinary blobs.
Running `git submodule update --init --recursive` does nothing here; if you find that instruction
anywhere, it is stale.

### You must build it after cloning

The server's own `.gitignore` excludes `build/`, so a fresh clone has TypeScript source and **no
compiled server**. Until you build it, every `mcp__godot__*` tool is missing and the Executor is
limited to plain text edits on `.gd` files.

```bash
cd docs/tools/godot-mcp && npm install && npm run build
```

That produces `build/index.js`, which each project's `.mcp.json` points at.

### Updating to a newer upstream

Because it is vendored, there is no `git submodule update`. Pull the changes in by hand:

1. Clone or fetch upstream somewhere outside this repository.
2. Copy its tracked files over `docs/tools/godot-mcp/`, keeping that directory's own `.gitignore`.
3. Rebuild (`npm install && npm run build`) and confirm `get_godot_version` still responds.
4. Check whether the tool set changed. `EXECUTOR.md`'s "Current MCP" section names specific tools
   (`run_project`, `game_screenshot`, `game_eval`, `read_scene`, `rename_file`, `write_file`,
   `delete_file`); if any were renamed or removed, run the `MCP-SWITCH.md` playbook rather than
   editing those references by hand — it exists to catch capabilities that have no equivalent in
   the new version instead of silently dropping them.
5. Commit the result as a normal change, noting the upstream revision in the commit message.

### Configuration

The server locates Godot through the **`GODOT_PATH` environment variable**. Its built-in
auto-detection does not scan Steam library folders on Windows or Linux, so a Steam install will
fail without it. `docs/machine_paths.json` records per-machine paths for agents to read, but it
does **not** feed the server — you still have to set the environment variable yourself and fully
restart your agent afterward.
