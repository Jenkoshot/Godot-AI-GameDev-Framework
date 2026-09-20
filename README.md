# Godot AI Monorepo Framework

Welcome to the **Godot AI Monorepo Framework**. This repository is a scalable, tiered architecture designed to solve the biggest bottlenecks in AI-assisted game development: context window bloat, Godot scene corruption, and code duplication. 

Instead of treating every game as an isolated folder, this monorepo acts as a centralized brain. It utilizes a universal **Architect & Executor Workflow** combined with a **Godot MCP Server** to build games safely, efficiently, and at scale—regardless of which LLM you prefer to use.

---

## 🚀 Why This Architecture Exists

If you've tried building games with AI, you know the pain points:
1. **The Context Trap:** You feed your whole project into an AI, the context window fills up, and the AI starts forgetting rules or hallucinating old code.
2. **Scene File Corruption:** Godot's `.tscn` files are fragile. When an LLM tries to guess text-based scene edits, it often corrupts the file.
3. **The Blank Canvas Problem:** AIs prefer writing from scratch. They will write a bespoke `player_controller.gd` 10 different times for 10 different games instead of reusing one.

**The Solution:**
- **The Architect Agent:** Reads your high-level docs, tracks project completion percentage, calculates bug triage, checks shared repositories for reusable code, and writes a strict "blueprint".
- **The Executor Agent:** Reads *only* the blueprint and executes it. 
- **The Global Repositories:** Forces the AI to harvest and reuse agnostic code and assets (`mechanics/`, `scenes/`, `assets/`) across all your games.

---

## 🛠️ The Agent Ecosystem (LLM Agnostic)

This framework is completely LLM-agnostic. Whether you use ChatGPT, Claude, Gemini, Cursor, or local models, the framework governs their behavior through markdown templates:

- **`ARCHITECT.md`**: The master planner playbook. Instructs your AI to design blueprints, track bugs, and manage the project state without writing code.
- **`EXECUTOR.md`**: The coder playbook. Instructs your AI to strictly follow the architect's blueprints and safely use the Godot MCP server to modify scenes and scripts.
- **`SOLO-AGENT.md`**: A unified playbook. For developers who prefer using a single AI (e.g., Cursor) to handle both planning and coding simultaneously.

---

## ⚖️ The Scale Tiers

Not every game needs the same level of bureaucracy. The framework dynamically categorizes projects into Tiers:
- **Lite Tier:** Best for game jams and prototypes. Minimal folders. State is tracked in root markdown files.
- **Standard Tier:** Best for indie games. Groups bugs and state into a clean `project-state/` folder.
- **Heavy Tier:** Best for massive RPGs or systems-heavy games. Mandates strict architecture logs, session tracking, and per-system tracking files.

*Need to upgrade a game from Lite to Heavy? Just run the `UPGRADE-TIER.md` playbook and the AI will restructure your project automatically.*

---

## 📂 The Three Workspaces (Where to run the AI)

You do not run the AI from just one place. You open your AI CLI or IDE in specific folders depending on the task.

### 1. The Root Workspace (`/Godot_AI_Framework_Public/`)
**Run your AI here when you want to:**
- Create a brand new game project (Run the `docs/templates/SETUP.md` playbook).
- Run python scripts to sync rules across all games (`python framework_tools/sync_templates.py`).
- Ask high-level questions about your entire portfolio of games.

### 2. The Project Workspace (`/Projects/[Your_Game]/`)
**Run your AI here to actually build the game.**
* **Step 1:** Ask your Architect AI to design a feature. It will read `ARCHITECT.md`, check the global repos, and output a blueprint.
* **Step 2:** Tell your Executor AI to execute the blueprint. It will read `EXECUTOR.md`, use the Godot MCP to write the code/scenes, and make an isolated test scene.
* **Step 3:** Playtest the test scene. Once it feels good, the Executor integrates it into the main game.

### 3. The Global Repositories (`/assets/`, `/scenes/`, `/mechanics/`)
**The centralized brain of your games.** 
When your AI builds a great generic system in one of your games, run the `HARVEST-REPO.md` playbook. The AI will extract the code, make it project-agnostic, and move it to `mechanics/` so future games can import it.

---

## ⚙️ Setting up your Godot Path (Steam & Standalone)

The Godot MCP Server (`docs/tools/godot-mcp`) needs to know exactly where your Godot executable is located on your machine to safely edit `.tscn` files.

If you are using the **Steam version** of Godot (or a custom path), you MUST configure this manually before starting:

1. Open the file `docs/machine_paths.json` in a text editor.
2. Find the `"YOUR_COMPUTER_NAME_HERE"` entry. 
3. Change `"YOUR_COMPUTER_NAME_HERE"` to match your actual computer's hostname (e.g., `DESKTOP-ABC123`).
4. Update the `"godot_path"` value to point to your Godot executable. 
   - **For Steam on Windows:** Usually `C:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe`
   - **For Standalone:** Wherever you extracted the Godot `.exe`.
5. Save the file.

---

## 🔧 Setting up the Godot MCP Server

Once your path is set above, you can initialize the MCP server:

1. Navigate to `docs/tools/godot-mcp/`.
2. Run `npm install` and `npm run build`.
3. In your preferred MCP client, configure the server by pointing it to the compiled build directory. 
4. The template configuration is located at `docs/templates/common/mcp_config.json`. The Python sync scripts (`python framework_tools/sync_templates.py`) will automatically drop this config into your game projects.

---

## 📝 Customizing the Framework

This monorepo is designed to be customized. If you find that the AI keeps making a specific mistake in your games, **do not correct it in the chat**. 
Instead, edit `docs/templates/tiers/standard/EXECUTOR.md` and add a new rule. Then, go to the root directory and run `python framework_tools/sync_templates.py`. Your new rule will instantly be pushed to every single game project you own!
