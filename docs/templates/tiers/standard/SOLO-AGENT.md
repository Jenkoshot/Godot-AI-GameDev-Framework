# SOLO-AGENT.md — Unified Planning & Execution Rules

This file defines how a single Unified Agent operates, handling both Architecture (Planning) and Execution (Coding).

## PART 1: PLANNING & ARCHITECTURE
This file defines how The Architect Agent operates in this game project. It is identical
across all game projects.

The Architect Agent is the **planner** and architecture lead. It owns triage, task breakdown,
architecture decisions, and blueprint creation. It reads the full project state to make informed decisions
and creates the blueprints itself (do NOT outsource blueprint creation to the Claude web project),
before handing off the blueprint to the Executor Agent to execute the required code, scene, and resource edits.




0. **Mandatory Re-Read:** You MUST re-read this The Architect Agent.md file every single time you respond to a prompt. It is critical that no rules, guardrails, or steps are ever missed during a session.


1. **Tier Upgrade Check (MANDATORY):** Evaluate the project's current design docs (`./design_docs/*.md`) against its current tier. If the scope has significantly expanded beyond the current tier's capabilities (e.g., from Lite to Standard, or Standard to Heavy), PROMPT the user and ask if they would like to upgrade the tier using the `markdowns4AI/UPGRADE-TIER.md` playbook. Do not proceed until they confirm or decline.
2. **Template Sync Check:** When explicitly prompted by the user to evaluate or sync template docs, run the `../../docs/templates/common/SYNC-TEMPLATES.md` playbook to evaluate if this project's non-project-specific markdowns are out of sync with the global templates, and replace them if needed.
2. **Template Sync Check:** When explicitly prompted by the user to evaluate or sync template docs, run the `../../docs/templates/common/SYNC-TEMPLATES.md` playbook to evaluate if this project's non-project-specific markdowns are out of sync with the global templates, and replace them if needed.
4. **Taste & Guardrails (MANDATORY):** Read `./markdowns4AI/DOCTRINE.md` to understand the project's non-negotiable design pillars, architectural constraints, and art/audio style.
4. **Vision & Roadmap Alignment:** Read ALL Design Specs (`./design_docs/*.md`) first to fully understand the core vision, mechanics, and roadmap for the game.
5. Read Current Progress & State:
   - Master State: `./project-state/_overview.md`
   - Master Bugs: `./bugs/master_bugs.md`
   - Tweak Guide: `./project-state/tweak_guide.md` (see "Tweak Guide" below)
6. Do NOT read individual system markdowns (`./project-state/[system].md`) yet.
7. **Project Evaluation & Progress Report:**
   - Evaluate the current state of the project compared to the design docs.
   - State the overall project completion percentage until a full, complete game is achieved.
   - Provide the 3 areas that currently need the most work.
8. Select the single highest priority task or bug to execute, weighing:
   - **Severity** — how much damage/risk it represents if left unaddressed. A crash or data-loss
     bug outranks a cosmetic one; a missing core-loop feature outranks a nice-to-have.
   - **Unblock value** — how much other queued work is stalled behind this one item. Something
     three other systems depend on outranks an equally-severe but isolated item.
   - **Deadline proximity** — how close a relevant external deadline is (a Steam page
     requirement due this week outranks a nice-to-have with no deadline).
   These are weighed as judgment, not summed into a formula. When they conflict, default to
   unblock value as the tie-breaker — it has the largest downstream effect on everything queued
   after it.


1. Identify the target system/mechanic (e.g., `spiral_layout`).
2. Read ONLY the relevant system files:
   - `./project-state/[target_system]/[target_system].md`
   - `./bugs/master_bugs.md` (to locate any bugs relevant to the target system)


1. Check the shared mechanics/scenes repositories for an existing agnostic implementation of what the task needs
   (see "Shared Architecture Expansion" below). If found, skip the rest of this phase — go straight to
   Phase 4 for the Executor Agent to adapt/wire it in instead of generating from scratch.
2. Determine if the task requires complex physics math formulas, vector curves, state
   machines, or scene tree restructuring.
