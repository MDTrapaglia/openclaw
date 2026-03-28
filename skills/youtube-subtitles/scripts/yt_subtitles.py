#!/usr/bin/env python3
"""Download YouTube subtitles and export plain text + JSON with timestamps."""

import argparse
import html
import json
import re
import subprocess
from pathlib import Path


TIME_RE = re.compile(r"^(\d{2}:\d{2}:\d{2}\.\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2}\.\d{3})")
TAG_RE = re.compile(r"<[^>]+>")


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def detect_video_id(url: str) -> str:
    out = run(["yt-dlp", "--print", "%(id)s", "--skip-download", url]).stdout.strip()
    if not out:
        raise RuntimeError("No se pudo obtener el ID del video con yt-dlp")
    return out


def download_subs(url: str, outdir: Path, langs: str):
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-subs",
        "--write-auto-subs",
        "--sub-format",
        "vtt",
        "--sub-langs",
        langs,
        "--output",
        str(outdir / "%(id)s.%(ext)s"),
        url,
    ]
    run(cmd)


def choose_vtt(outdir: Path, video_id: str, preferred_langs: list[str]) -> Path:
    candidates = sorted(outdir.glob(f"{video_id}*.vtt"))
    if not candidates:
        raise FileNotFoundError("No se descargaron subtítulos .vtt")

    def score(path: Path) -> tuple[int, int, str]:
        name = path.name
        lang_part = name.replace(f"{video_id}.", "").replace(".vtt", "")
        is_auto = 1 if "auto" in lang_part else 0
        lang_code = lang_part.replace(".auto", "")
        lang_score = preferred_langs.index(lang_code) if lang_code in preferred_langs else 999
        return (lang_score, is_auto, name)

    return sorted(candidates, key=score)[0]


def parse_vtt(vtt_path: Path):
    text = vtt_path.read_text(encoding="utf-8", errors="ignore")
    lines = [line.strip() for line in text.splitlines()]
    cues = []
    i = 0
    while i < len(lines):
        line = lines[i]
        match = TIME_RE.match(line)
        if match:
            start, end = match.groups()
            i += 1
            cue_lines = []
            while i < len(lines) and lines[i] != "":
                cue_lines.append(lines[i])
                i += 1
            raw = " ".join(cue_lines)
            cleaned = html.unescape(TAG_RE.sub("", raw)).strip()
            if cleaned:
                cues.append({"start": start, "end": end, "text": cleaned})
        else:
            i += 1
    return cues


def write_outputs(vtt_path: Path, cues: list[dict]):
    base = vtt_path.with_suffix("")
    txt_path = base.with_suffix(".txt")
    json_path = base.with_suffix(".json")

    txt_path.write_text("\n".join(c["text"] for c in cues), encoding="utf-8")
    json_path.write_text(json.dumps(cues, ensure_ascii=False, indent=2), encoding="utf-8")
    return txt_path, json_path


def main():
    parser = argparse.ArgumentParser(description="Descarga subtítulos de YouTube (VTT) y exporta TXT/JSON")
    parser.add_argument("url", help="URL de YouTube")
    parser.add_argument(
        "--langs",
        default="es,en",
        help="Lista de idiomas preferidos en orden (default: es,en)",
    )
    parser.add_argument(
        "--outdir",
        default=None,
        help="Directorio de salida. Por defecto: <skill>/extracted",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parent.parent
    outdir = Path(args.outdir) if args.outdir else skill_root / "extracted"

    video_id = detect_video_id(args.url)
    download_subs(args.url, outdir, args.langs)

    preferred_langs = [lang.strip() for lang in args.langs.split(",") if lang.strip()]
    vtt_path = choose_vtt(outdir, video_id, preferred_langs)
    cues = parse_vtt(vtt_path)
    if not cues:
        raise RuntimeError("No se pudieron parsear subtítulos desde el VTT")

    txt_path, json_path = write_outputs(vtt_path, cues)
    print(f"VTT: {vtt_path}")
    print(f"TXT: {txt_path}")
    print(f"JSON: {json_path}")


if __name__ == "__main__":
    main()
