#!/usr/bin/env python3
"""Push the framework's governance templates out to every game project.

Usage:
    python framework_tools/sync_templates.py                 # sync all projects
    python framework_tools/sync_templates.py --dry-run       # show what would change
    python framework_tools/sync_templates.py --project Foo   # one project only
    python framework_tools/sync_templates.py --prune         # also delete misplaced copies

Safety rules this script obeys:

* **Seed files are never overwritten.** `tweak_guide.md` and `architecture_decisions.md` are
  templates for content the project then fills in by hand. They are written only when missing.
  (The previous version of this script copied the blank templates over populated project files on
  every run, destroying the tweak table and the ADR log.)
* **User-owned files are never touched.** `DOCTRINE.md` and `PROJECT-PROFILE.md` are excluded.
* **Nothing is deleted unless you ask.** Misplaced copies of template files are reported by
  default and only removed with `--prune`.
"""
import argparse
import os
import re
import shutil
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECTS_DIR = os.path.join(ROOT_DIR, 'Projects')
TEMPLATES_DIR = os.path.join(ROOT_DIR, 'docs', 'templates')
COMMON_DIR = os.path.join(TEMPLATES_DIR, 'common')
TIERS_DIR = os.path.join(TEMPLATES_DIR, 'tiers')

VALID_TIERS = ('lite', 'standard', 'heavy')

# Project-owned. Never synced, never overwritten.
USER_OWNED = {'DOCTRINE.md', 'PROJECT-PROFILE.md'}

# Templates that seed content the project then edits. Written only if absent.
SEED_ONLY = {'tweak_guide.md', 'architecture_decisions.md'}

# Governance files that belong at the project root, not in markdowns4AI/.
ROOT_LEVEL = {'ARCHITECT.md', 'EXECUTOR.md', 'SOLO-AGENT.md', 'SETUP.md'}

# Directories never walked when looking for misplaced copies.
SKIP_DIRS = {'.git', '.godot', '.import', 'node_modules', 'addons', '.venv', '__pycache__'}


def clean_tier(raw):
    raw = (raw or '').lower()
    for tier in VALID_TIERS:
        if tier in raw:
            return tier
    return 'standard'


def get_project_tier(project_path):
    """Read the tier from PROJECT-PROFILE.md; fall back to ARCHITECT.md, then 'standard'."""
    profile = os.path.join(project_path, 'markdowns4AI', 'PROJECT-PROFILE.md')
    if os.path.exists(profile):
        with open(profile, 'r', encoding='utf-8') as fh:
            match = re.search(r'Current Tier:\s*\**\s*([A-Za-z]+)', fh.read(), re.IGNORECASE)
        if match:
            return clean_tier(match.group(1))

    architect = os.path.join(project_path, 'ARCHITECT.md')
    if os.path.exists(architect):
        with open(architect, 'r', encoding='utf-8') as fh:
            text = fh.read().lower()
        # Read it once, and prefer the most specific match.
        if 'heavy' in text:
            return 'heavy'
        if 'lite' in text:
            return 'lite'
    return 'standard'


def find_file_in_project(project_path, filename):
    found = []
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if filename in files:
            found.append(os.path.join(root, filename))
    return found


def get_default_dest(filename, project_path, tier):
    if filename in ROOT_LEVEL:
        return os.path.join(project_path, filename)
    if filename in ('run_tests.gd', 'test_case.gd'):
        return os.path.join(project_path, 'tests', filename)
    if filename == 'mcp_config.json':
        return os.path.join(project_path, '.agents', filename)
    if filename in SEED_ONLY:
        if tier == 'lite':
            return os.path.join(project_path, filename)
        return os.path.join(project_path, 'project-state', filename)
    return os.path.join(project_path, 'markdowns4AI', filename)


