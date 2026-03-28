---
name: context7
description: Obtener documentación y ejemplos de APIs/librerías actualizados vía Context7 MCP. Usar cuando el usuario pida docs recientes, dudas de API/versiones o ejemplos de uso de librerías (frameworks, SDKs, herramientas) y necesites resolver el library ID y traer documentación específica por tema.
---

# Context7

## Overview

Context7 MCP aporta documentación y ejemplos actualizados de librerías. Este skill define cómo resolver el library ID y consultar docs por tema.

## Flujo rápido

1. **Si ya conocés el ID de Context7** (ej: `/vercel/next.js`, `/supabase/supabase`):
   - Llamar `get-library-docs` con `context7CompatibleLibraryID` y opcionalmente `topic`.

2. **Si no conocés el ID**:
   - Llamar `resolve-library-id` con `libraryName` (ej: "Next.js", "Supabase", "MongoDB").
   - Elegir el ID correcto de la respuesta.
   - Llamar `get-library-docs` con ese ID.

## Buenas prácticas

- **Usar `topic`** para enfocar (ej: "routing", "auth", "hooks", "caching").
- **Paginar con `page`** si falta contenido (page=2, page=3...).
- Si el usuario pide una solución concreta, **traer docs** y luego responder con pasos/código citando lo relevante.

## Ejemplos

- “Necesito ejemplo de middleware en Next.js” → resolve ID `Next.js` → get docs con `topic: "middleware"`.
- “Cómo hago auth básica en Supabase” → si ya sabés `/supabase/supabase`, ir directo a `get-library-docs`.
