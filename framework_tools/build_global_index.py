#!/usr/bin/env python3
"""Regenerate `global-index/` from what is actually in the shared libraries.

The global index is the routing layer every planning session starts at: an agent reads
`global-index/README.md`, jumps to the right dimension/feature file, and finds the scripts,
scenes, and assets relevant to what it is about to build.

That only works if the index is true. A hand-maintained index drifts, and a drifted index is
worse than no index at all — it sends every future agent on a lookup that fails. So the index is
generated from the filesystem instead of edited by hand.

Usage:
    python framework_tools/build_global_index.py               # rewrite global-index/
    python framework_tools/build_global_index.py --dry-run     # report only
    python framework_tools/build_global_index.py --check       # exit 1 if out of date (for CI)

How an entry gets classified
----------------------------
For each file in `mechanics/`, `scenes/`, and `assets/`:

* **Feature area** comes from the file's category folder (e.g. `mechanics/movement/` ->
  `movement_general`), or from an explicit `<!-- index: movement_flight -->` marker in the
  companion `.md`.
* **Dimension** (2D / 3D / Agnostic) is inferred from the code: `Node2D`/`Vector2`/`Sprite2D` and
  friends mean 2D, `Node3D`/`Vector3`/`MeshInstance3D` mean 3D, both or neither means Agnostic.
  An explicit `<!-- dimension: 3D -->` marker in the companion `.md` always wins.
* **Description** is the first non-heading line of the companion `.md` (the file with the same
  base name), falling back to its `## What it does` section.

Entries are grouped by base name so a `.gd` + `.tscn` + `.md` trio becomes one entry listing all
its parts, and every link is written repo-relative so it resolves on any machine.
"""
import argparse
import os
import re
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_DIR = os.path.join(ROOT_DIR, 'global-index')

LIBRARIES = {
    'mechanics': os.path.join(ROOT_DIR, 'mechanics'),
    'scenes': os.path.join(ROOT_DIR, 'scenes'),
    'assets': os.path.join(ROOT_DIR, 'assets'),
}

DIMENSIONS = ('2D', '3D', 'Agnostic')

# Category folder -> feature-area file. Anything unmapped becomes <category>_general.
CATEGORY_MAP = {
    'ai': 'combat_logic',
    'audio': 'ui_feedback_and_juice',
    'camera': 'camera_systems',
    'combat': 'combat_logic',
    'input': 'movement_general',
    'minigame': 'minigames_and_rules',
    'models': 'environment_general',
    'movement': 'movement_general',
    'music': 'ui_feedback_and_juice',
    'procgen': 'procgen_general',
    'rules_engine': 'minigames_and_rules',
    'sfx': 'ui_feedback_and_juice',
    'shaders': 'shaders',
    'spawning': 'procgen_spawning',
    'ui': 'ui_components',
    'utility': 'movement_general',
    'vfx': 'vfx_general',
}

# The full set of feature files the index ships, so the taxonomy is stable even when empty.
FEATURE_AREAS = [
    'camera_systems', 'combat_logic', 'combat_loot', 'combat_projectiles',
    'combat_stats_and_damage', 'combat_weapons', 'environment_general',
    'environment_rocks_and_cliffs', 'environment_space', 'environment_vegetation',
    'environment_water', 'minigames_and_rules', 'movement_flight', 'movement_general',
    'movement_tethering', 'procgen_general', 'procgen_layouts', 'procgen_scatter_tools',
    'procgen_spawning', 'shaders', 'ui_components', 'ui_feedback_and_juice', 'ui_hud',
    'ui_transitions', 'vfx_decals', 'vfx_energy', 'vfx_explosions', 'vfx_fire', 'vfx_general',
    'vfx_impacts', 'vfx_liquid', 'vfx_smoke',
]

