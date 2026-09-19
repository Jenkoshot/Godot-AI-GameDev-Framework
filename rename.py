import os

mappings = {
    "asset_repository": "asset-repository",
    "mechanic_repository": "mechanic-repository",
    "scene_repository": "scene-repository",
    "EffectBlocks": "effect-blocks",
    "PolyBlocks": "poly-blocks",
    "Godot_Shader_Bible": "godot-shader-bible",
    "Godot_4_Snippets_Bible": "godot-4-snippets-bible",
    "Global_Index": "global-index",
    "ModelGeneration": "model-generation"
}

def replace_in_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return
    
    new_content = content
    for old, new in mappings.items():
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_content)
        print(f"Updated {path}")

for root, dirs, files in os.walk('.'):
    if '.git' in root or '.claude' in root or 'node_modules' in root or 'Projects' in root:
        continue
    for file in files:
        if file.endswith(('.md', '.gd', '.tscn', '.tres', '.gitignore', '.json', '.txt', '.godot', 'project.godot')):
            replace_in_file(os.path.join(root, file))
            
for old, new in mappings.items():
    if os.path.exists(old):
        os.rename(old, "temp_" + old)
        os.rename("temp_" + old, new)
        print(f"Renamed directory {old} to {new}")
