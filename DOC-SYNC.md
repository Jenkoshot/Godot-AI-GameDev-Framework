# DOC-SYNC Playbook

**Trigger:** When the user explicitly asks you to "run doc sync" or "sync docs to all projects".

**Description:** This protocol synchronizes the latest master template markdowns (from `docs/templates/`) to all child projects inside the `Projects/` directory.

## Execution Steps
1. Save the Python script below to `c:\Godot_Projects\scratch_sync.py`.
2. Execute it in the terminal via `python c:\Godot_Projects\scratch_sync.py`.
3. Read the output.
4. Delete the scratch script using `rm c:\Godot_Projects\scratch_sync.py`.
5. Report the sync results back to the user in a short summary.

```python
import os
import shutil

ROOT_DIR = r"c:\Godot_Projects"
PROJECTS_DIR = os.path.join(ROOT_DIR, "Projects")
TEMPLATES_DIR = os.path.join(ROOT_DIR, "docs", "templates")

EXCLUDE_FILES = ["PROJECT-PROFILE.md", "DOCTRINE.md", "mcp_config.json"]
EXCLUDE_DIRS = ["tests", "common", "tiers"]

def sync_project(project_path):
    # Determine tier by looking at unique tier files
    tier = "lite"
    if os.path.exists(os.path.join(project_path, "ORGANIZE.md")):
        tier = "heavy"
    elif os.path.exists(os.path.join(project_path, "DESIGN-DRIFT.md")):
        tier = "standard"
        
    print(f"Syncing {os.path.basename(project_path)} (Tier: {tier})...")
    
    sources = []
    
    # 1. Common templates
    common_dir = os.path.join(TEMPLATES_DIR, "common")
    if os.path.exists(common_dir):
        for f in os.listdir(common_dir):
            if f not in EXCLUDE_FILES and f not in EXCLUDE_DIRS:
                src = os.path.join(common_dir, f)
                if os.path.isfile(src): sources.append(src)
                
    # 2. Tier templates
    tier_dir = os.path.join(TEMPLATES_DIR, "tiers", tier)
    if os.path.exists(tier_dir):
        for f in os.listdir(tier_dir):
            if f not in EXCLUDE_FILES and f not in EXCLUDE_DIRS:
                src = os.path.join(tier_dir, f)
                if os.path.isfile(src): sources.append(src)
                
    # 3. Root templates (e.g. SETUP.md, UPGRADE-TIER.md)
    for f in os.listdir(TEMPLATES_DIR):
        src = os.path.join(TEMPLATES_DIR, f)
        if os.path.isfile(src) and f not in EXCLUDE_FILES and f not in EXCLUDE_DIRS:
            sources.append(src)
            
    # Copy them over
    for src in sources:
        dst = os.path.join(project_path, os.path.basename(src))
        shutil.copy2(src, dst)
            
if os.path.exists(PROJECTS_DIR):
    for project_name in os.listdir(PROJECTS_DIR):
        project_path = os.path.join(PROJECTS_DIR, project_name)
        if os.path.isdir(project_path):
            # Only sync if it's a configured AI project (has a GEMINI.md)
            if os.path.exists(os.path.join(project_path, "GEMINI.md")):
                sync_project(project_path)
            else:
                print(f"Skipping {project_name} (Not an AI-configured project)")
else:
    print("Projects directory not found.")
    
print("Sync complete.")
```
