---
name: "playwright-interactive"
description: "Inspect and debug a running web or Electron app with reusable sessions. Use for interactive UI verification."
---

# Interactive UI verification

Use the available runtime and the project's existing dependencies. Do not enable the removed `js_repl` feature, change sandbox settings, initialize a package, or install Playwright just to inspect an app.

## Choose the surface

- For web pages, use the installed Browser or Chrome skill and its current documented runtime. Respect an explicitly selected browser and the repository's automation rules.
- For Electron, use the project's existing inspection command when it covers the task. When direct Playwright inspection is appropriate and supported by the project, read [Electron inspection](references/electron.md).
- If the required capability is unavailable, continue independent implementation or checks and explain the specific missing capability. Ask only for information or authorization needed to proceed.

## Verify the requested result

Inspect the running surface affected by the change, exercise the relevant user flow, and check its visible result. Inspect additional states, viewports, controls or failure paths when the change or an observed problem warrants them. A full application audit belongs to a full application audit request.

Use screenshots for visual claims; DOM or layout measurements can help diagnose a problem but do not overrule visible clipping or a broken layout. Inspect the final loaded app rather than a loading shell. For desktop apps, check the as-launched window before resizing when window geometry matters.

Reuse healthy sessions during iteration. Reload after renderer changes and restart an owned Electron instance after main-process, preload or startup changes. Rebuild when needed to ensure the inspected app contains the final changes.

Use the user's chosen artifact directory. Otherwise save inspection screenshots and temporary data outside the repository in an OS temporary directory. Keep only evidence useful to explain the result, and report what was actually checked plus material limitations.

Close only the browser contexts or application processes you created. Never stop the user's running app or sweep unrelated processes.
