import os
import shutil
import re
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

projects_dir = os.path.join(ROOT_DIR, 'Projects')
templates_dir = os.path.join(ROOT_DIR, 'docs/templates')
common_dir = os.path.join(templates_dir, 'common')
tiers_dir = os.path.join(templates_dir, 'tiers')

def get_project_tier(project_path):
    profile_path = os.path.join(project_path, 'markdowns4AI', 'PROJECT-PROFILE.md')
    if os.path.exists(profile_path):
        with open(profile_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'Current Tier:\s*(.*)', content, re.IGNORECASE)
            if match:
                return match.group(1).strip().lower()
    
    # Fallback to checking ARCHITECT.md or just default to standard
    gemini_path = os.path.join(project_path, 'ARCHITECT.md')
    if os.path.exists(gemini_path):
        with open(gemini_path, 'r', encoding='utf-8') as f:
            if 'heavy' in f.read().lower():
                return 'heavy'
            if 'lite' in f.read().lower():
                return 'lite'
    return 'standard'

def find_file_in_project(project_path, filename):
    found = []
    for root, dirs, files in os.walk(project_path):
        if '.git' in dirs: dirs.remove('.git')
        if filename in files:
            found.append(os.path.join(root, filename))
    return found

def get_default_dest(filename, project_path, tier):
    if filename in ['ARCHITECT.md', 'EXECUTOR.md', 'SOLO-AGENT.md', 'SETUP.md', 'README.md']:
        return os.path.join(project_path, filename)
    elif filename in ['run_tests.gd', 'test_case.gd']:
        return os.path.join(project_path, 'tests', filename)
    elif filename == 'mcp_config.json':
        return os.path.join(project_path, '.agents', filename)
    elif filename in ['architecture_decisions.md', 'tweak_guide.md']:
        if tier == 'lite':
            return os.path.join(project_path, filename)
        else:
            return os.path.join(project_path, 'project-state', filename)
    else:
        return os.path.join(project_path, 'markdowns4AI', filename)

projects = [d for d in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, d))]

for project in projects:
    project_path = os.path.join(projects_dir, project)
    if not os.path.exists(os.path.join(project_path, 'project.godot')):
        continue
        
    tier = get_project_tier(project_path)
    print(f"Syncing Project: {project} (Tier: {tier})")
    
    # Collect all template files
    template_files = []
    
    # root templates
    for f in os.listdir(templates_dir):
        fp = os.path.join(templates_dir, f)
        if os.path.isfile(fp):
            template_files.append(fp)
            
    # common templates
    for root, dirs, files in os.walk(common_dir):
        for f in files:
            if f not in ['DOCTRINE.md', 'PROJECT-PROFILE.md']:
                template_files.append(os.path.join(root, f))
                
    # tier templates
    tier_path = os.path.join(tiers_dir, tier)
    if os.path.exists(tier_path):
        for root, dirs, files in os.walk(tier_path):
            for f in files:
                template_files.append(os.path.join(root, f))
                
    # Perform sync
    for t_file in template_files:
        filename = os.path.basename(t_file)
        
        existing_paths = find_file_in_project(project_path, filename)
        dest = get_default_dest(filename, project_path, tier)
        
        for ep in existing_paths:
            if os.path.normcase(os.path.normpath(ep)) != os.path.normcase(os.path.normpath(dest)):
                try:
                    os.remove(ep)
                    print(f"  Removed stray file: {ep}")
                except Exception as e:
                    print(f"  Failed to remove {ep}: {e}")
                    
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(t_file, dest)
        if dest in existing_paths:
            print(f"  Updated: {dest}")
        else:
            print(f"  Created: {dest}")

print("Sync complete.")
