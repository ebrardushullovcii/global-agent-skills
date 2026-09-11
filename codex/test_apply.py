import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import tomllib

SCRIPT = Path(__file__).with_name('apply.py')
spec = importlib.util.spec_from_file_location('codex_overrides', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ApplyTests(unittest.TestCase):
    def test_preserves_unrelated_settings_and_disables_duplicate_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            remote = home / 'plugins/cache/openai-curated-remote/stripe/7/skills/stripe-directory/SKILL.md'
            remote.parent.mkdir(parents=True)
            remote.write_text('fixture')
            original = '''model = "keep-model"
[desktop]
external-agent-import-sync-enabled = true
appearanceTheme = "dark"
[plugins."posthog@claude-plugins-official"]
enabled = false
[plugins."github@openai-curated"]
enabled = true
[[skills.config]]
path = "/keep/skill"
enabled = false
[mcp_servers.node_repl]
command = "/keep/browser"
'''
            result = module.settings(original, home)
            data = tomllib.loads(result)
            self.assertEqual(data['model'], 'keep-model')
            self.assertEqual(data['desktop']['appearanceTheme'], 'dark')
            self.assertFalse(data['desktop']['external-agent-import-sync-enabled'])
            self.assertEqual(data['mcp_servers']['node_repl']['command'], '/keep/browser')
            self.assertFalse(data['plugins']['posthog@claude-plugins-official']['enabled'])
            self.assertNotIn('github@openai-curated', data['plugins'])
            for name in module.IMPORTED_DUPLICATES:
                self.assertFalse(data['plugins'][name + '@claude-plugins-official']['enabled'])
            self.assertEqual(data['skills']['config'], [
                {'path': '/keep/skill', 'enabled': False},
                {'path': str(remote), 'enabled': False},
            ])
            self.assertEqual(module.settings(result, home), result)

    def test_apply_preserves_helpers_and_backups_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            home = root / 'codex'
            home.mkdir()
            (home / 'config.toml').write_text('model = "keep-model"\n')
            claude = root / 'claude'
            claude.mkdir()
            (claude / 'settings.json').write_text('{"unchanged": true}')
            for name in ('playwright', 'playwright-interactive', 'security-best-practices', 'speech', 'transcribe'):
                skill = home / 'skills' / name
                skill.mkdir(parents=True)
                (skill / 'SKILL.md').write_text('original')
                (skill / 'helper').write_text('keep helper')
            command = [sys.executable, str(SCRIPT), '--codex-home', str(home), '--apply']
            subprocess.run(command, check=True, capture_output=True)
            backups = list((home / 'backups').iterdir())
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / 'skills/speech/SKILL.md').read_text(), 'original')
            subprocess.run(command, check=True, capture_output=True)
            self.assertEqual(list((home / 'backups').iterdir()), backups)
            self.assertEqual((home / 'skills/speech/helper').read_text(), 'keep helper')
            self.assertEqual((claude / 'settings.json').read_text(), '{"unchanged": true}')


if __name__ == '__main__':
    unittest.main()
