# Procedural 3D Model Generation

Need a 3D asset and don't want to open Blender? Point an AI agent at this folder.

The agent does not hallucinate binary meshes. It writes a **JavaScript recipe** that constructs
the model mathematically using [`antics-modelkit`](https://www.npmjs.com/package/antics-modelkit).
That matters for iteration: "make the hilt 20% wider" is a parameter change, not a regeneration.

## Setup

```bash
npm install
```

That pulls `antics-modelkit`, `three`, and `@gltf-transform/cli`. It also unpacks the kit's own
52 KB technique guide at `node_modules/antics-modelkit/AGENTS.md` — the agent is required to read
it before writing a recipe, and it is the single most useful file in this workspace.

Optional, for the kit's contact-sheet previews:

```bash
npm i -D playwright && npx playwright install chromium
```

Everything else works without it; builds just skip the rendered sheets.

## The loop

```
write a recipe  →  npm run build  →  look at it in tester/  →  adjust numbers  →  repeat
```

```bash
npm run build                          # build every recipe
npm run build -- --only=rusty_sword    # build one
npm run list                           # show discovered recipes without building
```

`build.js` discovers every `*.mjs` in this folder and one level down inside model folders. For
each it runs the kit's validation gate, **dequantizes** the output (Godot does not read the kit's
quantized `.glb` correctly — this step is not optional), and copies the result into `tester/`.

## Looking at the result

```bash
# open tester/project.godot in Godot and press Play
```

`tester/` is a small Godot 4 project that loads every `.glb` sitting beside it.

| Input | Action |
| :--- | :--- |
| Left-drag | Orbit |
| Right-drag | Pan |
| Wheel, `+` / `-` | Zoom |
| `←` / `→` | Previous / next model |
| `F` | Frame the current model |
| `R` | Reload from disk after a rebuild |
| `G` | Toggle the ground grid |
| `W` | Toggle wireframe |
| `Esc` | Quit |

The translucent capsule beside the model is exactly one character height — the kit's size
reference — standing on a 1-metre grid. **Check every model against it.** Scale is the most
common failure, and an AI cannot see it.

## Writing a recipe

`models.mjs` ships with one worked example. Each exported function is one model:

```js
import { box, sit, mottle } from "antics-modelkit";
import { palette, PROPORTIONS } from "antics-modelkit/style";

const pal = palette("industrial");

export function example_crate() {
  const size = PROPORTIONS.prop.crate;
  return {
    category: "prop",
    palette: "industrial",
    stands: true,
    parts: [
      { geometry: mottle(sit(box(size, size, size)), [pal.timber.base, pal.timber.shade], 0.4),
        name: "body" },
    ],
  };
}
```

Three rules do most of the work:

1. **Size against `PROPORTIONS`, never a typed magic number.** Everything is measured in character
   heights. A crate modelled "about a metre" beside a character modelled "about two" is the
   commonest scale error there is.
2. **Take colours from a palette role** (`pal.timber.base`, `pal.metal.shade`), never a hex
   literal. One palette per file — that is what makes a set of assets look like a set.
3. **Return the declared object form** (`{ category, palette, parts }`) rather than a bare array.
   It is the only form the build gate can actually check.

`AGENTS.md` in this folder has the full vocabulary, the return formats, the creature pipeline, and
a catalogue of the traps that cost the most time — reversed windings being *invisible* rather than
wrong-looking, `weld()` before topological operations, Z-fighting on flush surfaces, origin
placement for Godot pivots, `mottle()` exploding triangle counts on dense meshes.

## Organising output

Once a model is approved, move it into a group folder:

```
general/rusty_sword/
├── rusty_sword.mjs      # the recipe
├── rusty_sword.glb      # the build output
└── reference.png        # whatever you worked from
```

Use one folder per game, or `general/` for cross-project assets. `build.js` keeps the `.glb` in
those folders up to date on later builds.

If the asset is broadly reusable, also copy the `.glb` into the framework's shared library at
`../assets/models/<category>/` and regenerate the index:

```bash
python ../framework_tools/build_global_index.py
```

## Which model to use

Use your strongest available model here. 3D spatial reasoning is the hardest thing in this
repository — far harder than the GDScript work — and the failure mode is a mesh that builds
cleanly, passes the gate, and still looks wrong.

## What is gitignored

`node_modules/`, `dist/`, `reference_input/`, and Godot's `tester/.godot/` cache plus the `.glb`
files copied into `tester/`. Your recipes, `build.js`, `AGENTS.md`, and the tester project itself
are all tracked.
