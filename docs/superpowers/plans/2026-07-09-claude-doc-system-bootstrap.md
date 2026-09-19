# Claude Doc System — Templates + Spinner Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce the four reusable agnostic template documents (CLAUDE.md, SETUP.md, ORGANIZE.md, MCP-SWITCH.md) from the approved spec, install them into Spinner, and run the existing-codebase bootstrap against Spinner to produce a real, accurate `project-state.md` + system spokes and `bugs.md` + system spokes.

**Architecture:** Canonical copies of the four agnostic docs live in `/home/avery/Godot_Projects/docs/templates/` (one shared git repo, tracked, versioned). Each game project — Spinner first — gets its own full copy at its root. Spinner's bootstrap uses the tiered audit: a mechanical Tier-1 structural scan builds the complete Script Registry from real `find` output, then a fixed, checkable heuristic promotes specific systems to Tier-2 depth, seeded from the existing Aug 2026 codebase audit already in memory rather than re-reading those files from scratch.

**Tech Stack:** Plain Markdown files, git, Bash (`find`/`grep`/`git`) for structural verification. No application code, no test framework — this plan adapts "test-first" to the domain: each doc-writing task's verification step is a structural check (required section headers present, no placeholder markers, registry/file counts reconcile with real `find` output) rather than a unit test, since the deliverable is documentation/config, not executable logic.

## Global Constraints

- The four agnostic docs (CLAUDE.md, SETUP.md, ORGANIZE.md, MCP-SWITCH.md) must be **byte-identical** between the canonical copy in `Godot_Projects/docs/templates/` and the copy installed in Spinner at bootstrap time — copy verbatim, do not paraphrase or re-derive per project.
- Per spec: **tri-state status is Coded / Wired-in / Verified-in-game**, and this axis tracks *integration completeness only* — it is independent of correctness. A feature can be "Wired-in" or "Verified-in-game" and still have an open bug (e.g., upgrade persistence runs and is visibly wired in, but has a data-loss bug — that bug goes in `bugs-core-gameplay.md`, it does not downgrade the tri-state entry).
- A feature that is **entirely absent** (not started at all, e.g., Ripple Unlock progression) is not given a tri-state entry in "Current Implementation" — it belongs only in that system doc's "Gaps vs. Design Docs" section.
- File moves/renames of files Godot tracks as resources (`.gd`, `.tscn`, `.tres`) must go through Godot MCP tools (e.g., `mcp__godot__rename_file`), never raw shell `mv`/`rm` — this does **not** apply to copying plain template Markdown files between `Godot_Projects/docs/templates/` and a game root, which are not Godot resources and are safe to `cp` directly.
- System docs and bug docs are created **only** for systems identified during this bootstrap (7 systems below) — no preemptive docs for hypothetical future systems.
- Every commit in `Godot_Projects/` uses that repo; every commit inside `Spinner/` uses Spinner's own separate repo. Do not mix them.

---

## Verified Ground Truth (gathered before writing this plan)

- **54 game scripts** under `Scripts/` (confirmed via `find ./Scripts -name "*.gd" | wc -l`).
- **13 addon/tooling scripts** under both `Addons/` (5 files) and `addons/` (8 files) — a case-mismatched duplicate folder pair, third-party `script-ide` plugin, not part of game systems. Flagged as an `ORGANIZE.md` candidate, not resolved in this plan.
- **4 autoloads** (from `project.godot`): `Player`, `Armoury`, `WarpManager`, `SaveData`.
- **26 design docs** across 10 `design_docs/` category folders.
- **Current HEAD:** `bab83de871af71507e60628b22daa0240b891b0` (Spinner repo).
- **System-to-script mapping** (verified count: 10+9+6+14+4+8+3 = 54, matches exactly):

| System | Script count | Scripts |
|---|---|---|
| Kinematic Engine | 10 | `Scripts/Layouts/archimedan_spiral.gd`, `Scripts/Layouts/kinematic_spiral.gd`, `Scripts/Layouts/lissajous_spiral.gd`, `Scripts/Layouts/logarithmic_spiral.gd`, `Scripts/Layouts/OvalOribtSpiral.gd`, `Scripts/Layouts/PhyllotaxisSpiral.gd`, `Scripts/Layouts/ulam_spiral.gd`, `Scripts/MasterScripts/master_spinner.gd`, `Scripts/MasterScripts/spiral_layout.gd`, `Scripts/Utils/prime_math.gd` |
| Synergy System | 9 | `Scripts/DataScripts/elements.gd`, `Scripts/DataScripts/Synergies/element_mutator_synergy.gd`, `Scripts/DataScripts/Synergies/Guard_Synergy.gd`, `Scripts/DataScripts/Synergies/Origin_Anchor_Synergy.gd`, `Scripts/DataScripts/Synergies/pattern_synergy.gd`, `Scripts/DataScripts/Synergies/synergy_rule.gd`, `Scripts/DataScripts/Synergies/Void_Isolation.gd`, `Scripts/element_container.gd`, `Scripts/Managers/Synergy_Engine.gd` |
| Visual Juice | 6 | `Scripts/BiomeCardShadow.gd`, `Scripts/Components/AgnosticTether.gd`, `Scripts/Components/JuiceyTxtPathTravel.gd`, `Scripts/Components/ScalePulseComponent.gd`, `Scripts/Components/spiral_sorter_component.gd`, `Scripts/FloatingText.gd` |
| UI & Grid | 14 | `Scripts/biome_board.gd`, `Scripts/Components/DragComponent.gd`, `Scripts/Components/InteractiveButtonComponent.gd`, `Scripts/Components/menu_card.gd`, `Scripts/main_menu.gd`, `Scripts/Managers/card_menu_manager.gd`, `Scripts/Managers/game_menu.gd`, `Scripts/Managers/inspector_controller.gd`, `Scripts/Managers/Settings.gd`, `Scripts/Managers/spinner_management_menu.gd`, `Scripts/MasterScripts/biome_card.gd`, `Scripts/MasterScripts/spinnercard.gd`, `Scripts/MasterScripts/unlock__lock_spinner_card.gd`, `Scripts/spinner_container.gd` |
| Biomes & Progression | 4 | `Scripts/DataScripts/biome_data.gd`, `Scripts/Managers/idlecardsway.gd`, `Scripts/Managers/idle_manager.gd`, `Scripts/Managers/warp_manager.gd` |
| Core Gameplay & Economy | 8 | `Scripts/DataScripts/armoury.gd`, `Scripts/DataScripts/player.gd`, `Scripts/DataScripts/Save_Data.gd`, `Scripts/DataScripts/spinner_data.gd`, `Scripts/DataScripts/stats_tracker.gd`, `Scripts/main.gd`, `Scripts/Utils/CascadeRouter.gd`, `Scripts/Utils/number_formatter.gd` |
| Audio | 3 | `Scripts/Components/Musicmanager_Component.gd`, `Scripts/Components/ThrottledAudioComponent.gd`, `Scripts/Components/UI_Audio.gd` |

