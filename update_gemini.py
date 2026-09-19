import os
import glob
import re

paths = glob.glob(r'c:/Godot_Projects/docs/templates/tiers/*/GEMINI.md')
paths.append(r'c:/Godot_Projects/GEMINI.md')

for path in paths:
    if not os.path.exists(path): continue
    content = open(path, encoding='utf-8').read()
    
    # 1. Update Phase 4 title and logic
    # Find Phase 4 section until Phase 5
    pattern = re.compile(r'### Phase 4: Handoff to Claude Code \(Task Execution\).*?(?=### Phase 5)', re.DOTALL)
    
    new_phase4 = """### Phase 4: Handoff to Executor (ChatGPT Codex or Claude Code)
1. **Task Evaluation & Routing:** Evaluate the complexity of the queued task to determine the appropriate executor:
   - **Low to Medium Complexity** (e.g., standard logic, minor fixes, isolated tweaks): Route to **ChatGPT Codex**.
   - **High Complexity** (e.g., deep reworks, complex architecture, large scale refactoring): Route to **Claude Code** (`sonnet 5.0` or `opus 5.0`).
2. **Parallel Branching (If Batched):** If handing off multiple tasks to be run in parallel, instruct the executor in the Handoff Prompt to create and checkout a specific git branch (e.g. `git checkout -b feature/ui-menu`) before making edits. Provide a separate prompt for the final session to merge the branches once verified.
3. **Handoff Prompt Generation:** Generate an easily copyable text block for the user to paste into the chosen executor (or multiple blocks if running parallel sessions). This prompt must direct the executor to the blueprint, define the exact scope of the task, and explicitly command them to handle branch creation/merging if applicable.
4. **Executor Recommendation:** Underneath the copyable prompt, explicitly tell the user which executor to use (e.g., "Use **ChatGPT Codex** for this task" or "Use **Claude Code (Sonnet 5.0 - Medium effort)**").
5. If the task is retiring/removing an entire system rather than building or fixing one, the executor will follow system removal guidelines (e.g., `REMOVE-SYSTEM.md` if present) and perform a dry-run diff for user approval before finalizing deletes.
6. The executor will directly edit the relevant `.gd`, `.tscn`, or `.tres` files to implement the changes.
7. The executor will update `./project-state/[target_system]/[target_system].md` with the new system state changes once execution is complete.

"""
    content = pattern.sub(new_phase4, content)
    
    # 2. Update Model Generation Protocol
    model_pattern = re.compile(r'## 3D Model Generation Protocol.*?(?=\n## |\Z)', re.DOTALL)
    new_model = """## 3D Model Generation Protocol

When the project requires a new, simple 3D asset (e.g., characters, basic props) and an existing one cannot be found in `../../asset-repository/` or other shared folders:
1. **Use Procedural Generation First:** Do NOT attempt to generate 3D model files manually via raw text. Instead, use the procedural generator located at `../../model-generation/` (or `model-generation/` from the root).
2. **Handoff to ChatGPT Codex:** As Gemini, do not modify the code directly. Instead, create a blueprint or task outlining the requirements and explicitly hand it off to **ChatGPT Codex**.
3. **Implementation by ChatGPT Codex:** ChatGPT Codex will modify `../../model-generation/models.mjs` and write a new exported function (using `antics-modelkit` primitives) to procedurally define the required 3D asset, following the existing examples.
4. **Building & Exporting:** The user or ChatGPT Codex will run `node build.js` inside the `../../model-generation/` directory to compile the code and generate the `.glb` file.
5. **Integration:** Use the resulting `.glb` file for the project's needs, ensuring the final `.import` configuration is handled according to `ASSET-STANDARDS.md`.
"""
    content = model_pattern.sub(new_model, content)
    
    open(path, 'w', encoding='utf-8').write(content)
    print("Updated", path)
