# Upgrade Tier Playbook

An on-demand playbook to smoothly upgrade a project's scale tier (e.g. Lite -> Standard, or Standard -> Heavy) when the scope of the project outgrows the current tier's capabilities. 
This is usually triggered if Antigravity detects significant design scope creep during `GEMINI.md` Phase 1.

## Process

1. **Approval & Target Selection:** State the current tier and the proposed target tier. Ensure the user confirms they want to proceed with the upgrade.
2. **File Replacement (Governance Sync):** 
   Replace the project's current AI governance files (`CLAUDE.md`, `GEMINI.md`, etc.) with the versions from the new target tier located in the global repository (`Godot_Projects/docs/templates/tiers/[target_tier]/`).
3. **Data Migration:** Execute the specific data migration steps based on the upgrade path.

### Path A: Lite -> Standard
The Lite tier uses monolithic state files (`project_state.md` and `bugs.md`), whereas the Standard tier requires per-system routing to prevent context collapse.
- **Migration Steps:**
  1. Read the contents of `project_state.md`.
  2. Create a `project-state/` folder.
  3. Create `project-state/_overview.md` and migrate the top-level status, working, and in-progress features into a Script Registry.
  4. Create individual `project-state/[system]/[system].md` files for every major system, splitting the monolithic contents into these new granular files.
  5. Create a `bugs/` folder and rename `bugs.md` to `bugs/master_bugs.md`.
  6. Delete the old `project_state.md`.

### Path B: Standard -> Heavy
The Standard tier lacks the hyper-strict paper trail features required for massive multi-agent or multi-year development.
- **Migration Steps:**
  1. Create the `project-state/session_log.md` file with its required header.
  2. Create the `project-state/architecture_decisions.md` (ADR) file.
  3. Create individual `bugs/[system]/[system].md` tracking files, breaking out the monolithic `bugs/master_bugs.md` into granular per-system files. Update `bugs/_overview.md` to be a master rollup.
  4. Ensure `CLAUDE.md` and `GEMINI.md` are correctly swapped, activating the rigorous "Last Verified Commit" testing requirements for all future sessions.

## Completion
Once migration is complete, inform the user that their project is now running on the upgraded tier and they can immediately begin their next task.
