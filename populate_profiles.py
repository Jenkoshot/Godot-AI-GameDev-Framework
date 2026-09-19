import os

profiles = {
    'Example_Project': {
        'Dimension': '3D',
        'Genre': 'Example Genre',
        'Camera Perspective': 'First-Person',
        'Art Style': 'Low-poly',
        'Core Gameplay Loop': '> Example gameplay loop...',
        'Key Technical Constraints': '- Constraint 1\n- Constraint 2'
    }
}

base_dir = r'Projects'

for proj, data in profiles.items():
    file_path = os.path.join(base_dir, proj, 'PROJECT-PROFILE.md')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    content = f'''# PROJECT-PROFILE.md

This file serves as a quick-reference overview of the project for AI agents.

## 1. Project Identification
- **Project Name:** {proj}
- **Current Tier:** Standard

## 2. Core Attributes
- **Dimension:** {data['Dimension']}
- **Genre:** {data['Genre']}
- **Camera Perspective:** {data['Camera Perspective']}
- **Art Style:** {data['Art Style']}

## 3. Core Gameplay Loop
{data['Core Gameplay Loop']}

## 4. Key Technical Constraints
{data['Key Technical Constraints']}
'''
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {proj}')
