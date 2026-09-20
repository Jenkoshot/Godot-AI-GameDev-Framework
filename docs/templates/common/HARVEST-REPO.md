# HARVEST-REPO Protocol

## Trigger Condition
This protocol is strictly **on-demand**. Do not run this during normal task execution. It is only triggered when the user explicitly requests an asset sweep (e.g., "Run the harvest repo protocol").

## Objective
To sweep the active game project for game-agnostic, generic, or highly reusable mechanics, scenes, shaders, and visual effects, and extract them into the global shared repositories so they can be reused across all future projects.

## The Harvesting Process

### Phase 1: Project Sweep (Gemini / Planner)
1. Scan the local project's `scripts/`, `scenes/`, and `shaders/` directories.
2. Identify assets that are **not deeply hardcoded** to this specific game's unique logic (e.g., a generic health component, a reusable dissolve shader, a stylized UI button, a standard enemy state machine).
3. **Strict Anti-Duplication Cross-Reference:** Before flagging any asset for extraction, you MUST cross-reference its core functionality and name against the existing shared repositories to ensure you are not duplicating an asset that already exists.
   - Check `../../mechanics/README.md`
   - Check `../../scenes/README.md`
   - Check `../../effect-blocks/README.md`
   - Check `../../poly-blocks/NatureBlocks/README.md`
   - **Deep Inspection:** If a listed asset sounds even vaguely similar to what you are harvesting, you MUST open and read its actual code/contents. Do not rely solely on the filename or description. Ensure you are not just uploading a renamed duplicate.
   If a similar asset exists, **DO NOT** extract a duplicate. Instead, if your local version is better, run a refactoring task to update the global version.
4. Draft a `harvest_plan.md` detailing which files should be extracted, which global repository they belong to, and what modifications (if any) are needed to make them completely game-agnostic.

### Phase 2: Extraction & Refactoring (Claude Code / Executor)
1. **Copy, Don't Move:** Copy the identified `.gd`, `.tscn`, or `.gdshader` files from the active project into the appropriate global repository:
   - Scripts and Logic: `../../mechanics/`
   - Prefabs and UI: `../../scenes/`
   - VFX and Particles: `../../effect-blocks/`
2. **Agnostic Refactoring:** Strip out any project-specific references (e.g., hardcoded paths to `res://player.tscn` or specific game singletons). Replace them with exported variables or signals so the asset is plug-and-play.
3. **Companion Documentation:** For every extracted asset, create a companion `.md` file right next to it (e.g., `health_component.md` next to `health_component.gd`). This file must explain what the asset does, its exported variables, and integration steps for future AIs.
4. **Update Master Indices:** Update the `README.md` AI Directory Guide of the target repository to include the newly harvested asset.

### Phase 3: Cleanup
1. Log the successful harvest in the local `project-state/session_log.md`.
2. Inform the user of exactly which assets were harvested and where they are now globally available.
