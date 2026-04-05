# Telegram Media IDs — Status & Learnings (2026-03-23)

## Context

We’re patching the Telegram extension to expose media IDs (file_id / file_unique_id) in the agent context so downstream skills can fetch media on-demand without relying on local media paths or polling.

## What we implemented

- Added **fileId** to Telegram media references and context payload.
- Added **fileUniqueId** to Telegram media references and context payload.
- Added **fallback**: when media isn’t downloaded, context still populates `MediaFileId` / `MediaFileUniqueId` directly from the inbound Telegram message.
- Added a **verbose log** to print resolved IDs at context build time:
  - `telegram: ctx media ids fileId=... fileUniqueId=...`

## Key learnings

- Telegram updates clearly include both `file_id` and `file_unique_id` in the inbound update payload.
- The gateway was **loading old bundles** due to hashed dist filenames. Copying only some `telegram-*.js` files was not sufficient.
- The runtime’s bundled imports are hash-tied; copying a single file can silently fail if imports are missing or mismatched.

## Errors / missteps

- **Copying only `dist/telegram-*.js`** was insufficient; the gateway still imported older hashes (e.g. `telegram-BEVBMePo.js`).
- Swapping full `dist/` earlier caused **extension entry escapes package directory** errors. We fixed that by **excluding** `dist/extensions/` from replacement.
- We assumed the context would contain MediaFileId when media fetch failed, but it didn’t—required explicit fallback logic.

## Current state

- Global OpenClaw is at: `/home/mtrapaglia/.npm-global/lib/node_modules/openclaw`
- The **entire `dist/` (except `dist/extensions/`) has been replaced** with the newly built bundle from the repo.
- Gateway is started manually via `openclaw gateway run`.

## Verification checklist (next session)

1. Start gateway with verbose logging:
   ```bash
   pkill -f openclaw-gateway || true
   OPENCLAW_LOG_LEVEL=debug OPENCLAW_LOG_VERBOSE=1 openclaw gateway run
   ```
2. Send a Telegram audio message.
3. Confirm log line appears:
   ```
   telegram: ctx media ids fileId=... fileUniqueId=...
   ```
4. If log appears, confirm session JSON contains those fields.

## Follow‑up actions

- If the log still does not appear, verify the **exact file imported** in `dist/channels-*.js`:
  - It should import the new `telegram-*.js` that contains the `ctx media ids` log.
- If needed, re-run full `pnpm build:docker` and replace `dist/` again (excluding `dist/extensions/`).
- Once confirmed, remove the debug log line (optional cleanup).

## File locations touched

- `extensions/telegram/src/bot-handlers.media.ts`
- `extensions/telegram/src/bot-handlers.runtime.ts`
- `extensions/telegram/src/bot-handlers.buffers.ts`
- `extensions/telegram/src/bot-message-context.types.ts`
- `extensions/telegram/src/bot-message-context.session.ts`

## Commit / branch

- Repo: `/home/mtrapaglia/.openclaw/workspace/openclaw`
- Branch: `feature/delete-last-message`
