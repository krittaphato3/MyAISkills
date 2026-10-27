---
name: desktop-app-developer
description: >-
  Builds and ships desktop apps with Electron or Tauri: main/renderer boundaries, IPC and
  sandboxing, native OS integration, auto-update, and per-platform packaging and code
  signing. Use when the deliverable is an installable desktop application. Web UI logic
  routes to frontend-web-engineer; mobile apps to mobile-developer.
metadata:
  version: 3.0.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: desktop-developer
---

# Desktop App Developer

A shipped desktop app must install cleanly, launch fast, respect the OS, update itself, and not be a security hole wrapped in a familiar UI. The renderer is a web page with the user's whole machine behind it — treat that boundary as the primary design constraint.

## WHEN TO USE

- **Desktop shells** — Electron or Tauri wrapping a web UI.
- **Native integration** — filesystem, tray/menu, notifications, global shortcuts, file associations, deep links.
- **Process/IPC design** — main vs renderer, preload bridges, typed channels.
- **Packaging & release** — installers, code signing, notarization, auto-update.
- **Startup/size problems** — cold start latency, installer size, memory.

## WHEN NOT TO USE

- **Web-only UI mechanics** — `frontend-web-engineer`.
- **Visual design language** — `ui-ux-architect`.
- **Mobile apps** — `mobile-developer` (React Native/Flutter/native).
- **CI pipeline construction** — `devops-pipeline-engineer`, which this skill feeds release jobs to.

## DECISION TREE

1. **Electron or Tauri?** Electron: mature, heavier, Node in main. Tauri: smaller binaries, Rust core, webview-per-OS rendering differences. Choose on team skills and binary-size requirements, and state the trade-off.
2. **Draw the process boundary.** Main owns OS access; renderer owns UI. Everything crossing is IPC over a narrow, validated surface.
3. **Key the channels.** Name channels by intent and validate every argument in main. Never expose a generic invoke.
4. **Lock the renderer down.** `contextIsolation: true`, `nodeIntegration: false`, sandbox on, CSP set, remote content isolated.
5. **Plan the OS integrations** the app actually needs — files, tray, shortcuts, notifications, deep links — and nothing more.
6. **Plan packaging per target OS**, including signing credentials as a prerequisite, not an afterthought.
7. **Wire auto-update** with signed artifacts, staged rollout, and a rollback, before the first public release.

## PATTERNS

### 1. Architecture
```text
main process   → windows, OS access, updater, filesystem, menus, tray
preload script → the ONLY bridge: narrow, typed, argument-validated API
renderer       → UI; sandboxed; no Node, no direct fs, no remote privilege
```

### 2. IPC
- Channels by intent (`file:open`, `settings:save`); validate and type arguments in the main handler.
- Never accept a raw path, URL, or shell string from the renderer — allow-list it.
- Return structured results/errors; do not leak stack traces or absolute paths into the renderer.

### 3. Native integration
- Files: OS dialogs in main; validate drag-drop paths.
- Menus/shortcuts: platform-native accelerators; never override OS-reserved combos.
- Deep links / file associations: validate the payload before acting.
- Persist state in the platform app-data dir, never beside the binary.

### 4. Packaging & signing
- **macOS**: hardened runtime + entitlements, Developer ID signing, notarize + staple; test on a clean machine.
- **Windows**: sign the installer and binaries; MSI/MSIX or signed NSIS.
- **Linux**: AppImage/deb/rpm; declare dependencies; test on the oldest supported distro.
- Pin the toolchain; aim for reproducible builds.

### 5. Auto-update
- Sign update artifacts and verify before applying; never apply an unverified update.
- Staged rollout with a rollback path; the app must still run when the update check or download fails.
- Window between "release published" and "update applied" must be recoverable.

### 6. Startup performance
- Defer non-essential work off the launch path; show UI early.
- Lazy-load heavy renderer modules; avoid importing analytics/telemetry at boot.
- Measure cold start as a budget, not an impression.

## FAILURE MODES & MITIGATIONS

Each entry is DETECT → FIX.

1. **Privilege leak** — DETECT: `nodeIntegration` on or blanket IPC exposed. FIX: narrow preload API + contextIsolation.
2. **Unvalidated IPC** — DETECT: renderer-supplied path/command used directly. FIX: allow-list and validate in main.
3. **Unsigned build** — DETECT: no signing/notarization step. FIX: add signing; record the credential prerequisite.
4. **No updater** — DETECT: releases with no update path. FIX: signed updates + staged rollout + rollback.
5. **Single-OS testing** — DETECT: only the dev OS was run. FIX: build/test every claimed target OS.
6. **Remote content privileged** — DETECT: third-party URL loaded with bridges attached. FIX: isolate it in a sandboxed window with no bridge.
7. **State in the install dir** — DETECT: writes beside the binary fail after install/update. FIX: platform app-data dir.
8. **Startup regression** — DETECT: cold start grows unmeasured. FIX: budget and measure it.

## QUANTITATIVE RULES

- `contextIsolation: true`, `nodeIntegration: false`, sandbox on unless a documented exception exists.
- CSP set on every window; no `unsafe-eval`; remote content allow-listed by origin.
- Every IPC channel validates its arguments in main; zero generic invoke bridges.
- Cold start and installer size carry explicit budgets; measured, not assumed.
- Every claimed target OS is built and smoke-tested before release.
- Release requires signed artifacts and a working update path.

## VERIFICATION GATE

- **Boundary secure?** contextIsolation on, nodeIntegration off, CSP set, channels validated.
- **Packages per target?** An artifact exists for each OS claimed, with the build evidence.
- **Signed/notarized?** Status stated honestly; unsigned is flagged, not hidden.
- **Updater works?** Signed update applied in a test, with rollback available.
- **Native integrations validated?** Each payload/path checked against an allow-list.
- **Startup measured?** Cold-start number attached.

```text
[DESKTOP DELIVERABLE]
App: {name} · Framework: {Electron/Tauri} · Targets: {OSes}
Main/preload/renderer: {channels n} · sandbox {on} · CSP {set}
Native: {files | tray | shortcuts | notifications | deep links}
Packaging: {target → artifact} · signed {yes/no} · notarized {yes/no/na}
Updater: {configured} · staged {yes} · rollback {path}
Startup: {x}ms cold · installer {x}MB
Evidence: {build path}
Remaining to ship: {credentials, listings, notarization}
```

## REFERENCES

- `frontend-web-engineer` — renderer UI mechanics.
- `ui-ux-architect` — design systems and visual language.
- `devops-pipeline-engineer` — CI jobs that build/sign/release.
- `mobile-developer` — the mobile counterpart.
- `desktop-developer` agent — the implementing role.

Ownership: maintained by desktop-developer; desktop-app-developer is the delivery-domain skill for native desktop shells.
