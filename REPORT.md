# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Checkpoint 1: "What is the agentic loop?"**

The agentic loop is the core reasoning cycle that enables AI agents to act autonomously. It consists of four main stages:

1. **Perceive** — Take in information from the environment (user input, files, APIs, tool outputs)
2. **Reason** — Analyze the information, plan next steps, and decide on actions
3. **Act** — Execute actions using available tools (read/write files, run commands, call APIs)
4. **Observe** — Process the results and feedback from those actions

Then the loop repeats: the agent uses new observations to reason about what to do next, continuing until the task is complete.

This loop is what allows agents to:
- Handle multi-step tasks
- Adapt when things don't go as planned
- Learn from tool outputs and adjust strategy
- Work toward goals without needing every step specified by the user

**Checkpoint 2: "What labs are available in our LMS?"**

Before MCP configuration, the agent explores local files and responds with information from the repository structure rather than live backend data.

## Task 1B — Agent with LMS tools

**Checkpoint 1: "What labs are available?"**

The agent now returns real lab names from the LMS backend:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. Lab 08 — lab-08

**Checkpoint 2: "Is the LMS backend healthy?"**

"Yes, the LMS backend is healthy. It currently has 56 items in the system."

## Task 1C — Skill prompt

**Checkpoint: "Show me the scores" (without specifying a lab)**

The agent now shows pass rates for all labs with nicely formatted tables:

```
Lab 01 – Products, Architecture & Roles

 Task                                        Avg Score  Attempts
 ───────────────────────────────────────────────────────────────
 Lab setup                                   84.3%      3,126
 Task 0: Practice the Git workflow           64.5%      306
 Task 1: Product & architecture description  55.1%      161
 Task 2: Roles and skills mapping            49.8%      83
```

The skill prompt teaches the agent to:
- Call `lms_labs` first when lab is not specified
- Format percentages with % symbol
- Keep responses concise but informative
- Use each lab title as the user-facing label

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
