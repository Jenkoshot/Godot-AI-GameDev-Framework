# HARVEST-REPO Protocol

## Trigger Condition
This protocol is strictly **on-demand**. Do not run this during normal task execution. It is only triggered when the user explicitly requests an asset sweep (e.g., "Run the harvest repo protocol").

## Objective
To sweep the active game project for game-agnostic, generic, or highly reusable mechanics, scenes, shaders, and visual effects, and extract them into the global shared repositories so they can be reused across all future projects.

## The Harvesting Process

### Phase 1: Project Sweep (Architect)
1. Scan the local project's `scripts/`, `scenes/`, and `shaders/` directories.
2. Identify assets that are **not deeply hardcoded** to this specific game's unique logic (e.g., a generic health component, a reusable dissolve shader, a stylized UI button, a standard enemy state machine).
3. **Strict Anti-Duplication Cross-Reference:** Before flagging any asset for extraction, you MUST cross-reference its core functionality and name against the existing shared repositories to ensure you are not duplicating an asset that already exists.
   - Check `../../mechanics/`
   - Check `../../scenes/`
   - Check `../../assets/`
   - **Deep Inspection:** If a listed asset sounds even vaguely similar to what you are harvesting, you MUST open and read its actual code/contents. Do not rely solely on the filename or description. Ensure you are not just uploading a renamed duplicate.
   If a similar asset exists, **DO NOT** extract a duplicate. Instead, if your local version is better, run a refactoring task to update the global version.
4. Draft a `harvest_plan.md` detailing which files should be extracted, which global repository they belong to, and what modifications (if any) are needed to make them completely game-agnostic.

### Phase 2: Extraction & Refactoring (Executor)
1. **Copy, Don't Move:** Copy the identified `.gd`, `.tscn`, or `.glb` files from the active project into the appropriate global repository:
   - Scripts and Logic: `../../mechanics/`
   - Prefabs and UI: `../../scenes/`
   - VFX, SFX, Models, Music: `../../assets/vfx/`, `../../assets/sfx/`, `../../assets/models/`, `../../assets/music/`
2. **Agnostic Refactoring:** Strip out any project-specific references (e.g., hardcoded paths to `res://player.tscn` or specific game singletons). Replace them with exported variables or signals so the asset is plug-and-play.
3. **Companion Documentation:** For every extracted asset, create a companion `.md` file right next to it (e.g., `health_component.md` next to `health_component.gd`). This file must explain what the asset does, its exported variables, and integration steps for future AIs.
4. **Regenerate the Global Index (MANDATORY).** The routing index every planning session starts
   at is generated from the libraries' actual contents, not hand-edited. From the
   `Godot_AI_Framework_Public` root, run:

   ```
   python framework_tools/build_global_index.py
   ```

   Verify with `python framework_tools/build_global_index.py --check` (exit 0 means current).
   If an entry landed in the wrong dimension or feature area, do NOT edit the generated file —
   add `<!-- index: <feature_area> -->` and/or `<!-- dimension: 2D|3D|Agnostic -->` to the
   entry's companion `.md` and regenerate. An index entry pointing at a file that is not there,
   or filed under the wrong dimension, is worse than no entry: it sends every future agent on a
   lookup that fails.

### Phase 3: Cleanup
1. Log the successful harvest in the local `project-state/session_log.md` (Heavy tier), or in the
   project's state file otherwise.
2. Inform the user of exactly which assets were harvested, where they are now globally available,
   and confirm the global index was regenerated.
