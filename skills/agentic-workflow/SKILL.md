---
name: agentic-workflow
description: Launch a multi-agent, sequential workflow to analyze a problem, research, plan, implement, review, and test a solution. Use when the user asks to run an agentic workflow with an orchestrator plus role-specific subagents, producing markdown outputs and code in /home/mtrapaglia/projects/pinza/coding_workflow.
---

# Agentic Workflow

## Overview

Run a sequential workflow coordinated by an **orchestrator agent** (ACP harness) that spawns role-specific subagents for: issue analysis → research → planning → coding → review → testing. All outputs are stored in a dated project folder.

## Key Files

Use these as the source of truth for role prompts and structure:

- `/home/mtrapaglia/projects/pinza/coding_workflow/ORCHESTRATOR_SPEC.md`
- `/home/mtrapaglia/projects/pinza/coding_workflow/AGENT_PROMPTS.md`

## Project Folder Rules

- Base: `/home/mtrapaglia/projects/pinza/coding_workflow/`
- Run folder: `<project_keywords>_<YYYY-MM-DD>` (keywords invented by orchestrator)
- Outputs (inside run folder):
  - `01_issue.md`
  - `02_research.md`
  - `03_plan.md`
  - `04_implementation.md`
  - `05_review.md`
  - `06_tests.md`

## Agent Map (ACP harness)

Use ACP `sessions_spawn` for every role. Default to the same harness id unless the user provides specific allowed IDs.

Recommended defaults:

- Orchestrator: `agentId: "codex"` (ACP)
- Issue Analyzer: `agentId: "codex"`
- Researcher: `agentId: "codex"`
- Planner: `agentId: "codex"`
- Coder: `agentId: "codex"`
- Reviewer: `agentId: "codex"`
- Tester: `agentId: "codex"`

If the user wants distinct `agentId`s per role, request the allowed ACP agent IDs and update the map.

## Launcher

See `references/launcher.md` for the orchestrator launch template and tool-call notes.

## Orchestration Flow (Sequential)

1. **Spawn Orchestrator (ACP)**
   - `runtime: "acp"`
   - `mode: "session"` (so it can pause and resume after user answers)
   - `thread: false` (Telegram group)
   - Provide: user request + run folder path + pointers to ORCHESTRATOR_SPEC + AGENT_PROMPTS.

2. **Orchestrator spawns subagents** (each in `mode: "run"`):
   - Issue → Research → Plan → Code → Review → Test
   - Collect each output and store in the run folder.

3. **User questions**
   - If Issue Analyzer raises ambiguities, Orchestrator stops and returns questions.
   - OpenClaw asks the user and then resumes the orchestrator with the answers.

4. **Looping**
   - If Review/Test fails acceptance criteria, Orchestrator can loop back to Planner or Coder.

## Tool Permissions by Role

- Issue Analyzer: read/write (no exec)
- Researcher: read/write + web_search/web_fetch
- Planner: read/write
- Coder: read/write/edit + exec
- Reviewer: read/write (exec optional if needed)
- Tester: read/write + exec

## Usage Notes

- Keep the orchestrator as the **only** agent that talks to the user.
- Keep outputs concise and structured; save everything in the run folder.
- Use default model unless overridden.
