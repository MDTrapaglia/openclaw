# Telegram permissions change log

Date: 2026-04-03

Summary

- Identified Telegram bot not responding due to invalid config value in `channels.telegram.execApprovals.target`.
- Set `channels.telegram.execApprovals.target` to `both`.
- Set `channels.telegram.execApprovals.enabled` to `false` to disable per-command approvals in Telegram.
- Restarted the user service `openclaw-gateway.service` after changes.
- Noted that group messages may require BotFather privacy mode to be disabled or the bot to be mentioned.

Commands executed

- `openclaw config set channels.telegram.execApprovals.target both`
- `openclaw config set channels.telegram.execApprovals.enabled false`
- `systemctl --user restart openclaw-gateway.service`

Notes

- Config file: `~/.openclaw/openclaw.json`
- If approvals should be re-enabled later: `openclaw config set channels.telegram.execApprovals.enabled true`
