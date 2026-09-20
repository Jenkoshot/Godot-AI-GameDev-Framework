<!-- GENERATED FILE - do not edit by hand.
     Regenerate with: python framework_tools/build_global_index.py
     Entries come from the actual contents of mechanics/, scenes/, and assets/.
     To change an entry's description, dimension, or feature area, edit its companion .md. -->

# Global Index — Master Directory

A relational routing table over the shared libraries, built for agent token efficiency. Instead of scanning `mechanics/`, `scenes/`, and `assets/` blind, an agent comes here first, picks the feature file matching what it is about to build, and gets the exact files plus their companion docs.

**Always start here.** Routing through the dimension-specific files (2D / 3D / Agnostic) is what stops an agent reaching for a `Node3D` mechanic in a 2D game.

---

## Status: empty

The shared libraries in this checkout contain no entries yet, so there are no feature files to route to. That is expected for a fresh clone — the libraries are populated from your own projects, not shipped pre-filled.

An agent that reaches this page should note the libraries are empty and proceed to build from scratch, rather than spending further calls looking for something to reuse.

To add the first entry: build the mechanic in a game, then run the `HARVEST-REPO.md` protocol from that project. It copies the files here, strips the game-specific coupling, writes the companion `.md`, and reruns this index.

Historical note: a previous version of this index listed ~1,200 entries pointing at two asset packs (`effect-blocks`, `poly-blocks`) that are not part of this distribution. Those hand-written descriptions are preserved in [`_ARCHIVED-ENTRY-NOTES.md`](./_ARCHIVED-ENTRY-NOTES.md) as a wishlist.

---

## Library layout

| Library | Contents |
| :--- | :--- |
| `../mechanics/` | Reusable `.gd` scripts by category, each with a companion `.md`. |
| `../scenes/` | Reusable `.tscn` / `.tres` structures. |
| `../assets/` | Raw assets: `models/` (with `building_pieces/`, `characters/`, `environment_assets/`, `props/` beneath it), `music/`, `sfx/`, `vfx/`. |

---

## Feature taxonomy

Every entry lands in one of these feature areas, under one of the three dimensions (2D / 3D / Agnostic). A feature file is created the first time something classifies into it, so the sections above list only what exists right now.

`camera_systems`, `combat_logic`, `combat_loot`, `combat_projectiles`, `combat_stats_and_damage`, `combat_weapons`, `environment_general`, `environment_rocks_and_cliffs`, `environment_space`, `environment_vegetation`, `environment_water`, `minigames_and_rules`, `movement_flight`, `movement_general`, `movement_tethering`, `procgen_general`, `procgen_layouts`, `procgen_scatter_tools`, `procgen_spawning`, `shaders`, `ui_components`, `ui_feedback_and_juice`, `ui_hud`, `ui_transitions`, `vfx_decals`, `vfx_energy`, `vfx_explosions`, `vfx_fire`, `vfx_general`, `vfx_impacts`, `vfx_liquid`, `vfx_smoke`

To steer where an entry lands, put `<!-- index: vfx_explosions -->` and/or `<!-- dimension: 3D -->` in its companion `.md`. Otherwise the category folder and the code itself decide.
