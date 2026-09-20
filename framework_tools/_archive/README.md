# Archived one-off migration scripts

**Do not run anything in this folder.**

These are throwaway scripts written during the framework's own refactors — renaming the
governance files, renumbering template steps, swapping agent names, reshaping the Phase 4 handoff
block. They were each run once against the author's local tree and then never maintained. They are
kept only as a record of how the templates got to their current shape.

They are unsafe for three separate reasons:

| Script | Problem |
| :--- | :--- |
| `update_architect.py`, `update_models.py` | Contain `ros.path.join` — a typo that raises `NameError` on the first call. They cannot run at all. |
| `check_handoff.py`, `check_phase4.py`, `update_handoff.py`, `update_profile.py` | Hardcode `c:\Godot_AI_Framework\docs\templates\tiers`. On any other machine they are silent no-ops; on a machine that happens to have that path, they rewrite the wrong repo. |
| `update_executor.py` | Hardcodes `c:/Godot_Projects/...`. Same problem. |
| `rename.py` | Rewrites strings across every `.md`/`.gd`/`.tscn`/`.json` in the repo and renames top-level directories. Its renames were applied long ago; running it now would corrupt the tree. |
| `populate_profiles.py` | Writes a hardcoded `Example_Project` profile to `Projects/Example_Project/PROJECT-PROFILE.md` — the wrong location (profiles live in `markdowns4AI/`) for a project that does not exist. |

`update_profile.py` is worth reading if you are curious why the shipped `ARCHITECT.md` templates
had a duplicated step 2 and a `1, 2, 2, 4, 4, 5…` numbering run: it tried to insert a "Project
Profile" step 3 and renumber around it, and got the renumbering wrong. That damage has since been
repaired, and the Project Profile read it was trying to add is now step 3 for real.

## The maintained tools

Two scripts in the parent folder are live and supported:

- `framework_tools/sync_templates.py` — push all common + tier templates to every project.
- `framework_tools/sync_tiers.py` — push only the tier-specific governance files.

Both support `--dry-run` and `--project NAME`; `sync_templates.py` also has `--prune`. Neither
will ever overwrite `DOCTRINE.md`, `PROJECT-PROFILE.md`, a populated `tweak_guide.md`, or a
populated `architecture_decisions.md`.
