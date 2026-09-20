// models.mjs — the default recipe file for this workspace.
//
// Every exported function is one model. `npm run build` compiles each into dist/<name>.glb,
// dequantizes it for Godot, and copies it into tester/ so you can look at it.
//
// Before writing anything here, read AGENTS.md in this folder (workflow) and
// node_modules/antics-modelkit/AGENTS.md (technique). The second one is the important one.

import { box, merge, sit, mottle } from "antics-modelkit";
import { palette, PROPORTIONS } from "antics-modelkit/style";

const pal = palette("industrial");

/**
 * A worked example: a simple crate, sized against the character reference.
 *
 * It demonstrates the three things every recipe should do:
 *   1. Size against PROPORTIONS rather than typing magic numbers.
 *   2. Take colours from a palette role, never a hardcoded hex value.
 *   3. Return the declared object form ({ category, palette, parts }) so the build gate can
 *      actually check extent, palette membership, and play-size legibility.
 *
 * Delete this once you have recipes of your own — it is here so a fresh clone has something
 * that builds.
 */
export function example_crate() {
  const size = PROPORTIONS.prop.crate ?? 0.6;

  const body = sit(box(size, size, size));
  const lid = sit(box(size * 1.04, size * 0.08, size * 1.04)).translate(0, size, 0);

  return {
    category: "prop",
    palette: "industrial",
    stands: true,
    parts: [
      { geometry: mottle(body, [pal.timber.base, pal.timber.shade], 0.4), name: "body" },
      { geometry: lid, color: pal.timber.deep, name: "lid" },
    ],
  };
}

// Add your own models below.
//
// export function rusty_sword() {
//   ...
//   return { category: "prop", palette: "industrial", parts: [...] };
// }
