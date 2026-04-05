---
name: youtube-obsidian-notes
description: Download YouTube auto-captions, split them into topic notes heuristically, add Obsidian-friendly frontmatter, and copy the resulting .md files into the local Obsidian vault. Use when the user gives a YouTube link and asks to generate Obsidian notes or split a transcription into themed notes.
---

# YouTube → Obsidian Notes

## Overview

Automate the full pipeline: fetch auto-captions from a YouTube video, segment the text into topic notes, add frontmatter, and place the notes into the Obsidian vault.

## Quick workflow

1. Run the script with the YouTube URL (and optional language/tags).
2. Confirm the output folder in the Obsidian vault.
3. Report the final location back to the user.

## Run the script

Use `scripts/yt_to_obsidian.py`.

```bash
python /home/mtrapaglia/openclaw/skills/youtube-obsidian-notes/scripts/yt_to_obsidian.py \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --lang es \
  --tags "transcripcion, youtube" \
  --obsidian-root /home/mtrapaglia/Documents/Obsidian
```

### Arguments

- `--url` (required): YouTube video URL.
- `--lang` (optional, default `es`): caption language code.
- `--tags` (optional, default `transcripcion`): comma-separated tags for frontmatter.
- `--obsidian-root` (optional): Obsidian vault path. Default: `/home/mtrapaglia/Documents/Obsidian`.

### Output behavior

- Creates a cache under `~/.openclaw/workspace/obsidian-notes/<slug>`.
- Copies the final notes into: `<obsidian-root>/<video title>/`.
- Each note includes YAML frontmatter with `title`, `source`, `video_url`, `language`, `created`, and `tags`.

## Notes & troubleshooting

- Relies on YouTube auto-captions (`yt-dlp --write-auto-sub`). If a video has no captions, the script will fail and report the error.
- The heuristic splitter uses caption cues and a similarity threshold; if the result is too coarse or too granular, re-run with manual edits after generation.
