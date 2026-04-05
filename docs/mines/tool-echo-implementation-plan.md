# Tool Echo to Requester — Plan de Implementación

## Objetivo

Enviar al **mismo chat** que originó la solicitud un mensaje con:

- **Nombre de herramienta**
- **Parámetros/argumentos** (solo comando/params, **sin output**)

Aplica a **todas las sesiones** (main/subagents) y **todos los canales**. Evitar loops: el mensaje de eco **no** debe disparar otro eco.

---

## Alcance

- Activación por config: `tools.echoToRequester` (default `false`).
- Habilitarlo en el config por defecto del entorno (según lo definido).
- Echo usa el **mismo chat_id/account_id/provider** del request original.

---

## Diseño (alto nivel)

1. **Config**
   - Agregar flag `tools.echoToRequester: boolean`.
   - Default `false`.
   - Documentar en docs de configuración/herramientas.

2. **Hook en ejecución de tools**
   - Interceptar **antes** de ejecutar la tool.
   - Construir payload legible: `{ toolName, args }`.
   - Enviar mensaje vía router con metadatos del request original.
   - Marcar el mensaje como interno/eco (`meta.toolEcho = true`) para evitar re-echo.

3. **Routing**
   - Reusar el **mismo canal** (Telegram, Discord, etc.).
   - Usar `chat_id`/`account_id`/`provider` del request entrante.

4. **Anti-loop**
   - Si `meta.toolEcho === true`, **no** emitir eco.
   - Asegurar que el echo no pase por la misma capa de invocación de tools.

---

## Seguridad / Privacidad

- **Redacción de secretos** en args (tokens, passwords, headers, keys, cookies).
- Sanitizer centralizado para args antes del echo.
- (Opcional) allow/deny list por tool para evitar spam o leaks.

---

## Formato de mensaje sugerido

```
🔧 tool: <toolName>
args: <string legible de params>
```

---

## Archivos a tocar (tentativo)

- Config por defecto (`openclaw.json` o equivalente)
- Pipeline de ejecución de tools
- Router/dispatcher de mensajes
- Docs de configuración/herramientas

---

## Checklist

- [x] Añadir flag `tools.echoToRequester` (default false)
- [ ] Habilitar flag en config del entorno
- [x] Implementar hook en tool invocation
- [x] Sanitizar args antes de echo
- [x] Enviar mensaje con tool + args
- [ ] Anti-loop implementado
- [x] Docs actualizadas
- [ ] Tests / validación manual básica
