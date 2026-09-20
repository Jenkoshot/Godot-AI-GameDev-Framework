#!/usr/bin/env node
/**
 * Build every procedural model recipe in this workspace and prepare the output for Godot.
 *
 * Pipeline per recipe:
 *   1. `npx modelkit build <recipe>`  -> runs the kit's validation gate, writes dist/<name>.glb
 *   2. `npx gltf-transform dequantize` -> Godot does not read the kit's quantized output
 *                                         correctly, so this step is NOT optional
 *   3. copy into tester/ so the inspection project can load it
 *
 * Usage:
 *   node build.js                 build every recipe found
 *   node build.js --only=sword    build just the recipe (or output) named "sword"
 *   node build.js --list          list discovered recipes and exit
 *   node build.js --no-tester     skip the copy into tester/
 *
 * Recipes are discovered, not hardcoded: every `*.mjs` in this folder is a recipe, as is every
 * `*.mjs` one level down inside a model folder (e.g. `general/rusty_sword/rusty_sword.mjs`).
 */
'use strict';

const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const DIST = path.join(ROOT, 'dist');
const TESTER = path.join(ROOT, 'tester');

const IGNORED_DIRS = new Set(['node_modules', 'dist', 'tester', '.git', 'reference_input']);

const args = process.argv.slice(2);
const only = (args.find((a) => a.startsWith('--only=')) || '').slice(7) || null;
const listOnly = args.includes('--list');
const skipTester = args.includes('--no-tester');

/** Every `*.mjs` at the root, plus every `*.mjs` one directory down. */
function discoverRecipes() {
  const found = [];
  for (const entry of fs.readdirSync(ROOT, { withFileTypes: true })) {
    if (entry.isFile() && entry.name.endsWith('.mjs')) {
      found.push(entry.name);
      continue;
    }
    if (!entry.isDirectory() || IGNORED_DIRS.has(entry.name) || entry.name.startsWith('.')) {
      continue;
    }
    const sub = path.join(ROOT, entry.name);
    for (const child of fs.readdirSync(sub, { withFileTypes: true })) {
      if (child.isFile() && child.name.endsWith('.mjs')) {
        found.push(path.join(entry.name, child.name));
      } else if (child.isDirectory()) {
        const nested = path.join(sub, child.name);
        for (const leaf of fs.readdirSync(nested, { withFileTypes: true })) {
          if (leaf.isFile() && leaf.name.endsWith('.mjs')) {
            found.push(path.join(entry.name, child.name, leaf.name));
          }
        }
      }
    }
  }
  return found.sort();
}