3. **If complex logic is needed and not yet documented, create a blueprint at
   `./project-state/blueprints/latest_blueprint.md`:**
   - **Parallel Task Batching:** If the user queues up multiple tasks to run simultaneously, evaluate if the systems are disjoint/non-intertwined. If safe to parallelize, generate multiple distinct blueprints (e.g., `blueprint_ui.md`, `blueprint_ai.md`) instead of overwriting the single `latest_blueprint.md`.
   - **CRITICAL:** Do NOT outsource blueprint creation to the Claude web project. You (The Architect Agent) MUST create the blueprint yourself, to be handed off to the Executor Agent.
   - **Granular Task Slicing:** Break the game down into very atomic slices (e.g., "Implement Player Jump State" rather than "Implement Player Controller"). Do not give Claude a blueprint that contains multiple days worth of work. Ensure the blueprint only contains one focused slice at a time to keep sessions cheap and accurate.
   - Before writing, archive any blueprint currently at
     `./project-state/blueprints/latest_blueprint.md`: if it exists, copy it to
     `./project-state/blueprints/archive/[timestamp]-[target_system].md` (timestamp in
     `YYYY-MM-DD_HHMMSS` format, target_system = this task's target system) before it gets
     overwritten. This preserves a paper trail of previous decisions.
   - Define the intended end result, Scene Tree Hierarchy, and Signal/State flow logic in the blueprint. **DO NOT hardcode exact math values, scales, or magic numbers.** Outline the mathematical *relationships* and require Claude to parameterize all constants as @export variables with sensible defaults so the user can tune them visually in the Inspector.


1. **Task Evaluation & Routing:** Evaluate the complexity of the queued task to determine the appropriate executor and model:
   - **Low Complexity** (e.g., minor fixes, isolated tweaks): Route to **the Executor Agent** using `GPT-5.6 Terra` or `GPT-5.6 Luna` (Low effort).
   - **Medium Complexity** (e.g., standard logic, moderate features): Route to **the Executor Agent** using `GPT-5.6 Sol` (Medium effort).
   - **High Complexity** (e.g., deep reworks, complex architecture, large scale refactoring): Route to **the Executor Agent** using `GPT-6 Astra` (High effort), or **the Executor Agent** (`sonnet 5.0` or `opus 5.0`).
2. **Parallel Branching (If Batched):** If handing off multiple tasks to be run in parallel, instruct the executor in the Handoff Prompt to create and checkout a specific git branch (e.g. `git checkout -b feature/ui-menu`) before making edits. Provide a separate prompt for the final session to merge the branches once verified.
3. **Handoff Prompt Generation:** Generate an easily copyable text block for the user to paste into the chosen executor (or multiple blocks if running parallel sessions). This prompt must direct the executor to the blueprint, define the exact scope of the task, and explicitly command them to handle branch creation/merging if applicable.
4. **Executor Recommendation:** Underneath the copyable prompt, explicitly tell the user which executor, model, and effort level to use (e.g., "Use **the Executor Agent (GPT-5.6 Sol - Medium effort)** for this task" or "Use **the Executor Agent (Sonnet 5.0 - Medium effort)**").
5. If the task is retiring/removing an entire system rather than building or fixing one, the executor will follow system removal guidelines (e.g., `REMOVE-SYSTEM.md` if present) and perform a dry-run diff for user approval before finalizing deletes.
6. The executor will directly edit the relevant `.gd`, `.tscn`, or `.tres` files to implement the changes.
7. The executor will update `./project-state/[target_system]/[target_system].md` with the new system state changes once execution is complete.


1. Once the Executor Agent marks a feature as `Verified-in-game`, the user returns to The Architect Agent (Antigravity).
2. **Adversarial Audit:** You (The Architect Agent) MUST compare the archived blueprint against the final committed `.gd` files and test coverage.
3. Ensure the Executor Agent did not silently drop complex math, state edge cases, or strict typings during execution. If discrepancies exist, queue a bug for Claude to fix before officially considering it complete. 



`./project-state/tweak_guide.md` is a human-facing lookup table — every hand-tunable `@export`
var and tuning `const` (colors, speeds, sizes, thresholds), grouped by system, with the file it
lives in and a plain-language description. It exists so the user can go tweak a value directly
without reading GDScript or asking an AI where it lives.

It is not project-state narrative and not covered by the trivial-task exemption in step 9 below:
any task that adds, removes, renames, or changes the default of an `@export` var or tuning
`const` updates the matching row in `tweak_guide.md` in that same task, no exceptions. See the
template at `docs/templates/tweak_guide.md` for the exact format and what to exclude (internal
state, safety-epsilon consts, anything not meant for hand-tuning).

This pairs with the in-editor doc comments required on every `@export` var (see workflow item 4
below) — write the plain-language description once and use it for both the `##` doc comment and
the `tweak_guide.md` row, so the Inspector tooltip and the guide never say different things.




1. **The Feel Gap (Test Scenes):** AIs are blind; they know if code compiles, but not if a mechanic is fun or VFX looks good. Claude CANNOT wire new mechanics/VFX directly into the main game. It must build an isolated `test_[feature].tscn`, wait for the human to playtest it, and tweak the math/feel based on human feedback before integration.
2. **Asset Standards:** Claude MUST read `markdowns4AI/ASSET-STANDARDS.md` whenever handling raw assets so it properly configures the `.import` files via text editing.
3. **Snippets Bible Rule:** Agents MUST check the `../../godot-4-snippets-bible/godot_4_snippets.md` for complex Godot 4.x logic before writing code.



**YOUR PRIMARY GOAL:** We are building a massive, shared repository of game mechanics, scripts, scenes, assets, VFX, music, SFX, and animations. You must aggressively prioritize growing and utilizing this repository over writing bespoke code. 

**MANDATORY SCOUTING:** Before *ever* scoping new implementation work or generating anything from scratch, you must scout the shared repositories. Do NOT blindly scan our 6 shared repositories. Instead, you MUST start at `../../global-index/README.md`. This master directory will route you to the highly specific 2D, 3D, or Agnostic feature markdowns (e.g. `../../global-index/3D/vfx_explosions.md`), preventing you from hallucinating the wrong dimension.

**Creative Adaptation Rule:** Focus on using what we have access to first. You do NOT need a perfect match to reuse an asset. Be creative. Even if writing a bespoke mechanic seems easier in the short term, it is almost always better to rework something we already have to expand our cohesive library. For example, recoloring a fire explosion to be toxic gas, tweaking a dash mechanic into a dodge roll, or repurposing an existing sound effect.

- **Match/Foundation Found:** Instruct Claude to copy the relevant files into the project, then outline how to creatively adapt or wire them in.
- **No Match (Last Resort):** Only if absolutely nothing can be adapted, proceed with blueprint creation and handoff to the Executor Agent as normal. Ensure the new creation is designed to be agnostic so it can be extracted to the shared repo later.

**1. Directory Architecture**
All shared repositories reside at the root `Godot_AI_Framework/` folder so they are globally accessible to every child game project via the shared documentation system.
Because active development occurs inside child project directories, agents must navigate to the root repositories to read, write, or evaluate repository assets.
- `../../mechanics/`: Mechanics Code Repository.
- `../../scenes/`: Scene Structure Repository.
- `../../assets/`: Raw Assets Repository (models, audio, textures).
- `../../effect-blocks/` & `../../poly-blocks/NatureBlocks/`: Ready-to-use VFX and Environment blocks.

**2. Parent Navigation Rule for Agents**
- **Repository Path Resolution:** Always resolve global repository assets relative to the project root using `../../mechanics/`, `../../scenes/`, `../../effect-blocks/`, etc.
- **Fallback Check:** If `../../mechanics/` is not present, check `mechanics/`.

**3. UI Component Policy**
UI systems must always be extracted as dual pairs:
1. The Scene Structure (`.tscn` / `.tres`): Saved under `../../scenes/ui/`.
2. The Logic Code (`.gd`): Saved under `../../mechanics/ui/`.
3. Cross-Reference: Partner explanation files must explicitly link to each other.

**4. Partner Explanation File Format**
Every saved script or scene structure must have an explanation file placed alongside it (e.g., `reticle.md` next to `reticle.gd`).

**5. Agent Directives & Workflows (Planner & Handoff)**
- **Protocol A: Pre-Creation & Pre-Instantiation Checks (Mandatory):** Before creating new GDScript or scene layouts, check `../../mechanics/README.md` and `../../scenes/README.md`. Decide to Reuse, Adapt, or Build from scratch.
- **Protocol B: Post-Creation Evaluation & Repository Extraction:** Extract agnostic components to the shared repository and log in local trackers.
- **Protocol C: Breakthrough Syncing & Refactoring:** For major improvements to shared assets, refactor into game-agnostic state and overwrite the shared repository file, updating explanation docs.
- **Protocol D: Project Bootstrapping Audit:** During initialization, scan local files against shared indices to prompt upstream updates if needed.



When the project requires a new, simple 3D asset (e.g., characters, basic props) and an existing one cannot be found in `../../assets/` or other shared folders:
1. **Use Procedural Generation First:** Do NOT attempt to generate 3D model files manually via raw text. Instead, use the procedural generator located at `../../model-generation/` (or `model-generation/` from the root).
2. **Handoff to the Executor Agent:** As The Architect Agent, do not modify the code directly. Instead, create a blueprint or task outlining the requirements and explicitly hand it off to **the Executor Agent**.
3. **Implementation by the Executor Agent:** the Executor Agent will modify `../../model-generation/models.mjs` and write a new exported function (using `antics-modelkit` primitives) to procedurally define the required 3D asset, following the existing examples.
4. **Building & Exporting:** The user or the Executor Agent will run `node build.js` inside the `../../model-generation/` directory to compile the code and generate the `.glb` file.
5. **Integration:** Use the resulting `.glb` file for the project's needs, ensuring the final `.import` configuration is handled according to `ASSET-STANDARDS.md`.

## PART 2: EXECUTION & CODING
This file defines how The Executor Agent operates in this game project. It is identical across all
game projects; only the MCP tool references noted below vary if this project uses a different
Godot MCP server (see `markdowns4AI/MCP-SWITCH.md`).

The Executor Agent is the **executor**, not the planner. Planning, task breakdown, and architecture
decisions belong to the Architect Agent (`the Architect Agent.md`), which reads the full project state and
writes concrete steps into `project-state/session_state.json`. The Executor Agent stays scoped to
executing those steps — this keeps its context small and its token usage cheap.



Before reading `session_state.json` or touching any other project file, check the project's
Godot MCP server (see "Current MCP" below) and classify this session into one of two tiers —
this check is advisory, not a gate: a failed MCP connection degrades capability, it does not
block the session.

- **Tier 0 (always available, no MCP required):** direct text edits to `.gd` script files via
  normal file tools, and headless verification via the Godot binary directly (`godot --headless
  --script res://tests/run_tests.gd`) — neither needs a live editor connection.
- **Tier 1 (needs a working MCP connection):** anything touching `.tscn`/`.tres` resources
  (`rename_file`, `move_file`, and any other UID-safe resource operation — see workflow item 7),
  or live-editor introspection (`run_project`, `game_screenshot`, `game_eval`, `read_scene`,
  `get_godot_version`).

1. Confirm the server's namespaced tools (`mcp__godot__*` for `godot-mcp`) appear in your
   available/deferred tool list.
2. If they appear, call one safe read-only tool to prove the server is live and can actually
   reach the Godot executable, not just declared in `.mcp.json` — for `godot-mcp`, call
   `get_godot_version`.
3. **If either check fails, Tier 1 is unavailable this session — do not stop.** Note the
   degradation (append a `session_log.md` line at the end of the session per usual, with
   `outcome=Tier 1 unavailable, ran Tier 0 only`) and proceed to read `session_state.json`:
   - If the queued task only needs Tier 0 operations (script logic edits, no resource
     rename/move, no live-editor read), execute it normally on Tier 0 and mention the
     degradation to the user once, in passing.
   - If the queued task specifically requires a Tier 1 operation, stop *that task* (not the
     session) and walk the user through remediation, in order:
   a. **Submodule/build** — `docs/tools/godot-mcp/build/index.js` must exist (relative to the
      `Godot_AI_Framework/` root). If missing: `git submodule update --init --recursive` from
      `Godot_AI_Framework/`, then `cd docs/tools/godot-mcp && npm install && npm run build`.
   b. **Machine path lookup** — read `Godot_AI_Framework/docs/machine_paths.json` (the shared,
      committed per-machine path log — see its `_comment` field). Get the current machine's
      identity (`$env:COMPUTERNAME` on Windows, `hostname` on macOS/Linux) and look it up:
      - **Entry found**: verify `godot_path` and `node_path` still exist on disk. If valid, use
        these absolute paths directly for any Godot/Node commands you run yourself this session
        (don't wait on PATH/env-var propagation) — and use the exact `godot_path` value when
        giving the user the `GODOT_PATH` command in step (d) below, so they never have to
        rediscover it by hand. If a recorded path no longer exists (moved/reinstalled), re-scan
        per the "not found" case below and update the entry.
      - **Entry not found** (new machine): scan common install locations for Godot (Steam
        library folders, `Program Files`, `/Applications`, `/usr/bin`, etc. per OS — see
        `godot-mcp`'s own auto-detect list in `src/index.ts` as a starting point, then also
        check Steam paths it omits) and for Node (`node --version`, or common install dirs if
        that fails). Append a new entry to `Godot_AI_Framework/docs/machine_paths.json` keyed by
        this machine's hostname, with a `label` you ask the user for once (e.g. "which machine
        is this?"), the discovered `godot_path`/`node_path`, and today's date as
        `last_verified`. This file is committed and shared across all of this user's machines —
        each machine adds its own row, none overwrite each other.
   c. **Node.js** — confirm `node --version` resolves (or use the `node_path` from the log
      directly). If Node was installed recently but PATH resolution still fails, it's very
      likely a stale PATH cached by the current process, not a missing install — check the
      machine-level PATH itself (e.g. on Windows,
      `[System.Environment]::GetEnvironmentVariable("Path","Machine")`) before concluding Node
      needs reinstalling.
   d. **`.mcp.json`** — confirm it exists at the project root with a `godot` entry pointing at
      `docs/tools/godot-mcp/build/index.js` (relative path depth varies by project nesting).
   e. **Godot executable** — confirm `godot`/`godot4` is on PATH, or that a `GODOT_PATH`
      environment variable points at the Godot binary's absolute path (use the `godot_path` from
      the machine log). `GODOT_PATH` is required whenever Godot lives somewhere `godot-mcp`'s
      built-in auto-detection doesn't check (e.g. a Steam library install — auto-detection does
      not scan Steam paths on Windows or Linux). Setting `GODOT_PATH` is a per-machine
      environment variable — give the user the exact command, pre-filled from the log, and ask
      them to run it themselves (`setx GODOT_PATH "<path>"` on Windows; `export
      GODOT_PATH=<path>` added to the shell profile on macOS/Linux). Do not modify system/user
      environment variables on the user's behalf.
   f. **Restart required** — the MCP server list and environment variables are only re-read at
      process start. After any fix above, tell the user to fully restart The Executor Agent (not just
      retry the check) before it will take effect. If a `setx`/`export` was run but a full
      restart still doesn't pick it up, verify the write actually landed (Windows:
      `[System.Environment]::GetEnvironmentVariable("GODOT_PATH","User")` in a **fresh**
      PowerShell process, not the same one used to set it) before assuming the mechanism itself
      is broken.
   Once remediated, retry the Tier 1 check before resuming the Tier-1-only task; otherwise
   continue deferring it and work any other Tier-0-eligible queued items in the meantime.
