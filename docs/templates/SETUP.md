# SETUP — Project Scaffolding Playbook

**Trigger:** the user asks to "run the SETUP playbook", "set up a new project", or "scaffold
`Projects/<Name>`".

Run this once per project. It is idempotent — if `ARCHITECT.md` already exists at the project
root, stop at Step 1 and do nothing.

This scaffolds the two-agent workflow: an **Architect** session that plans (`ARCHITECT.md`) and an
**Executor** session that implements (`EXECUTOR.md`). If the user only has one AI available,
scaffold `SOLO-AGENT.md` instead and tell them to use that.

## Step 0 — MCP server verification & auto-config

Idempotent — safe to re-run if the configs already exist.

1. Check that `docs/tools/godot-mcp/build/index.js` exists (relative to the
   `Godot_AI_Framework_Public/` root). The server's source is vendored into this repository, but
   its compiled output is gitignored, so a fresh clone never has it. If missing, build it:
   `cd docs/tools/godot-mcp && npm install && npm run build`.
2. Copy `docs/templates/common/mcp_config.json` into this project's `.agents/mcp_config.json`
   (create the `.agents/` folder if missing) AND into `.mcp.json` at the project root. Unmodified
   except for the relative path to `build/index.js` in both files, which must be adjusted for
   this project's depth under `Godot_AI_Framework_Public/` (default two levels down:
   `../../docs/tools/godot-mcp/build/index.js`).
3. **Godot path:** read `Godot_AI_Framework_Public/docs/machine_paths.json` and look up this
   machine's hostname (`$env:COMPUTERNAME` on Windows, `hostname` on macOS/Linux). If there is no
   entry, ask the user for their Godot executable path and add one. Then remind the user that the
   MCP server reads the **`GODOT_PATH` environment variable**, not this file — give them the exact
   command to run themselves (`setx GODOT_PATH "<path>"` on Windows, `export GODOT_PATH=<path>`
   in their shell profile on macOS/Linux) and tell them a full agent restart is required
   afterward. Do not modify their environment variables on their behalf.
4. Check that `gdformat`/`gdlint` are on PATH (`gdformat --version`). If missing, install with
   `pip install gdtoolkit`.

## Step 1 — Existence check

If `ARCHITECT.md` (or `SOLO-AGENT.md`) exists at the project root, stop here. Setup is complete.

## Step 2 — Scope & Tier Detection

1. Scan the project for existing game code beyond boilerplate (non-empty `scripts/`-equivalent
   folder with real logic, not just default template files). Auto-detect:
   - **New project** — no meaningful existing code.
   - **Existing codebase** — real game code already present.
2. **Tier Evaluation:** Read the `design_docs/` folder (if it exists) to estimate the complexity
   of the project. Propose a Scale Tier to the user:
   - **Lite Tier:** Best for game jams, prototypes, and very small scoped games.
   - **Standard Tier:** Best for most indie games (uses per-system routing but low bureaucracy).
   - **Heavy Tier:** Best for massive systems-heavy games or multi-developer projects.
3. Prompt the user to confirm the Tier. Do not proceed until they do.

## Step 3 — Godot project & repository bootstrap

Do this before scaffolding docs, for both the new-project and existing-codebase paths.

1. **`project.godot`** — if it does not exist, the project is not a Godot project yet. Either
   create a minimal valid `project.godot` (with `config_version=5`, an
   `[application]` section naming the project, and `config/features=PackedStringArray("4.4",
   "Forward Plus")`), or tell the user to create it once in the Godot editor
   (Project → New Project) and come back. Prefer asking — a project created in the editor gets a
   correct feature set and a valid `icon.svg` for free.
2. **`icon.svg`** — if missing, create one (any valid SVG will do) and point
   `config/icon="res://icon.svg"` at it, so the engine and the project manager render the project
   correctly.
3. **Git** — if there is no `.git` directory, run `git init` **inside this project folder**.
   Every game is its own independent repository; the framework's root `.gitignore` deliberately
   excludes `Projects/*/` so a game never gets committed into the framework repo. Write a project
   `.gitignore` covering at least `.godot/`, `.import/`, `export.cfg`, and `export_presets.cfg`.
4. **`design_docs/`** — if missing, create it and tell the user their GDD must live there as
   `.md` files. Every Architect phase globs `./design_docs/*.md`; a design doc anywhere else will
   not be read.

## Step 4a — New project path

1. **Copy Common Files:** Create a `markdowns4AI/` folder at the project root. Copy
   `PROJECT-PROFILE.md`, `ASSET-STANDARDS.md`, `DOCTRINE.md`, `MCP-SWITCH.md`,
   `HARVEST-REPO.md`, and `UPGRADE-TIER.md` from the framework's `docs/templates/common/`
   directory into it. Copy the framework's `docs/templates/common/tests/` folder to the
   project's `tests/` (not into `markdowns4AI/`).