def collect_templates(tier):
    """Every template file that should exist in a project of this tier."""
    files = []
    for name in sorted(os.listdir(TEMPLATES_DIR)):
        path = os.path.join(TEMPLATES_DIR, name)
        if os.path.isfile(path):
            files.append(path)

    for root, dirs, names in os.walk(COMMON_DIR):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in sorted(names):
            if name not in USER_OWNED:
                files.append(os.path.join(root, name))

    tier_path = os.path.join(TIERS_DIR, tier)
    if os.path.isdir(tier_path):
        for root, dirs, names in os.walk(tier_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in sorted(names):
                if name not in USER_OWNED:
                    files.append(os.path.join(root, name))

    # Guard against two templates resolving to the same destination filename.
    by_name = {}
    for path in files:
        name = os.path.basename(path)
        if name in by_name and by_name[name] != path:
            print("  ! WARNING: two templates named %s (%s and %s). Using the latter."
                  % (name, os.path.relpath(by_name[name], ROOT_DIR),
                     os.path.relpath(path, ROOT_DIR)))
        by_name[name] = path
    return [by_name[n] for n in sorted(by_name)]


def same_content(src, dest):
    try:
        with open(src, 'rb') as a, open(dest, 'rb') as b:
            return a.read() == b.read()
    except OSError:
        return False


def sync_project(project_path, dry_run, prune):
    tier = get_project_tier(project_path)
    print("\nSyncing project: %s (tier: %s)" % (os.path.basename(project_path), tier))
    stats = {'created': 0, 'updated': 0, 'unchanged': 0, 'preserved': 0, 'misplaced': 0}

    for template in collect_templates(tier):
        filename = os.path.basename(template)
        dest = get_default_dest(filename, project_path, tier)

        # Report (and optionally remove) copies sitting somewhere other than the canonical path.
        for existing in find_file_in_project(project_path, filename):
            if os.path.normcase(os.path.normpath(existing)) == os.path.normcase(os.path.normpath(dest)):
                continue
            stats['misplaced'] += 1
            rel = os.path.relpath(existing, project_path)
            if prune:
                if dry_run:
                    print("  [dry-run] would delete misplaced: %s" % rel)
                else:
                    try:
                        os.remove(existing)
                        print("  Deleted misplaced: %s" % rel)
                    except OSError as exc:
                        print("  ! Failed to delete %s: %s" % (rel, exc))
            else:
                print("  ? Misplaced copy (left alone; re-run with --prune to remove): %s" % rel)

        # Seed files hold hand-written project content. Write only when missing.
        if filename in SEED_ONLY and os.path.exists(dest):
            stats['preserved'] += 1
            print("  Preserved (seed file already populated): %s"
                  % os.path.relpath(dest, project_path))
            continue

        exists = os.path.exists(dest)
        if exists and same_content(template, dest):
            stats['unchanged'] += 1
            continue

        if dry_run:
            print("  [dry-run] would %s: %s"
                  % ('update' if exists else 'create', os.path.relpath(dest, project_path)))
        else:
            parent = os.path.dirname(dest)
            if parent:
                os.makedirs(parent, exist_ok=True)
            shutil.copy2(template, dest)
            print("  %s: %s" % ('Updated' if exists else 'Created',
                                os.path.relpath(dest, project_path)))
        stats['updated' if exists else 'created'] += 1

    print("  -> %d created, %d updated, %d unchanged, %d seed file(s) preserved, "
          "%d misplaced copy/copies" % (stats['created'], stats['updated'], stats['unchanged'],
                                        stats['preserved'], stats['misplaced']))
    return stats


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--dry-run', action='store_true',
                        help='show what would change without writing anything')
    parser.add_argument('--project', metavar='NAME',
                        help='sync only this project directory under Projects/')
    parser.add_argument('--prune', action='store_true',
                        help='delete copies of template files found outside their canonical path')
    args = parser.parse_args()

    if not os.path.isdir(PROJECTS_DIR):
        print("No Projects/ directory at %s - nothing to sync." % PROJECTS_DIR)
        return 0

    names = sorted(d for d in os.listdir(PROJECTS_DIR)
                   if os.path.isdir(os.path.join(PROJECTS_DIR, d)))
    if args.project:
        if args.project not in names:
            print("No such project: %s\nAvailable: %s"
                  % (args.project, ', '.join(names) or '(none)'))
            return 1
        names = [args.project]

    if args.dry_run:
        print("DRY RUN - no files will be written.")

    synced = 0
    for name in names:
        project_path = os.path.join(PROJECTS_DIR, name)
        if not os.path.exists(os.path.join(project_path, 'project.godot')):
            print("\nSkipping %s (no project.godot — not a Godot project)." % name)
            continue
        sync_project(project_path, args.dry_run, args.prune)
        synced += 1

    print("\nSync complete. %d project(s) processed." % synced)
    if not args.prune:
        print("Note: misplaced copies were reported but not deleted. Re-run with --prune to "
              "remove them.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