CODE_EXT = {'.gd', '.gdshader'}
SCENE_EXT = {'.tscn', '.tres'}
ASSET_EXT = {'.glb', '.gltf', '.obj', '.fbx', '.png', '.jpg', '.jpeg', '.svg', '.webp',
             '.ogg', '.wav', '.mp3'}
SKIP_FILES = {'README.md', '.keep', '.gdignore'}
SKIP_DIRS = {'.git', '.godot', '.import', 'node_modules', '__pycache__'}

HINT_2D = re.compile(r'\b(Node2D|Vector2|Sprite2D|CharacterBody2D|RigidBody2D|Area2D|'
                     r'TileMap|CanvasItem|Camera2D|CollisionShape2D|Path2D)\b')
HINT_3D = re.compile(r'\b(Node3D|Vector3|MeshInstance3D|CharacterBody3D|RigidBody3D|Area3D|'
                     r'Camera3D|CollisionShape3D|Path3D|GPUParticles3D|StaticBody3D)\b')


ACRONYMS = {'Ui': 'UI', 'Hud': 'HUD', 'Vfx': 'VFX', 'Sfx': 'SFX', 'Ai': 'AI',
            'Procgen': 'ProcGen', '2d': '2D', '3d': '3D'}


def title_case(name):
    words = [w.capitalize() for w in re.split(r'[_\-\s]+', name) if w]
    return ' '.join(ACRONYMS.get(w, w) for w in words)


