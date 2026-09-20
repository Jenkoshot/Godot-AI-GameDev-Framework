# ModelKit Workspace Instructions

> **Applies to any AI agent working in `model-generation/`** — Claude Code, ChatGPT Codex,
> Gemini/Antigravity, or anything else. The filename is `AGENTS.md` because that is what Codex
> loads automatically; if your agent looks for `CLAUDE.md` or `GEMINI.md`, create a one-line
> pointer file beside this one that tells it to read this document.

You are an AI assistant specialized in generating and modifying 3D models using `antics-modelkit`. **Before building any asset**, you MUST read the kit's own comprehensive guide:

```
node_modules/antics-modelkit/AGENTS.md
```

That 52KB file documents every verb, every trap, and every rule learned from shipped failures. This file (AGENTS.md) is the WORKFLOW and ROUTING layer on top of it. The kit's guide is the TECHNIQUE layer underneath. Read both, build from both.

---

## Phase 0: Thinking Path

**Run through this decision tree BEFORE writing any code.** Present your answers to the user as a brief summary and wait for confirmation.

### Step 1 — What Am I Making?

Identify the asset type from the user's request:

| Type | Examples | Route |
|---|---|---|
| **Static prop** | Crate, barrel, lamp, table, bench | → Section 3 (Recipe Fundamentals) |
| **Static structure** | Wall, fence, pier, bridge, building | → Section 3 (Recipe Fundamentals) |
| **Plant / terrain** | Tree, bush, grass, rock, ground | → Section 3 (Recipe Fundamentals) |
| **Vehicle / machine** | Car, boat, plane, clock mechanism | → Section 3 + declare `front` and `sides` |
| **Creature / character** | Person, animal, monster, NPC | → Section 7 (Creature Pipeline) |

### Step 2 — What Game Is This For?

Assets are grouped by the project they belong to. Each group gets a folder in this workspace and
one default palette, so everything built for a game shares a colour set and material response.

- **If the user names a game**, use its folder. If that game has a `markdowns4AI/DOCTRINE.md` in
  `../Projects/<Game>/`, read its "Art & Audio Taste" section — that is the authoritative style
  constraint and it beats any default recorded here.
- **If the user does not name a game**, ask. Never guess: a prop built to the wrong palette has
  to be rebuilt, not recoloured.
- **For cross-project assets**, use `general/` and ask which palette to target.

Run `npx modelkit palettes` to list the available palettes if the user is unsure.

Record the mapping as you establish it, so later sessions do not re-ask:

| Game folder | Default palette | Notes |
|---|---|---|
| `general` | *ask* | Cross-project assets |

### Step 3 — What Category?

Pick one from the kit's category table:

| Category | What it means | Size reference |
|---|---|---|
| `prop` | Something a character could pick up, sit on, or stand beside | `PROPORTIONS.prop` |
| `plant` | Anything grown — bush, tree, flower | `PROPORTIONS.prop` (bush) or taller |
| `character` | The reference everything else is sized against | `PROPORTIONS.character` |
| `structure` | Built, but not a building: pier, bridge, wall, fence | Varies |
| `building` | Has an interior and storeys | `PROPORTIONS.building` |
| `vehicle` | Moves under its own power | Varies |
| `terrain` | Ground, water, the world | Varies |

### Step 4 — Does It Need Texture?

Textures are **opt-in**. Default is flat colour from the palette. Use procedural textures when:
- The surface is large and flat (walls, floors, roofs) — flat colour returns one value and looks like a sticker
- The material identity depends on surface detail (wood grain, stone joints, fabric weave)
- The user explicitly asks for textured surfaces

Available generators: `plank`, `stone`, `plaster`, `grain`, `polished`, `tile`, `panel`, `ribbed`, `fur`, `weave`

For small props, **prefer `mottle()` over textures** — it breaks up flat colour at zero texture cost.

### Step 5 — Present the Plan

