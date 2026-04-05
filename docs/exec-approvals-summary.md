# Exec approvals — resumen rápido

## ¿Cuándo pide aprobación `exec`?

Depende de **ask mode** + **allowlist** + **safeBins** + políticas del host (gateway/node).

### 1) `ask=always`

- **Siempre** pide aprobación.

### 2) `ask=on-miss` (comportamiento típico)

- **Pide aprobación solo si** el comando **NO** está en allowlist / safeBins.

### 3) `ask=off`

- **No** pide aprobación, **salvo** que el host fuerce approvals por política.

## ¿Dónde se define?

- Para `host=gateway` o `host=node` aplica el archivo:
  - `~/.openclaw/exec-approvals.json`
- También se puede editar vía UI (Control UI → Exec approvals) o CLI.

## Safe Bins vs Allowlist

- **safeBins**: bins “seguros” (stdin-only), no piden aprobación.
- **allowlist**: comandos exactos/paths permitidos.
- Si el bin/command no entra en ninguno, con `ask=on-miss` pedirá aprobación.

## Shell y expansión

- Comandos con shell/expansiones (`&&`, `|`, `;`, `$()`, etc.) suelen requerir aprobación si no están allowlisteados explícitamente.

## Config Telegram (aprobar desde Telegram)

Habilitar Telegram como cliente de approvals:

```json
{
  "channels": {
    "telegram": {
      "execApprovals": {
        "enabled": true,
        "approvers": [6602358063],
        "target": "both"
      }
    }
  }
}
```

- `approvers`: IDs numéricos de Telegram que pueden aprobar
- `target`: `dm` | `channel` | `both`

## CLI equivalente

```bash
openclaw config set channels.telegram.execApprovals.enabled true
openclaw config set channels.telegram.execApprovals.approvers '[6602358063]'
openclaw config set channels.telegram.execApprovals.target both
```

---

Si querés, puedo inspeccionar la config actual de approvals y listar qué comandos pedirían approval hoy.
