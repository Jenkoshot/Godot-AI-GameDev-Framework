# UPGRADE-TIER Playbook

**Trigger:** When the user explicitly requests to upgrade the project's scale tier (e.g., from Lite to Standard, or Standard to Heavy) either proactively or when prompted by you during a session check.

**Description:** This protocol cleanly upgrades the project's tracking folders and documentation files to a higher tier of bureaucracy, allowing the AI to safely manage a more complex architecture without losing existing progress.

## Execution Steps

1. **Verify Goal:** Confirm with the user exactly which Tier they are upgrading to (Lite -> Standard, Lite -> Heavy, or Standard -> Heavy).
2. **Update Profile:** Find `markdowns4AI/PROJECT-PROFILE.md` (or `ARCHITECT.md`) and change the internal tier string (e.g., change "Current Tier: Lite" to "Current Tier: Standard").
3. **Execute Template Sync:** Immediately run `python framework_tools/sync_templates.py` (from the Godot_AI_Framework_Public root) or command the user to run it. This will drop the new governance files for the target tier into the project.
4. **Restructure Tracking Files (MANDATORY):** You must physically move and map the old state files into the new structure:
   - **If upgrading from Lite to Standard:**
     - Create `project-state/`, `project-state/blueprints/`, and `bugs/` directories.
     - Move `./project_state.md` to `project-state/_overview.md`.
     - Move `./tweak_guide.md` to `project-state/tweak_guide.md`.
     - Move `./bugs.md` to `bugs/master_bugs.md`.
     - Read the game's GDScript logic. Carve out individual system files (e.g., `project-state/player_controller/player_controller.md`) based on logical boundaries and populate them with the state of those systems.
   - **If upgrading from Standard to Heavy:**
     - Retain `project-state/` and `bugs/`.
     - Create `project-state/session_log.md` and `project-state/architecture_decisions.md`.
     - Expand `bugs/master_bugs.md` into distinct per-system bug files inside `bugs/[system]/[system].md` and write a root `bugs/_overview.md`.
5. **Delete Leftovers:** Ensure no old files are left stranded at the root. If moving from Lite, remove the root `project_state.md`, `tweak_guide.md`, and `bugs.md`.
6. **Report:** Provide the user a brief summary of the completed upgrade and the newly available systems.
