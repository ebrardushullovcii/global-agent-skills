# Codex-only overrides

These changes are separate from the shared `skills/` collection and the root installers. They do not write to Claude settings, Claude plugins, or `~/.agents/skills`.

The overrides replace the obsolete `js_repl` UI-testing setup with current browser routing and focused Electron guidance, make verification proportional to the task, respect existing authorization, and keep inspection artifacts out of repositories by default. Stripe Directory is selected only for an explicit directory request.

`apply.py` preserves unrelated Codex settings. It disables automatic external-agent imports and the imported Figma, Convex, Linear, Slack, Stripe and Sentry plugins in Codex, retaining the separately installed remote versions as the active integrations. The disabled packages remain cached and can be re-enabled deliberately if a unique workflow is needed. It leaves PostHog's project-specific enablement and the separate Sentry CLI plugin alone. It removes obsolete GitHub/Figma `openai-curated` and bundled Sites entries and disables the installed remote Stripe Directory skill in favor of the narrow local one.

Use these settings only when the replacement remote integrations are already installed. The script expects the original Playwright, Playwright Interactive, Security Best Practices, Speech and Transcribe skills to exist; their unchanged helpers, assets and reference files remain installed. Only override files are versioned here, with the original licenses and notices. Stripe Directory is standalone.

Preview and apply:

```sh
python3 codex/apply.py
python3 codex/apply.py --apply
```

The script backs up changed local files before applying and is safe to rerun. Restart Codex after applying so active tasks receive the updated plugin and skill selection. After a managed Stripe plugin update, rerun the script to disable the new version's broad Directory skill as well.

Do not copy the whole local Codex config, authentication files, app state or backups into Git. These portable changes intentionally exclude private machine state. Do not run the shared root installer to apply these Codex-only overrides.
