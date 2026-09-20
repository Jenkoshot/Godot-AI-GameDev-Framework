# UPGRADE-TIER Playbook

**Trigger:** When the user explicitly requests to upgrade the project's scale tier (Lite ->
Standard, Lite -> Heavy, or Standard -> Heavy), either proactively or in response to the tier
check in `ARCHITECT.md` Phase 1.

**Description:** Cleanly upgrades the project's tracking folders and governance files to a higher
tier, so the agents can manage a more complex architecture without losing existing progress. This
is a one-way migration of real project data — treat it as such.

## Execution Steps

1. **Approval & Target Selection.** State the current tier and the proposed target tier, and
   confirm with the user before touching anything. Do not proceed on an implied yes.
2. **Commit first (MANDATORY).** This playbook moves and deletes project state files, and step 4
   runs a sync script that overwrites files. Ensure the project's git working tree is clean, or
   have the user commit, before continuing. If the project has no git repository yet, run
   `git init` and make an initial commit first.
3. **Update Profile.** In `markdowns4AI/PROJECT-PROFILE.md`, change the tier string (e.g.
   "Current Tier: Lite" -> "Current Tier: Standard"). The sync scripts read this line to decide
   which tier's templates to push — if it is wrong, everything downstream is wrong.
4. **Execute Template Sync.** Run `python framework_tools/sync_tiers.py` from the
   `Godot_AI_Framework_Public` root, or have the user run it. This drops the target tier's
   governance files (`ARCHITECT.md`, `EXECUTOR.md`, `SOLO-AGENT.md`, `REMOVE-SYSTEM.md`, and the
   tier's extra playbooks) into the project.
   Prefer `sync_tiers.py` over `sync_templates.py` here: `sync_templates.py` also copies the blank
   `tweak_guide.md` and `architecture_decisions.md` templates, which is exactly what you are about
   to migrate real content into.
5. **Restructure Tracking Files (MANDATORY).** Physically move and map the old state files into
   the new structure.

   ### Path A: Lite -> Standard
   Lite uses monolithic state files; Standard needs per-system routing to prevent context
   collapse.
   1. Read the full contents of `project_state.md` before moving anything.
   2. Create `project-state/`, `project-state/blueprints/`,
      `project-state/blueprints/archive/`, and `bugs/`.
   3. Move `./project_state.md` to `project-state/_overview.md`, keeping the top-level status,
      Working/In Progress lists, and Script Registry intact.
   4. Move `./tweak_guide.md` to `project-state/tweak_guide.md` **as-is** — never regenerate it
      from the blank template; its rows are hand-earned.
   5. Move `./bugs.md` to `bugs/master_bugs.md`.
   6. Read the game's GDScript and carve out individual system files
      (e.g. `project-state/player_controller/player_controller.md`) along logical boundaries,
      populating each with that system's state pulled from the old monolith.
   7. Move any existing `blueprint.md` to `project-state/blueprints/latest_blueprint.md`, and
      any `blueprints_archive/` contents into `project-state/blueprints/archive/`.

   ### Path B: Standard -> Heavy
   Standard lacks the paper-trail features that long-running or multi-agent development needs.
   1. Retain `project-state/` and `bugs/` as they are.
   2. Create `project-state/session_log.md` with its header, and
      `project-state/architecture_decisions.md` (seed from
      `docs/templates/tiers/heavy/architecture_decisions.md` only if the project has no ADR log
      yet — never overwrite an existing one).
   3. Expand `bugs/master_bugs.md` into per-system files at `bugs/[system]/[system].md`, and
      write `bugs/_overview.md` as the master rollup. Preserve every bug's existing status and
      severity through the split.
   4. Add a "Last Verified Commit" field to `project-state/_overview.md`, seeded with the current
      `git rev-parse HEAD`.

   ### Path C: Lite -> Heavy
   Run Path A in full, then Path B in full. Do not attempt to jump directly — the intermediate
   per-system split in Path A is what Path B's per-system bug files are derived from.

6. **Delete Leftovers.** Ensure no old files are stranded at the root. After Path A, remove the
   root `project_state.md`, `tweak_guide.md`, and `bugs.md` — but only once you have confirmed
   their content landed in the new locations.
7. **Update agent pointer files.** If the project has `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`
   pointer files, confirm they still name role files that exist after the sync.
8. **Report.** Summarize the completed upgrade: which files moved where, which systems were
   carved out, and which new playbooks the project now has (`DESIGN-DRIFT.md` at Standard,
   plus `ORGANIZE.md` at Heavy).
