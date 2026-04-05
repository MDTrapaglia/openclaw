#!/usr/bin/env python
"""
Download YouTube auto-captions, segment heuristically into topic notes, and place in Obsidian folder.

Usage:
  python yt_to_obsidian.py --url <youtube_url> [--lang es] [--obsidian-root /path] [--tags tag1,tag2]

Outputs:
  - A folder under obsidian-root named after the video title
  - A workspace cache under ~/.openclaw/workspace/obsidian-notes/<slug>
"""
import argparse
import datetime
import re
import subprocess
from pathlib import Path
import shutil
import sys

WORKSPACE = Path("/home/mtrapaglia/.openclaw/workspace")
DEFAULT_OBSIDIAN = Path("/home/mtrapaglia/Documents/Obsidian")

STOPWORDS = set('''a al algo algunas algunos ante antes como con contra cual cuales cuando de del desde donde dos el ella ellas ellos en entre era erais eran eras eres es esa esas ese eso esos esta estaba estabais estaban estabas estad estadlo estar estaras estara estaran estaras estare estareis estaremos estareis estaria estarias estariamos estarian estarias estas este esto estos estuve estuviera estuvierais estuvieran estuvieras estuvieron estuviste estuvisteis estuviéramos estuviéramos estoy estan estaré estaría estoy estamos están etc ha habéis haber habia habiais habian habias han has hasta hay la las le les lo los me mi mis muy mas más menos no nos o os para pero por porque que se sea seais sean seas sera seran seras sere sereis seremos seriais serian serias si sin sobre sois somos son soy su sus te tener tengo tiene tienen tu tus un una unas unos y ya'''.split())

def run(cmd):
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{result.stderr.strip()}")
    return result.stdout.strip()


def slugify(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\wáéíóúñüÁÉÍÓÚÑÜ-]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def title_from_segment(segment):
    words = re.findall(r"[\wáéíóúñü]+", " ".join(segment).lower())
    words = [w for w in words if len(w) > 4 and w not in STOPWORDS]
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    top = sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:3]
    if not top:
        return "nota"
    return " ".join(w for w, _ in top)


def normalize_line(line: str) -> str:
    line = line.strip().lower()
    line = re.sub(r"\s+", " ", line)
    line = re.sub(r"[\?\!\.,;:]+$", "", line)
    return line


