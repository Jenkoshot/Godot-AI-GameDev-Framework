#!/usr/bin/env python3
"""Push only the *tier-specific* governance files out to every game project.

Narrower than sync_templates.py: it touches the files under
`docs/templates/tiers/<tier>/` and nothing else. Use this after a tier upgrade, or when you have
changed a tier's ARCHITECT/EXECUTOR/SOLO-AGENT rules and do not want the common templates
re-copied.

Usage:
    python framework_tools/sync_tiers.py                 # sync all projects
    python framework_tools/sync_tiers.py --dry-run       # show what would change
    python framework_tools/sync_tiers.py --project Foo   # one project only

Like sync_templates.py, this never overwrites a populated seed file
(`architecture_decisions.md`, `tweak_guide.md`) and never touches `DOCTRINE.md` or
`PROJECT-PROFILE.md`.
"""
import argparse
import os
import shutil
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS_DIR = os.path.join(ROOT_DIR, 'Projects')
TIERS_DIR = os.path.join(ROOT_DIR, 'docs', 'templates', 'tiers')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_templates import (  # noqa: E402
    SEED_ONLY, SKIP_DIRS, USER_OWNED, get_default_dest, get_project_tier, same_content,
)


def sync_project(project_path, dry_run):
    tier = get_project_tier(project_path)
    print("\nSyncing tier docs for: %s (tier: %s)" % (os.path.basename(project_path), tier))

    tier_path = os.path.join(TIERS_DIR, tier)
    if not os.path.isdir(tier_path):
        print("  ! No template directory for tier '%s' - skipping." % tier)
        return

    templates = []
    for root, dirs, names in os.walk(tier_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in sorted(names):
            if name not in USER_OWNED:
                templates.append(os.path.join(root, name))

    created = updated = unchanged = preserved = 0
    for template in templates:
        filename = os.path.basename(template)
        dest = get_default_dest(filename, project_path, tier)

        if filename in SEED_ONLY and os.path.exists(dest):
            preserved += 1
            print("  Preserved (seed file already populated): %s"
                  % os.path.relpath(dest, project_path))
            continue

        exists = os.path.exists(dest)
        if exists and same_content(template, dest):
            unchanged += 1
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
        if exists:
            updated += 1
        else:
            created += 1

    print("  -> %d created, %d updated, %d unchanged, %d seed file(s) preserved"
          % (created, updated, unchanged, preserved))


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--dry-run', action='store_true',
                        help='show what would change without writing anything')
    parser.add_argument('--project', metavar='NAME',
                        help='sync only this project directory under Projects/')
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
            print("\nSkipping %s (no project.godot - not a Godot project)." % name)
            continue
        sync_project(project_path, args.dry_run)
        synced += 1

    print("\nTier sync complete. %d project(s) processed." % synced)
    return 0


if __name__ == '__main__':
    sys.exit(main())