Summarize to the user:
- **Asset**: what you'll build
- **Category**: which one and why
- **Palette**: which one (from game default or user choice)
- **Style**: flat colour, mottled, or textured (and which generators)
- **Complexity**: simple (one function) or compound (multiple sub-functions)
- **Route**: static recipe vs creature pipeline

**Wait for user approval before writing code.**

---

## Section 1: Environment & MCP Health Check

Before any work, verify the environment:

1. **ModelKit Check:** Confirm `antics-modelkit` is installed (check `package.json`).
   - If not installed: `npm init -y`, `npm i antics-modelkit three`, `npm i -D @gltf-transform/cli`. Ensure `build.js` and `npm run build` exist.
2. **Godot MCP Check:** Confirm `mcp__godot__*` tools are available.
   - Call `get_godot_version` to prove the server is live.
   - **Use MCP tools** for `.tscn`/`.tres` operations. Do NOT use raw shell commands for Godot resource operations.
3. **Read the kit guide:** `node_modules/antics-modelkit/AGENTS.md` — read it end to end on your first build. On subsequent builds, re-read the relevant sections.

---

## Section 2: The Kit's Vocabulary

**Always use the kit's own verbs. Do NOT reach for raw `THREE.BoxGeometry` or `THREE.SphereGeometry`.**

Import from the root (`antics-modelkit`) for the modelling vocabulary:

### Surfaces — the shapes of things
| Verb | What it does |
|---|---|
| `sweep(rings)` | Rings along a polyline — tubes, columns, organic curves |
| `ribbon(spine, section)` | Flat sections past ~5:1 aspect ratio — roads, planks, wings |
| `lathe(profile)` | Surface of revolution — bowls, vases, wheels. **Derives winding automatically** |
| `patch(nu, nv, fn)` | Parametric grid — terrain, curved panels, hulls |
| `extrude(shape, opts)` | An outline with optional holes — walls, facades, frames |
| `contour(field, res)` | Iso-surface of a scalar field — organic blobs, terrain |

### Primitives
| Verb | What it does |
|---|---|
| `box(w, h, d)` | Box standing on y=0 |
| `rect(w, h, x, y)` | 2D rectangle for extrude outlines and holes |
| `spine(points, steps)` | Smooth polyline from control points |
| `limb(len, r)` | A tapered cylinder for creature limbs |

### Combining
| Verb | What it does |
|---|---|
| `merge(geos)` | Concatenate geometries into one buffer. Does NOT fuse. |
| `weld(geo)` | Merge coincident vertices. **Do this before any topological operation.** |
| `remesh(parts, opts)` | Voxel fusion — for chunky overlapping lumps. Feature:extent must be >1:40. |
| `subdivide(geo, n)` | Loop subdivision |
| `facet(geo)` | Flat-shade — split shared vertices so each face has its own normal |
| `mirror(geo, axis)` | Reflect and weld the seam. Un-reverses flipped winding. |

### Deforming
| Verb | What it does |
|---|---|
| `twist(geo, rate)` | Twist about Y. Rate is radians per unit height. |
| `taper(geo, k, height)` | Scale toward k at height, clamp past it. k=0 gives a true point. |
| `bend(geo, curvature)` | Curve about Y in the XY plane. Radius = 1/curvature. |
| `deform(geo, fn)` | Arbitrary vertex map |
| `sit(geo)` | Drop geometry to sit on y=0. **Refuses a bound skin.** |

### Placing
| Verb | What it does |
|---|---|
| `array(geo, positions)` | Instance a geometry at multiple positions |
| `alongPath(points, n)` | Generate n evenly-spaced positions WITH FACING along a path |
| `grid(nx, nz, sx, sz)` | Regular grid of positions |
| `dice(geo, size)` | Subdivide faces to roughly `size` — for `mottle()` on sparse meshes |

### Colour
| Verb | What it does |
|---|---|
| `tint(geo, color)` | Set vertex colour on entire geometry |
| `paint(geo, fn)` | Per-vertex colour from a function of position |
| `mottle(geo, colors, scale)` | Per-face colour variation. **Pass `{ dice: false }` on dense meshes.** |
| `tileOver(geo, n)` | Set texture repeat. Apply AFTER scaling. |

