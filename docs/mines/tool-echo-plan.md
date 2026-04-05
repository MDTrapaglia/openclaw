# Tool Echo to Requester — Plan

## Objetivo

Cuando se invoque cualquier herramienta (exec/read/write/edit/web_search/web_fetch/cron/etc), enviar un mensaje al **mismo chat** que lo solicitó con:

- nombre de la herramienta
- parámetros/argumentos (solo comando/params, **sin output**)

Debe aplicar a **todas las sesiones** (main/subagents) y **todos los canales**. Evitar loops: el mensaje de eco **no** debe disparar otro eco.

## Restricciones

- Controlado por config: `tools.echoToRequester` (default **false**)
- Para este entorno, habilitarlo en el config por defecto.
- Usar el mismo `chat_id`/`account_id` del request original.
- Evitar overhead y duplicación.

## Diseño

1. **Agregar flag de config**
   - `tools.echoToRequester: boolean`
   - Default false
   - Documentar en docs de tools/config.

2. **Hook en la canalización de invocación de tools**
   - Interceptar justo antes de ejecutar la tool
   - Construir payload: `{ toolName, args }` (string legible)
   - Enviar mensaje via router de mensajes usando metadatos del request original
   - Marcar el mensaje de eco con un flag interno para **no re-eco** (ej. `meta.toolEcho: true` o `internal: true`)

3. **Routing**
   - Reutilizar la misma superficie/canal (Telegram, etc.)
   - Reusar `chat_id`/`account_id`/`provider` del request entrante

4. **Anti-loop**
   - Si `meta.toolEcho === true`, saltar el echo
   - Asegurar que el echo no pase por la misma capa de tool invocation

## Archivos a tocar (tentativo)

- Config default (ej. `openclaw.json`, `default.config`, etc.)
- Módulo de ejecución de tools (pipeline)
- Módulo de envío de mensajes/routers (para reusar)
- Docs de configuración/herramientas

## Checklist

- [ ] Añadir flag `tools.echoToRequester` (default false)
- [ ] Habilitar flag en config del entorno
- [ ] Implementar hook en tool invocation
- [ ] Enviar mensaje con tool + args
- [ ] Anti-loop implementado
- [ ] Docs actualizadas
- [ ] Tests/validación básica manual

## Nota

El echo se limita a parámetros (comando/args), no incluye output.
