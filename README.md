# Godot AI GameDev Framework

Welcome to the **Godot AI GameDev Framework**. This repository is a scalable, tiered architecture designed to solve the biggest bottlenecks in AI-assisted game development: context window bloat, Godot scene corruption, and code duplication. 

Instead of treating every game as an isolated folder, this monorepo acts as a **centralized brain** utilizing a universal Architect & Executor Workflow.

---

## 🖥️ Compatibility & Tested Environments

While the markdown templates technically allow you to use any AI, this framework has been rigorously tested against specific configurations:
- **Tested AI Agents:** ChatGPT Codex, Claude Code, and Antigravity (Gemini).
- **Primary Environment:** Fully tested using the Desktop App versions of these AIs on **Windows**.
- **CLI Environments:** It should work perfectly with terminal/CLI versions of these AIs on Windows as well, provided your Node/Python environment variables are set up correctly.
- **Linux/macOS:** Currently **untested**. Because the framework relies on standard Python and Node.js scripts, it should be natively compatible, but certain pathing logic (like pointing to the Godot executable in `machine_paths.json`) will require your own manual configuration.

---

## ⚡ 1. Initial Installation

Setting up the framework is completely automated. Open your preferred AI terminal (like Antigravity or Claude Code) at the **root of this repository** and say:

> *"Run the SETUP-FRAMEWORK playbook."*

The AI will automatically install the Node and Python requirements, compile the Godot MCP server, and ask you for your Godot `.exe` file path to configure the environment.

---

## 🏗️ 2. The Root Workspace (The Director)

When your AI is running at the **root of the repository**, it acts as the Director. This is where you brainstorm ideas, create new games, and manage the overall workflow. 

**Demo Prompts (Run at the Root):**
* **Brainstorming:** *"I want to make a cozy farming game mixed with a roguelike. Read my GDD.md, critique it, and let's brainstorm a core gameplay loop."*
* **Creating a Project:** *"Run the SETUP playbook based on my GDD. I want to create a new Standard Tier project called FarmRogue."*
* **Editing the Workflow:** *"I want to update the EXECUTOR.md template so that the AI always adds a header comment to every script it writes. Update the template and run sync_templates.py to push it to all my games."*
* **Updating Global Tooling:** *"Look at my framework_tools python scripts. Can you write a new script that automatically zips up my projects for a release?"*

**Behind the Scenes (Creating a Project):**
When you run the SETUP playbook, here is exactly what the AI does automatically:
1. **Reads the GDD:** It absorbs your game's mechanics, scope, and aesthetic.
2. **Tier Selection:** It asks you whether the project should be a Lite, Standard, or Heavy tier based on the GDD scope.
3. **Documentation Scaffolding:** Depending on the tier, it generates the tracking files. (Lite gets 3 root markdown files; Standard gets a `project-state/` folder; Heavy gets per-system folders like `combat/` and `inventory/`).
4. **Godot Project Creation:** It physically creates the `Projects/[YourGame]/` directory, generates a valid `project.godot` file, and an `icon.svg` so the engine recognizes it immediately.
5. **Git Initialization:** It runs `git init` inside your specific project folder. This ensures every single game you make acts as an isolated Git repository, ready to be pushed to its own GitHub page.

---

## ⚖️ The Scale Tiers: Choosing Your Architecture

Not every game needs the same level of AI bureaucracy. If you force an AI to read 20 architectural documents for a Flappy Bird clone, you waste tokens. If you don't use enough documentation for a massive RPG, the AI will hallucinate. 

### 🟢 Lite Tier
* **What it has:** Zero folder clutter. State is tracked in just three files located directly at the root of your game: `project_state.md`, `bugs.md`, and `tweak_guide.md`.
* **How it works:** The AI reads those three files instantly, giving it lightning-fast context on your game without navigating directories.

### 🟡 Standard Tier
* **What it has:** Cleans up the root directory by moving documentation into dedicated `project-state/` and `bugs/` folders. It introduces the `blueprints/` directory.
* **How it works:** The Architect AI drafts detailed Markdown blueprints in the blueprints folder. The Executor AI reads that blueprint and executes it, keeping planning and coding completely separated for higher quality code.

### 🔴 Heavy Tier
* **What it has:** Granular, per-system tracking. Instead of one master state file, documentation is split into discrete folders (e.g., `project-state/combat/`, `project-state/inventory/`). It also enforces `architecture_decisions.md` (ADRs) and `session_log.md` tracking.
* **How it works:** Completely eliminates context-window bloat. If the AI is working on the inventory, it is strictly forbidden from reading the combat documentation. It ensures the AI only loads the exact context it needs for the task at hand.

---

## 🎮 3. Working on a Project (The Daily Loop)

You don't need to clutter the repo with test assets to see if this works. You can prove it yourself in 5 minutes. Here is the exact step-by-step loop for building a feature:

**Step 1: The Architect (Project Evaluation & Planning)**
Open your Architect AI inside `Projects/[YourGame]/`. 
*Prompt:* > *"What is the state and progress of the project, and what is the next task?"*

The Architect will evaluate your entire project, calculate completion percentage, and present you with **3 tasks** to choose from. 

**Step 2: Task Selection & Blueprinting**
*Prompt:* > *"Let's go with Task 2."*

Once you choose a task, the Architect will generate a highly detailed blueprint. At the end, it will give you a copy-paste prompt and recommend which model size and effort level the Executor should use.

