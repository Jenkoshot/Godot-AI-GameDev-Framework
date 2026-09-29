# Godot AI GameDev Framework

**A structured Godot 4 + AI workspace for turning a game idea into a real project and working through it one task at a time.**

I built this because I got tired of aimless AI-assisted development.

My original workflow was basically: copy GDScript files into Gemini, attach my GDD, ask it to add or fix something, paste the result back into Godot, and repeat. As my projects grew, I even built a small web app to combine all of my `.gd` files into one AI-readable TXT/PDF so Gemini could see more of the codebase at once.

Better coding agents solved part of that problem, but they did not solve the bigger one:

> **I still didn't have a development workflow.**

I could ask an AI to implement almost anything, but I was still deciding what to work on based on whatever interested me that day. I did not have a reliable picture of what was finished, what was broken, what depended on something else, what should come next, or whether the implementation was still aligned with the original game design.

This framework is the workflow I gradually built around that problem.

It is **not an AI that makes a game while you sit back and watch**. It is a workspace for keeping the developer in control of the game while giving AI agents enough structure, context, tools, and persistent project state to help move it forward deliberately.

The core loop is:

```text
Game idea
   ↓
Design / GDD
   ↓
Create a structured Godot project
   ↓
Architect reads design + current state + bugs
   ↓
Architect proposes 3 high-priority tasks
   ↓
You choose what to work on
   ↓
Architect creates an implementation blueprint
   ↓
Executor implements it
   ↓
You playtest, judge the feel, and iterate
   ↓
Architect audits what actually landed
   ↓
Project state / bugs / documentation are updated
   ↓
"What’s next?"
   ↓
Repeat
```

You can ignore the Architect's recommendations at any time and give it a custom task. The framework exists to provide structure, not to take creative control away from you.

## What the framework is trying to solve

The coding agent is only one part of making a game. The harder long-term problem is keeping **design intent, implementation state, priorities, bugs, architecture, tuning information, testing, and reusable work** coherent while the project changes over months of development.

The framework therefore treats your GDD as living project context rather than a document you write once and forget. It tracks what parts of that design actually exist in the game, what still needs work, and what has been deliberately changed or removed.

It also supports multiple games in the same workspace. Each game keeps its own design and project state, while reusable mechanics, scenes, shaders, assets, and other work can be harvested into shared libraries for later projects.

The goal is simple:

> **Go from "I have a game idea" to "I know what I should work on next" — then keep repeating that loop until there is a game.**

---

## Where this came from

This framework grew out of my own learning process as a beginner solo developer.

The workflow evolved roughly like this:

```text
Manual Godot / GDScript
        ↓
Copy individual scripts into web AI
        ↓
Compile the codebase into AI-readable TXT/PDF
        ↓
Specialized AI roles and handoffs
        ↓
Repo-aware coding agents + Godot MCP
        ↓
Persistent project state + Architect / Executor split
        ↓
Tests, audits, bug tracking, design-drift protection
        ↓
Reusable multi-project workspace
```

Each step came from a problem I ran into while trying to make games. The framework is still evolving, and it is deliberately open to being changed, stripped down, or combined with better tools.

---

## What is inside

| Layer | Purpose |
| :--- | :--- |
| **Project tiers** | Scale the amount of process/documentation to the size of the game instead of forcing a prototype and a large project through the same workflow. |
| **Architect** | Reads the design, project state, bugs, and dependencies; proposes priorities; then creates a concrete blueprint for the task you choose. |
| **Executor** | Implements the chosen blueprint, uses Godot tooling where appropriate, writes/tests code, and records what changed. |
| **Human playtest gate** | You decide whether the mechanic actually looks, feels, and behaves correctly. Passing automated checks is not the same thing as being good in-game. |
| **Adversarial audit** | The Architect can compare the finished implementation against the original blueprint and flag things that were missed or changed. |
| **Persistent project state** | Keeps future AI sessions aware of what exists, what is verified, what is broken, and what decisions have already been made. |
| **Design docs + doctrine** | Keep implementation connected to the game you actually intended to make and preserve your non-negotiable design choices. |
| **Bug + tweak tracking** | Separates broken behavior from tunable gameplay values so iteration does not depend on remembering where everything lives. |
| **Godot MCP** | Lets compatible agents inspect and interact with Godot rather than treating the project as only a pile of text files. |
| **Shared libraries** | Encourages later games to reuse/adapt mechanics, scenes, shaders, assets, and other work before generating another version from scratch. |
| **Procedural 3D workspace** | Integrates Antics ModelKit for deterministic, code-generated 3D assets that can be iterated and viewed in a Godot test project. |

A key principle is that **repeated corrections should become durable rules**. If an AI repeatedly does something you do not want, the intended fix is not to keep correcting it in disposable chats. Update the framework rule or the project's doctrine so future sessions inherit the lesson.

