# Bot Recovery Notes

This repo was used to rebuild and reinstall OpenClaw after a broken global install showed missing hashed `dist/` modules.

## Symptoms

- Gateway/plugin load failures like:
  - `Error: Cannot find module '../../logger-kwZIqwuw.js'`
  - `Error: Cannot find module '../../plugin-entry-BNczxv7M.js'`
  - `Error: Cannot find module '../../paths-ViKUYWUK.js'`
- Control UI warning:
  - `Missing Control UI assets at .../dist/control-ui/index.html`

These indicate the packaged global install was missing or inconsistent `dist/` assets.

## Recovery Steps (Clean Rebuild)

1. Clone the repo:

   ```bash
   git clone https://github.com/openclaw/openclaw.git /home/mtrapaglia/openclaw
   ```

2. Install deps:

   ```bash
   cd /home/mtrapaglia/openclaw
   pnpm install
   ```

3. Build core `dist/` assets:

   ```bash
   pnpm build
   ```

4. Build Control UI assets:

   ```bash
   pnpm ui:build
   ```

5. Reinstall globally via npm (because `pnpm -g` was not configured with `PNPM_HOME`):
   ```bash
   npm -g install /home/mtrapaglia/openclaw
   ```

## Notes

- The rebuilt package version ended up as `2026.3.23` (repo HEAD at the time).
- After reinstall, restart the gateway and verify plugins load.
- If future missing-hash errors appear, prefer rebuilding from repo rather than patching individual files.