### Rigs
| Verb | What it does |
|---|---|
| `stitch(rings)` | Close a ring set from `sweep` into a watertight mesh with caps |
| `rig(parts, joints)` | Simple rig for mechanical motion |
| `rigTree(spec, parent, geo)` | Full skeleton tree for characters |
| `weightsFor(geo, bones)` | Automatic bone weights |
| `bindTo(geo, joint)` | Rigid attachment to one bone — hat, sword, hoof |
| `socketOn(body, from, dir)` | Cast against body surface — where a limb or feature exits |
| `collar(radius, depth, proud)` | The geometry that covers a socket joint |

### Subpath Modules

| Import path | When to use |
|---|---|
| `antics-modelkit/style` | **Always.** Palette and proportions. |
| `antics-modelkit/texture` | When a surface needs grain, joints, or weave |
| `antics-modelkit/creature` | For rigged characters and animals |
| `antics-modelkit/anim` | For animated rigs and gait cycles |
| `antics-modelkit/basis` | For camera math, orientation, signed directions |
| `antics-modelkit/validate` | For checking geometry and assembly |
| `antics-modelkit/motion` | For checking mechanical motion and clearances |

---

## Section 3: Recipe Architecture Rules

### The Two Rules That Fixed More Bugs Than Every Check

**1. DERIVE THE NUMBER FROM THE THING IT HAS TO MEET.**

Never type a coordinate that describes a relationship. If a fruit hangs below a canopy, sample the canopy's underside. If a gable caps a wall, read the wall's top edge. Two numbers that describe how two things relate agree the day you write them and drift the moment either side moves.

```js
// BAD — typed coordinates that will drift
const roofY = 3.2;
const gutterY = 3.15;

// GOOD — derived from the thing it meets
const roofY = wallHeight;
const gutterY = roofY - gutterDrop;
```

**2. MEASURE SIGNS, NEVER PICK THEM.**

A mirrored basis still turns, banks, walks, collides — it is a perfect reflection of a working thing. Use `basis.js` rather than deriving directions. The kit's convention: **+Z forward, +Y up, right is −X**.

### The Traps That Cost The Most Time

1. **A reversed winding is INVISIBLE, not wrong-looking.** Backface culling makes the surface vanish. Use `checkGeometry()`. Use `--winding` preview.
2. **`weld()` before anything topological.** `ExtrudeGeometry` returns non-indexed geometry — a pile of loose triangles.
3. **Primitives don't share an origin.** `box` stands on y=0; a swept shape wraps around its spine. Use `sit()`.
4. **`Math.exp(-(x / w) ** 2)` IS A SYNTAX ERROR.** JS refuses unary minus before `**`. Write `Math.exp(-((x / w) ** 2))`.
5. **Every operation returns a CLONE.** Mutating the input afterwards changes something nobody is holding.
6. **The commonest error is a coefficient against the wrong quantity.** Name the quantity in the expression. Render after each one.
7. **The Lampshade / Bowl Problem (Thickness).** Open surfaces (lampshades, bowls, open boxes, tents) built from a single 2D line will be INVISIBLE from the inside due to backface culling. If the player can see inside an object, its geometry MUST have thickness (e.g., draw a U-shaped profile for `lathe` rather than a single line) so it forms a closed solid shell. Always use `--turn` to check for gaping holes.
8. **The Z-Fighting Problem (Flickering).** Two flat surfaces perfectly flush with each other (e.g., a metal strap on a crate, a poster on a wall) will violently flicker in-engine. Always push surface details *proud* by a tiny margin (e.g., `.translate(0, 0, 0.02)`) so the engine can depth-sort them.
9. **The Pivot / Origin Problem.** Godot places objects by their local origin. If you build a door, the origin must be at the hinge. If you build a floor prop, the origin must be at the bottom center. Shift geometry relative to the origin early using `.translate()`, or use `sit(geo)` to snap the bounding box bottom to `y=0`.
10. **Emissive Clipping (The White Dot).** Choosing a "bright" color for a glowing material will clip to pure white under Godot's tone mapper, destroying the hue. Use the palette's calibrated `Lit` roles (e.g., `pal.glassLit.base`) rather than guessing bright hex values.
11. **The "Voxel Blob" (Misusing `remesh`).** `remesh()` is a voxel fusion operation with a ~1:40 resolution limit. If you use it to attach a tiny detail to a massive object, the detail will melt or vanish. Just use `merge()` and let the shapes intersect.
12. **The Polycount Nuke (`mottle` dicing).** `mottle()` automatically subdivides (dices) faces to add color noise. If you apply it to an already dense or curved mesh (like a character or lathe), it will exponentially explode the triangle count. Always pass `{ dice: false }` to `mottle()` on dense geometry.
13. **Stretched Textures (Order of Operations).** Textures and UVs are mapped using real-world arc length. If you scale or stretch geometry *after* applying a texture, the texture stretches with it. Build the final shape and size FIRST, then apply textures/colors LAST.
14. **The Hovering Gap (Floating Point Over-engineering).** Do not try to make two shapes perfectly touch (e.g., leg at `0.8`, table bottom at `0.8`). Floating-point errors will leave hairline gaps of light. Intentionally intersect solids by a small margin (e.g., push the leg to `0.85`). Overlap is safe; gaps are bugs.

