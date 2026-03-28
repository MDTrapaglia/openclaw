# Launcher (Orchestrator)

Use this template when you need to launch the workflow.

## Inputs

- `USER_REQUEST`: the user’s request/problem statement.
- `RUN_FOLDER`: `/home/mtrapaglia/projects/pinza/coding_workflow/<keywords>_<YYYY-MM-DD>`
- `SPEC_PATH`: `/home/mtrapaglia/projects/pinza/coding_workflow/ORCHESTRATOR_SPEC.md`
- `PROMPTS_PATH`: `/home/mtrapaglia/projects/pinza/coding_workflow/AGENT_PROMPTS.md`

## Launcher Prompt (to Orchestrator)

```
You are the Orchestrator for a sequential, multi-agent workflow.

Context:
- Spec: ${SPEC_PATH}
- Role prompts: ${PROMPTS_PATH}
- Run folder: ${RUN_FOLDER}
- User request: ${USER_REQUEST}

Rules:
- You are the only agent that can talk to the user.
- Spawn subagents sequentially: Issue → Research → Plan → Code → Review → Test.
- Save outputs as:
  01_issue.md, 02_research.md, 03_plan.md, 04_implementation.md, 05_review.md, 06_tests.md
- If Issue stage yields questions, stop and return them so the user can answer.
- If Review/Test fails acceptance criteria, loop back to Planner or Coder.
```

## Tool Call (by OpenClaw)

Use ACP harness for the Orchestrator:

- `sessions_spawn` with `runtime: "acp"`, `mode: "session"`, `thread: false`, `agentId: "codex"` (or custom if configured).
