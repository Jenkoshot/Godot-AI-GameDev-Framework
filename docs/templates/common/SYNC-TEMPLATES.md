# SYNC-TEMPLATES.md - Template Synchronization Playbook

**Trigger:** When the user asks you to "sync template docs", "evaluate template docs", or run the template sync playbook.

## Objective
Ensure that individual game projects in the `Projects/` directory have up-to-date, non-project-specific AI and organization markdown files, keeping them aligned with the global templates.

## What is considered a "Template Doc"?
These are files that govern AI behavior, setup, or standards.
**Target Files for Synchronization:**
- `ARCHITECT.md`
- `EXECUTOR.md`
- `SOLO-AGENT.md`
- `markdowns4AI/ASSET-STANDARDS.md`
- `SETUP.md`
- `markdowns4AI/UPGRADE-TIER.md`
- `markdowns4AI/HARVEST-REPO.md`
- `markdowns4AI/MCP-SWITCH.md`
- Any other markdown file explicitly located in `docs/templates/common/` or `docs/templates/tiers/`.

**Files to EXCLUDE (Never Sync / Overwrite):
- `markdowns4AI/PROJECT-PROFILE.md` (Project specific overview)**
- `markdowns4AI/DOCTRINE.md` (Project specific taste and rules)
- `project-state/` (Project specific progress and blueprints)
- `bugs/` (Project specific bug tracking)
- `design_docs/` (Project specific design documents)
- Any actual `.gd`, `.tscn`, or Godot project files.

## Sync Process
When executing a sync, follow these steps:
1. **Determine the Target:** Are we syncing a specific project or all projects?
2. **Determine the Tier:** For each target project, check its current tier (Lite, Standard, Heavy) by inspecting its setup or existing `ARCHITECT.md` / `SETUP.md`.
3. **Compare Files:** Compare the project's template docs with the canonical ones in `docs/templates/common/` and `docs/templates/tiers/[tier]/`.
4. **Update:** If a project's template doc is missing or out of sync (different content), remove the old one in the project and replace it with the latest version from `docs/templates/`.
5. **Report:** After completion, output a summary of which projects were evaluated and which files were updated.

