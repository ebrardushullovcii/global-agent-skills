# Electron inspection

Use the installed Playwright package and the repository's Electron entrypoint. Resolve packages from that workspace rather than installing another copy. Execute through an available Node execution tool or a temporary Node script; this workflow does not depend on the removed `js_repl` feature.

Follow the repository's isolation rules. For an app with personal data, launch an owned instance with a temporary user-data directory and synthetic fixtures. Do not attach to the user's profile by default. Confirm how the app selects its data directory before launching; do not assume a generic flag overrides app-specific storage.

Playwright's `_electron.launch({ args, cwd, env })` creates an owned application instance. Use `electronApp.windows()` or `firstWindow()` and verify the title/URL and loaded contents to select the real application window; a first window may be a splash screen. Use that window's normal input APIs for interaction and `screenshot()` for evidence. Do not open a scratch page with `electronApp.context().newPage()`; Electron does not reliably support it.

After a main-process, preload or startup change, close the owned instance with `electronApp.close()`, rebuild when required, and relaunch with the same isolated data configuration. Renderer-only changes can use the selected window's `reload()` when the running build supports it.

For high-DPI displays, screenshots can be in device pixels even with `scale: "css"`. Normalize to the window's content dimensions only when coordinate-based follow-up requires CSS pixels; retain original resolution for pixel-level rendering defects. If using `BrowserWindow.capturePage()` for this, select the BrowserWindow corresponding to the inspected page instead of assuming the first BrowserWindow is the app.

Keep the session alive through the relevant checks and close the owned instance in cleanup, including after errors. A lost execution session is not proof the Electron process exited.