> **Current status:** this repository is the scaffolding, rules, and tooling for the workflow — not a finished one-click game generator. Some shared libraries intentionally start empty, and there are still rough edges documented in [Known Limitations](#known-limitations--rough-edges).

---

## Contents

1. [The mental model](#1-the-mental-model)
2. [Requirements](#2-requirements)
3. [Installation](#3-installation)
4. [Connecting your AI agent](#4-connecting-your-ai-agent)
5. [Your first game, start to finish](#5-your-first-game-start-to-finish)
6. [The daily loop](#6-the-daily-loop)
7. [Anatomy of a generated project](#7-anatomy-of-a-generated-project)
8. [The scale tiers](#8-the-scale-tiers)
9. [Playbook reference](#9-playbook-reference)
10. [The shared libraries](#10-the-shared-libraries)
11. [Procedural 3D modeling](#11-procedural-3d-modeling)
12. [framework_tools](#12-framework_tools)
13. [Customizing AI behavior](#13-customizing-ai-behavior)
14. [Troubleshooting](#14-troubleshooting)
15. [Known limitations & rough edges](#known-limitations--rough-edges)
16. [Repository layout](#repository-layout)
17. [Credits & licensing](#credits--licensing)

---

## 1. The mental model

There are three working roles in the framework. They are separated so that deciding **what should be built**, deciding **how it should be built**, and actually **changing the project** do not collapse into one long AI session.

### The Director — workspace-level work

The Director operates at the framework root. It is for creating projects, maintaining the framework, managing shared tooling/libraries, and other work that spans games. It is not the agent that decides the design of an individual game.

### The Architect — decide what comes next and blueprint it

The Architect operates inside one game project.

At the start of a normal development cycle it reads the project's doctrine, design documents, current implementation state, known bugs, and relevant dependencies. It produces an **estimated project snapshot** and recommends three high-priority tasks.

**You choose the task.** The Architect does not get to decide what game you make.

Once you choose, it creates an implementation blueprint describing the intended result, relevant files/scenes, scene structure, signals, exported tuning values, tests, dependencies, and important mathematical relationships. It then produces a handoff for the Executor.

After implementation and your playtest, the Architect can perform an adversarial audit: compare the blueprint with what actually landed and flag omissions, unexpected changes, or follow-up work.

### The Executor — implement the chosen task

The Executor works from the approved blueprint rather than inventing the project's direction as it codes.

It can edit GDScript, use the Godot MCP for supported editor/project operations, run formatting/linting/headless tests, and update the implementation state after the work is complete.

The separation is a **workflow choice**, not a claim that every project needs two different AI products. If you prefer one agent, `SOLO-AGENT.md` combines the responsibilities while preserving a planning phase and an implementation phase.

### The human role — the part the framework does not replace

The framework deliberately leaves the most important judgment to you.

You decide what game you want to make, which proposed task to choose, whether to ignore the recommendations, whether an implementation matches your intent, and whether something actually feels good when played.

Automated tests can prove that a value is calculated correctly. They cannot prove that the value is fun.

### The development loop

```text
                 ┌──────────────────────────────────────────────┐
                 │                                              │
You → Architect → 3 priorities → you choose → blueprint → Executor
 ↑                                                       │
 │                                                       ↓
 └──── updated state ← audit ← iterate ← you playtest ───┘
```

That loop is the center of the framework. The rest of the repository exists to give it reliable context, tools, persistence, and reusable building blocks.

---

## 2. Requirements

| Requirement | Version | Why |
| :--- | :--- | :--- |
| **Godot** | 4.4+ | Target engine. The MCP server drives this binary. |
| **Node.js** | 18+ | Builds and runs the Godot MCP server and the 3D modelkit. |
| **Python** | 3.8+ | `framework_tools/` sync scripts. |
| **gdtoolkit** | latest | Provides `gdformat` / `gdlint`, which `EXECUTOR.md` runs before every headless check. `pip install gdtoolkit` |
| **Git** | any | Each game becomes its own independent repository. |

### Tested environments

- **AI agents:** ChatGPT Codex, Claude Code, Antigravity (Gemini).
- **Primary:** desktop app versions of those agents, on **Windows**.
- **CLI:** should work on Windows given a correct Node/Python PATH.
- **Linux/macOS:** **untested.** The logic is portable Python and Node, but every path in
  `docs/machine_paths.json` and the `GODOT_PATH` instructions are written Windows-first. Expect to
  do your own pathing.

### MCP servers used

Both are declared in `docs/templates/common/mcp_config.json`, which gets copied into each project.

- **`godot`** — [tugcantopaloglu/godot-mcp](https://github.com/tugcantopaloglu/godot-mcp), vendored
  at `docs/tools/godot-mcp/`. ~157 tools: `run_project`, `game_screenshot`, `game_eval`,
  `read_scene`, `modify_scene_node`, `rename_file`, `manage_autoloads`, `manage_input_map`, and so on.
- **`context7`** — pulled on demand via `npx @upstash/context7-mcp`. The Executor uses it to look up
  current Godot 4 API signatures instead of recalling them.

---

## 3. Installation

### The short version

```bash
git clone <your-fork-url> Godot_AI_Framework_Public
cd Godot_AI_Framework_Public
cd docs/tools/godot-mcp && npm install && npm run build && cd ../../..
cd model-generation && npm install && cd ..
pip install gdtoolkit
```

Then configure your Godot path — see [3.3](#33-tell-the-framework-where-godot-is) below. That step
is the one people get wrong.

### The AI-assisted version

Open an AI terminal at the **root of this repository** and say:

> *"Run the SETUP-FRAMEWORK playbook."*

It will walk `SETUP-FRAMEWORK.md`: verify prerequisites, `npm install && npm run build` the MCP
server, `npm install` the modelkit, ask for your Godot executable path, and write it into
`docs/machine_paths.json`.

**It will not restart your agent for you, and it must be restarted.** See 3.3.

### 3.1 Build the MCP server — this is not optional

`docs/tools/godot-mcp/build/` is excluded from version control by that project's own `.gitignore`.
A fresh clone has TypeScript source and **no compiled server**. Until you build it, every
`mcp__godot__*` tool is missing and the Executor is limited to plain text edits.

```bash
cd docs/tools/godot-mcp && npm install && npm run build
```

Verify: `docs/tools/godot-mcp/build/index.js` now exists.

> **Note:** godot-mcp is **vendored**, not a git submodule — its source is committed directly
> into this repository. There is no `git submodule update` step. See
> [`docs/tools/README.md`](docs/tools/README.md) for how to update it to a newer upstream.

### 3.2 Install the modelkit

```bash
cd model-generation && npm install
```

This pulls `antics-modelkit` and `three`. It also unpacks the kit's own 52 KB technique guide at
`model-generation/node_modules/antics-modelkit/AGENTS.md`, which the AI is required to read before
generating any 3D model.

### 3.3 Tell the framework where Godot is

There are **two separate places** this has to be recorded, and skipping the second is the single
most common reason the MCP "doesn't work."

**(a) `docs/machine_paths.json`** — a committed, hostname-keyed log so your agents can find Godot
on any of your machines without rediscovering it.

Find your hostname:
- Windows PowerShell: `$env:COMPUTERNAME`
- macOS / Linux: `hostname`

Replace the `YOUR_COMPUTER_NAME_HERE` placeholder key with that value, and fill in the real paths:

```json
{
  "machines": {
    "MY-DESKTOP": {
      "label": "My Dev Machine",
      "os": "windows",
      "godot_path": "C:\\Program Files\\Godot\\Godot_v4.4-stable_win64.exe",
      "godot_version": "4.4",
      "godot_source": "standalone",
      "node_path": "C:\\Program Files\\nodejs\\node.exe",
      "last_verified": "2026-09-20"
    }
  }
}
```

**(b) The `GODOT_PATH` environment variable** — this is what the MCP server itself actually reads.
`mcp_config.json` does **not** inject it. The server auto-detects Godot in a few standard
locations, but it does **not** scan Steam library folders on Windows or Linux, so a Steam install
will fail auto-detection.

```powershell
setx GODOT_PATH "C:\Program Files\Godot\Godot_v4.4-stable_win64.exe"
```

```bash
export GODOT_PATH=/path/to/godot   # add to ~/.bashrc or ~/.zshrc
```

**Then fully quit and relaunch your AI agent.** Environment variables and the MCP server list are
read once at process start. Retrying the tool call in the same session will not pick it up.

Verify: ask your agent to call `get_godot_version`. A version string means you are done.

### 3.4 Install gdtoolkit

```bash
pip install gdtoolkit
```

Verify with `gdformat --version`. The Executor runs `gdformat .` and `gdlint .` on modified scripts
before every headless test run.

---

## 4. Connecting your AI agent

**This is a manual step the framework does not do for you, and nothing works properly without it.**

The governance files are named `ARCHITECT.md`, `EXECUTOR.md`, and `SOLO-AGENT.md`. No AI agent
auto-loads files with those names. Each agent looks for its own filename:

| Agent | Auto-loads |
| :--- | :--- |
| Claude Code | `CLAUDE.md` |
| ChatGPT Codex | `AGENTS.md` |
| Antigravity / Gemini CLI | `GEMINI.md` |

So after a project is scaffolded, you have two options.

**Option A — pointer file (recommended).** Create the file your agent looks for, containing one
line. In `Projects/<YourGame>/`:

```bash
echo "Read and follow EXECUTOR.md in this directory. Re-read it at the start of every response." > CLAUDE.md
```

```bash
echo "Read and follow ARCHITECT.md in this directory. Re-read it at the start of every response." > AGENTS.md
```

This keeps the real rules in one file that `sync_templates.py` can update.

**Option B — say it every session.** Start each session with *"Read ARCHITECT.md and follow it."*
Works, but you will forget, and the templates open with a mandatory-re-read directive that assumes
the file is already loaded.

> If you run **both** agents in the same folder, give each a pointer file aimed at its own role.
> Do not point both at the same document.

---

## 5. Your first game, start to finish

### Step 1 — Write a design document

Create `Projects/<YourGame>/design_docs/` and put your GDD in it as one or more `.md` files.

**The folder name matters.** Every Architect template reads `./design_docs/*.md` by glob. A
`GDD.md` sitting at the project root will not be found.

It does not need to be polished. A page of "here's the loop, here's the feel, here's the scope" is
enough for the Architect to reason about scope and pick a tier. You can also brainstorm it with the
Director first:

> *"I want a cozy farming game mixed with a roguelike. Help me write a GDD covering the core loop,
> progression, and a realistic first-milestone scope. Save it to
> `Projects/FarmRogue/design_docs/GDD.md`."*

### Step 2 — Scaffold the project

From the repo root:

> *"Run the SETUP playbook from `docs/templates/SETUP.md` for `Projects/FarmRogue`, reading its
> design_docs to propose a tier."*

The playbook will:

1. Check the MCP server is built and copy `mcp_config.json` into the project as both
   `.agents/mcp_config.json` and `.mcp.json`, fixing the relative path depth.
2. Read `design_docs/` and **propose a tier**, then wait for you to confirm.
3. Create `markdowns4AI/` and copy in the common + tier governance files.
4. Scaffold the tier's tracking files (see [Section 7](#7-anatomy-of-a-generated-project)).
5. Write the project's own root `README.md` with empty Working / In Progress / Known Issues lists.
6. Edit `project.godot` to add `gdscript/warnings/untyped_declaration=2`, which makes Godot itself
   enforce strict typing.
7. Create a folder architecture (`scenes/`, `scripts/`, `audio/sfx/`, `vfx/`, …) based on what the
   design docs actually call for.

Its Step 3 also bootstraps the project itself: it checks for `project.godot` and `icon.svg`
(offering to create them, though letting Godot's own **Project → New Project** make them is
cleaner), runs `git init` inside the project folder, writes a project `.gitignore`, and creates
`design_docs/` if it is missing. Each game is its own repository — the framework's root
`.gitignore` deliberately excludes `Projects/*/`.

Step 4a also creates your **agent pointer file** (`CLAUDE.md` / `AGENTS.md` / `GEMINI.md`) after
asking which agent you run — see [Section 4](#4-connecting-your-ai-agent) for why that matters.

### Step 3 — Fill in the two files only you can write

The Architect treats both as mandatory reads. They ship as placeholders full of `[Insert X Here]`,
and an unfilled doctrine means the AI invents your taste for you.

**`markdowns4AI/PROJECT-PROFILE.md`** — name, tier, 2D/3D, genre, camera, art style, core loop,
technical constraints. Cheap to fill; it is the first thing the agent reads to orient itself.
**The `Current Tier:` line is load-bearing** — `sync_templates.py` parses it to decide which tier's
templates to push.

**`markdowns4AI/DOCTRINE.md`** — your non-negotiables:

```markdown
## Design Pillars
- Combat is turn-based. Never propose real-time action.
- No punishment mechanics. The player cannot lose progress.

## Architectural Constraints
- Never use singletons for gameplay state. Autoloads are for services only.
- UI does not use state machines.

## Art & Audio Taste
- 16-bit pixel art, strict NES palette.
- Lo-fi synthwave only.
```

Doctrine is the highest-leverage file in the project. Every wasted argument you have with the AI
about style is one line you should have written here.

### Step 4 — Wire up your agent

Create the pointer files from [Section 4](#4-connecting-your-ai-agent). Restart the agent.

### Step 5 — Build

Go to [The daily loop](#6-the-daily-loop).

---

## 6. The daily loop

### 6.1 — Architect: evaluate and choose

Open your Architect agent in `Projects/<YourGame>/`.

> *"What is the state and progress of the project, and what is the next task?"*

It reads doctrine → design docs → state → bugs, reports a completion percentage, and presents
**three** candidate tasks weighed by severity, unblock value, and deadline proximity. It then stops
and waits. It will not start planning until you choose.

> *"Let's go with Task 2."*

### 6.2 — Architect: blueprint

Now it writes the blueprint. Where depends on tier:

| Tier | Blueprint path | Archive path |
| :--- | :--- | :--- |
| Lite | `blueprint.md` | `blueprints_archive/<timestamp>-<system>.md` |
| Standard / Heavy | `project-state/blueprints/latest_blueprint.md` | `project-state/blueprints/archive/<timestamp>-<system>.md` |

A blueprint covers one **atomic slice** — "Implement Player Jump State", not "Implement Player
Controller" — and specifies the scene tree, the signal/state flow, the `@export` surface, and the
mathematical *relationships*. It is explicitly forbidden from hardcoding magic numbers; every
constant becomes an `@export` you can tune in the Inspector.

If you queue several independent tasks, it will write separate blueprints and instruct each
Executor session to work on its own git branch.

It finishes with a copy-paste handoff prompt and a model/effort recommendation.

It also writes `session_state.json` — the machine-readable task queue the Executor opens with —
so the handoff survives a context clear even if you lose the chat.

> The recommendation names an **effort tier** (low / medium / high), not a specific model. Map it
> to whatever you actually have available; model names go stale far faster than these templates do.

### 6.3 — Executor: implement

Open your Executor agent in the same folder. Paste the Architect's prompt verbatim.

**Session-start MCP health check.** Before anything else the Executor classifies the session:

- **Tier 0** (always available): text edits to `.gd`, `gdformat`/`gdlint`, headless test runs.
- **Tier 1** (needs a live MCP connection): anything touching `.tscn`/`.tres`, plus live-editor
  introspection — `run_project`, `game_screenshot`, `game_eval`, `read_scene`.

If Tier 1 is down it does **not** stop. It runs Tier 0 work and defers Tier 1 tasks, walking you
through remediation (build the server → check `machine_paths.json` → check Node → check `.mcp.json`
→ set `GODOT_PATH` → restart).

**Rules it operates under:**

- **Anti-hallucination pre-fetch.** Before editing any `.gd` that references scene nodes, it must
  `read_scene` the companion `.tscn`. No guessed `@onready` paths.
- **No raw `mv`/`rm` on Godot resources.** Ever, including as a workaround when MCP is down.
- **Strict GDScript 4 typing.** Explicit types, explicit return types, and a `##` doc comment above
  every `@export` var — Godot renders it as the Inspector tooltip.
- **Guardrails.** A file containing `# @GUARDRAIL: LEAVE THIS ALONE` is off limits unless you
  explicitly override. Add that comment to your own fragile core files.
- **The Feel Gap.** *The Executor may not wire a new mechanic or VFX directly into your main game.*
  It builds an isolated `test_<feature>.tscn`, hands it to you to playtest, and tunes from your
  feedback before integration. Expect this — it is deliberate, because an AI can tell you code
  compiles but not whether a jump feels good.
- **Tests are a gate.** Any new public function or signal on a system being marked `Wired-in` or
  higher needs a test case in `tests/test_<system>.gd` before it can reach `Verified-in-game`.
- **Reuse first.** Before writing anything new it is required to scout the shared libraries via
  `global-index/README.md`. (See [Section 10](#10-the-shared-libraries) for the current state of
  those.)

**Implementation status is tri-state**, and it is about *integration*, not correctness:

| Status | Meaning |
| :--- | :--- |
| `Coded` | The script exists and compiles. |
| `Wired-in` | It is connected into the scene tree / signal graph. |
| `Verified-in-game` | You have played it and confirmed it works. Requires a passing test. |

A `Verified-in-game` feature can still carry an open bug. Bugs are tracked separately and never by
downgrading this status.

### 6.4 — Playtest and tweak

Open the project in Godot and press Play (or let the Executor drive it via `run_project` +
`game_screenshot`).

> *"The player moves too slow. Raise the speed, and log the adjustment in the tweak guide."*

### 6.5 — Close the loop: the adversarial audit

**Do not skip this.** Once the Executor marks something `Verified-in-game`, go back to the
Architect:

> *"Run the Phase 5 adversarial audit on the last task."*

It diffs the archived blueprint against the code that actually landed, looking for silently dropped
math, missing edge cases, and weakened typing — and files bugs for what it finds. This is the step
that catches an Executor quietly simplifying a spec, and it is the reason the blueprint archive
exists.

### 6.6 — Verification commands

```bash
gdformat .
```

```bash
gdlint .
```

```bash
godot --headless --script res://tests/run_tests.gd
```

`run_tests.gd` auto-discovers every `res://tests/test_*.gd`, instantiates it, and runs every
`test_`-prefixed method. Test files `extends TestCase` and get `assert_true`, `assert_eq`, and
`assert_almost_eq`. Both files are copied into your project by SETUP.

---

## 7. Anatomy of a generated project

```
Projects/FarmRogue/
├── project.godot              # you create this in the Godot editor
├── icon.svg
├── .mcp.json                  # Godot + context7 MCP wiring
├── .agents/mcp_config.json    #   (same content, for agents that read this location)
├── ARCHITECT.md               # planner rules      ─┐
├── EXECUTOR.md                # implementer rules   ├─ synced from docs/templates/
├── SOLO-AGENT.md              # single-agent rules ─┘
├── CLAUDE.md / AGENTS.md      # YOU create these — see Section 4
├── README.md                  # auto-maintained: Working / In Progress / Known Issues
├── design_docs/               # YOUR GDD lives here. Exact folder name required.
├── markdowns4AI/              # all non-root governance docs
│   ├── PROJECT-PROFILE.md     #   you fill in — tier lives here
│   ├── DOCTRINE.md            #   you fill in — your non-negotiables
│   ├── ASSET-STANDARDS.md     #   .import config rules
│   ├── HARVEST-REPO.md        #   extract-to-shared-library playbook
│   ├── MCP-SWITCH.md          #   swap MCP servers
│   ├── UPGRADE-TIER.md        #   tier migration
│   ├── REMOVE-SYSTEM.md       #   safe system retirement
│   ├── DESIGN-DRIFT.md        #   (Standard & Heavy only)
│   └── ORGANIZE.md            #   (Heavy only)
├── tests/
│   ├── run_tests.gd           # headless runner
│   ├── test_case.gd           # TestCase base class
│   └── test_<system>.gd       # written by the Executor
└── <tier-specific state — see below>
```

### The tracking files, and what each is for

**`project_state.md` / `project-state/_overview.md`** — the master ledger. Completion percentage,
active features and their tri-state status, the Script Registry, the roadmap. Read first, every
session.

**`bugs.md` / `bugs/master_bugs.md` / `bugs/<system>/<system>.md`** — the bug tracker. Status moves
`reported → investigating → resolved` (Heavy adds a fourth, `verified`, meaning confirmed fixed
in-game rather than merely in the diff). Severity is revised as information arrives, not fixed at
intake. When the Executor hits something it can't cheaply fix, it files here rather than derailing.

**`tweak_guide.md`** — the game-feel ledger, and the file most worth knowing about. Every
hand-tunable `@export` var and tuning `const`, grouped by system, in a table: variable, file,
kind, default, what it does in plain language, and safe range. Deliberately excludes internal
state and safety epsilons — it is a table of *knobs*, not internals. Keeping it current is
non-skippable: any task that adds, renames, or re-defaults a tunable updates its row in the same
task. This is how you retune your game without asking an AI where anything lives.

**`blueprints/`** — Architect output, one atomic slice at a time. Archived on use so the Phase 5
audit has something to diff against.

**`architecture_decisions.md` (Heavy)** — an ADR log. *Why* the boss uses a state machine instead
of a behavior tree. Prevents a future session from "helpfully" undoing a deliberate decision.

**`session_log.md` (Heavy)** — append-only, one line per session:
`YYYY-MM-DD HH:MM | agent=… | phase=… | target_system=… | outcome=…`. Cheap protocol-drift
detection after the fact.

**`project-state/archived_systems/`** — where `REMOVE-SYSTEM.md` parks retired systems instead of
deleting them, so reinstating one is a copy-back rather than an archaeology project.

### `session_state.json` — the execution payload

The Architect writes this in its Phase 4, and it is the first file the Executor reads. It is the
durable half of the handoff: the copy-paste prompt carries the task into a new chat, and this file
carries it across a context clear.

```json
{
  "status": "queued",
  "target_system": "player_controller",
  "blueprint_used": "project-state/blueprints/latest_blueprint.md",
  "branch": null,
  "steps": ["Implement the jump state per the blueprint"]
}
```

`status` moves `queued` → `COMPLETED`. `blueprint_used` is a path or `null`; if it is a path, the
Executor reads that blueprint before starting, and archives it when the task completes.
`branch` is set only when the Architect batches parallel tasks onto separate git branches.

If the file is missing but you pasted a handoff prompt, the Executor treats the prompt as
authoritative and writes the payload itself before starting. If there is neither, it reports that
there is no queued work rather than inventing a task.

---

## 8. The scale tiers

Bureaucracy should match scope. Twenty architecture documents for a Flappy Bird clone is wasted
tokens; three files for a 40-hour RPG guarantees hallucination.

### Lite — jams, prototypes, tiny scopes

Zero folder clutter. Three files at the project root: `project_state.md`, `bugs.md`,
`tweak_guide.md`. Blueprint at `blueprint.md`. The agent reads all state instantly.

Playbooks: `REMOVE-SYSTEM.md` (delete, no archive).

### Standard — most indie games

State moves into `project-state/` and `bugs/`. Adds `project-state/blueprints/` with an archive,
and per-system state files (`project-state/<system>/<system>.md`) so the Architect can deep-dive
one system without loading the rest.

Playbooks: Standard's `REMOVE-SYSTEM.md` (archive, don't delete) + `DESIGN-DRIFT.md`.

### Heavy — systems-heavy or multi-year projects

Everything Standard has, plus per-system **bug** files (`bugs/<system>/<system>.md` rolled up into
`bugs/_overview.md`), a 4-state bug lifecycle, `architecture_decisions.md`, `session_log.md`, and
a **Last Verified Commit** marker advanced only after a passing headless run.

Playbooks: Heavy's `REMOVE-SYSTEM.md` + `DESIGN-DRIFT.md` + `ORGANIZE.md`.

The payoff is strict context isolation: working on inventory, the agent is forbidden from reading
combat documentation.

### Changing tier later

The Architect checks scope against tier at the start of every session and will offer an upgrade if
you have outgrown it. Or ask directly:

> *"Run the UPGRADE-TIER playbook. Take this project from Lite to Standard."*

It updates the tier string in `PROJECT-PROFILE.md`, syncs the new governance files, physically
migrates and splits the state files, and deletes the stranded originals.

> The playbook covers Lite → Standard, Standard → Heavy, and Lite → Heavy (which runs the first
> two in sequence). It commits first, migrates your `tweak_guide.md` across **as-is** rather than
> regenerating it, and only deletes the old root files once their content has landed in the new
> locations.

---

## 9. Playbook reference

Playbooks are markdown procedures you invoke by telling the AI to run them.

| Playbook | What it does | Run from | Agent | Tiers |
| :--- | :--- | :--- | :--- | :--- |
| `SETUP-FRAMEWORK.md` | One-time framework install: build MCP, install deps, map Godot path. | repo root | Director | — |
| `docs/templates/SETUP.md` | Reads your GDD, picks a tier, bootstraps `project.godot`/git/`design_docs/`, scaffolds all project docs and your agent pointer file, enforces strict typing. | repo root | Director / Architect | all |
| `ARCHITECT.md` | The planner rulebook: triage → 3 tasks → blueprint → payload + handoff → audit. | project | Architect | all |
| `EXECUTOR.md` | The implementer rulebook: MCP health, typing, tests, doc consistency. | project | Executor | all |
| `SOLO-AGENT.md` | Both role sets in one document, for single-agent setups, with rules that keep planning and execution separated. | project | Solo | all |
| `HARVEST-REPO.md` | Sweeps your game for reusable systems, makes them agnostic, files them in the shared libraries. | project | Architect → Executor | all |
| `UPGRADE-TIER.md` | Migrates a project up a tier, restructuring and splitting state files. | project | Architect | all |
| `SYNC-TEMPLATES.md` | The AI-driven equivalent of `sync_templates.py`: compare project docs to the global templates and replace stale ones. | repo root | Director | all |
| `MCP-SWITCH.md` | Remaps every `mcp__<server>__*` reference when you change MCP servers, flagging capabilities with no equivalent. | project | Executor | all |
| `ASSET-STANDARDS.md` | Rules for hand-editing `.import` files so pixel art stays crisp and `.glb` files get colliders. | project | Executor | all |
| `DESIGN-DRIFT.md` | Read-only audit: where the code and the design docs disagree. Never auto-resolves — you pick the fix direction per item. | project | Architect | Std, Heavy |
| `REMOVE-SYSTEM.md` | Retires a whole system: full scope trace, mandatory dry-run diff, archive-don't-delete, reinstatement path. | project | Executor | all |
| `ORGANIZE.md` | Proposes folder/naming cleanups as a numbered list behind an approval gate; routes every move through MCP. | project | Executor | Heavy |

**`REMOVE-SYSTEM.md` deserves a callout.** Deleting a system by hand is how you get dangling
`class_name` references and orphaned autoloads. This playbook traces every touchpoint — scenes,
autoloads, input map actions, collision layers, tests, state docs, tweak_guide rows, Script
Registry entries, plus a codebase-wide grep for the system's identifiers — then shows you the full
diff and waits for approval before touching anything.

---

## 10. The shared libraries

The framework's "extreme reuse mandate" says: before writing any new mechanic, start at
`global-index/README.md`, route to the right dimension-specific feature file (2D / 3D / Agnostic),
and reuse or adapt rather than build. You do not need a perfect match — recolor the fire explosion
into toxic gas, turn the dash into a dodge roll.

| Library | Purpose |
| :--- | :--- |
| `global-index/` | The routing layer, generated from the libraries below. Feature files appear under `2D/`, `3D/`, `Agnostic/` as content classifies into them. Always the entry point — never scan the libraries blind. |
| `mechanics/` | Reusable `.gd` scripts, one folder per category, each with a companion `.md` explaining dependencies and wiring. |
| `scenes/` | Reusable `.tscn` / `.tres` structures. |
| `assets/` | Raw assets: `models/` (with `building_pieces/`, `characters/`, `environment_assets/`, `props/` beneath it), `music/`, `sfx/`, `vfx/`. |
| `godot-4-snippets-bible/` | Godot 4 API reference and a running log of corrected syntax hallucinations. |

### Current state — read this before relying on any of it

**The libraries ship empty.** `mechanics/`, `scenes/`, and `assets/` contain only their READMEs
and placeholder category folders. Nothing is pre-filled; they grow from your own projects.

**The index tells agents this, and it is generated rather than hand-maintained.**
`global-index/README.md` is built from the libraries' actual contents by
`framework_tools/build_global_index.py`. Feature files (`global-index/3D/vfx_explosions.md` and
friends) are created the first time something classifies into them, so there are no stub files and
no links that resolve to nothing. When the libraries are empty the index says so plainly, and the
templates instruct agents to note it once and build from scratch rather than spending further
calls hunting for reuse.

> **What changed:** the index previously listed ~1,196 entries behind 1,185 absolute
> `file:///C:/Godot_AI_Framework/...` links to the original author's drive — 1,102 of them
> pointing at `effect-blocks/` and `poly-blocks/`, two asset packs not included in this
> distribution. Only 48 of those entries carried a hand-written description; the rest were
> generated filename listings. The 48 descriptions are preserved in
> [`global-index/_ARCHIVED-ENTRY-NOTES.md`](global-index/_ARCHIVED-ENTRY-NOTES.md) as a wishlist,
> and the index is now generated so it cannot drift from reality again.

**Regenerating the index:**

```bash
python framework_tools/build_global_index.py
```

`--dry-run` reports without writing; `--check` exits non-zero if the index has drifted, which
makes it usable as a pre-commit or CI guard. `HARVEST-REPO.md` runs it automatically as its
Phase 2 step 4.

**Steering classification.** The generator infers a feature area from the category folder and a
dimension from the code (`Vector2`/`Node2D` versus `Vector3`/`Node3D`; both or neither means
Agnostic), reading `.tscn` node types as well as `.gd`. Override either with an HTML comment in
the entry's companion `.md`:

```markdown
<!-- index: vfx_explosions -->
<!-- dimension: 3D -->
```

Never edit a generated file — change the companion doc and regenerate.

**The snippets bible is 12 lines** — three API notes (`move_and_slide`, tweens, navigation) and an
empty correction log. It is a seed, not a reference. Its real value is the logging directive: when
you correct an AI's Godot 3-ism, it appends the correct syntax so the mistake does not recur.

### Filling the libraries: HARVEST-REPO

This is how the libraries are meant to grow. After you build something good:

> *"Run the HARVEST-REPO protocol."*

1. **Sweep** — scan `scripts/`, `scenes/`, `shaders/` for things not deeply coupled to this game.
2. **Anti-duplication** — cross-reference against the existing libraries, opening and *reading*
   anything that sounds even vaguely similar rather than trusting filenames. If yours is better,
   refactor the global version instead of adding a near-duplicate.
3. **Plan** — a `harvest_plan.md` listing what moves where and what needs generalizing.
4. **Extract** — *copy*, never move. Strip hardcoded `res://` paths and game-specific singletons,
   replacing them with `@export`s and signals.
5. **Document** — a companion `.md` beside every extracted file: what it does, dependencies,
   required autoloads and project settings, step-by-step wiring, source project, known gotchas.
   UI is always extracted as a **pair** — scene into `scenes/ui/`, script into `mechanics/ui/` —
   with each companion doc cross-linking the other.
6. **Index** — run `python framework_tools/build_global_index.py`, verify with `--check`, then
   log the harvest. If an entry landed in the wrong dimension or feature area, fix the markers in
   its companion `.md` and regenerate rather than editing the generated file.

---

## 11. Procedural 3D modeling

`model-generation/` wraps [`antics-modelkit`](https://www.npmjs.com/package/antics-modelkit). The AI
does not hallucinate binary meshes — it writes a **JavaScript recipe** that constructs the model
mathematically, which means iteration is a parameter change rather than a regeneration.

Full documentation lives in [`model-generation/README.md`](model-generation/README.md); the
agent-facing workflow and technique rules are in `model-generation/AGENTS.md`.

### Setup

```bash
cd model-generation && npm install
```

That also unpacks the kit's own 52 KB technique guide at
`model-generation/node_modules/antics-modelkit/AGENTS.md`, which the agent is required to read
before writing a recipe. It is the most useful file in that workspace.

### The loop

1. Open an AI terminal in `model-generation/` and drop in a reference image.
2. The agent runs the kit's **Phase 0 thinking path** — what am I making, what category
   (`prop` / `plant` / `character` / `structure` / `building` / `vehicle` / `terrain`), which
   palette, flat colour or textured — then presents the plan and waits for your approval.
3. It writes the recipe into `models.mjs` (or a per-model file) using the kit's verbs — `sweep`,
   `lathe`, `extrude`, `patch`, `contour`, `merge`, `weld`, `mirror`, `twist`, `taper`, `bend`,
   `sit`, `mottle` — sizing everything against `PROPORTIONS.character`.
4. Build:

```bash
npm run build
```

`build.js` discovers every `*.mjs` recipe (and every one a level down inside a model folder),
runs the kit's validation gate on each, **dequantizes** the output — Godot does not read the
kit's quantized `.glb` correctly, so this is not optional — and copies the result into `tester/`.
`npm run list` shows what it found without building; `-- --only=<name>` targets one recipe or one
model; `--no-tester` skips the copy.

### Looking at it

Open `model-generation/tester/project.godot` in Godot and press Play. It loads every `.glb` beside
it: left-drag orbits, right-drag pans, wheel zooms, `←`/`→` switch models, `F` frames, `W`
toggles wireframe, `R` reloads after a rebuild.

A translucent capsule exactly one character height tall stands beside the model on a 1-metre
grid. **Check every model against it.** Scale is the most common failure and the one an AI
genuinely cannot see — the same Feel Gap problem as gameplay, in a different medium.

Iterate by editing the recipe, never by regenerating:

> *"Make the hilt 20% wider and give the blade a faint blue emissive."*

### Promoting a model to the shared library

Once approved, move it into a group folder (`general/<name>/`, or one per game) holding the
recipe, the `.glb`, and the reference images. If it is broadly reusable, also copy the `.glb` to
`assets/models/<category>/` and regenerate the index:

```bash
python framework_tools/build_global_index.py
```

### Use your strongest model here

3D spatial reasoning is the hardest thing in this repository — harder than the GDScript work —
and the failure mode is a mesh that builds cleanly, passes the gate, and still looks wrong. The
kit's guide catalogues the traps in detail: reversed windings are *invisible* rather than
wrong-looking, `weld()` before any topological operation, Z-fighting on flush surfaces, origin
placement for Godot pivots, `mottle()` exploding triangle counts on dense meshes.

## 12. framework_tools

Three maintained tools live here. The eleven one-off migration scripts that used to sit beside
them have been moved to `framework_tools/_archive/` — see that folder's README for why none of
them should ever be run.

### The three you use

**`sync_templates.py`** — the full push. Reads each project's tier from
`markdowns4AI/PROJECT-PROFILE.md`, then copies every common + tier template into it.

```bash
python framework_tools/sync_templates.py
```

**`sync_tiers.py`** — tier files only. Use this after a tier upgrade, or when you have changed a
tier's rules and do not want the common templates re-copied.

```bash
python framework_tools/sync_tiers.py
```

**`build_global_index.py`** — regenerates `global-index/` from the actual contents of
`mechanics/`, `scenes/`, and `assets/`. Run it after harvesting anything into the shared
libraries; `HARVEST-REPO.md` runs it for you.

```bash
python framework_tools/build_global_index.py
```

It also takes `--dry-run`, and `--check` (exit 1 if the index has drifted — useful as a
pre-commit or CI guard). See [Section 10](#current-state--read-this-before-relying-on-any-of-it)
for how entries get classified.

The two sync scripts accept the same flags:

| Flag | Effect |
| :--- | :--- |
| `--dry-run` | Print every change without writing anything. Worth running first. |
| `--project NAME` | Sync one project under `Projects/` instead of all of them. |
| `--prune` | (`sync_templates.py` only) Also delete copies of template files found outside their canonical path. |

Both only touch directories under `Projects/` that contain a `project.godot`. Games kept elsewhere
are silently skipped.

**What they will never overwrite:**

- `DOCTRINE.md` and `PROJECT-PROFILE.md` — project-owned, excluded entirely.
- `tweak_guide.md` and `architecture_decisions.md` — *seed* files. They are written only when
  missing. Once your project has content in them, the scripts report `Preserved` and move on.
- `project-state/`, `bugs/`, `design_docs/`, and your `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` pointer
  files — not in the template set at all.

Files whose content already matches are reported as unchanged rather than rewritten, so a repeat
run is a no-op. Misplaced copies are reported but **not** deleted unless you pass `--prune`.

```bash
python framework_tools/sync_templates.py --dry-run
```

### The eleven you don't

`framework_tools/_archive/` holds `rename.py`, `populate_profiles.py`, `update_profile.py`,
`update_architect.py`, `update_executor.py`, `update_executor_final.py`, `update_handoff.py`,
`update_models.py`, `update_models_final.py`, `check_handoff.py`, and `check_phase4.py`.

They are one-off scripts from this repo's own refactors, kept as a record and nothing more:

- `update_architect.py` and `update_models.py` contain `ros.path.join` — a typo that raises
  `NameError` immediately. They cannot run at all.
- `check_handoff.py`, `check_phase4.py`, `update_handoff.py`, and `update_profile.py` hardcode
  `c:\Godot_AI_Framework\docs	emplates	iers`; `update_executor.py` hardcodes
  `c:/Godot_Projects/`. No-ops on your machine — or worse, if you happen to have those paths.
- `rename.py` rewrites strings repo-wide and renames top-level directories. Running it today
  would corrupt the tree.
- `populate_profiles.py` writes a hardcoded profile for a nonexistent `Example_Project` to the
  wrong location.

`update_profile.py` is the one worth reading: it is what introduced the duplicated step 2 and the
`1, 2, 2, 4, 4, 5…` numbering in every shipped `ARCHITECT.md`. That damage is now repaired, and
the Project Profile read it was trying to add is a real step 3.

---

## 13. Customizing AI behavior

**The core idea: when the AI does something that annoys you, do not correct it in chat.** Chat
corrections evaporate at the end of the session. Edit the rule, sync it, and every project you own
learns the lesson permanently.

```
docs/templates/common/     →  shared by every tier (ASSET-STANDARDS, DOCTRINE, HARVEST-REPO,
                              MCP-SWITCH, PROJECT-PROFILE, SYNC-TEMPLATES, UPGRADE-TIER,
                              tweak_guide, tests/, mcp_config.json)
docs/templates/tiers/*/    →  per-tier ARCHITECT / EXECUTOR / SOLO-AGENT + tier-specific playbooks
```

Workflow:

1. Decide the scope. A rule for everyone → `common/`. A rule only Heavy projects need →
   `tiers/heavy/`. A rule for one game only → that project's `markdowns4AI/DOCTRINE.md`.
2. Edit the template. Be specific and imperative — *"Never use `get_node()` with a string literal;
   always use `@onready` with `%UniqueName`."*
3. Push it: `python framework_tools/sync_templates.py --dry-run` to preview, then the same
   command without the flag. Or ask the Director to run the `SYNC-TEMPLATES.md` playbook, which
   walks the same changes but shows you each one for approval first.
4. Restart any open agent session so it re-reads the file.

**What `sync_templates.py` will never overwrite:** `DOCTRINE.md` and `PROJECT-PROFILE.md` are
excluded because they are yours; `tweak_guide.md` and `architecture_decisions.md` are written only
when missing; and `project-state/`, `bugs/`, and `design_docs/` are not in the template set at all.

You can also edit the framework itself from the Director:

> *"Update the EXECUTOR template so the AI adds a header comment to every script it writes, then
> sync it to all my games."*

---

## 14. Troubleshooting

**The agent says the `mcp__godot__*` tools don't exist.**
The server isn't built. `cd docs/tools/godot-mcp && npm install && npm run build`, then fully
restart the agent — the MCP server list is read once at process start.

**Tools exist but `get_godot_version` fails.**
The server can't find Godot. Set `GODOT_PATH` to the absolute path of the executable and restart
the agent. This is required for Steam installs specifically: the server's auto-detection does not
scan Steam library folders on Windows or Linux. Verify the variable landed by reading it in a
*fresh* shell — the one you ran `setx` in won't show it.

**I set `GODOT_PATH` and it still fails.** Run this in a *new* PowerShell window:

```bash
powershell -Command "[System.Environment]::GetEnvironmentVariable('GODOT_PATH','User')"
```

If that's empty, the `setx` didn't take. If it's correct, the agent wasn't fully restarted — quit
the whole application, not just the session.

**The Executor says there's no queued work / `status: idle`.**
The Architect never wrote a payload — usually because you jumped straight to the Executor. Run the
Architect first, or just paste a task description: the Executor treats a pasted handoff prompt as
authoritative and writes the payload itself. See [Section 7](#session_statejson--the-execution-payload).

**The agent ignores `ARCHITECT.md` / `EXECUTOR.md`.**
No agent auto-loads those filenames. Create the pointer file your agent actually reads —
[Section 4](#4-connecting-your-ai-agent).

**The Architect can't find my design docs.**
They must be `.md` files inside `design_docs/` at the project root. Every template globs
`./design_docs/*.md`.

**My game doesn't show up in `git status`.**
By design. The root `.gitignore` excludes every top-level directory and every subdirectory of
`Projects/`, because each game is meant to be its own independent repository. Run `git init` inside
your game's folder and push it to its own remote. The framework repo tracks the framework; your
game repo tracks your game.

**`gdformat` / `gdlint` not found.**
`pip install gdtoolkit`, and make sure your Python scripts directory is on PATH.

**`npm run build` fails in `model-generation/`.**
Usually dependencies: run `npm install` in that folder first. If it reports *"Nothing to build:
no recipe exports a model function yet"*, that is not an error — add an
`export function myProp() { ... }` to `models.mjs`. `npm run list` shows what it discovered.

**The model loads in `tester/` but looks the wrong size.**
Compare it against the translucent capsule — that is exactly one character height. The modelkit
sizes everything in character heights, so a prop built "about a metre" next to a character built
"about two" is the commonest error there is. Fix it by deriving the dimension from
`PROPORTIONS`, not by scaling the mesh afterwards.

**The agent keeps building `test_something.tscn` instead of putting the feature in my game.**
Working as intended — the Feel Gap rule. Playtest the isolated scene, give feedback, and it will
integrate after you approve the feel.

**The agent recommends an effort level rather than a model.**
Intentional. The templates deliberately say "mid-tier model at medium reasoning effort" instead of
naming products, because model names go stale much faster than these rules do. Map the tier to
whatever you have.

---
## Known limitations & rough edges

Everything below is a real, verified gap in the repository as published. None of it is fatal, but
knowing it up front saves you a confusing afternoon.

**Already repaired:** the governance templates (duplicated step numbering, find/replace damage,
broken cross-references), the missing handoff payload, the `sync_templates.py` data-loss bug, the
incoherent solo-agent document, the `SETUP` playbook's missing project bootstrap, the 1,185 dead
index links, the eleven landmine scripts in `framework_tools/`, the missing LICENSE, the
`.gitmodules` entry for a submodule that was never one, and the
`model-generation/` workspace — which was not merely broken but **entirely untracked by git**,
its own `.gitignore` having excluded `build.js`, `models.mjs`, `package.json`, and `AGENTS.md`
from every clone. What remains is content: the shared libraries are empty until you fill them.

### A. The shared libraries are empty
`mechanics/`, `scenes/`, and `assets/` ship with READMEs and placeholder folders but no entries.
The reuse mandate that opens every planning session therefore finds nothing on a fresh clone.

This is now *honest* rather than broken — the generated index says plainly that it is empty, and
the templates tell agents to note it once and build from scratch instead of hunting. But you do
not get the reuse the design promises until you populate the libraries yourself, which is what
`HARVEST-REPO.md` is for.

`godot-4-snippets-bible/godot_4_snippets.md` is likewise a 12-line seed: three API notes and an
empty correction log.

### B. Packaging and setup
- `docs/tools/godot-mcp/build/` is gitignored by that project's own `.gitignore`, so a fresh clone
  has no compiled server until you build it. This is the single most common setup failure.
- `mcp_config.json` does not inject `GODOT_PATH`, so `machine_paths.json` is only ever read by an
  agent by hand — it never reaches the MCP server automatically. Setting the environment variable
  and fully restarting the agent remains a manual step.
- `machine_paths.json` ships with a `YOUR_COMPUTER_NAME_HERE` placeholder and a Godot **4.3** Steam
  path, while the framework targets 4.4+.
- `.gitignore` whitelists `/new_project_design_docs/`, which does not exist, and
  `/Projects/Example_Project/`, which exists only as an empty directory.
- There is no root `.mcp.json`, so the Director has no Godot tools. That is intentional — MCP is
  configured per project — but worth knowing before you try scene work from the root.

### C. Cross-agent portability
The templates phrase code review and security review agent-neutrally, but `/code-review` and
`/security-review` are still named as examples because they exist in Claude Code. On Codex or
Gemini, do the equivalent pass manually.

### D. Tier feature availability is deliberately uneven
`ORGANIZE.md` ships only in Heavy. `DESIGN-DRIFT.md` only in Standard and Heavy.
`architecture_decisions.md` and `session_log.md` only in Heavy. Lite's `REMOVE-SYSTEM.md` deletes
rather than archives, and Lite has a 3-state bug lifecycle where Heavy has 4. This is by design —
less bureaucracy at smaller scope — but it means a playbook you read about may not be in your
project.

---

## Repository layout

```
Godot_AI_Framework_Public/
├── README.md                     # this file
├── LICENSE                       # MIT, plus third-party component notices
├── SETUP-FRAMEWORK.md            # one-time install playbook
├── ARCHITECT.md                  # Director rules for an agent opened at the repo root
├── .gitignore                    # ignores every game project (each gets its own repo)
│
├── Projects/                     # your games live here (gitignored, one repo each)
│
├── docs/
│   ├── machine_paths.json        # per-machine Godot/Node paths, keyed by hostname
│   ├── templates/
│   │   ├── SETUP.md              # project scaffolding playbook
│   │   ├── common/               # tier-independent templates + tests/ + mcp_config.json
│   │   └── tiers/{lite,standard,heavy}/
│   └── tools/
│       ├── README.md             # what is vendored here and how to update it
│       └── godot-mcp/            # vendored MCP server (build/ is gitignored — you must build it)
│
├── framework_tools/              # 3 maintained tools
│   └── _archive/                 #   11 historical one-offs — never run these
├── global-index/                 # GENERATED routing index; feature files appear as content does
│   └── _ARCHIVED-ENTRY-NOTES.md  #   48 curated descriptions from the old hand-written index
├── mechanics/                    # shared scripts (currently empty)
├── scenes/                       # shared scenes (currently empty)
├── assets/{models,music,sfx,vfx}/  # shared raw assets (currently empty)
├── godot-4-snippets-bible/       # Godot 4 API notes + hallucination correction log
└── model-generation/             # antics-modelkit procedural 3D workspace
    ├── models.mjs                #   recipes; ships with one worked example
    ├── build.js                  #   discover -> gate -> dequantize -> copy to tester/
    └── tester/                   #   Godot project that loads and orbits every built .glb
```

---

## Credits & licensing

**Godot MCP server** — this repository vendors
[tugcantopaloglu/godot-mcp](https://github.com/tugcantopaloglu/godot-mcp) at
`docs/tools/godot-mcp/`, under its own MIT license (`docs/tools/godot-mcp/LICENSE`, retained in
full). All credit for that server belongs to its author. See
[`docs/tools/README.md`](docs/tools/README.md) for how it is tracked and updated.

**antics-modelkit** — the procedural 3D workspace depends on the
[`antics-modelkit`](https://www.npmjs.com/package/antics-modelkit) npm package, installed at build
time and not vendored here.

**context7** — MCP documentation server by [Upstash](https://github.com/upstash/context7), invoked
via `npx` and not vendored here.

**This framework is released under the [MIT License](LICENSE).** The vendored godot-mcp keeps its
own MIT license and copyright notice at `docs/tools/godot-mcp/LICENSE`; the npm dependencies are
installed at build time rather than vendored and carry their own terms. `LICENSE` lists all of
them.

---

Happy devving. If you improve a rule, improve it in `docs/templates/` and sync it — that is the
whole point.
