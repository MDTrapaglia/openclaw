import { redactSensitiveText } from "../../logging/redact.js";

const MAX_TOOL_ECHO_CHARS = 2000;

function truncateText(input: string, maxChars: number): string {
  if (input.length <= maxChars) {
    return input;
  }
  return `${input.slice(0, maxChars)}…`;
}

function renderToolArgs(args: unknown): string {
  if (args == null) {
    return "<none>";
  }
  let raw: string;
  if (typeof args === "string") {
    raw = args;
  } else {
    try {
      raw = JSON.stringify(args, null, 2);
    } catch {
      raw = "<unserializable>";
    }
  }
  const redacted = redactSensitiveText(raw);
  return truncateText(redacted, MAX_TOOL_ECHO_CHARS);
}

export function formatToolEchoText(toolName: string | undefined, args: unknown): string {
  const safeName = toolName?.trim() || "tool";
  const renderedArgs = renderToolArgs(args);
  return `🔧 tool: ${safeName}\nargs: ${renderedArgs}`;
}