def read_text(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as fh:
            return fh.read()
    except OSError:
        return ''


def detect_dimension(companion_text, code_text):
    marker = re.search(r'<!--\s*dimension:\s*(2D|3D|Agnostic)\s*-->', companion_text, re.I)
    if marker:
        return marker.group(1).capitalize().replace('d', 'D')
    blob = code_text + companion_text
    two, three = bool(HINT_2D.search(blob)), bool(HINT_3D.search(blob))
    if two and not three:
        return '2D'
    if three and not two:
        return '3D'
    return 'Agnostic'


def detect_feature(companion_text, category):
    marker = re.search(r'<!--\s*index:\s*([a-z0-9_]+)\s*-->', companion_text, re.I)
    if marker and marker.group(1).lower() in FEATURE_AREAS:
        return marker.group(1).lower()
    if category in CATEGORY_MAP:
        return CATEGORY_MAP[category]
    guess = '%s_general' % category
    return guess if guess in FEATURE_AREAS else 'movement_general'


def extract_description(text):
    section = re.search(r'^##\s*What it does\s*$(.*?)(?=^##\s|\Z)', text, re.M | re.S)
    body = section.group(1) if section else text
    for line in body.split('\n'):
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('<!--'):
            continue
        if line.startswith('>'):
            line = line[1:].strip()
        return re.sub(r'\s+', ' ', line)
    return ''


def collect():
    """Return {dimension: {feature: {entry_name: {'desc':…, 'files':[(kind, relpath)]}}}}"""
    tree = {d: {f: {} for f in FEATURE_AREAS} for d in DIMENSIONS}
    total = 0

    for lib_name, lib_path in LIBRARIES.items():
        if not os.path.isdir(lib_path):
            continue
        for root, dirs, names in os.walk(lib_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            rel_root = os.path.relpath(root, lib_path)
            parts = [] if rel_root == '.' else rel_root.split(os.sep)
            category = parts[0] if parts else lib_name

            groups = {}
            for name in sorted(names):
                if name in SKIP_FILES:
                    continue
                base, ext = os.path.splitext(name)
                ext = ext.lower()
                if ext not in CODE_EXT | SCENE_EXT | ASSET_EXT | {'.md'}:
                    continue
                groups.setdefault(base, []).append(name)

            for base, names_in_group in sorted(groups.items()):
                paths = [os.path.join(root, n) for n in names_in_group]
                has_payload = any(os.path.splitext(p)[1].lower() != '.md' for p in paths)
                if not has_payload:
                    continue

                companion = next((p for p in paths if p.lower().endswith('.md')), None)
                companion_text = read_text(companion) if companion else ''
                # Scan scenes as well as scripts: a .tscn's node types (GPUParticles3D,
                # Sprite2D, …) are often the only dimension signal an entry has.
                code_text = ''.join(read_text(p) for p in paths
                                    if os.path.splitext(p)[1].lower() in CODE_EXT | SCENE_EXT)

                dim = detect_dimension(companion_text, code_text)
                feat = detect_feature(companion_text, category)
                desc = extract_description(companion_text)

                files = []
                for p in sorted(paths):
                    ext = os.path.splitext(p)[1].lower()
                    kind = ('DOC' if ext == '.md' else
                            'GD' if ext in CODE_EXT else
                            'TSCN' if ext in SCENE_EXT else 'ASSET')
                    # Store absolute; the link is made relative at render time, because it has
                    # to resolve from global-index/<dimension>/, not from global-index/.
                    files.append((kind, os.path.basename(p), p))

                entry = tree[dim][feat].setdefault(title_case(base),
                                                   {'desc': desc, 'files': []})
                if desc and not entry['desc']:
                    entry['desc'] = desc
                entry['files'].extend(files)
                total += 1
    return tree, total


HEADER_NOTE = """<!-- GENERATED FILE - do not edit by hand.
     Regenerate with: python framework_tools/build_global_index.py
     Entries come from the actual contents of mechanics/, scenes/, and assets/.
     To change an entry's description, dimension, or feature area, edit its companion .md. -->
"""


def render_feature(dim, feature, entries):
    """Render one feature file, or return None when there is nothing to list.

    Returning None means the file is not created at all. An index of empty stubs is just a
    different kind of noise — a feature file appears the first time something classifies into it.
    """
    if not entries:
        return None
    out = [HEADER_NOTE, '# %s (%s)' % (title_case(feature), dim), '']
    out += ['Scripts, scenes, and assets available for this feature area. Every path is '
            'relative to this file.', '']
    here = os.path.join(INDEX_DIR, dim)
    for name in sorted(entries):
        data = entries[name]
        out.append('### %s' % name)
        if data['desc']:
            out.append('> %s' % data['desc'])
        out.append('')
        out.append('- **Files:**')
        for kind, filename, abspath in sorted(set(data['files']), key=lambda f: (f[0], f[1])):
            rel = os.path.relpath(abspath, here).replace(os.sep, '/')
            out.append('  - [%s] [**%s**](%s)' % (kind, filename, rel))
        out.append('')
    return '\n'.join(out)


def render_readme(tree, total):
    out = [HEADER_NOTE, '# Global Index — Master Directory', '',
           'A relational routing table over the shared libraries, built for agent token '
           'efficiency. Instead of scanning `mechanics/`, `scenes/`, and `assets/` blind, an '
           'agent comes here first, picks the feature file matching what it is about to build, '
           'and gets the exact files plus their companion docs.', '',
           '**Always start here.** Routing through the dimension-specific files (2D / 3D / '
           'Agnostic) is what stops an agent reaching for a `Node3D` mechanic in a 2D game.', '']

    if total == 0:
        out += ['---', '',
                '## Status: empty',
                '',
                'The shared libraries in this checkout contain no entries yet, so there are no '
                'feature files to route to. That is expected for a fresh clone — the libraries '
                'are populated from your own projects, not shipped pre-filled.',
                '',
                'An agent that reaches this page should note the libraries are empty and proceed '
                'to build from scratch, rather than spending further calls looking for something '
                'to reuse.',
                '',
                'To add the first entry: build the mechanic in a game, then run the '
                '`HARVEST-REPO.md` protocol from that project. It copies the files here, strips '
                'the game-specific coupling, writes the companion `.md`, and reruns this index.',
                '',
                'Historical note: a previous version of this index listed ~1,200 entries pointing '
                'at two asset packs (`effect-blocks`, `poly-blocks`) that are not part of this '
                'distribution. Those hand-written descriptions are preserved in '
                '[`_ARCHIVED-ENTRY-NOTES.md`](./_ARCHIVED-ENTRY-NOTES.md) as a wishlist.',
                '']
    else:
        out += ['---', '', '## Status', '',
                '%d entr%s across the shared libraries.'
                % (total, 'y' if total == 1 else 'ies'), '']

    out += ['---', '',
            '## Library layout', '',
            '| Library | Contents |',
            '| :--- | :--- |',
            '| `../mechanics/` | Reusable `.gd` scripts by category, each with a companion `.md`. |',
            '| `../scenes/` | Reusable `.tscn` / `.tres` structures. |',
            '| `../assets/` | Raw assets: `models/` (with `building_pieces/`, `characters/`, '
            '`environment_assets/`, `props/` beneath it), `music/`, `sfx/`, `vfx/`. |',
            '']

    for dim in DIMENSIONS:
        populated = [f for f in FEATURE_AREAS if tree[dim][f]]
        if not populated:
            continue
        out += ['---', '', '## %s' % dim, '']
        for feature in populated:
            count = len(tree[dim][feature])
            out.append('- [%s](./%s/%s.md) — %d entr%s'
                       % (title_case(feature), dim, feature, count,
                          'y' if count == 1 else 'ies'))
        out.append('')

    out += ['---', '', '## Feature taxonomy', '',
            'Every entry lands in one of these feature areas, under one of the three dimensions '
            '(2D / 3D / Agnostic). A feature file is created the first time something classifies '
            'into it, so the sections above list only what exists right now.', '',
            '`' + '`, `'.join(FEATURE_AREAS) + '`', '',
            'To steer where an entry lands, put `<!-- index: vfx_explosions -->` and/or '
            '`<!-- dimension: 3D -->` in its companion `.md`. Otherwise the category folder and '
            'the code itself decide.', '']
    return '\n'.join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--dry-run', action='store_true', help='report without writing')
    parser.add_argument('--check', action='store_true',
                        help='exit 1 if the index on disk is out of date')
    args = parser.parse_args()

    tree, total = collect()
    planned = {}
    for dim in DIMENSIONS:
        for feature in FEATURE_AREAS:
            body = render_feature(dim, feature, tree[dim][feature])
            if body is not None:
                planned[os.path.join(INDEX_DIR, dim, feature + '.md')] = body
    planned[os.path.join(INDEX_DIR, 'README.md')] = render_readme(tree, total)

    stale = [p for p, body in planned.items()
             if not os.path.exists(p) or read_text(p) != body]

    print("Indexed %d entr%s from the shared libraries."
          % (total, 'y' if total == 1 else 'ies'))

    if args.check:
        if stale:
            print("OUT OF DATE: %d file(s) differ. Run build_global_index.py." % len(stale))
            for p in sorted(stale)[:10]:
                print("  " + os.path.relpath(p, ROOT_DIR))
            return 1
        print("Index is up to date.")
        return 0

    if args.dry_run:
        print("DRY RUN - %d file(s) would change." % len(stale))
        for p in sorted(stale):
            print("  " + os.path.relpath(p, ROOT_DIR))
        return 0

    # Remove feature files that are no longer part of the taxonomy.
    for dim in DIMENSIONS:
        dim_dir = os.path.join(INDEX_DIR, dim)
        if os.path.isdir(dim_dir):
            for name in sorted(os.listdir(dim_dir)):
                if name.endswith('.md') and os.path.join(dim_dir, name) not in planned:
                    os.remove(os.path.join(dim_dir, name))
                    print("  Removed obsolete: %s/%s" % (dim, name))

    written = 0
    for path, body in sorted(planned.items()):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path) or read_text(path) != body:
            with open(path, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(body)
            written += 1
    print("Wrote %d file(s); %d already current." % (written, len(planned) - written))
    return 0


if __name__ == '__main__':
    sys.exit(main())