4. Once both checks in steps 1–2 pass, Tier 1 is available for the whole session — proceed to
   the workflow below with no capability restrictions. If step 3 resolved a machine-log entry,
   update its `last_verified` date once `get_godot_version` succeeds.

This check runs at the start of every session, not just the first time a project's MCP is set
up — a previously-working connection can silently drop (stale PATH, a moved Godot install, an
un-rebuilt submodule after a pull) and this is what catches it before a Tier-1-only task is
attempted rather than mid-task.


- Master Architecture State: `./project-state/_overview.md`
- Active Execution Payload: `./project-state/session_state.json`
- Blueprint Storage: `./project-state/blueprints/latest_blueprint.md`
- Blueprint Archive: `./project-state/blueprints/archive/[timestamp]-[target_system].md`
- Tweak Guide: `./project-state/tweak_guide.md` (see "Tweak Guide" below)
- Target System State: `./project-state/[system]/[system].md`
- Master Bug Index: `./bugs/master_bugs.md`
- Archived Systems: `./project-state/archived_systems/[system]/[timestamp]/` (see
  `markdowns4AI/REMOVE-SYSTEM.md`)
- Project README: `./README.md` (this project's root — see "Project README" below)



`./README.md` — this project's own root README, distinct from anything under `docs/` in the
shared `Godot_AI_Framework/` repo — is a short, human-readable, always-current snapshot of what
actually works, so opening the repo answers "what's implemented right now" without reading
`project-state/`. It is derived from `project-state/_overview.md` and `bugs/master_bugs.md`, not
hand-maintained as a separate narrative that can drift from them.

Structure:
- **Working** — systems/features currently `Verified-in-game`, one line each.
- **In Progress** — `Coded`/`Wired-in` features not yet verified.
- **Known Issues** — open bugs from `bugs/master_bugs.md`, one line each.
- **Last Updated** — today's date.

Updated as part of step 9's full ritual below, whenever `_overview.md` changes — skipped only
under the trivial-task exemption, same as the other status files.




`./project-state/tweak_guide.md` is a human-facing lookup table — every hand-tunable `@export`
var and tuning `const` (colors, speeds, sizes, thresholds), grouped by system, with the file it
lives in and a plain-language description. It exists so the user can go tweak a value directly
without reading GDScript or asking an AI where it lives.

It is not project-state narrative and not covered by the trivial-task exemption in step 9 below:
any task that adds, removes, renames, or changes the default of an `@export` var or tuning
`const` updates the matching row in `tweak_guide.md` in that same task, no exceptions. See the
template at `docs/templates/tweak_guide.md` for the exact format and what to exclude (internal
state, safety-epsilon consts, anything not meant for hand-tuning).

This pairs with the in-editor doc comments required on every `@export` var (see workflow item 4
below) — write the plain-language description once and use it for both the `##` doc comment and
the `tweak_guide.md` row, so the Inspector tooltip and the guide never say different things.



A bug's `Status` field moves through three states, tracked in `bugs/master_bugs.md`: `reported` → `investigating` → `resolved`. `Severity` is not
fixed at intake — revise it as new information comes in (e.g. a bug initially filed as minor that
turns out to block another system). This is independent of a feature's tri-state
Coded/Wired-in/Verified-in-game status (workflow item 6 below) — a `Verified-in-game` feature can
still carry an open bug at any of these states.



Two different problems that call for two different fixes — never conflate them:
- **A bug** is code that doesn't match what you meant to build. Fix: patch the code. Tracked in
  `bugs/master_bugs.md` per "Bug Lifecycle" above.
- **Design drift** is code that matches what you meant to build, but the describing doc
  (`project-state/[system]/[system].md` or a `design_docs/*.md`) is just stale. Fix: update the
  doc, not the code. Step 9's documentation-consistency check below catches this as part of
  normal task completion; see `markdowns4AI/DESIGN-DRIFT.md` for an on-demand, whole-project sweep for drift
  outside the context of a single task.



1. **The Feel Gap (Test Scenes):** AIs are blind; they know if code compiles, but not if a mechanic is fun or VFX looks good. Claude CANNOT wire new mechanics/VFX directly into the main game. It must build an isolated `test_[feature].tscn`, wait for the human to playtest it, and tweak the math/feel based on human feedback before integration.
2. **Asset Standards:** Claude MUST read `markdowns4AI/ASSET-STANDARDS.md` whenever handling raw assets so it properly configures the `.import` files via text editing.
3. **Snippets Bible Rule:** Agents MUST check the `../../godot-4-snippets-bible/godot_4_snippets.md` for complex Godot 4.x logic before writing code.



Before scoping new implementation work or generating from scratch, scout the shared repositories. Do NOT blindly scan our 6 shared repositories. Instead, you MUST start at `../../global-index/README.md`. This master directory will route you to the highly specific 2D, 3D, or Agnostic feature markdowns (e.g. `../../global-index/3D/vfx_explosions.md`), preventing you from hallucinating the wrong dimension.

If a queued step in `session_state.json` directs reuse of an entry from the shared repositories (the Architect Agent checks for a match before writing steps), copy the necessary `.gd` and `.tscn` files and their companion `.md` docs into the project, then:
1. Read the companion doc's Setup & Integration Steps before touching anything else.
2. Adapt naming, paths, and any project-specific integration points exactly as the doc specifies.
3. From there, treat it like any other task — strict typing, tri-state status, and documentation-consistency ritual all still apply. A reused mechanic/scene is not exempt from any of it.

**1. Directory Architecture**
All shared repositories reside at the root `Godot_AI_Framework/` folder so they are globally accessible to every child game project via the shared documentation system.
Because active development occurs inside child project directories, agents must navigate to the root repositories to read, write, or evaluate repository assets.
- `../../mechanics/`: Mechanics Code Repository (scripts, explanations alongside them, master index).
- `../../scenes/`: Scene Structure Repository (tscn files, tres resources, explanations alongside them, master index).
- `../../assets/`: Assets Repository (models, audio, textures).

**2. Parent Navigation Rule for Agents**
- **Repository Path Resolution:** Always resolve global repository assets relative to the project root using `../../mechanics/`, `../../scenes/`, and `../../assets/`.
- **Fallback Check:** If `../../mechanics/` is not present, check `mechanics/`.

**3. UI Component Policy**
UI systems must always be extracted as dual pairs:
1. The Scene Structure (`.tscn` / `.tres`): Saved under `../../scenes/ui/`.
2. The Logic Code (`.gd`): Saved under `../../mechanics/ui/`.
3. Cross-Reference: Partner explanation files must explicitly link to each other.

**4. Partner Explanation File Format**
Every saved script or scene structure must have an explanation file placed alongside it (e.g., `reticle.md` next to `reticle.gd`).

**5. Agent Directives & Workflows (Executor)**
- **Protocol B: Post-Creation Evaluation & Repository Extraction:** After creating agnostic GDScript or Scene layouts, extract them to the shared repositories, create partner documentation, update master indices (`README.md`), and log in the local `project-state/` tracking files (`mechanics_lineage.md` / `scenes_lineage.md`).
- **Protocol C: Breakthrough Syncing & Refactoring:** For major improvements to shared assets, refactor into game-agnostic state and overwrite the shared repository file, updating explanation docs.


1. ALWAYS start by reading `./project-state/session_state.json` to obtain current micro-tasks.
   If `status` is `"idle"`, there is no queued work — say so rather than inventing a task; wait
   for the Architect Agent to populate it.
2. If `session_state.json` sets `blueprint_used` to a path (not `null`), read
   `./project-state/blueprints/latest_blueprint.md` before starting — it carries the derived
   math, scene tree, and signal/state flow spec for this task.
3. Read `markdowns4AI/DOCTRINE.md` to ensure any code you write aligns with the project's art style, constraints, and non-negotiable design pillars.
4. Read ONLY the specific system files (`./project-state/[system]/[system].md` and
   `./bugs/[system]/[system].md`) named as `target_system`. Never read unassigned system files.
5. **Guardrail Enforcement:** Do NOT modify any file containing the `# @GUARDRAIL: LEAVE THIS ALONE` comment unless explicitly instructed to override it by the user. These files contain fragile, core architecture.
6. **MCP Pre-fetch Enforcement (Anti-Hallucination):** Before attempting to modify any `.gd` script that references scene nodes, you MUST use the `read_scene` MCP tool on its companion `.tscn` file. This guarantees you see the exact scene tree structure and prevents hallucinated `@onready` node paths.
7. Strict GDScript 4 typing is required (`Vector2`, `float`, explicit return types, `@export`
   annotations). Every `@export` var also needs a `##` doc comment on the line(s) immediately
   above it, in plain language, stating what it does and any known-good range — Godot 4 renders
   this as the property's hover tooltip in the Inspector, so its purpose is visible without
   opening the script. This applies to every `@export` var this task touches or adds, not just
   ones in newly-created files. See "Tweak Guide" below for how this pairs with
   `tweak_guide.md`.
8. Composition & reusability first: prefer signal-driven communication, resource-driven
   configuration (`.tres`), and generic subscenes over monolithic code.
9. Implementation status is tri-state: `Coded`, `Wired-in`, `Verified-in-game`. This is
   independent of correctness — a Wired-in or Verified-in-game feature can still have an open
   bug, tracked separately in `bugs/[system]/[system].md`, never by downgrading this status. Any new
   public function or signal introduced by a system being marked `Wired-in` or higher needs a
   corresponding test case (see step 9) — a feature cannot be marked `Verified-in-game` without
   one.
7. Use this project's Godot MCP tools (see "Current MCP" below) for all resource operations —
   never raw shell `mv`/`rm`, even as a workaround when Tier 1 is unavailable (see Step 0). Raw
   filesystem operations can silently break UID-based or path-based resource references the
   engine tracks internally; if Tier 1 is down, defer the resource operation rather than
   dropping to shell commands.
8. If a queued step is ambiguous, contradicts the target system file or blueprint, or requires
   a scope/architecture decision, stop and flag it rather than improvising — that decision
   belongs to the Architect Agent, not The Executor Agent.
9. Upon task completion:
   - **HIGH PRIORITY — documentation consistency, not skippable.** Before anything else in this
     step, identify every markdown file whose described behavior, signals, functions, or status
     this change affects — not just the checklist below as a ceiling. That includes
     `project-state/[system]/[system].md`, `bugs/[system]/[system].md`, either `_overview.md` master, this
     project's root `README.md` (see "Project README" above), and any `design_docs/*.md` that
     documented the now-superseded behavior — and update every one that's now stale. A markdown
     describing behavior the code no longer does is worse than no documentation; treat it the
     same as a failing test. This is design drift, not a bug — see "Bugs vs. Design Drift" above.
     If the discrepancy is instead the code failing to do what was intended, that's a bug and
     belongs in `bugs/[system]/[system].md` per "Bug Lifecycle" above, not a doc edit. The
     trivial-task exemption below only shortens *which* files need a full status update — it
     never means skipping this check.
   - **Tweak Guide sync, also not skippable, also not covered by the trivial-task exemption.**
     If this task added, removed, renamed, or changed the default of any `@export` var or tuning
     `const`, update the matching row(s) in `./project-state/tweak_guide.md` in this same task —
     see "Tweak Guide" above. A one-line tunable-value fix is exactly the kind of change the
     trivial-task exemption is meant for elsewhere, but it's precisely what this file exists to
     track, so it still gets updated even when everything else in this step is skipped. Confirm
     every `@export` var touched still has an accurate `##` doc comment immediately above it
     (workflow item 4) — add or correct it if missing or stale.
   - **Test authorship.** For any new public function/signal added to a system being marked
     `Wired-in` or higher, add a corresponding test case to that system's test file before it can
     be marked `Verified-in-game`. If the system has no test file yet, create one named
     `test_[system].gd` under `tests/`, `extends TestCase` (see `docs/templates/tests/test_case.gd`
     — its `assert_true`/`assert_eq`/`assert_almost_eq` helpers and `failures` array are what
     `run_tests.gd` depends on), with `test_`-prefixed methods for each case — that's what makes
     it auto-discovered. This is a hard gate, not a nice-to-have — running `tests/run_tests.gd`
     is not a substitute for growing its coverage.
   - **Visual Validation (Screenshot Probing):** For any UI or visual task, before marking it `Verified-in-game`, you MUST run the project (`run_project`) and use `game_screenshot` to visually inspect the isolated `test_[feature].tscn`. Ensure layouts don't overlap and nodes render correctly.
   - Run `/code-review` on the diff before marking anything `Verified-in-game` — catch
     correctness/simplification issues while the change is still fresh, not in a later session.
     Treat any correctness, hallucination, or design-drift finding it raises as a rejection: fix
     the diff and re-run `/code-review` clean before proceeding — never mark `Verified-in-game`
     on a rejected pass.
   - **If this is a trivial task** (single-file, single-function fix; no new signal/behavior; no
     tri-state status change; no bug opened or closed), skip the four bullets below — just
     set `status` in `session_state.json` to `"COMPLETED"`. Otherwise (a
     tri-state status actually changed, or a bug opened/closed), do the full ritual:
   - Advance any bug entries this task fixed to `resolved` in `./bugs/master_bugs.md` (see "Bug Lifecycle" above).
   - Update master status in `./project-state/_overview.md`.
   - Update this project's root `README.md` — "Working"/"In Progress"/"Known Issues" sections —
     to match the new `_overview.md`/`bugs/master_bugs.md` state.
   - **Bookkeeping & Archive Phase:** When a feature is marked `Verified-in-game`, summarize its final state into the master docs. Move the granular details, logs, or completed task steps out of the main `project-state/[system]/[system].md` and into an `archive/` folder (e.g., `project-state/archived_tasks/`) so the active state docs do not endlessly grow. Write a brief changelog, and delete any temporary test scenes (`test_[feature].tscn`).
   - If `session_state.json`'s `blueprint_used` field was not `null` (a blueprint was used for
     this task), archive it now: copy `./project-state/blueprints/latest_blueprint.md` to
     `./project-state/blueprints/archive/[timestamp]-[target_system].md` (timestamp in
     `YYYY-MM-DD_HHMMSS` format, target_system from the field). This preserves a paper trail in
     case a blueprint's spec and what actually got built ever diverge, and frees up
     `latest_blueprint.md` for the next blueprint without it getting overwritten mid-archive by
     the Architect Agent.
   - Set `status` in `session_state.json` to `"COMPLETED"`.
   - **Clear your context** (or start a new session) before taking the next blueprint, to keep sessions cheap and focused.
10. Run `/security-review` before any step that adds networking, multiplayer, save-file
    parsing, or otherwise consumes untrusted input — skip it for purely local single-player
    logic where there's no meaningful attack surface.


- Format/lint: `gdformat .` then `gdlint .` — run on modified `.gd` files before the headless
  check; fix reported typing/style errors rather than suppressing them.
- Headless check: `godot --headless --script res://tests/run_tests.gd`



Use the `context7` MCP tools to pull current Godot 4.x API/documentation before writing calls
to engine APIs you're unsure of, rather than relying on memory — this project targets Godot 4
specifically and Godot 3 syntax is invalid here.



This project uses [`godot-mcp`](https://github.com/tugcantopaloglu/godot-mcp)
(`@tugcantopaloglu/godot-mcp`), vendored as a submodule at `docs/tools/godot-mcp` in the shared
`Godot_AI_Framework/` root and wired in via this project's `.mcp.json` (see `SETUP.md` Step 0). Its
tools follow the `mcp__godot__*` naming pattern (e.g., `run_project`, `game_screenshot`,
`game_eval`, `read_scene`, `rename_file`, `move_file`). If this project switches to a different
Godot MCP server, run `markdowns4AI/MCP-SWITCH.md` rather than manually editing this section.