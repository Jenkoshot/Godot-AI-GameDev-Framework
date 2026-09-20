# ARCHITECT.md (Repository Root) — Director Rules

**You are reading this because an agent was opened at the root of the framework repository, not
inside a game project.** At the root you are the **Director**: you do meta-work on the framework
itself. You do not plan or implement game features here.

> This file used to be a stale copy of the per-project Architect template. It is not one any more.
> The real, current planner rules live at `docs/templates/tiers/<tier>/ARCHITECT.md` and are
> copied into each project by the `SETUP` playbook. If you are trying to plan a game feature, you
> are in the wrong directory — open your agent inside `Projects/<YourGame>/` instead.

## What the root workspace is for

1. **Brainstorming and writing design docs** for a new game, before it exists as a project.
2. **Creating projects** — run `docs/templates/SETUP.md`.
3. **Editing the framework's own rules** — the templates under `docs/templates/`, then syncing
   them out to existing projects.
4. **Repo-wide tooling** — `framework_tools/`, the shared libraries, the global index.

## What is NOT available here

- **No Godot MCP.** There is no `.mcp.json` at the repository root; MCP is configured per project
  by the `SETUP` playbook. Do not attempt `.tscn`/`.tres` operations from here.
- **No project state.** There is no `project-state/`, `bugs/`, `design_docs/`, or `DOCTRINE.md` at
  the root. Those are per-project.

## Root-level playbooks

| Task | Playbook |
| :--- | :--- |
| First-time framework install | `SETUP-FRAMEWORK.md` |
| Create/scaffold a new game project | `docs/templates/SETUP.md` |
| Push updated rules to existing projects | `docs/templates/common/SYNC-TEMPLATES.md` |

## Rules for root-level work

1. **Never edit a project's governance files in place.** `ARCHITECT.md`, `EXECUTOR.md`, and
   `SOLO-AGENT.md` inside `Projects/<Game>/` are generated copies. Edit the template under
   `docs/templates/` and sync, or the next sync silently reverts the change.
2. **Know which layer a rule belongs to** before editing:
   - `docs/templates/common/` — applies to every project, every tier.
   - `docs/templates/tiers/<tier>/` — applies to one tier only.
   - A project's own `markdowns4AI/DOCTRINE.md` — applies to one game only. Never sync this.
3. **`DOCTRINE.md` and `PROJECT-PROFILE.md` are user-owned.** They are excluded from template
   syncing on purpose. Never overwrite a project's copy of either.
4. **Preview a sync before running it.** `framework_tools/sync_templates.py --dry-run` prints
   every file it would touch. It will not overwrite a populated `tweak_guide.md` or
   `architecture_decisions.md`, and it never touches `DOCTRINE.md` or `PROJECT-PROFILE.md` — but
   it does replace governance files wholesale, so confirm the target projects are committed
   first. Prefer `sync_tiers.py` when only tier governance changed. Misplaced copies are reported
   and only deleted with `--prune`, which needs the user's explicit go-ahead.
5. **Three scripts in `framework_tools/` are live tools** — `sync_templates.py`,
   `sync_tiers.py`, and `build_global_index.py`. Everything under `framework_tools/_archive/` is a
   historical one-off migration script: hardcoded to paths that no longer exist, and in two cases
   unable to run at all. Never run them, and never treat them as examples of working code.
6. **Each game is its own git repository.** The root `.gitignore` excludes every top-level
   directory and every `Projects/*/` subdirectory by design. Run `git init` inside the game's
   folder; never `git add` a game from the root.
7. **Keep the shared libraries honest.** `global-index/` is **generated**, never hand-edited. If
   you add or remove anything in `mechanics/`, `scenes/`, or `assets/`, regenerate it in the same
   change:

   ```
   python framework_tools/build_global_index.py
   ```

   `--check` exits non-zero when the index has drifted, so it works as a pre-commit or CI guard.
   To correct an entry's dimension or feature area, edit the `<!-- index: -->` /
   `<!-- dimension: -->` markers in its companion `.md` and regenerate — never patch the
   generated file. An index entry pointing at a file which is not there is worse than no entry:
   it sends every future agent on a dead lookup.

## Shared library layout

| Path | Contents |
| :--- | :--- |
| `global-index/` | Generated routing index over the libraries below. `2D/`, `3D/`, `Agnostic/` feature files, created as content classifies into them. The entry point for all scouting — never scan the libraries blind. |
| `mechanics/` | Reusable `.gd` scripts by category, each with a companion `.md`. |
| `scenes/` | Reusable `.tscn` / `.tres` structures. |
| `assets/` | Raw models, music, SFX, VFX. |
| `godot-4-snippets-bible/` | Godot 4 API notes and the running log of corrected syntax hallucinations. |
| `model-generation/` | Procedural 3D modelling workspace (`antics-modelkit`). |
