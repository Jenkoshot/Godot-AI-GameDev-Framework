import os
import shutil
import re

projects_dir = 'C:/Godot_Projects/Projects'
tiers_dir = 'C:/Godot_Projects/docs/templates/tiers'

def clean_tier_string(t):
    t = t.lower()
    if 'heavy' in t: return 'heavy'
    if 'lite' in t: return 'lite'
    return 'standard'

def get_project_tier(project_path):
    profile_path = os.path.join(project_path, 'markdowns4AI', 'PROJECT-PROFILE.md')
    if os.path.exists(profile_path):
        with open(profile_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'Current Tier:\s*(.*)', content, re.IGNORECASE)
            if match:
                return clean_tier_string(match.group(1))
    
    gemini_path = os.path.join(project_path, 'GEMINI.md')
    if os.path.exists(gemini_path):
        with open(gemini_path, 'r', encoding='utf-8') as f:
            t = f.read().lower()
            if 'heavy' in t: return 'heavy'
            if 'lite' in t: return 'lite'
    return 'standard'

def find_file_in_project(project_path, filename):
    found = []
    for root, dirs, files in os.walk(project_path):
        if '.git' in dirs: dirs.remove('.git')
        if filename in files:
            found.append(os.path.join(root, filename))
    return found

def get_default_dest(filename, project_path):
    if filename in ['GEMINI.md', 'CLAUDE.md', 'AGENTS.md', 'SETUP.md', 'README.md', 'ORGANIZE.md']:
        return os.path.join(project_path, filename)
    elif filename in ['run_tests.gd', 'test_case.gd']:
        return os.path.join(project_path, 'tests', filename)
    elif filename == 'mcp_config.json':
        return os.path.join(project_path, '.agents', filename)
    elif filename in ['architecture_decisions.md', 'tweak_guide.md']:
        return os.path.join(project_path, 'project-state', filename)
    else:
        return os.path.join(project_path, 'markdowns4AI', filename)

projects = [d for d in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, d))]

for project in projects:
    project_path = os.path.join(projects_dir, project)
    if not os.path.exists(os.path.join(project_path, 'project.godot')):
        continue
        
    tier = get_project_tier(project_path)
    print(f"Syncing Tier Docs for: {project} (Tier: {tier})")
    
    template_files = []
    tier_path = os.path.join(tiers_dir, tier)
    if os.path.exists(tier_path):
        for root, dirs, files in os.walk(tier_path):
            for f in files:
                template_files.append(os.path.join(root, f))
                
    for t_file in template_files:
        filename = os.path.basename(t_file)
        existing_paths = find_file_in_project(project_path, filename)
        
        if existing_paths:
            for ep in existing_paths:
                shutil.copy2(t_file, ep)
                print(f"  Updated: {ep}")
        else:
            dest = get_default_dest(filename, project_path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(t_file, dest)
            print(f"  Created: {dest}")

print("Tier sync complete.")