**Step 3: The Executor (Coding)**
Open your Executor AI in the same folder. Paste the exact prompt the Architect just gave you. The Executor will read the blueprint, use the Godot MCP to safely modify the `.tscn` files, and write the GDScript.

**Step 4: Playtest & Tweak**
Open the project in the Godot Engine and press Play. If the movement feels too slow, ask the Executor: 
*Prompt:* > *"The player moves too slow. Increase the speed variable, and don't forget to log this adjustment in the tweak_guide.md file."*

---

## 🎨 4. Procedural 3D Modeling Deep Dive (`antics.gg`)

Need a 3D asset but don't know how to use Blender? Open your AI terminal inside the `/model-generation/` folder. 

This folder uses the `antics.gg` procedural modelkit. The AI doesn't hallucinate raw binary 3D meshes. Instead, it writes a Javascript recipe (`models.mjs`) that mathematically constructs the model.

**Step-by-Step Generation:**
1. Drop a reference image (concept art) into the chat.
2. *Prompt:* > *"Analyze this image. I need a low-poly stylized medieval broadsword. Write the procedural generation recipe for it in models.mjs. Use basic extrusions and bevels."*
3. Run `node build.js` in your terminal.
4. It will spit out a `.glb` file. Drag this file into your global `assets/models/` folder.
5. *Iteration:* If the sword looks wrong, do not regenerate it from scratch! Tell the AI: *"Modify the script to make the hilt 20% wider and the blade slightly glowing blue."* It only has to change a few variables in the code.

*Pro-Tip:* Always use the smartest models available (like Claude 3.5 Sonnet or GPT-4o) for this workspace. 3D spatial math is highly complex.

---

## 🗂️ The Anatomy of a Game Project (Tracking Files)

If you are wondering exactly how the AI keeps track of your game without reading the entire codebase every time, it uses these specific markdown files generated inside your `Projects/[YourGame]/` folder.

**The Core State Files (Present in all Tiers):**
* **`project_state.md`**: The master ledger. It tracks the current completion percentage of the game, the active features, and the high-level roadmap. The AI reads this first to know where it is.
* **`bugs.md` (or `bugs/master_bugs.md`)**: The central bug tracker. It is strictly formatted. If the Executor AI encounters a bug it cannot easily fix within its token limit, it writes it here for the Architect to triage later.
* **`tweak_guide.md`**: The "Game Feel" ledger. Whenever the AI writes a script with an exposed variable (e.g., `export var player_speed = 500`), it logs that variable and file path here. You, the human, can open this file, read what variables exist, and go into the Godot Inspector to manually tweak the game feel without needing to ask the AI where the code is.

**The Advanced Tracking Files (Standard & Heavy Tiers):**
* **`blueprints/` directory**: When the Architect designs a feature, it writes a detailed `.md` file here. The Executor reads *only* that blueprint to write the code. This prevents the Executor from getting confused by the rest of the game's documentation.
* **`architecture_decisions.md` (ADRs)**: Used in Heavy tier. If the AI makes a major structural decision (e.g., "We are using a State Machine for the boss instead of a Behavior Tree because..."), it logs it here. If the AI ever gets confused later, it reads this file to remember *why* the codebase is structured that way.
* **`session_log.md`**: Used in Heavy tier. A running diary of what the AI did during every session, allowing it to trace its own steps if something breaks.

---

## 📖 The Playbook Directory (Command Reference)

The framework is driven by "Playbooks" located in `docs/templates/` and `framework_tools/`. Think of these as magic spells you can cast by simply telling the AI to run them.

| Playbook / Template | What it does | Where to call it | Which Agent |
| :--- | :--- | :--- | :--- |
| **`SETUP.md`** | Consumes your GDD, selects a tier, scaffolds the Godot project, and inits Git. | Root Directory | Architect |
| **`ARCHITECT.md`** | The core rulebook governing how your planning AI creates blueprints and tracks bugs. | Automatically read | Architect |
| **`EXECUTOR.md`** | The core rulebook governing how your coding AI safely edits Godot scenes via MCP. | Automatically read | Executor |
| **`SOLO-AGENT.md`** | A unified rulebook for users who only use a single AI (like Cursor) for both planning and coding. | Automatically read | Solo Agent |
| **`HARVEST-REPO.md`** | Extracts a cool system from your game, makes it agnostic, and saves it to global `mechanics/`. | Project Directory | Architect |
| **`UPGRADE-TIER.md`** | Upgrades a Lite game to a Standard/Heavy game by automatically restructuring its folders. | Project Directory | Architect |
| **`DESIGN-DRIFT.md`** | Audits your game's codebase against your GDD and highlights where you went off track. | Project Directory | Architect |
| **`REMOVE-SYSTEM.md`** | Safely unhooks and deletes a bloated or broken feature without corrupting the rest of the game. | Project Directory | Executor |
| **`ORGANIZE.md`** | Cleans up messy folders, deletes orphaned files, and standardizes naming conventions. | Project Directory | Executor |
| **`sync_templates.py`** | A python script that pushes your custom rule updates to every single game you own. | Root Directory | Terminal |

---

## 🔧 Customizing AI Behavior

If the AI makes a mistake that annoys you, **do not correct it in chat**. Open `docs/templates/common/EXECUTOR.md`, add a rule saying *"Never do X again"*, and run the Python sync script at the root. Your AI will instantly learn that lesson for every game you ever build. Happy devving!
