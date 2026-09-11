#!/usr/bin/env python3
"""Apply the Codex-only overrides without changing shared or Claude files."""
import argparse
import json
from datetime import datetime
from pathlib import Path
import re
import shutil

IMPORTED_DUPLICATES = ('figma', 'convex', 'linear', 'slack', 'stripe', 'sentry')
OLD_PLUGIN_IDS = ('github@openai-curated', 'figma@openai-curated', 'sites@openai-bundled')
HEADER = re.compile(r'(?m)^\[([^\n]+)\][ \t]*$')


def section_span(text, header):
    matches = list(HEADER.finditer(text))
    for i, match in enumerate(matches):
        if match.group(1) == header:
            return match.start(), matches[i + 1].start() if i + 1 < len(matches) else len(text)
    return None


def set_false(text, header, key):
    span = section_span(text, header)
    if span is None:
        return text.rstrip() + f'\n\n[{header}]\n{key} = false\n'
    start, end = span
    block = text[start:end]
    pattern = re.compile(r'(?m)^' + re.escape(key) + r'\s*=.*$')
    if pattern.search(block):
        block = pattern.sub(f'{key} = false', block)
    else:
        block = block.rstrip() + f'\n{key} = false\n\n'
    return text[:start] + block + text[end:]


def settings(text, codex_home):
    text = set_false(text, 'desktop', 'external-agent-import-sync-enabled')
    for name in IMPORTED_DUPLICATES:
        text = set_false(text, f'plugins."{name}@claude-plugins-official"', 'enabled')
    for name in OLD_PLUGIN_IDS:
        span = section_span(text, f'plugins."{name}"')
        if span:
            text = text[:span[0]] + text[span[1]:]
    # Disable the managed broad Directory skill; a narrow local skill replaces it.
    # Resolve installed versions instead of embedding this machine's cache path.
    for path in sorted((codex_home / 'plugins/cache/openai-curated-remote/stripe').glob('*/skills/stripe-directory/SKILL.md')):
        encoded = json.dumps(str(path))
        blocks = list(HEADER.finditer(text))
        found = False
        for i, match in enumerate(blocks):
            if match.group(1) != '[skills.config]':
                continue
            end = blocks[i + 1].start() if i + 1 < len(blocks) else len(text)
            block = text[match.start():end]
            if re.search(r'(?m)^path\s*=\s*' + re.escape(encoded) + r'\s*$', block):
                updated = re.sub(r'(?m)^enabled\s*=.*$', 'enabled = false', block)
                if not re.search(r'(?m)^enabled\s*=', block):
                    updated = block.rstrip() + '\nenabled = false\n\n'
                text = text[:match.start()] + updated + text[end:]
                found = True
                break
        if not found:
            text = text.rstrip() + f'\n\n[[skills.config]]\npath = {encoded}\nenabled = false\n'
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex-home', type=Path, default=Path.home() / '.codex')
    parser.add_argument('--apply', action='store_true', help='Apply changes; default only lists changed files')
    args = parser.parse_args()
    home = args.codex_home.expanduser().resolve()
    config = home / 'config.toml'
    if config.is_symlink():
        parser.error('Refusing to overwrite a symlinked config.toml.')
    if not config.is_file():
        parser.error('An existing Codex config.toml is required.')
    overrides = Path(__file__).resolve().parent / 'skill-overrides'
    changes = {config: settings(config.read_text(), home).encode()}
    for skill in sorted(overrides.iterdir()):
        target = home / 'skills' / skill.name
        if skill.name != 'stripe-directory' and not (target / 'SKILL.md').is_file():
            parser.error(f'Install the original {skill.name} skill before applying its override.')
        for source in skill.rglob('*'):
            if source.is_file():
                dest = target / source.relative_to(skill)
                if dest.is_symlink() or any(p.is_symlink() for p in dest.parents if p != home.parent):
                    parser.error(f'Refusing to overwrite a symlinked destination: {dest}')
                changes[dest] = source.read_bytes()
    changes = {p: data for p, data in changes.items() if not p.exists() or p.read_bytes() != data}
    if not changes:
        print('Codex overrides already applied.')
        return
    if args.apply:
        backup = home / 'backups' / ('guidance-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
        for path, data in changes.items():
            if path.exists():
                copy = backup / path.relative_to(home)
                copy.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, copy)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        print(f'Applied {len(changes)} Codex-only file changes. Backup: {backup}')
    else:
        for path in changes:
            print(path.relative_to(home))
        print('Run with --apply to apply these Codex-only changes.')


if __name__ == '__main__':
    main()