---

## Section 4: The Style System

### Palettes — Pick Names, Not Numbers

```js
import { palette, PROPORTIONS } from "antics-modelkit/style";

const pal = palette("industrial");
// Use: pal.timber.base, pal.timber.shade, pal.timber.deep, pal.timber.light
// Use: pal.metal.base, pal.brick.shade, pal.glass.deep, pal.glassLit.base
```

- **ONE palette per file.** That is the point — every asset shares a colour set and material response.
- **`base`** on lit faces, **`shade`** on faces turned away, **`deep`** in recesses, **`light`** on highlights.
- The shade/deep/light variants are DERIVED from the base — guaranteed contrast.
- Need a colour the set lacks? Use `extendPalette()`.
- **Never hardcode hex values.** If you must use a specific colour, put it in one `const` block at the top of the file.

### Proportions — Read Before Typing a Dimension

```js
const C = PROPORTIONS.character.height;   // 1.0 — the reference
const P = PROPORTIONS.prop;               // P.crate, P.lamppost, etc.
const B = PROPORTIONS.building;           // B.storey, B.doorWidth, B.doorHeight, etc.
```

Everything is sized against a character. A prop that reads correctly beside a person reads correctly anywhere.

### Textures — Opt-In Only

When you need them, use the `surface()` + generator pattern:

```js
import { surface, plaster } from "antics-modelkit/texture";

{ geometry: wall, name: "walls",
  texture: surface(plaster(2.2), [pal.plaster.deep, pal.tile.base, pal.plaster.base], { key: "plaster" }) }
```

Colours come from palette roles, so a texture cannot drift off-palette.

---

## Section 5: Return Format

Every model function must return one of two shapes:

### Bare Array (simple assets, no style checks)
```js
export function myProp() {
  return [
    { geometry: geo1, color: 0xaabbcc, name: "body" },
    { geometry: geo2, color: 0x112233, name: "detail" },
  ];
}
```

### Declared Object (recommended — opts into extent and colour checks)
```js
export function myProp() {
  return {
    category: "prop",           // REQUIRED — picks size reference and legibility floors
    palette: "industrial",      // which palette — checked against actual colours used
    parts: [
      { geometry: geo1, color: pal.timber.base, name: "body" },
      { geometry: geo2, color: pal.metal.shade, name: "strap" },
    ],
    // Optional declarations:
    front: "partName",          // for vehicles — which part faces forward
    sides: "own" | "viewer" | "none",  // how left/right part names are interpreted
    anchors: { seat: [x, y, z] },      // named points the runtime can query
    loose: true,                        // suppress floating-part warnings (e.g., scatter of shells)
    stands: true,                       // asset is meant to stand on y=0
  };
}
```

