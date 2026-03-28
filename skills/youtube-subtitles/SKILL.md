---
name: youtube-subtitles
description: Descargar subtítulos de videos de YouTube (manuales o auto) a partir de un link y exportar TXT plano + JSON con timestamps. Usar cuando el usuario pida “explicame de qué trata este video”, “extraé subtítulos”, “resumí este video”, o cuando necesite aplicar una técnica descrita en un video de YouTube.
---

# YouTube Subtitles

## Overview

Extraer subtítulos desde un link de YouTube y generar: (1) texto plano y (2) JSON con timestamps.

## Quick start

1. Ejecutar el script con el link del video.
2. Usar los outputs TXT/JSON para resumir, explicar o aplicar la técnica del video.

```bash
python scripts/yt_subtitles.py "https://www.youtube.com/watch?v=..."
```

## Workflow

### 1) Descargar subtítulos

Usar `scripts/yt_subtitles.py`.

**Parámetros:**

- `url` (obligatorio): link de YouTube
- `--langs` (opcional): idiomas preferidos en orden (default: `es,en`)
- `--outdir` (opcional): carpeta de salida. Por defecto: `<skill>/extracted`

Ejemplos:

```bash
python scripts/yt_subtitles.py "https://youtu.be/VIDEOID" --langs "es,en"
python scripts/yt_subtitles.py "https://youtu.be/VIDEOID" --outdir /tmp/subs
```

### 2) Usar los outputs

- **TXT plano**: texto limpio, una línea por cue.
- **JSON**: lista de cues con `start`, `end`, `text`.

Usar el TXT/JSON para:

- Explicar de qué trata el video.
- Extraer pasos/técnicas y aplicarlas al trabajo en curso.
- Resumir o buscar secciones relevantes.

## Recursos

### scripts/

- `yt_subtitles.py`: descarga subtítulos (manuales o auto), elige el mejor idioma disponible y exporta TXT/JSON.