def parse_vtt_to_cues(vtt_path: Path):
    lines = vtt_path.read_text(encoding="utf-8").splitlines()
    cues = []
    current = []
    last_norm = None
    for line in lines:
        line = line.strip()
        if not line:
            if current:
                cue = " ".join(current).strip()
                if cue and (not cues or cues[-1] != cue):
                    cues.append(cue)
                current = []
            continue
        if line.startswith("WEBVTT"):
            continue
        if line.upper().startswith("NOTE") or line.upper().startswith("STYLE") or line.upper().startswith("REGION"):
            continue
        if line.lower().startswith("kind:") or line.lower().startswith("language:"):
            continue
        if re.match(r"^\d\d:\d\d:\d\d\.\d{3} -->", line):
            continue
        if re.match(r"^\d+$", line):
            continue
        line = re.sub(r"<[^>]+>", "", line)
        line = re.sub(r"\[[^\]]+\]", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        if not line:
            continue
        norm = normalize_line(line)
        if norm == last_norm:
            continue
        last_norm = norm
        current.append(line)
    if current:
        cue = " ".join(current).strip()
        if cue and (not cues or cues[-1] != cue):
            cues.append(cue)
    return cues


def segment_cues(cues, window=6, min_seg=20, max_seg=60, threshold=0.20):
    def keywords(text):
        words = re.findall(r"[\wáéíóúñü]+", text.lower())
        words = [w for w in words if len(w) > 4 and w not in STOPWORDS]
        return set(words)

    kw = [keywords(c) for c in cues]
    segments = []
    current = []

    for i, c in enumerate(cues):
        current.append(c)
        if len(current) < min_seg:
            continue
        if i + 1 >= len(cues):
            continue
        curr_kw = set().union(*kw[max(0, i - window + 1): i + 1])
        next_kw = set().union(*kw[i + 1: min(len(cues), i + 1 + window)])
        if curr_kw or next_kw:
            inter = len(curr_kw & next_kw)
            union = len(curr_kw | next_kw)
            sim = inter / union if union else 1.0
        else:
            sim = 1.0
        if sim < threshold or len(current) >= max_seg:
            segments.append(current)
            current = []

    if current:
        segments.append(current)
    return segments


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--lang", default="es")
    parser.add_argument("--obsidian-root", default=str(DEFAULT_OBSIDIAN))
    parser.add_argument("--tags", default="transcripcion")
    args = parser.parse_args()

    obsidian_root = Path(args.obsidian_root)
    obsidian_root.mkdir(parents=True, exist_ok=True)

    title = run(["yt-dlp", "--print", "title", args.url])
    safe_folder = title.replace("/", "-")

    # Download auto-subs via android client (more reliable)
    before = {p.resolve() for p in WORKSPACE.glob(f"*.{args.lang}.vtt")}
    run([
        "yt-dlp",
        "--write-auto-sub",
        "--sub-lang", args.lang,
        "--skip-download",
        "--sub-format", "vtt",
        "--extractor-args", "youtube:player_client=android",
        "-o", str(WORKSPACE / "%(title)s.%(ext)s"),
        args.url,
    ])

    after = {p.resolve() for p in WORKSPACE.glob(f"*.{args.lang}.vtt")}
    new_files = list(after - before)
    if new_files:
        vtt_path = max(new_files, key=lambda p: p.stat().st_mtime)
    else:
        # fallback: pick the most recent vtt of this language
        candidates = list(WORKSPACE.glob(f"*.{args.lang}.vtt"))
        if not candidates:
            raise FileNotFoundError(f"Subtitle file not found for lang {args.lang}")
        vtt_path = max(candidates, key=lambda p: p.stat().st_mtime)

    cues = parse_vtt_to_cues(vtt_path)
    if not cues:
        raise RuntimeError("No cues parsed from VTT")

    segments = segment_cues(cues)

    slug = slugify(title)
    cache_dir = WORKSPACE / "obsidian-notes" / slug
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    date = datetime.date.today().isoformat()
    tags = ", ".join([t.strip() for t in args.tags.split(",") if t.strip()])

    # Build sentence lists per segment (soft adjustment)
    sentence_segments = []
    for segment in segments:
        joined = " ".join(segment)
        sentences = re.split(r"(?<=[\.!?])\s+", joined)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_segments.append(sentences)

    for idx, segment in enumerate(sentence_segments, start=1):
        note_title = title_from_segment(segment)
        safe_title = slugify(note_title)
        fname = f"{idx:02d}-{safe_title}.md"
        fm = (
            "---\n"
            f"title: \"{note_title}\"\n"
            f"source: \"{title}\"\n"
            f"video_url: \"{args.url}\"\n"
            f"language: {args.lang}\n"
            f"created: {date}\n"
            f"tags: [{tags}]\n"
            "---\n\n"
        )
        # include 1-2 previous sentences + 1 next sentence (soft context)
        prev_sent = []
        next_sent = []
        if idx > 1:
            prev = sentence_segments[idx - 2]
            prev_sent = prev[-2:]
        if idx < len(sentence_segments):
            nxt = sentence_segments[idx]
            next_sent = nxt[:1]
        merged = prev_sent + segment + next_sent

        # de-dup repeated lines inside a segment (normalized, short window)
        cleaned = []
        recent_norm = []
        for line in merged:
            norm = normalize_line(line)
            if norm in recent_norm:
                continue
            cleaned.append(line)
            recent_norm.append(norm)
            if len(recent_norm) > 8:
                recent_norm.pop(0)
        body = "\n".join(cleaned)
        (cache_dir / fname).write_text(fm + body, encoding="utf-8")

    target_dir = obsidian_root / safe_folder
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    for p in cache_dir.glob("*.md"):
        shutil.copy2(p, target_dir / p.name)

    print(str(target_dir))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