**Always prefer the declared object.** It is the only way the build gate can check your work.

---

## Section 6: Build, Preview & Validation

### The Loop
```
write recipe  →  preview it  →  fix what you see  →  build (gate + .glb)  →  test in Godot
```

### Preview Commands
```sh
npx modelkit preview <name> --models=<file>           # look at it — auto-framed
npx modelkit preview <name> --models=<file> --turn    # four quarter turns — catches missing faces
npx modelkit preview <name> --models=<file> --winding # back-faces in magenta — catches reversed winding
npx modelkit preview <name> --models=<file> --normals # shaded by normal direction
npx modelkit preview <name> --models=<file> --readable --px=44  # legibility at play size
npx modelkit preview <name> --models=<file> --elev=0  # eye level — USE ON ANYTHING WITH A FACE
npx modelkit preview <name> --models=<file> --walk=6  # six frames of motion — USE ON ANYTHING RIGGED
```

### Build Command
```sh
npx modelkit build <file>       # gate every asset, write dist/*.glb, write contact sheets
```

### What The Gate Does

| Level | What it catches |
|---|---|
| **Hard fail** | NaN positions. Inverted winding on closed shells. |
| **Fixed silently** | Degenerate triangles (stripped automatically). |
| **Reported only** | Palette membership, category extent, play-size legibility, floating parts, unknown category, vehicle without `front`. |

### After Building — Dequantize for Godot

```sh
npm run build          # every recipe
npm run build -- --only=rusty_sword   # just one
node build.js --list   # show discovered recipes without building
```

`build.js` discovers every `*.mjs` in this folder (and one level down inside model folders),
runs the kit's gate on each, then **dequantizes** the output with `gltf-transform`. That second
step is not optional — Godot does not read the kit's quantized output correctly. It then copies
each `.glb` into `tester/` for inspection. Pass `--no-tester` to skip that copy.

A recipe with no exports is reported and skipped rather than failing the run.

---

## Section 7: Creature & Character Pipeline

For any rigged character or animal, use the creature system rather than assembling parts manually.

### The Pipeline
```js
import { creature, humanoid, grow, garment } from "antics-modelkit/creature";

// 1. Define the graph
const c = creature(humanoid({ h: 1.0, headHeights: 3.2 }));  // a chibi
console.log(c.measure());  // what animal is this? Check the numbers.

// 2. Grow the body — one closed shell, automatically skinned
const { geometry, skin, report } = grow(c, { resolution: 80 });

// 3. Add clothing as garments on the SAME skeleton
const coat = garment(c, { over: ["Hips", "Spine", "Chest", "Neck"], out: 0.022 });

// 4. Export with shared skin
writeGLB([
  { name: "body", geometry: body.geometry, skin: body.skin },
  { name: "coat", geometry: coat.geometry, skin: coat.skin },  // SAME object
], "figure.glb");
```

### Archetypes
| Archetype | What it is | Key measurements |
|---|---|---|
| `humanoid(opts)` | Biped. Bones are Unity/VRM names. | `headHeights` (7.5 photo, 5-6 stylised, 2-4 chibi) |
| `quadruped(opts)` | Four-legged animal. | `legToDepth` (1.3 typical) |
| `arachnid(opts)` | Many-legged creature. | `legToDepth` (0.2 — body slung between limbs) |

### Garments — Clothing the Figure
- `over` is a list of **BONES** — the garment's cut is the bone list
- Trunk alone = tank top. Add shoulders + upper arms = t-shirt. Add lower arms = long sleeves.
- **Give it a `hem`** or it wraps under and dissolves into the legs
- **One garment per limb** when limbs are close together (boots, trouser legs) — two shells in one garment fuse
- `out` is bounded by what the cloth may touch — too proud and limbs weld together

### Faces and Features
- Use `socketOn(body, headCenter, direction)` to place features on the grown skull surface
- At chibi scale: two eyes + two brows = entire face. Nose and mouth are sub-pixel at play size.
- **Catchlights**: one bright spot near the top of each eye makes it look alive. Worth more than any other feature.