2. **Copy Tier Files:** From `docs/templates/tiers/[chosen_tier]/`, copy `ARCHITECT.md`,
   `EXECUTOR.md`, and `SOLO-AGENT.md` to the **project root**, and copy every other file in that
   directory (`REMOVE-SYSTEM.md`, and `DESIGN-DRIFT.md` / `ORGANIZE.md` where the tier has them)
   into `markdowns4AI/`. The root/`markdowns4AI` split matters: the sync scripts assume it.
3. **Agent pointer files (IMPORTANT):** no AI agent auto-loads a file named `ARCHITECT.md` or
   `EXECUTOR.md`. Ask the user which agent(s) they run, then create the pointer file each one
   actually reads at the project root — `CLAUDE.md` for Claude Code, `AGENTS.md` for ChatGPT
   Codex, `GEMINI.md` for Gemini/Antigravity — each containing a single line directing that agent
   to the role file it should follow, e.g. `Read and follow EXECUTOR.md in this directory.
   Re-read it at the start of every response.` Without this, the governance files are never
   loaded and none of the rules apply.
4. **Scaffold Architecture based on Tier:**
   - **If Lite:** Create `project_state.md`, `bugs.md`, and `tweak_guide.md` at the project root
     (use `docs/templates/common/tweak_guide.md` as the tweak guide's starting content).
   - **If Standard:** Create `project-state/`, `project-state/blueprints/`,
     `project-state/blueprints/archive/`, and `bugs/`. Write `project-state/_overview.md`,
     `project-state/tweak_guide.md`, and `bugs/master_bugs.md`.
   - **If Heavy:** Everything Standard creates, plus `bugs/_overview.md`,
     `project-state/session_log.md`, and `project-state/architecture_decisions.md` (seed the last
     one from `docs/templates/tiers/heavy/architecture_decisions.md`). Add a "Last Verified
     Commit" field to `project-state/_overview.md`.
5. **Project README:** Write this project's root `README.md` with the structure: empty "Working",
   "In Progress", "Known Issues" lists, and "Last Updated" set to today's date.
6. **Strict Mode Enforcement:** Edit `project.godot` to ensure a `[debug]` section exists and add
   `gdscript/warnings/untyped_declaration=2` to natively enforce strict GDScript 4 typing.
7. **Dynamic Asset Scaffolding:** Read the game's `design_docs/` to understand the core
   mechanics, features, and required assets. Based on your judgement of the game's design,
   dynamically create a robust internal folder architecture in the Godot project root (e.g.
   `scenes/`, `scripts/`, `audio/sfx/`, `vfx/`, `shaders/`, `levels/`, with nested subdirectories
   as the specific game needs).

## Step 4b — Existing codebase path (tiered audit)

If the codebase already has files, do everything in Step 4a, then perform a mechanical audit
(grep for `@export`, `signal`, `class_name`, autoload entries) and populate the chosen Tier's
tracking files from what you find rather than leaving them empty.

- **Lite:** Populate `project_state.md`, `bugs.md`, and `tweak_guide.md`.
- **Standard:** Create per-system markdowns `project-state/[system]/[system].md` based on grep
  boundaries, and populate `bugs/master_bugs.md`.
- **Heavy:** Create per-system markdowns `project-state/[system]/[system].md` and
  `bugs/[system]/[system].md`.

In all tiers, populate `tweak_guide.md` from every `@export` var and tuning `const` the audit
found — that table is the single most useful artifact of this pass.

Then offer, once, to run design-drift (`markdowns4AI/DESIGN-DRIFT.md`) or organization
(`markdowns4AI/ORGANIZE.md`) review — but only mention the ones the chosen tier actually ships.

## Step 5 — Hand off

Report what was created or found, then tell the user, concisely:

1. **Fill in `markdowns4AI/PROJECT-PROFILE.md` and `markdowns4AI/DOCTRINE.md` before the first
   real task.** Both ship as placeholders and both are mandatory reads in Architect Phase 1 — an
   empty `DOCTRINE.md` means the agent invents the project's taste for it.
2. **Restart the agent** so it picks up the new pointer file and the project's `.mcp.json`.
3. Their next session starts with the Architect: *"What is the state and progress of the project,
   and what is the next task?"*
4. The shared repositories at `../../mechanics/`, `../../scenes/`, and `../../assets/` are checked
   before any new implementation work, via the routing index at `../../global-index/README.md`.
   If those are empty in this checkout, agents will fall back to building from scratch — that is
   expected, not an error.
5. They can run the `markdowns4AI/HARVEST-REPO.md` protocol any time to sweep the active project
   for generic, reusable assets and file them into those shared repositories.
