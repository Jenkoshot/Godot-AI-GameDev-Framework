# Asset Standards

When dragging raw assets into Godot, it auto-generates `.import` files. AIs usually ignore these, resulting in blurry pixel art or 3D models without collision.

## Agent Directives (Claude)
Whenever you are handling raw assets, you MUST read this file and properly configure the generated `.import` files by modifying them via text editing.

### UI / 2D Textures (Pixel Art)
- **Compression**: Must be disabled (e.g., set to VRAM uncompressed or lossless depending on the specific standard).
- **Filtering**: Must use **Nearest** filtering to preserve sharp edges for pixel art.

### 3D Models (`.glb` / `.fbx`)
- **Colliders**: Must be configured to generate colliders on import.
- **Scale**: Must respect the intended scale configuration.