- **Tier-2 significance heuristic** (mechanical, checkable — resolves the spec's deferred item): a system is promoted to Tier-2 (full read, real signal-flow detail) if **any** of:
  1. It contains an autoload/singleton script (cross-referenced against `project.godot`'s `[autoload]` list), OR
  2. It has a corresponding `design_docs/` category folder with ≥1 file, OR
  3. It was explicitly named as architecturally significant in the existing Aug 2026 memory audit.

  All 7 systems above satisfy criterion 2 (every one maps to a `design_docs/` folder) and most satisfy 1 or 3, so **all 7 get Tier-2 depth** for this bootstrap — seeded from the existing audit already in memory, not re-read from scratch. Only the tooling/addon scripts stay Tier-1 (registry line only, no system doc).

---

## Task 1: Write canonical CLAUDE.md template

**Files:**
- Create: `/home/avery/Godot_Projects/docs/templates/CLAUDE.md`

**Interfaces:**
- Produces: the canonical CLAUDE.md content that Task 5 copies verbatim into Spinner.

- [ ] **Step 1: Write the file**

```markdown
# Claude Workflow — Godot Game Projects

This file defines how Claude approaches work in this game project. It is identical across
all game projects; only the MCP tool references noted below vary if this project uses a
different Godot MCP server (see MCP-SWITCH.md).

## Principles

**Composition & reusability first.** Systems, scripts, and scenes should be composable and
configurable rather than tightly coupled to this game's specific content, so they can be
reused in future projects when they fit. Prefer signal-driven communication, resource-driven
configuration (`.tres` data over hardcoded values), and generic components over one-off code.

**Do only what the request needs.** The workflow steps below are not mandatory ritual for
every message — apply them when they're actually necessary to properly respond to what was
asked. A one-line question about what a function does doesn't need a full context-check pass.

## Workflow (when judged necessary)

1. **Orient cheaply first.** Check `project-state.md`'s "Overall Status" and "Recently
   Updated" sections — a few lines, not a deep read.
2. **Session-start drift check**, only if `HEAD` has moved since the commit hash recorded in
   `project-state.md`'s "Last Verified Commit" — otherwise skip entirely:
   - Diff actual script/scene filenames on disk against the Script Registry in
     `project-state.md`. Flag anything unlisted (orphan) and anything listed-but-deleted
     (dangling entry) into `project-state-orphans.md`.
   - Diff each system doc's "Design Doc Sources" commit markers against the current commit
     hashes of those files under `design_docs/`. Flag any system whose design docs changed
     since last sync in `project-state.md`'s "Design Sync Status" section.
3. **For the specific system being worked on:** read `project-state-[system].md` and
   `bugs-[system].md`. If what they describe doesn't match the actual code, update the doc
   first, then proceed with the task.
4. **Inspect the running game** (screenshot, run, test input) when necessary to confirm
   actual behavior — code existing is not the same as a feature working.
5. **Propose three focused tasks** with trade-offs and a recommendation, when the request
   calls for planning next steps rather than a specific fix.
6. **After the user's request is fully satisfied** (not after every individual edit): update
   the relevant `project-state-[system].md` and `bugs-[system].md`, then update the master
   `project-state.md` and `bugs.md` to reflect it. Advance the "Last Verified Commit" marker.
7. **Create new system docs on demand** — when work touches a system with no existing
   `project-state-[system].md`/`bugs-[system].md`, create both at that point (not
   preemptively), and register the system in the master docs.

## Implementation status is tri-state, not binary

Every feature tracked in a `project-state-[system].md` gets exactly one of:

- **Coded** — the script/logic exists.
- **Wired-in** — it's actually called/connected from the systems that should invoke it.
- **Verified-in-game** — observed working correctly in a running instance of the game.

This is independent of correctness — a Wired-in or Verified-in-game feature can still have an
open bug. Bugs are tracked separately in `bugs-[system].md`, never by downgrading this status.
A feature that hasn't been started at all isn't given a tri-state entry — it belongs only in
that system's "Gaps vs. Design Docs" section.

## Industry practices to default to (Godot-specific)

- Signal-driven communication between systems, not direct cross-references.
- Composition over inheritance.
- Autoload managers for cross-system state, not scattered singletons.
- Resource-driven configuration (`.tres`) over hardcoded values.
- Scene composition via reusable subscenes over monolithic scenes.
- Use the engine's own class reference (`godot --headless --doctool <dir>`) or live
  `ClassDB` reflection via the MCP when unsure of an API — don't guess from training data,
  which may not match the installed engine version.

## Current MCP

This project's Godot MCP server tools follow the `mcp__godot__*` naming pattern (e.g.,
`run_project`, `game_screenshot`, `game_eval`, `read_scene`). If this project switches to a
different Godot MCP server, run `MCP-SWITCH.md` rather than manually editing this section.
```

- [ ] **Step 2: Verify structural completeness**

Run:
```bash
grep -c '^## ' /home/avery/Godot_Projects/docs/templates/CLAUDE.md
grep -iE 'TBD|TODO|fill in|placeholder' /home/avery/Godot_Projects/docs/templates/CLAUDE.md
```
Expected: first command prints `5` (five `##` sections); second command prints nothing (no
placeholder markers).

- [ ] **Step 3: Commit**

```bash
cd /home/avery/Godot_Projects
git add docs/templates/CLAUDE.md
git commit -m "Add canonical CLAUDE.md template

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 2: Write canonical SETUP.md template

**Files:**
- Create: `/home/avery/Godot_Projects/docs/templates/SETUP.md`

**Interfaces:**
- Consumes: nothing from other tasks (self-contained bootstrap procedure).
- Produces: the canonical SETUP.md content that Task 5 copies verbatim into Spinner, and that
  Tasks 6-14 in this plan effectively execute by hand for Spinner's first run.

- [ ] **Step 1: Write the file**

```markdown
# Claude Project Setup

Run this once per project. It is idempotent — if `CLAUDE.md`, `project-state.md`, and
`bugs.md` all already exist at the project root, do nothing.

## Step 1 — Existence check

If `CLAUDE.md`, `project-state.md`, and `bugs.md` all exist, stop here. Setup is complete.

## Step 2 — Scope detection

Scan the project for existing game code beyond boilerplate (non-empty `Scripts/`-equivalent
folder with real logic, not just default template files). Auto-detect:

- **New project** — no meaningful existing code.
- **Existing codebase** — real game code already present.

State the detected assumption to the user before proceeding; let them correct it.

## Step 3a — New project path

- Copy `CLAUDE.md`, `ORGANIZE.md`, `MCP-SWITCH.md` from the canonical templates at
  `/home/avery/Godot_Projects/docs/templates/` into this project's root, unmodified.
- Write an empty `project-state.md` master (empty Script Registry, empty Implemented/Missing
  tables, "Last Verified Commit" set to current `HEAD`).
- Write an empty `bugs.md` master (empty Open Bugs table, empty Recently Fixed).
- If a `design_docs/`-equivalent folder exists despite no code yet, seed
  `project-state.md`'s "Missing/Gap Systems" table from its category folders.

## Step 3b — Existing codebase path (tiered audit)

**Tier 1 (always, mechanical):**
1. Enumerate every script/scene file: `find . -name "*.gd" -o -name "*.tscn" -o -name "*.tres"`.
2. For each file, grep for `signal`, `func`, `class_name`, `extends` to note its structural
   role.
3. Read `project.godot`'s `[autoload]` section to get the singleton list.
4. Read `design_docs/`'s folder structure (if present) to get candidate system boundaries.
5. Group scripts into systems using judgment — informed by design doc categories, folder
   structure, or autoload boundaries, whichever fits this specific project. No fixed rule.
6. Build the complete Script Registry table in `project-state.md` from this pass. Every file
   found in step 1 must have exactly one registry row (primary system + optional secondary).

**Tier 2 (selective, deep) — promote a system from Tier 1 to Tier 2 if any of:**
   - It contains an autoload/singleton script, OR
   - It has a corresponding `design_docs/` category folder with at least one file, OR
   - It is explicitly named as architecturally significant in any existing project memory/
     prior audit available to Claude.

   For each Tier-2 system: do a full read of its scripts, and produce a real
   `project-state-[system].md` with signal flow, script responsibilities, integration points,
   and per-feature tri-state status (Coded / Wired-in / Verified-in-game). If a prior audit of
   this exact codebase already exists (e.g., in Claude's session memory), seed from that
   rather than re-reading files that haven't changed since.

   Systems that don't meet any Tier-2 criterion get a Tier-1 stub: a Script Registry entry
   only, with a `project-state-[system].md` containing just "Current Implementation: not yet
   audited in depth."

7. Prompt the user once: "Would you like a project organization review too?" If yes, invoke
   `ORGANIZE.md`. If no, log the decline in `project-state.md`'s "Organization Notes" section
   so it is never auto-suggested again — the user can still request it manually anytime.

## Step 4 — Write remaining templates

Write `project-state-[system].md` / `bugs-[system].md` shells only for systems identified in
Step 3 — never preemptively for hypothetical future systems.

## Step 5 — Hand off

Report what was created or found. All future sessions defer to `CLAUDE.md`'s normal workflow.
```

- [ ] **Step 2: Verify structural completeness**

Run:
```bash
grep -c '^## ' /home/avery/Godot_Projects/docs/templates/SETUP.md
grep -iE 'TBD|TODO|fill in|placeholder' /home/avery/Godot_Projects/docs/templates/SETUP.md
```
Expected: first prints `6`; second prints nothing.

- [ ] **Step 3: Commit**

```bash
cd /home/avery/Godot_Projects
git add docs/templates/SETUP.md
git commit -m "Add canonical SETUP.md template

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 3: Write canonical ORGANIZE.md template

**Files:**
- Create: `/home/avery/Godot_Projects/docs/templates/ORGANIZE.md`

**Interfaces:**
- Produces: the canonical ORGANIZE.md content copied verbatim into Spinner in Task 5.

- [ ] **Step 1: Write the file**

```markdown
# Claude Project Organization Review

An on-demand utility for reviewing and improving file/folder naming and structure. Invocable
two ways: standalone, any time the user asks for a cleanup pass; or offered once during
`SETUP.md`'s initial bootstrap run.

## Process

1. **Survey** current file/folder naming and structure against Godot conventions (consistent
   casing, folder-per-responsibility, no duplicate/near-duplicate folders) and this project's
   own existing patterns.
2. **Propose** specific renames/moves as a numbered list, each with a one-line reason. Never
   execute anything unprompted.
3. **Approval gate.** Wait for explicit user approval — per item or as a batch.
4. **Execution.** Route every move/rename of a Godot-tracked resource (`.gd`, `.tscn`,
   `.tres`) through Godot MCP file operations (e.g., `mcp__godot__rename_file`) — never raw
   shell `mv`/`rm`. Raw filesystem operations can silently break UID-based or path-based
   resource references the engine tracks internally.
5. **Decline handling.** Any declined proposal is logged into `project-state.md`'s
   "Organization Notes" section — what was proposed, when, and that it was declined — so it
   is never auto-resurfaced. The user can still request a fresh review manually at any time.
```

- [ ] **Step 2: Verify structural completeness**

Run:
```bash
grep -c '^## ' /home/avery/Godot_Projects/docs/templates/ORGANIZE.md
grep -iE 'TBD|TODO|fill in|placeholder' /home/avery/Godot_Projects/docs/templates/ORGANIZE.md
```
Expected: first prints `1`; second prints nothing.

- [ ] **Step 3: Commit**

```bash
cd /home/avery/Godot_Projects
git add docs/templates/ORGANIZE.md
git commit -m "Add canonical ORGANIZE.md template

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 4: Write canonical MCP-SWITCH.md template

**Files:**
- Create: `/home/avery/Godot_Projects/docs/templates/MCP-SWITCH.md`

**Interfaces:**
- Produces: the canonical MCP-SWITCH.md content copied verbatim into Spinner in Task 5.

- [ ] **Step 1: Write the file**

```markdown
# Claude MCP Migration

Run this only when this project adopts a different Godot MCP server than the one currently
configured (see `CLAUDE.md`'s "Current MCP" section for what's active now).

## Process

1. Scan `CLAUDE.md` for every `mcp__<server>__<action>` tool reference.
2. Load the new MCP server's tool list/schema (via its own documentation or by inspecting its
   available tools directly).
3. Map each old capability to its nearest equivalent in the new server.
4. Rewrite `CLAUDE.md`'s tool references and "Current MCP" section in place — leave the
   workflow structure and principles sections untouched.
5. Flag any capability that has no equivalent in the new server, so it's a visible, explicit
   gap rather than a silently dropped capability.
```

- [ ] **Step 2: Verify structural completeness**

Run:
```bash
grep -c '^## ' /home/avery/Godot_Projects/docs/templates/MCP-SWITCH.md
grep -iE 'TBD|TODO|fill in|placeholder' /home/avery/Godot_Projects/docs/templates/MCP-SWITCH.md
```
Expected: first prints `1`; second prints nothing.

- [ ] **Step 3: Commit**

```bash
cd /home/avery/Godot_Projects
git add docs/templates/MCP-SWITCH.md
git commit -m "Add canonical MCP-SWITCH.md template

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 5: Install the four templates into Spinner

**Files:**
- Create: `/home/avery/Godot_Projects/Spinner/CLAUDE.md`
- Create: `/home/avery/Godot_Projects/Spinner/SETUP.md`
- Create: `/home/avery/Godot_Projects/Spinner/ORGANIZE.md`
- Create: `/home/avery/Godot_Projects/Spinner/MCP-SWITCH.md`

**Interfaces:**
- Consumes: the four canonical files from Tasks 1-4.
- Produces: Spinner now has all four agnostic docs at its root, ready for SETUP.md Step 1 to
  find them absent for `project-state.md`/`bugs.md` and proceed with bootstrap (Tasks 6-14).

- [ ] **Step 1: Copy the templates (plain Markdown, not Godot resources — safe to `cp`)**

```bash
cp /home/avery/Godot_Projects/docs/templates/CLAUDE.md /home/avery/Godot_Projects/Spinner/CLAUDE.md
cp /home/avery/Godot_Projects/docs/templates/SETUP.md /home/avery/Godot_Projects/Spinner/SETUP.md
cp /home/avery/Godot_Projects/docs/templates/ORGANIZE.md /home/avery/Godot_Projects/Spinner/ORGANIZE.md
cp /home/avery/Godot_Projects/docs/templates/MCP-SWITCH.md /home/avery/Godot_Projects/Spinner/MCP-SWITCH.md
```

- [ ] **Step 2: Verify byte-identical copies**

Run:
```bash
diff /home/avery/Godot_Projects/docs/templates/CLAUDE.md /home/avery/Godot_Projects/Spinner/CLAUDE.md
diff /home/avery/Godot_Projects/docs/templates/SETUP.md /home/avery/Godot_Projects/Spinner/SETUP.md
diff /home/avery/Godot_Projects/docs/templates/ORGANIZE.md /home/avery/Godot_Projects/Spinner/ORGANIZE.md
diff /home/avery/Godot_Projects/docs/templates/MCP-SWITCH.md /home/avery/Godot_Projects/Spinner/MCP-SWITCH.md
```
Expected: no output from any `diff` (files identical).

- [ ] **Step 3: Commit (in Spinner's own repo)**

```bash
cd /home/avery/Godot_Projects/Spinner
git add CLAUDE.md SETUP.md ORGANIZE.md MCP-SWITCH.md
git commit -m "Install Claude workflow templates

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 6: Verify ground truth is unchanged before writing project-state.md

**Files:**
- No files written — sanity check only, guards the embedded data in Task 7.

**Interfaces:**
- Consumes: nothing.
- Produces: a pass/fail confirmation that the counts baked into Task 7's file content are
  still accurate.

- [ ] **Step 1: Re-run the discovery commands to confirm no drift since planning**

```bash
cd /home/avery/Godot_Projects/Spinner
find ./Scripts -name "*.gd" | wc -l
git rev-parse HEAD
```
Expected: `54` and `bab83de871af71507e60628b22daa0240b891b0`. If either differs, stop — do not
proceed to Task 7 until the Script Registry table and commit references in that task are
re-derived to match the new reality.

---

## Task 7: Write project-state.md master hub for Spinner

**Files:**
- Create: `/home/avery/Godot_Projects/Spinner/project-state.md`

**Interfaces:**
- Consumes: the verified ground truth confirmed in Task 6 (this task is self-contained — the
  full Script Registry table is embedded directly below, not fetched from another task).
- Produces: the master doc that Tasks 8-14's system docs link back to, and that future
  sessions read first per `CLAUDE.md`'s workflow step 1.

**Rollup rule** (resolves ambiguity, stated once here for reuse by Tasks 8-14): a system's
rollup status in the "Implemented Systems" table is the **weakest** tri-state status among its
tracked (non-absent) features — a system with one Coded-only feature and the rest
Verified-in-game still rolls up to "Coded," because the whole system isn't reliable to call
done until every tracked feature is.

- [ ] **Step 1: Write the file**

```markdown
# Project State — Spinner (Master)

## Overall Status

Core kinematic/grid/economy loop is playable and verified in-game. The two headline design
systems for this build — Synergy and the associated Visual Juice payoff (traveling text,
tethers) — are fully coded but not wired into gameplay yet. See system docs for detail.

## Implemented Systems

| System | Rollup Status | Detail Doc |
|---|---|---|
| Kinematic Engine | Verified-in-game | [project-state-kinematic-engine.md](project-state-kinematic-engine.md) |
| Audio | Verified-in-game | [project-state-audio.md](project-state-audio.md) |
| UI & Grid | Wired-in | [project-state-ui-grid.md](project-state-ui-grid.md) |
| Core Gameplay & Economy | Wired-in | [project-state-core-gameplay.md](project-state-core-gameplay.md) |
| Biomes & Progression | Wired-in | [project-state-biomes-progression.md](project-state-biomes-progression.md) |
| Synergy System | Coded | [project-state-synergy-system.md](project-state-synergy-system.md) |
| Visual Juice | Coded | [project-state-visual-juice.md](project-state-visual-juice.md) |

## Missing/Gap Systems

| Gap | Design Doc | Notes |
|---|---|---|
| Ripple Unlock progression (backward cascade, attuned rewards, SPS milestone gating) | `design_docs/Biomes_Progression/Ripple_Unlock_System/` | Not implemented; see project-state-biomes-progression.md |
| Prismatic biome theming (white Origin → primary → secondary → Abyss) | `design_docs/Biomes_Progression/Prismatic_Biome_Directory/` | Implementation still uses original elemental theming (Fire/Water/Earth/etc.) |
| Spinner Tier 3/4, Void endgame roster | `design_docs/Spinner_Roster/` | Not started; deferred past current milestone |

## Critical Blockers

- None currently blocking forward progress. Synergy System and Visual Juice are the priority
  integration work (see their detail docs for the specific gaps).

## Recently Updated

- 2026-07-09 — Initial bootstrap of this documentation system (this file and all system
  spokes created).

## Script Registry

| Script/Scene Path | Primary System | Secondary System(s) |
|---|---|---|
| Scripts/Layouts/archimedan_spiral.gd | Kinematic Engine | - |
| Scripts/Layouts/kinematic_spiral.gd | Kinematic Engine | - |
| Scripts/Layouts/lissajous_spiral.gd | Kinematic Engine | - |
| Scripts/Layouts/logarithmic_spiral.gd | Kinematic Engine | - |
| Scripts/Layouts/OvalOribtSpiral.gd | Kinematic Engine | - |
| Scripts/Layouts/PhyllotaxisSpiral.gd | Kinematic Engine | - |
| Scripts/Layouts/ulam_spiral.gd | Kinematic Engine | - |
| Scripts/MasterScripts/master_spinner.gd | Kinematic Engine | UI & Grid |
| Scripts/MasterScripts/spiral_layout.gd | Kinematic Engine | - |
| Scripts/Utils/prime_math.gd | Kinematic Engine | - |
| Scripts/DataScripts/elements.gd | Synergy System | - |
| Scripts/DataScripts/Synergies/element_mutator_synergy.gd | Synergy System | - |
| Scripts/DataScripts/Synergies/Guard_Synergy.gd | Synergy System | - |
| Scripts/DataScripts/Synergies/Origin_Anchor_Synergy.gd | Synergy System | - |
| Scripts/DataScripts/Synergies/pattern_synergy.gd | Synergy System | - |
| Scripts/DataScripts/Synergies/synergy_rule.gd | Synergy System | - |
| Scripts/DataScripts/Synergies/Void_Isolation.gd | Synergy System | - |
| Scripts/element_container.gd | Synergy System | - |
| Scripts/Managers/Synergy_Engine.gd | Synergy System | - |
| Scripts/BiomeCardShadow.gd | Visual Juice | UI & Grid |
| Scripts/Components/AgnosticTether.gd | Visual Juice | Synergy System |
| Scripts/Components/JuiceyTxtPathTravel.gd | Visual Juice | - |
| Scripts/Components/ScalePulseComponent.gd | Visual Juice | - |
| Scripts/Components/spiral_sorter_component.gd | Visual Juice | Kinematic Engine |
| Scripts/FloatingText.gd | Visual Juice | - |
| Scripts/biome_board.gd | UI & Grid | Core Gameplay & Economy |
| Scripts/Components/DragComponent.gd | UI & Grid | - |
| Scripts/Components/InteractiveButtonComponent.gd | UI & Grid | - |
| Scripts/Components/menu_card.gd | UI & Grid | - |
| Scripts/main_menu.gd | UI & Grid | - |
| Scripts/Managers/card_menu_manager.gd | UI & Grid | - |
| Scripts/Managers/game_menu.gd | UI & Grid | - |
| Scripts/Managers/inspector_controller.gd | UI & Grid | - |
| Scripts/Managers/Settings.gd | UI & Grid | - |
| Scripts/Managers/spinner_management_menu.gd | UI & Grid | - |
| Scripts/MasterScripts/biome_card.gd | UI & Grid | - |
| Scripts/MasterScripts/spinnercard.gd | UI & Grid | - |
| Scripts/MasterScripts/unlock__lock_spinner_card.gd | UI & Grid | Biomes & Progression |
| Scripts/spinner_container.gd | UI & Grid | - |
| Scripts/DataScripts/biome_data.gd | Biomes & Progression | - |
| Scripts/Managers/idlecardsway.gd | Biomes & Progression | - |
| Scripts/Managers/idle_manager.gd | Biomes & Progression | - |
| Scripts/Managers/warp_manager.gd | Biomes & Progression | - |
| Scripts/DataScripts/armoury.gd | Core Gameplay & Economy | - |
| Scripts/DataScripts/player.gd | Core Gameplay & Economy | - |
| Scripts/DataScripts/Save_Data.gd | Core Gameplay & Economy | - |
| Scripts/DataScripts/spinner_data.gd | Core Gameplay & Economy | Synergy System |
| Scripts/DataScripts/stats_tracker.gd | Core Gameplay & Economy | - |
| Scripts/main.gd | Core Gameplay & Economy | - |
| Scripts/Utils/CascadeRouter.gd | Core Gameplay & Economy | Synergy System |
| Scripts/Utils/number_formatter.gd | Core Gameplay & Economy | - |
| Scripts/Components/Musicmanager_Component.gd | Audio | - |
| Scripts/Components/ThrottledAudioComponent.gd | Audio | - |
| Scripts/Components/UI_Audio.gd | Audio | - |
| Addons/script-ide/** and addons/script-ide/** (13 files) | Tooling (third-party editor plugin, not a game system) | - |

## Design Sync Status

| System | Last-Synced Design Commit | Status |
|---|---|---|
| Kinematic Engine | bab83de8 | In sync |
| Synergy System | bab83de8 | In sync |
| Visual Juice | bab83de8 | In sync |
| UI & Grid | bab83de8 | In sync |
| Biomes & Progression | bab83de8 | In sync |
| Core Gameplay & Economy | bab83de8 | In sync |
| Audio | bab83de8 | In sync |

## Organization Notes

(Empty — no `ORGANIZE.md` proposals made yet.)

## Last Verified Commit

`bab83de871af71507e60628b22daa0240b891b0`
```

- [ ] **Step 2: Verify structural completeness**

Run:
```bash
cd /home/avery/Godot_Projects/Spinner
grep -c '^## ' project-state.md
grep -iE 'TBD|TODO|fill in' project-state.md
grep -c '^|.*\.gd' project-state.md
```
Expected: first prints `9`; second prints nothing; third prints `54` (registry rows for game
scripts).

- [ ] **Step 3: Commit**

```bash
cd /home/avery/Godot_Projects/Spinner
git add project-state.md
git commit -m "Add master project-state.md for Spinner

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 8: Write project-state-kinematic-engine.md and bugs-kinematic-engine.md

**Files:**
- Create: `/home/avery/Godot_Projects/Spinner/project-state-kinematic-engine.md`
- Create: `/home/avery/Godot_Projects/Spinner/bugs-kinematic-engine.md`

**Interfaces:**
- Consumes: existing Aug 2026 memory audit finding that "the kinematic heartbeat, core loop,
  grid manager, audio throttle, and warp system are solid and match docs well," plus Jul 8
  2026 session findings that spinner mechanics were functional in a live run.
- Produces: linked from `project-state.md`'s Implemented Systems table (Task 7).

- [ ] **Step 1: Write project-state-kinematic-engine.md**

```markdown
# Project State — Kinematic Engine

## Current Implementation

The kinematic/spiral layout system drives spinner motion and positioning. Seven interchangeable
layout strategies (`Scripts/Layouts/*.gd`: Archimedean, kinematic, Lissajous, logarithmic,
oval-orbit, phyllotaxis, Ulam spiral) implement a shared shape-generation interface consumed by
`Scripts/MasterScripts/spiral_layout.gd`, which `master_spinner.gd` uses to position spinner
instances each tick. `Scripts/Utils/prime_math.gd` provides shared math helpers (prime
sequences / spacing calculations) used across the spiral layouts.

| Feature | Status | Script(s) | Notes |
|---|---|---|---|
| Global heartbeat / tick-driven motion | Verified-in-game | `master_spinner.gd`, `spiral_layout.gd` | Confirmed functional in 2026-07-08 live playtest session |
| Parametric spiral shapes (7 variants) | Verified-in-game | `Layouts/*.gd` | Matches `design_docs/Kinematic_Engine/Parametric_Shapes/` |
| Prime-based spacing math | Wired-in | `Utils/prime_math.gd` | Used by layouts; not independently visually verified |

## Gaps vs. Design Docs

No significant gaps identified against `design_docs/Kinematic_Engine/Global_Heartbeat/` and
`design_docs/Kinematic_Engine/Parametric_Shapes/` as of this audit.

## Known Issues & Workarounds

None currently tracked. See `bugs-kinematic-engine.md`.

## Related Systems

- **UI & Grid** — `master_spinner.gd` is also referenced there for board placement.
- **Visual Juice** — `spiral_sorter_component.gd` consumes kinematic layout output for sort
  animations.

## Design Doc Sources

- `design_docs/Kinematic_Engine/Global_Heartbeat/global_heartbeat.md` — synced at `bab83de8`
- `design_docs/Kinematic_Engine/Parametric_Shapes/parametric_shapes.md` — synced at `bab83de8`
```

- [ ] **Step 2: Write bugs-kinematic-engine.md**

```markdown
# Bugs — Kinematic Engine

## Open Bugs

None currently tracked.

## Fixed Bugs

None yet.
```

- [ ] **Step 3: Verify structural completeness**

```bash
cd /home/avery/Godot_Projects/Spinner
grep -c '^## ' project-state-kinematic-engine.md
grep -c '^## ' bugs-kinematic-engine.md
grep -iE 'TBD|TODO|fill in' project-state-kinematic-engine.md bugs-kinematic-engine.md
```
Expected: `5`, `2`, and no output from the third command.

- [ ] **Step 4: Commit**

```bash
cd /home/avery/Godot_Projects/Spinner
git add project-state-kinematic-engine.md bugs-kinematic-engine.md
git commit -m "Add Kinematic Engine project-state and bugs docs

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 9: Write project-state-synergy-system.md and bugs-synergy-system.md

**Files:**
- Create: `/home/avery/Godot_Projects/Spinner/project-state-synergy-system.md`
- Create: `/home/avery/Godot_Projects/Spinner/bugs-synergy-system.md`

**Interfaces:**
- Consumes: existing Aug 2026 memory audit finding: "`SynergyEngine.calculate_global_yield()`
  is never called; `synergy_rules` arrays on `SpinnerData` are empty; payouts use only
  `base_value × affinity × crit`."
- Produces: linked from `project-state.md`'s Implemented Systems table.

- [ ] **Step 1: Write project-state-synergy-system.md**

```markdown
# Project State — Synergy System

## Current Implementation

`Scripts/Managers/Synergy_Engine.gd` implements `calculate_global_yield()` and a rule-matching
structure. Six synergy rule types exist under `Scripts/DataScripts/Synergies/`: element
mutator, guard, origin anchor, pattern, generic synergy rule base, and void isolation.
`Scripts/element_container.gd` and `Scripts/DataScripts/elements.gd` provide the element-typing
data these rules match against.

| Feature | Status | Script(s) | Notes |
|---|---|---|---|
| Synergy rule types (6 variants) | Coded | `DataScripts/Synergies/*.gd` | Classes exist and are structurally complete |
| Global yield calculation | Coded | `Managers/Synergy_Engine.gd:calculate_global_yield()` | Never called from the payout pipeline |
| Synergy rule population per spinner | Coded | `DataScripts/spinner_data.gd` | `synergy_rules` arrays are empty at runtime — no rules are ever assigned to a `.tres` resource |

## Gaps vs. Design Docs

Every mechanic described across `design_docs/Synergy_System/` (Color_Attunement_Potency,
Logic_Separation, Origin_Core_Anchor, Pattern_Matrix_Sequence, Population_Composition,
Ring_Guard_Context) has a corresponding coded rule class, but none affect actual payouts.
Current payout math is `base_value × affinity × crit` only — the entire synergy multiplier
layer is a no-op in live gameplay. This is the single largest gap between design intent and
shipped behavior in the codebase.

## Known Issues & Workarounds

None tracked as bugs yet — the disconnect is a missing integration, not a defect in existing
code. See `bugs-synergy-system.md` if integration work introduces regressions.

## Related Systems

- **Core Gameplay & Economy** — payout pipeline (`spinner_data.gd`) is where
  `calculate_global_yield()` needs to be invoked.
- **Visual Juice** — traveling text and tether visuals are meant to represent active synergy
  connections; currently nothing drives them because no synergy state exists at runtime.

## Design Doc Sources

- `design_docs/Synergy_System/Color_Attunement_Potency/color_attunement_potency.md` — synced at `bab83de8`
- `design_docs/Synergy_System/Logic_Separation/logic_separation.md` — synced at `bab83de8`
- `design_docs/Synergy_System/Origin_Core_Anchor/origin_core_anchor.md` — synced at `bab83de8`
- `design_docs/Synergy_System/Pattern_Matrix_Sequence/pattern_matrix_sequence.md` — synced at `bab83de8`
- `design_docs/Synergy_System/Population_Composition/population_composition.md` — synced at `bab83de8`
- `design_docs/Synergy_System/Ring_Guard_Context/ring_guard_context.md` — synced at `bab83de8`
```

- [ ] **Step 2: Write bugs-synergy-system.md**

```markdown
# Bugs — Synergy System

## Open Bugs

### Synergy engine never invoked
- **Script:** `Scripts/Managers/Synergy_Engine.gd`
- **Priority:** High
- **Description:** `calculate_global_yield()` is fully implemented but has no call site
  anywhere in the payout pipeline. This is tracked here rather than only as a "gap" because it
  represents a specific, fixable integration defect, not an unstarted feature.

## Fixed Bugs

None yet.
```

- [ ] **Step 3: Verify structural completeness**

```bash
cd /home/avery/Godot_Projects/Spinner
grep -c '^## ' project-state-synergy-system.md
grep -c '^## ' bugs-synergy-system.md
grep -iE 'TBD|TODO|fill in' project-state-synergy-system.md bugs-synergy-system.md
```
Expected: `5`, `2`, no output from the third command.

- [ ] **Step 4: Commit**

```bash
cd /home/avery/Godot_Projects/Spinner
git add project-state-synergy-system.md bugs-synergy-system.md
git commit -m "Add Synergy System project-state and bugs docs

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 10: Write project-state-visual-juice.md and bugs-visual-juice.md

**Files:**
- Create: `/home/avery/Godot_Projects/Spinner/project-state-visual-juice.md`
- Create: `/home/avery/Godot_Projects/Spinner/bugs-visual-juice.md`

**Interfaces:**
- Consumes: existing Aug 2026 memory audit findings on `JuiceyTxtPathTravel.gd` (traveling
  text accumulator, "fully coded but never invoked... `biome_board` creates static floating
  text instead"), `AgnosticTether.gd` ("only activates via T-key debug binding"), and HDR
  glow/camera dynamics gaps.
- Produces: linked from `project-state.md`'s Implemented Systems table.

- [ ] **Step 1: Write project-state-visual-juice.md**

```markdown
# Project State — Visual Juice

## Current Implementation

`Scripts/Components/JuiceyTxtPathTravel.gd` implements a per-sweep traveling-text accumulator
intended to replace per-lap floating numbers with a single juiced trail. `Scripts/FloatingText.gd`
is the simpler static floating-text component actually in use. `Scripts/Components/AgnosticTether.gd`
implements tether-line visuals between spinners. `Scripts/Components/ScalePulseComponent.gd` and
`Scripts/Components/spiral_sorter_component.gd` provide juice animation (pulse scaling, sort
transitions). `Scripts/BiomeCardShadow.gd` provides drop-shadow polish on biome cards.

| Feature | Status | Script(s) | Notes |
|---|---|---|---|
| Traveling text accumulator (JuicedPathTraveler) | Coded | `Components/JuiceyTxtPathTravel.gd` | Never instantiated; `biome_board.gd` uses static `FloatingText.gd` instead |
| Tether network visuals | Coded | `Components/AgnosticTether.gd` | Only activates via a T-key debug input binding, not synergy-driven |
| Scale pulse / sort juice | Verified-in-game | `ScalePulseComponent.gd`, `spiral_sorter_component.gd` | Confirmed rendering in 2026-07-08 playtest |
| HDR glow | Wired-in | (shader-level, see `design_docs/Visual_Juice/Shaders_Polish/`) | Configured; camera dynamics and drag-swap interaction glow not implemented |

## Gaps vs. Design Docs

`design_docs/Visual_Juice/Traveling_Text_Gradient_Trail/` describes the JuicedPathTraveler
accumulator as the primary payout feedback mechanism — it exists in code but is entirely
unused in the live game. `design_docs/Visual_Juice/Blueprint_Tethers/` describes tethers as
synergy-state-driven; current tether activation is a developer debug binding, not tied to any
game state. `design_docs/Visual_Juice/Shaders_Polish/` describes camera dynamics and drag-swap
interaction effects neither of which are implemented.

## Known Issues & Workarounds

The T-key debug binding for tethers should be removed or gated behind a debug flag before any
public build — see `bugs-visual-juice.md`.

## Related Systems

- **Synergy System** — tethers and traveling text are both meant to visualize synergy state,
  which currently doesn't exist at runtime (see project-state-synergy-system.md).
- **Kinematic Engine** — `spiral_sorter_component.gd` consumes kinematic layout positions.

## Design Doc Sources

- `design_docs/Visual_Juice/Blueprint_Tethers/blueprint_tethers.md` — synced at `bab83de8`
- `design_docs/Visual_Juice/Shaders_Polish/shaders_polish.md` — synced at `bab83de8`
- `design_docs/Visual_Juice/Traveling_Text_Gradient_Trail/traveling_text_gradient_trail.md` — synced at `bab83de8`
```

- [ ] **Step 2: Write bugs-visual-juice.md**

```markdown
# Bugs — Visual Juice

## Open Bugs

### Tether network only reachable via debug key binding
- **Script:** `Scripts/Components/AgnosticTether.gd`
- **Priority:** Medium
- **Description:** Tethers only render when the T-key debug input is pressed. There is no
  synergy-driven trigger. Should either be gated out of release builds or wired to real state
  before shipping.

## Fixed Bugs

None yet.
```

- [ ] **Step 3: Verify structural completeness**

```bash
cd /home/avery/Godot_Projects/Spinner
grep -c '^## ' project-state-visual-juice.md
grep -c '^## ' bugs-visual-juice.md
grep -iE 'TBD|TODO|fill in' project-state-visual-juice.md bugs-visual-juice.md
```
Expected: `5`, `2`, no output from the third command.

- [ ] **Step 4: Commit**

```bash
cd /home/avery/Godot_Projects/Spinner
git add project-state-visual-juice.md bugs-visual-juice.md
git commit -m "Add Visual Juice project-state and bugs docs

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 11: Write project-state-ui-grid.md and bugs-ui-grid.md

**Files:**
- Create: `/home/avery/Godot_Projects/Spinner/project-state-ui-grid.md`
- Create: `/home/avery/Godot_Projects/Spinner/bugs-ui-grid.md`

**Interfaces:**
- Consumes: existing memory audit finding that "grid manager... solid and match docs well,"
  plus Jul 8 2026 session findings ("Game rendering successfully," "Game input system
  functional," "Scene transitions functioning without errors").
- Produces: linked from `project-state.md`'s Implemented Systems table.

- [ ] **Step 1: Write project-state-ui-grid.md**

```markdown
# Project State — UI & Grid

## Current Implementation

`Scripts/biome_board.gd` is the grid manager — placement, swap, and board-state logic for
spinner cards within a biome. Supporting UI: menu navigation (`main_menu.gd`,
`card_menu_manager.gd`, `game_menu.gd`, `spinner_management_menu.gd`, `Settings.gd`),
inspection (`inspector_controller.gd`), and card-level components (`menu_card.gd`,
`biome_card.gd`, `spinnercard.gd`, `unlock__lock_spinner_card.gd`, `InteractiveButtonComponent.gd`,
`DragComponent.gd`, `spinner_container.gd`).

| Feature | Status | Script(s) | Notes |
|---|---|---|---|
| Grid placement / swap mechanics | Verified-in-game | `biome_board.gd` | Confirmed solid against design in prior audit and 2026-07-08 playtest |
| Scene transitions (menu ↔ gameplay) | Verified-in-game | `main_menu.gd`, `game_menu.gd` | Confirmed functioning without errors in 2026-07-08 session |
| Drag-to-swap interaction | Wired-in | `Components/DragComponent.gd` | Functional; not exhaustively edge-case tested |
| Card unlock/lock state | Wired-in | `unlock__lock_spinner_card.gd` | Uses generic requirement gates, not the design's specific ripple-unlock ordering (see Gaps) |

## Gaps vs. Design Docs

`design_docs/UI/Grid_Manager/` is otherwise well matched by `biome_board.gd`. The unlock
ordering gap belongs primarily to Biomes & Progression (Ripple Unlock system) but surfaces
here too since `unlock__lock_spinner_card.gd` is the UI-facing consumer of that missing logic.

## Known Issues & Workarounds

None tracked as bugs yet. See `bugs-ui-grid.md`.

## Related Systems

- **Biomes & Progression** — unlock gating logic origin.
- **Kinematic Engine** — `master_spinner.gd` is shared for board placement.
- **Core Gameplay & Economy** — `biome_board.gd` reads payout data from `spinner_data.gd`.

## Design Doc Sources

- `design_docs/UI/Grid_Manager/grid_manager.md` — synced at `bab83de8`
```

- [ ] **Step 2: Write bugs-ui-grid.md**

```markdown
# Bugs — UI & Grid

## Open Bugs

None currently tracked.

## Fixed Bugs

None yet.
```

- [ ] **Step 3: Verify structural completeness**

```bash
cd /home/avery/Godot_Projects/Spinner
grep -c '^## ' project-state-ui-grid.md
grep -c '^## ' bugs-ui-grid.md
grep -iE 'TBD|TODO|fill in' project-state-ui-grid.md bugs-ui-grid.md
```
Expected: `5`, `2`, no output from the third command.

- [ ] **Step 4: Commit**

```bash
cd /home/avery/Godot_Projects/Spinner
git add project-state-ui-grid.md bugs-ui-grid.md
git commit -m "Add UI & Grid project-state and bugs docs

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 12: Write project-state-biomes-progression.md and bugs-biomes-progression.md

**Files:**
- Create: `/home/avery/Godot_Projects/Spinner/project-state-biomes-progression.md`
- Create: `/home/avery/Godot_Projects/Spinner/bugs-biomes-progression.md`

**Interfaces:**
- Consumes: existing memory audit findings that the warp system is solid, that Ripple Unlock
  progression is not implemented, and that the game uses elemental (not prismatic) biome
  theming.
- Produces: linked from `project-state.md`'s Implemented Systems table and Missing/Gap Systems
  table (Ripple Unlock and prismatic theming rows).

- [ ] **Step 1: Write project-state-biomes-progression.md**

```markdown
# Project State — Biomes & Progression

## Current Implementation

`Scripts/Managers/warp_manager.gd` (autoload: `WarpManager`) handles biome-to-biome warp
transitions. `Scripts/DataScripts/biome_data.gd` holds per-biome configuration.
`Scripts/Managers/idle_manager.gd` and `idlecardsway.gd` handle idle-state progression/animation
while away from a biome.

| Feature | Status | Script(s) | Notes |
|---|---|---|---|
| Warp/biome transition | Verified-in-game | `Managers/warp_manager.gd` | Confirmed solid in prior audit |
| Idle progression | Wired-in | `Managers/idle_manager.gd`, `idlecardsway.gd` | Functional; not independently verified in a long-idle session |
| Biome unlock gating | Wired-in | `biome_data.gd` | Uses generic requirement gates, not the designed Ripple Unlock ordering |

## Gaps vs. Design Docs

`design_docs/Biomes_Progression/Ripple_Unlock_System/` describes backward-cascade unlock
propagation, attuned-card rewards, and SPS-milestone gating — none of this is implemented;
current unlock is a simple generic gate with no specific ordering logic.
`design_docs/Biomes_Progression/Prismatic_Biome_Directory/` describes a revised prismatic
color model (white Origin → Red/Blue/Yellow primaries → Purple/Green/Orange secondaries →
Abyss) superseding the original elemental theme (Fire/Water/Earth/Wind/Lightning/Tech/Void/
Demonic/Angelic) the current implementation still uses throughout `biome_data.gd` and related
UI. This is a full theming pivot, not a small gap — resolving it is a scope decision, not a
bug fix.

## Known Issues & Workarounds

None tracked as bugs yet. See `bugs-biomes-progression.md`.

## Related Systems

- **UI & Grid** — `unlock__lock_spinner_card.gd` is the UI consumer of unlock-gating logic.
- **Core Gameplay & Economy** — SPS (spins-per-second) milestone data needed for Ripple Unlock
  gating lives in the economy/stats layer.

## Design Doc Sources

- `design_docs/Biomes_Progression/Prismatic_Biome_Directory/prismatic_biome_directory.md` — synced at `bab83de8`
- `design_docs/Biomes_Progression/Ripple_Unlock_System/ripple_unlock_system.md` — synced at `bab83de8`
- `design_docs/Biomes_Progression/Shifting_Baseline_Model/shifting_baseline_model.md` — synced at `bab83de8`
```

- [ ] **Step 2: Write bugs-biomes-progression.md**

```markdown
# Bugs — Biomes & Progression

## Open Bugs

None currently tracked.

## Fixed Bugs

None yet.
```

- [ ] **Step 3: Verify structural completeness**

```bash
cd /home/avery/Godot_Projects/Spinner
grep -c '^## ' project-state-biomes-progression.md
grep -c '^## ' bugs-biomes-progression.md
grep -iE 'TBD|TODO|fill in' project-state-biomes-progression.md bugs-biomes-progression.md
```
Expected: `5`, `2`, no output from the third command.

- [ ] **Step 4: Commit**

```bash
cd /home/avery/Godot_Projects/Spinner
git add project-state-biomes-progression.md bugs-biomes-progression.md
git commit -m "Add Biomes & Progression project-state and bugs docs

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 13: Write project-state-core-gameplay.md and bugs-core-gameplay.md

**Files:**
- Create: `/home/avery/Godot_Projects/Spinner/project-state-core-gameplay.md`
- Create: `/home/avery/Godot_Projects/Spinner/bugs-core-gameplay.md`

**Interfaces:**
- Consumes: existing memory audit findings: "upgrade system mutates loaded `.tres` resources
  in memory without persisting the multiplier, causing all upgrades to vanish on reload,"
  "100 trillion starting spins is a debug value," "lap scoring prints every frame... will tank
  performance."
- Produces: linked from `project-state.md`'s Implemented Systems table; the three bugs above
  populate this system's bugs doc as Critical/High priority.

- [ ] **Step 1: Write project-state-core-gameplay.md**

```markdown
# Project State — Core Gameplay & Economy

## Current Implementation

`Scripts/main.gd` is the top-level game entry point. `Scripts/DataScripts/player.gd` (autoload:
`Player`), `armoury.gd` (autoload: `Armoury`), and `Save_Data.gd` (autoload: `SaveData`) hold
core player/economy/persistence state. `spinner_data.gd` holds per-spinner runtime state
including payout values. `stats_tracker.gd` tracks lap/spin statistics.
`Scripts/Utils/CascadeRouter.gd` compiles cascade execution matrices for chained payout
triggers. `Scripts/Utils/number_formatter.gd` formats large numeric values for display.

| Feature | Status | Script(s) | Notes |
|---|---|---|---|
| Core game loop / tick-driven payout | Verified-in-game | `main.gd`, `spinner_data.gd` | Confirmed solid in prior audit and 2026-07-08 playtest |
| Save/load persistence | Wired-in | `Save_Data.gd` | Functions, but see upgrade-persistence bug below |
| Upgrade application | Wired-in | `armoury.gd`, `spinner_data.gd` | Applies correctly within a session; does not persist across reload (bug, see `bugs-core-gameplay.md`) |
| Cascade routing | Coded | `Utils/CascadeRouter.gd` | Guards on `spinner.data.get_synergy_jumps()`, a method that doesn't exist on `SpinnerData` — this makes cascade routing a no-op regardless of synergy state |
| Stats tracking | Wired-in | `stats_tracker.gd` | Functional; lap-scoring log spam is a performance bug, not a correctness issue (see bugs doc) |

## Gaps vs. Design Docs

`design_docs/Core_Gameplay/Game_Loop/` is well matched by `main.gd`/`spinner_data.gd`.
`design_docs/Core_Gameplay/Economy_Tuning/` describes upgrade multipliers that should persist
across sessions — the current implementation does not (tracked as a bug, not a gap, since the
persistence mechanism exists and is simply broken rather than absent).

## Known Issues & Workarounds

See `bugs-core-gameplay.md` for the upgrade-persistence, debug-value, and log-spam issues —
all three were identified in the prior full-codebase audit and are not yet fixed.

## Related Systems

- **Synergy System** — `CascadeRouter.gd`'s missing `get_synergy_jumps()` dependency lives on
  `SpinnerData`, shared with the Synergy System's data model.
- **Biomes & Progression** — SPS milestone data for Ripple Unlock gating would be sourced from
  `stats_tracker.gd`.

## Design Doc Sources

- `design_docs/Core_Gameplay/Economy_Tuning/economy_tuning.md` — synced at `bab83de8`
- `design_docs/Core_Gameplay/Game_Loop/game_loop.md` — synced at `bab83de8`
```

- [ ] **Step 2: Write bugs-core-gameplay.md**

```markdown
# Bugs — Core Gameplay & Economy

## Open Bugs

### Upgrade multipliers do not persist across reload
- **Script:** `Scripts/DataScripts/armoury.gd`, `Scripts/DataScripts/spinner_data.gd`
- **Priority:** Critical
- **Description:** Upgrades mutate loaded `.tres` resources in memory only. The multiplier is
  never written back to persistent save data, so all purchased upgrades vanish on reload.

### Cascade routing is a silent no-op
- **Script:** `Scripts/Utils/CascadeRouter.gd`
- **Priority:** High
- **Description:** Execution matrix compilation guards on `spinner.data.get_synergy_jumps()`,
  which is not defined anywhere on `SpinnerData`. The guard always fails, so cascade routing
  never executes, with no error surfaced.

### Debug starting-spins value left in production data
- **Script:** `Scripts/DataScripts/player.gd` (or associated default `.tres`)
- **Priority:** Medium
- **Description:** Starting spins value is set to 100 trillion, a debug convenience value that
  must not ship.

### Lap scoring logs every frame
- **Script:** `Scripts/DataScripts/stats_tracker.gd`
- **Priority:** Medium
- **Description:** Lap scoring prints on every frame (up to 120x/sec at full spinner count),
  which will degrade performance at scale. Should be throttled or removed.

## Fixed Bugs

None yet.
```

- [ ] **Step 3: Verify structural completeness**

```bash
cd /home/avery/Godot_Projects/Spinner
grep -c '^## ' project-state-core-gameplay.md
grep -c '^## ' bugs-core-gameplay.md
grep -iE 'TBD|TODO|fill in' project-state-core-gameplay.md bugs-core-gameplay.md
```
Expected: `5`, `2`, no output from the third command.

- [ ] **Step 4: Commit**

```bash
cd /home/avery/Godot_Projects/Spinner
git add project-state-core-gameplay.md bugs-core-gameplay.md
git commit -m "Add Core Gameplay & Economy project-state and bugs docs

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 14: Write project-state-audio.md and bugs-audio.md

**Files:**
- Create: `/home/avery/Godot_Projects/Spinner/project-state-audio.md`
- Create: `/home/avery/Godot_Projects/Spinner/bugs-audio.md`

**Interfaces:**
- Consumes: existing memory audit finding that "audio throttle" is solid and matches docs.
- Produces: linked from `project-state.md`'s Implemented Systems table.

- [ ] **Step 1: Write project-state-audio.md**

```markdown
# Project State — Audio

## Current Implementation

`Scripts/Components/Musicmanager_Component.gd` handles background music playback.
`Scripts/Components/ThrottledAudioComponent.gd` rate-limits high-frequency SFX (e.g., spin/tick
sounds) to avoid audio clipping/spam under heavy load. `Scripts/Components/UI_Audio.gd` handles
UI interaction sounds (clicks, menu transitions).

| Feature | Status | Script(s) | Notes |
|---|---|---|---|
| Music playback | Verified-in-game | `Musicmanager_Component.gd` | Confirmed solid in prior audit |
| Throttled SFX | Verified-in-game | `ThrottledAudioComponent.gd` | Matches `design_docs/Audio/Split-Layer_Mix/` throttling intent |
| UI interaction sounds | Wired-in | `UI_Audio.gd` | Functional; not independently re-verified this audit |

## Gaps vs. Design Docs

No significant gaps identified against `design_docs/Audio/Split-Layer_Mix/` as of this audit.

## Known Issues & Workarounds

None currently tracked. See `bugs-audio.md`.

## Related Systems

- **Core Gameplay & Economy** — throttled SFX volume/frequency likely scales with spin rate
  from `stats_tracker.gd`.

## Design Doc Sources

- `design_docs/Audio/Split-Layer_Mix/split-layer_mix.md` — synced at `bab83de8`
```

- [ ] **Step 2: Write bugs-audio.md**

```markdown
# Bugs — Audio

## Open Bugs

None currently tracked.

## Fixed Bugs

None yet.
```

- [ ] **Step 3: Verify structural completeness**

```bash
cd /home/avery/Godot_Projects/Spinner
grep -c '^## ' project-state-audio.md
grep -c '^## ' bugs-audio.md
grep -iE 'TBD|TODO|fill in' project-state-audio.md bugs-audio.md
```
Expected: `5`, `2`, no output from the third command.

- [ ] **Step 4: Commit**

```bash
cd /home/avery/Godot_Projects/Spinner
git add project-state-audio.md bugs-audio.md
git commit -m "Add Audio project-state and bugs docs

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 15: Write bugs.md master hub for Spinner

**Files:**
- Create: `/home/avery/Godot_Projects/Spinner/bugs.md`

**Interfaces:**
- Consumes: the four open bugs logged in Task 13 (`bugs-core-gameplay.md`) and the one open
  bug each from Tasks 9 and 10 (`bugs-synergy-system.md`, `bugs-visual-juice.md`).
- Produces: the master bugs doc read by `CLAUDE.md`'s workflow.

- [ ] **Step 1: Write the file**

```markdown
# Bugs — Spinner (Master)

## Open Bugs by System

| System | Open Count | Detail Doc |
|---|---|---|
| Kinematic Engine | 0 | [bugs-kinematic-engine.md](bugs-kinematic-engine.md) |
| Synergy System | 1 | [bugs-synergy-system.md](bugs-synergy-system.md) |
| Visual Juice | 1 | [bugs-visual-juice.md](bugs-visual-juice.md) |
| UI & Grid | 0 | [bugs-ui-grid.md](bugs-ui-grid.md) |
| Biomes & Progression | 0 | [bugs-biomes-progression.md](bugs-biomes-progression.md) |
| Core Gameplay & Economy | 4 | [bugs-core-gameplay.md](bugs-core-gameplay.md) |
| Audio | 0 | [bugs-audio.md](bugs-audio.md) |

## Recently Fixed

None yet — this is the initial bootstrap.

## Critical/Showstopper Bugs

- **Upgrade multipliers do not persist across reload** (Core Gameplay & Economy) — data loss
  on every session end; highest-priority fix before any further economy tuning.
```

- [ ] **Step 2: Verify counts reconcile**

```bash
cd /home/avery/Godot_Projects/Spinner
grep -c '^### ' bugs-synergy-system.md bugs-visual-juice.md bugs-core-gameplay.md
```
Expected: `bugs-synergy-system.md:1`, `bugs-visual-juice.md:1`, `bugs-core-gameplay.md:4` —
matching the Open Count column above (1, 1, 4).

- [ ] **Step 3: Commit**

```bash
cd /home/avery/Godot_Projects/Spinner
git add bugs.md
git commit -m "Add master bugs.md for Spinner

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

## Task 16: Final verification pass across the whole doc system

**Files:**
- No new files — this task verifies Tasks 1-15 are internally consistent.

**Interfaces:**
- Consumes: every file created in Tasks 1-15.

- [ ] **Step 1: Verify every system doc referenced in project-state.md actually exists**

```bash
cd /home/avery/Godot_Projects/Spinner
for f in project-state-kinematic-engine.md project-state-synergy-system.md \
         project-state-visual-juice.md project-state-ui-grid.md \
         project-state-biomes-progression.md project-state-core-gameplay.md \
         project-state-audio.md bugs-kinematic-engine.md bugs-synergy-system.md \
         bugs-visual-juice.md bugs-ui-grid.md bugs-biomes-progression.md \
         bugs-core-gameplay.md bugs-audio.md; do
  test -f "$f" && echo "OK: $f" || echo "MISSING: $f"
done
```
Expected: all 14 lines print `OK:`, none print `MISSING:`.

- [ ] **Step 2: Verify no orphan scripts (Script Registry covers every real file)**

```bash
cd /home/avery/Godot_Projects/Spinner
find ./Scripts -name "*.gd" | wc -l
grep -c '^| Scripts/' project-state.md
```
Expected: both print `54`.

- [ ] **Step 3: Verify all four agnostic templates present at Spinner root and match canonical copies**

```bash
diff /home/avery/Godot_Projects/docs/templates/CLAUDE.md /home/avery/Godot_Projects/Spinner/CLAUDE.md
diff /home/avery/Godot_Projects/docs/templates/SETUP.md /home/avery/Godot_Projects/Spinner/SETUP.md
diff /home/avery/Godot_Projects/docs/templates/ORGANIZE.md /home/avery/Godot_Projects/Spinner/ORGANIZE.md
diff /home/avery/Godot_Projects/docs/templates/MCP-SWITCH.md /home/avery/Godot_Projects/Spinner/MCP-SWITCH.md
```
Expected: no output from any command.

- [ ] **Step 4: Confirm git status is clean in both repos**

```bash
cd /home/avery/Godot_Projects && git status --short
cd /home/avery/Godot_Projects/Spinner && git status --short
```
Expected: no output from either command (everything committed).

No commit needed for this task — it's verification-only, and any files it would touch were
already committed in their respective tasks.