### Key Creature Rules
- **Watch it move.** Stills stop being useful quickly. Use `--walk` preview.
- **`measure()` is the product.** It tells you what you built — read it before rendering.
- **The body is a SUBSTRATE.** Colour blocking and features are what make it a character, not more geometry.

---

## Section 8: Create a New Model Workflow

1. **Run Phase 0** (Thinking Path above) — determine type, game, category, palette, style.
2. **Read the kit guide**: `node_modules/antics-modelkit/AGENTS.md` — or re-read relevant sections.
3. **Check `reference_input/`** for any images the user dropped. Analyze shape, colours, parts.
4. **Clarify requirements** — ask specific questions based on references and the user's prompt.
5. **Present the Phase 0 summary** and **wait for approval**.
6. **Write the recipe** in the appropriate `.mjs` file:
   - Import from `antics-modelkit` (not `three`)
   - Use `palette()` and `PROPORTIONS`
   - Return a `{ parts, category, palette }` declaration
   - Derive every dimension from the thing it has to meet
7. **Preview the model:**
   ```sh
   npx modelkit preview <name> --models=<file> --turn
   ```
   Check the four-quarter contact sheet. Look for missing faces, floating parts, reversed winding.
8. **Build the model:**
   ```sh
   npm run build
   ```
   Read the gate output. Fix any hard failures. Review advisories.
9. **Test in Godot — this is the step that actually catches things:**
   - `build.js` has already copied the `.glb` into `tester/`.
   - Tell the user to open `tester/project.godot` and press Play. It loads every `.glb` in that
     folder: left-drag orbits, right-drag pans, wheel zooms, arrow keys switch models, `F` frames,
     `W` toggles wireframe, `R` reloads from disk after a rebuild.
   - A translucent capsule one character-height tall stands beside the model, on a 1-metre grid.
     **Scale errors are the single most common failure** — check the model against that capsule
     before declaring it done.
   - You cannot judge this yourself. Wait for the user's verdict.
10. **Organize after approval:**
    - Create `<group>/<model_name>/` — group by game, or use `general/` for cross-project assets.
    - Move reference images from `reference_input/` into it.
    - Move the `.glb` and `.mjs` recipe into it. `build.js` keeps that copy up to date on
      subsequent builds.
    - If the asset is broadly reusable, also copy the `.glb` into the framework's shared
      `../assets/models/<category>/` and run `python ../framework_tools/build_global_index.py`.

---

## Section 9: Edit an Existing Model Workflow

1. Identify the existing model folder.
2. Read the recipe `.mjs` file and any reference images.
3. **Re-read the relevant AGENTS.md sections** for the verbs used in the recipe.
4. Modify the recipe as requested.
5. **Preview with `--turn`** to check the change from all angles.
6. Rebuild: `npm run build -- --only=<name>`.
7. The build copies it into `tester/` for you. Ask the user to press `R` in the running
   inspector (or press Play) and give you their verdict on the change.

---

## Directory Architecture

```
model-generation/
├── AGENTS.md                    # This file — workflow and routing
├── models.mjs                   # Default recipe file; ships with one worked example
├── build.js                     # Discover recipes -> gate -> dequantize -> copy to tester/
├── package.json                 # Dependencies (antics-modelkit, three, gltf-transform)
├── reference_input/             # Drop reference images here (gitignored)
├── tester/                      # Godot project that loads every .glb beside it
│   ├── project.godot
│   └── inspector.gd             #   orbit/pan/zoom, model switching, 1-character scale capsule
├── dist/                        # Build output, .glb (gitignored — regenerate with npm run build)
├── general/                     # Cross-project assets
│   └── <model_name>/            #   recipe .mjs + .glb + reference images
└── <your-game>/                 # One folder per game, same shape as general/
```

Anything more than one level deep inside a model folder is ignored by recipe discovery, so keep
`<group>/<model_name>/<model_name>.mjs` as the shape.
