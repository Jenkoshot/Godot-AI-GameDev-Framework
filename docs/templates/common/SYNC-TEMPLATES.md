# SYNC-TEMPLATES — Template Synchronization Playbook

**Trigger:** When the user asks you to "sync template docs", "evaluate template docs", or run the
template sync playbook.

**Run from:** the `Godot_AI_Framework_Public` root.

## Objective

Ensure the game projects in `Projects/` carry up-to-date, non-project-specific governance
markdown, aligned with the canonical templates in `docs/templates/`.

This playbook is the careful, review-first equivalent of `framework_tools/sync_templates.py`. Use
the playbook when you want to see and approve each change; use the script when you just want the
files pushed. They target the same files and the same destinations.

## File classes

### 1. Sync freely — overwrite whenever the canonical version differs

| File | Destination in project |
| :--- | :--- |
| `ARCHITECT.md` | project root |
| `EXECUTOR.md` | project root |
| `SOLO-AGENT.md` | project root |
| `SETUP.md` | project root |
| `ASSET-STANDARDS.md` | `markdowns4AI/` |
| `HARVEST-REPO.md` | `markdowns4AI/` |
| `MCP-SWITCH.md` | `markdowns4AI/` |
| `SYNC-TEMPLATES.md` | `markdowns4AI/` |
| `UPGRADE-TIER.md` | `markdowns4AI/` |
| `REMOVE-SYSTEM.md` | `markdowns4AI/` |
| `DESIGN-DRIFT.md` (Standard, Heavy) | `markdowns4AI/` |
| `ORGANIZE.md` (Heavy only) | `markdowns4AI/` |
| `mcp_config.json` | `.agents/` (and mirrored to `.mcp.json` at the root) |
| `run_tests.gd`, `test_case.gd` | `tests/` |

The root/`markdowns4AI/` split is not cosmetic — the sync scripts assume it, and a file in the
wrong place becomes a duplicate that drifts.

### 2. Seed files — write ONLY if absent, never overwrite

These ship as empty templates and then hold real, hand-written project content. Overwriting one
destroys work that is not recoverable from any other file.

- `tweak_guide.md` (`project-state/tweak_guide.md`, or the project root in Lite)
- `architecture_decisions.md` (`project-state/`, Heavy only)

If the project's copy already exists, **leave it alone** — even if it differs from the template.
Differing is the expected state.

### 3. Never sync, never overwrite — project-owned

- `markdowns4AI/PROJECT-PROFILE.md` — the project's identity and tier
- `markdowns4AI/DOCTRINE.md` — the project's design pillars and taste
- `project-state/` — progress, blueprints, session log
- `bugs/` — bug tracking
- `design_docs/` — the GDD
- `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` — the user's agent pointer files
- Any `.gd`, `.tscn`, `.tres`, or Godot project file

## Sync Process

1. **Determine the target.** One project, or all of `Projects/`? Only directories containing a
   `project.godot` are game projects.
2. **Confirm the working tree is clean.** This playbook overwrites files. If the project has
   uncommitted changes, say so and let the user commit before you proceed.
3. **Determine the tier.** Read `markdowns4AI/PROJECT-PROFILE.md`'s `Current Tier:` line. Fall
   back to inspecting the project's existing `ARCHITECT.md` only if the profile is missing, and
   say which source you used.
4. **Compare.** Diff each class-1 file against the canonical version in
   `docs/templates/common/` and `docs/templates/tiers/[tier]/`.
5. **Report before writing.** List every file that would change, grouped as create / update /
   skip-because-seed / skip-because-project-owned. Present misplaced copies (a class-1 file
   sitting somewhere other than its destination) separately — those need deleting, and deletion
   needs explicit approval.
6. **Update** on approval: replace out-of-date class-1 files, create missing ones, and leave
   classes 2 and 3 untouched.
7. **Check pointer files.** After syncing, confirm any `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`
   pointer files still name role files that exist.
8. **Report** which projects were evaluated and exactly what changed.