/** True if the recipe actually exports something for the kit to build. */
function hasExports(relPath) {
  const text = fs.readFileSync(path.join(ROOT, relPath), 'utf8');
  return /^\s*export\s+(function|const|let|default|\{)/m.test(text);
}

/** The model names a recipe exports, so `--only` can match either a file or a model. */
function exportedNames(relPath) {
  const text = fs.readFileSync(path.join(ROOT, relPath), 'utf8');
  const names = [];
  const re = /^\s*export\s+(?:async\s+)?(?:function\s+|const\s+|let\s+)([A-Za-z_$][\w$]*)/gm;
  let m;
  while ((m = re.exec(text)) !== null) names.push(m[1]);
  return names;
}

/** `--only` matches a recipe's filename OR one of the model names it exports. */
function matchesOnly(relPath, wanted) {
  if (path.basename(relPath, '.mjs') === wanted) return true;
  return exportedNames(relPath).includes(wanted);
}

/**
 * Resolve a dependency's CLI entry point so we can run it with Node directly.
 *
 * Going through `npx` is not an option here: on Windows the shims are `.cmd` files, which
 * recent Node refuses to `execFile` without `shell: true`, and `shell: true` concatenates
 * rather than escapes the arguments — and ours include filesystem paths. Reading `bin` out of
 * the package's own manifest avoids both problems and works identically on every platform.
 */
function resolveCli(pkg, binName) {
  // Read the manifest off disk rather than via require.resolve: packages with an "exports"
  // map (antics-modelkit is one) deliberately do not expose "./package.json".
  let dir = ROOT;
  let manifest = null;
  for (;;) {
    const candidate = path.join(dir, 'node_modules', ...pkg.split('/'), 'package.json');
    if (fs.existsSync(candidate)) {
      manifest = candidate;
      break;
    }
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  if (!manifest) {
    throw new Error(`${pkg} is not installed`);
  }
  const { bin } = JSON.parse(fs.readFileSync(manifest, 'utf8'));
  const rel = typeof bin === 'string' ? bin : bin && bin[binName];
  if (!rel) {
    throw new Error(`${pkg} declares no "${binName}" binary`);
  }
  return path.resolve(path.dirname(manifest), rel);
}

function run(pkg, binName, cmdArgs) {
  let cli;
  try {
    cli = resolveCli(pkg, binName);
  } catch (err) {
    throw new Error(
      `Could not find ${binName} (${pkg}). Run "npm install" in model-generation/ first.\n  ${err.message}`
    );
  }
  execFileSync(process.execPath, [cli, ...cmdArgs], { stdio: 'inherit', cwd: ROOT });
}

function main() {
  let recipes = discoverRecipes();

  if (only) {
    recipes = recipes.filter((r) => matchesOnly(r, only));
    if (!recipes.length) {
      const all = discoverRecipes();
      const choices = new Set();
      for (const r of all) {
        choices.add(path.basename(r, '.mjs'));
        for (const n of exportedNames(r)) choices.add(n);
      }
      throw new Error(
        `Nothing named "${only}". Available recipes and models: ` +
          `${[...choices].sort().join(', ') || '(none)'}`
      );
    }
  }

  if (listOnly) {
    if (!recipes.length) {
      console.log('No .mjs recipes found.');
    } else {
      console.log('Discovered recipes:');
      for (const r of recipes) {
        console.log(`  ${r}${hasExports(r) ? '' : '   (no exports - will be skipped)'}`);
      }
    }
    return;
  }

  if (!recipes.length) {
    console.log('No .mjs recipe files found in this workspace.');
    console.log('Write one (start from models.mjs) and run this again.');
    return;
  }

  const buildable = recipes.filter(hasExports);
  for (const skipped of recipes.filter((r) => !buildable.includes(r))) {
    console.log(`Skipping ${skipped} - it exports no model functions yet.`);
  }
  if (!buildable.length) {
    console.log('\nNothing to build: no recipe exports a model function yet.');
    console.log('Add an `export function myProp() { ... }` to models.mjs and run this again.');
    return;
  }

  // Recorded before the build so we can tell this run's output from stale artifacts. Backed off
  // by a second because filesystem mtime resolution is coarser than Date.now() on some systems.
  const startedAt = Date.now() - 1000;

  console.log('Building models with antics-modelkit...');
  for (const recipe of buildable) {
    console.log(`\n-- ${recipe}`);
    run('antics-modelkit', 'modelkit', ['build', recipe]);
  }

  if (!fs.existsSync(DIST)) {
    console.log('\nThe kit produced no dist/ folder - nothing to post-process.');
    return;
  }

  // Only post-process what this run actually produced. dist/ accumulates across builds, so
  // without this a targeted build would re-dequantize every stale artifact beside it.
  let glbs = fs.readdirSync(DIST).filter(
    (f) => f.endsWith('.glb') && fs.statSync(path.join(DIST, f)).mtimeMs >= startedAt
  );
  // If --only named a specific model rather than a recipe file, narrow to it.
  if (only && glbs.some((f) => path.basename(f, '.glb') === only)) {
    glbs = glbs.filter((f) => path.basename(f, '.glb') === only);
  }

  if (!glbs.length) {
    console.log('\nNo .glb files were produced - check the gate output above for hard failures.');
    return;
  }

  if (!skipTester && !fs.existsSync(TESTER)) {
    fs.mkdirSync(TESTER, { recursive: true });
  }

  for (const file of glbs) {
    const filePath = path.join(DIST, file);
    console.log(`\nDequantizing ${file} for Godot compatibility...`);
    run('@gltf-transform/cli', 'gltf-transform', ['dequantize', filePath, filePath]);

    if (!skipTester) {
      fs.copyFileSync(filePath, path.join(TESTER, file));
      console.log(`Copied to tester/${file}`);
    }

    // If a per-model archive folder exists (e.g. general/<name>/), drop a copy there too.
    const name = path.basename(file, '.glb');
    for (const group of fs.readdirSync(ROOT, { withFileTypes: true })) {
      if (!group.isDirectory() || IGNORED_DIRS.has(group.name) || group.name.startsWith('.')) {
        continue;
      }
      const archive = path.join(ROOT, group.name, name);
      if (fs.existsSync(archive) && fs.statSync(archive).isDirectory()) {
        fs.copyFileSync(filePath, path.join(archive, file));
        console.log(`Copied to ${group.name}/${name}/${file}`);
      }
    }
  }

  console.log('\nDone. Your models are ready for Godot.');
  if (!skipTester) {
    console.log('Open tester/project.godot and press Play to inspect them.');
  }
}

try {
  main();
} catch (error) {
  console.error('\nBuild failed:', error.message);
  process.exit(1);
}
