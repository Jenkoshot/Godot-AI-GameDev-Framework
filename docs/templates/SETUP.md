# Antigravity Project Setup

Run this once per project. It is idempotent — if `ARCHITECT.md` already exists, do nothing.

This project uses a unified agent workflow: Gemini CLI (Antigravity) plans and hands off execution to Claude Code via `ARCHITECT.md`.

## Step 0 — MCP server verification & auto-config

Run once per project, idempotent — safe to re-run if the submodule or configs already exist.

1. Check that `docs/tools/godot-mcp` (relative to the `Godot_AI_Framework/` root) is an initialized
   submodule, not an empty folder. If empty, run `git submodule update --init --recursive` from
   `Godot_AI_Framework/`.
2. Check that `docs/tools/godot-mcp/build/index.js` exists. If missing, build it:
   `cd docs/tools/godot-mcp && npm install && npm run build`.
3. Copy `docs/templates/common/mcp_config.json` into this project's `.agents/mcp_config.json`
   (create the `.agents/` folder if missing) AND into `.mcp.json` at the project root. Unmodified except for the relative path to
   `build/index.js` in both files, which must be adjusted for this project's depth under `Godot_AI_Framework/`
   (default two levels down: `../../docs/tools/godot-mcp/build/index.js`).
4. Handle `GODOT_PATH` via `Godot_AI_Framework/docs/machine_paths.json` as normal.
5. Check that `gdformat`/`gdlint` are on PATH (`gdformat --version`). If missing, install with `pip install gdtoolkit`.

## Step 1 — Existence check

If `ARCHITECT.md` exists, stop here. Setup is complete.

## Step 2 — Scope & Tier Detection

1. Scan the project for existing game code beyond boilerplate (non-empty `Scripts/`-equivalent
   folder with real logic, not just default template files). Auto-detect:
   - **New project** — no meaningful existing code.
   - **Existing codebase** — real game code already present.
2. **Tier Evaluation:** Read the `design_docs/` folder (if it exists) to estimate the complexity of the project. Propose a Scale Tier to the user:
   - **Lite Tier:** Best for game jams, prototypes, and very small scoped games.
   - **Standard Tier:** Best for most indie games (uses per-system routing but low bureaucracy).
   - **Heavy Tier:** Best for massive systems-heavy games or multi-developer projects.
3. Prompt the user to confirm the Tier. 

## Step 3a — New project path

1. **Copy Common Files:** Create a markdowns4AI/ folder at the root. Copy `markdowns4AI/PROJECT-PROFILE.md`, `markdowns4AI/ASSET-STANDARDS.md`, `markdowns4AI/DOCTRINE.md`, `markdowns4AI/MCP-SWITCH.md`, `markdowns4AI/HARVEST-REPO.md`, and the `tests/` folder from the framework's `docs/templates/common/` directory into the project's markdowns4AI/ folder (create it if missing, but ensure ARCHITECT.md and EXECUTOR.md stay at the root).
2. **Copy Tier Files:** Copy the specific governance files from the framework's `docs/templates/tiers/[chosen_tier]/` directory into the project's markdowns4AI/ folder (create it if missing, but ensure ARCHITECT.md and EXECUTOR.md stay at the root).
3. **Scaffold Architecture based on Tier:**
   - **If Lite:** Create `project_state.md`, `bugs.md`, and `tweak_guide.md` at the project root.
   - **If Standard:** Create `project-state/`, `project-state/blueprints/`, and `bugs/` folders. Write `project-state/_overview.md`, `project-state/tweak_guide.md`, and `bugs/master_bugs.md`.
   - **If Heavy:** Create `project-state/`, `project-state/blueprints/`, and `bugs/` folders. Write `project-state/_overview.md`, `project-state/tweak_guide.md`, `bugs/_overview.md`, `project-state/session_log.md`, and `project-state/architecture_decisions.md`.
4. **Project README:** Write this project's root `README.md` with the structure: empty "Working", "In Progress", "Known Issues" lists, and "Last Updated" set to today's date.
5. **Strict Mode Enforcement**: Edit `project.godot` to ensure `[debug]` exists and add `gdscript/warnings/untyped_declaration=2` to natively enforce strict GDScript 4 typings.
6. **Dynamic Asset Scaffolding**: Read the game's `design_docs/` to understand the core mechanics, features, and required assets. Based on your judgement of the game's design, dynamically create a robust internal folder architecture in the Godot project root (e.g., `scenes/`, `scripts/`, `audio/sfx/`, `vfx/`, `shaders/`, `levels/`, along with appropriate nested subdirectories based on the specific game's needs).

## Step 3b — Existing codebase path (tiered audit)

If the codebase already has files, perform a mechanical audit (grep for `@export`, `signal`, etc.) and populate the chosen Tier's tracking files. 
- For Lite: Populate `project_state.md`, `bugs.md`, and `tweak_guide.md`.
- For Standard: Create per-system markdowns `project-state/[system]/[system].md` based on grep boundaries, and populate `bugs/master_bugs.md`.
- For Heavy: Create per-system markdowns `project-state/[system]/[system].md` and `bugs/[system]/[system].md`.

Prompt the user to review organization (`markdowns4AI/ORGANIZE.md`) or design drift (`markdowns4AI/DESIGN-DRIFT.md`) if those tools are available in their chosen tier.

## Step 4 — Hand off

Report what was created or found. All future sessions defer to the unified agent workflow where Gemini
CLI (Antigravity) plans and hands off execution to Claude Code via `ARCHITECT.md`. Mention to the user that the shared repositories at
new implementation work. Also remind them they can run the `markdowns4AI/HARVEST-REPO.md` protocol anytime to sweep their active project for generic assets.
