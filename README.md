# Godot AI GameDev Framework

Welcome to the **Godot AI GameDev Framework**. This repository is a scalable, tiered architecture designed to solve the biggest bottlenecks in AI-assisted game development: context window bloat, Godot scene corruption, and code duplication. 

Instead of treating every game as an isolated folder, this monorepo acts as a **centralized brain** utilizing a universal Architect & Executor Workflow.

## 🛠️ Included Tools & Ecosystem

This framework comes pre-packaged with powerful tools that allow AI to build games autonomously:
1. **Godot MCP Server:** A Model Context Protocol server (`docs/tools/godot-mcp/`) that allows the AI to natively read and modify Godot `.tscn` and `.tres` files without corrupting them.
2. **Procedural 3D Modelkit (`antics.gg`):** An integrated Node.js library (`model-generation/`) that allows the AI to generate and modify 3D `.glb` assets purely through code parameters, saving you from opening Blender.
3. **Global Harvesting:** Shared `assets/`, `scenes/`, and `mechanics/` folders where the AI can extract and store generic code (like a dialogue system) to instantly reuse in your future games.

---

## ⚡ 1. Initial Installation

Setting up the framework is completely automated. Open your preferred AI terminal (like Antigravity or Claude Code) at the **root of this repository** and say:

> *"Run the SETUP-FRAMEWORK playbook."*

The AI will automatically install the Node and Python requirements, compile the Godot MCP server, and ask you for your Godot `.exe` file path to configure the environment.

---

## 🌍 2. The Root Level (The Director Workspace)

When your AI is running at the **root of the repository**, it acts as the Director. This is where you brainstorm ideas, create new games, and manage the overall workflow. 

**Where to put your GDD?**
If you have a Game Design Document, drop it anywhere at the root (or in `docs/`) and tell the AI to read it.

### Demo Prompts (Run at the Root):
* **Brainstorming:** *"I want to make a cozy farming game mixed with a roguelike. Read my GDD.md, critique it, and let's brainstorm a core gameplay loop."*
* **Creating a Project:** *"Run the SETUP playbook. I want to create a new Standard Tier project called 'FarmRogue' based on our GDD."*
* **Editing the Workflow:** *"I want to update the EXECUTOR.md template so that the AI always adds a header comment to every script it writes. Update the template and run sync_templates.py to push it to all my games."*
* **Updating Global Tooling:** *"Look at my framework_tools python scripts. Can you write a new script that automatically zips up my projects for a release?"*

---

## 🏗️ 3. The Project Level (The Architect & Executor Workspace)

Once a project is created, open your AI terminal **inside the project folder** (e.g., `Projects/FarmRogue/`). 

Here, your AI splits into two roles: **The Architect** (planning, tracking bugs, architecture) and **The Executor** (writing code, modifying scenes).

### Demo Prompts (Run at the Project Level):
* **Task Evaluation:** *"Read the project_state.md and bugs/master_bugs.md. What is the highest priority feature or bug we should work on next?"*
* **Custom Task Planning (The Architect):** *"I want to add a double-jump mechanic. Create a highly detailed architectural plan for this. Once done, give me a copy-paste prompt to send to my Executor Agent, and tell me what LLM model size and effort level I should use for it."*
* **Coding (The Executor):** *"Execute the latest blueprint you just made for the double-jump. Use the Godot MCP to modify the Player.tscn file."*
* **Concept Art & Vibe Checks:** *"Generate a concept image for what the main menu UI should look like based on our game's theme."*

### 🐙 Per-Project Version Control (Git)
A massive advantage of this framework is that **every project is its own Git repository**. 
If you want to push your game to GitHub, just create an empty repo online, give the SSH link to the AI, and say:
> *"Initialize a git repo here, make an initial commit, and push it to this link: [git@github.com...]"*

---

## 🎨 4. Procedural 3D Modeling

Need a 3D asset? Open your AI terminal inside the `/model-generation/` folder. 

This folder uses the `antics.gg` procedural modelkit. **How it works:** The AI doesn't try to hallucinate raw binary 3D meshes. Instead, it writes a Javascript recipe (`models.mjs`) that mathematically constructs the model using parameters (extrude, bevel, twist).

### Demo Prompts (Run in `/model-generation/`):
* *"I need a low-poly medieval broadsword. Here is a concept image to base it on. Write the recipe in models.mjs."*
* *"Modify the broadsword script to make the hilt wider and the blade slightly glowing blue."*

**Pro-Tip:** Use higher-level, highly capable LLMs (like Claude 3.5 Sonnet or GPT-4o) for procedural modeling, as the spatial reasoning required to code 3D math is extremely complex. Because the models are parameterized, you can ask the AI to simply "tweak the blade length" and it only has to change a single number in the code!

---

## 🌾 5. Global Harvesting (Never Write Code Twice)

When you build a fantastic, reusable system (like an Inventory UI or a Dialogue Manager) inside one of your games, don't leave it trapped there!

Open your AI in that game's folder and say:
> *"Run the HARVEST-REPO playbook on our new Dialogue System."*

The AI will carefully untangle the code from your specific game, make it project-agnostic, and move it to the global `mechanics/` or `assets/` folder. The next time you start a new game, your AI can instantly import that system.

---

## ⚖️ Customizing The Tiers & Behavior

This framework scales with you. Projects are divided into **Lite**, **Standard**, and **Heavy** tiers. A game jam game (Lite) has almost no bureaucracy. A massive RPG (Heavy) has strict per-system documentation and architectural logging.

If you ever need to scale up a game, just tell the AI: *"Run the UPGRADE-TIER playbook."*

If the AI makes a mistake that annoys you, **do not correct it in chat**. Open `docs/templates/common/EXECUTOR.md`, add a rule saying *"Never do X again"*, and run the sync script. Your AI will instantly learn that lesson for every game you ever build. Happy devving!
