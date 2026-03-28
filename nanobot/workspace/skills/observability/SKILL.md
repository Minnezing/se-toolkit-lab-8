---
name: observability
description: Use observability tools to investigate errors and traces
always: true
---

# Observability Skill

You have access to observability tools for querying VictoriaLogs and VictoriaTraces.

## Available Tools

**Log tools (VictoriaLogs):**
- `logs_search` — Search logs by LogsQL query and time range
- `logs_error_count` — Count errors per service over a time window

**Trace tools (VictoriaTraces):**
- `traces_list` — List recent traces for a service
- `traces_get` — Fetch a specific trace by ID

**Cron tool:**
- `cron` — Schedule recurring jobs (use for proactive health checks)

## Strategy

### When the user asks "What went wrong?" or "Check system health":

Follow this investigation workflow:

1. **Start with `logs_error_count`** using a narrow time window (2-10 minutes)
   - This tells you which services have recent errors
   
2. **Use `logs_search`** to inspect error details for the affected service
   - Include `service.name:"Learning Management Service"` for LMS backend
   - Include `severity:ERROR` to filter for errors
   - Use `_time:2m` or `_time:5m` for very recent issues
   
3. **Extract trace_id** from error log entries (look for `otelTraceID` or `trace_id` field)
   
4. **Use `traces_get`** to fetch the full trace and understand the failure path
   - Look for spans with errors or exceptions
   - Note which operation failed and why
   
5. **Summarize findings** in one coherent explanation:
   - Mention the affected service
   - Cite specific log evidence (error message, timestamp)
   - Cite trace evidence (which span failed, what operation)
   - Name the root failing operation (e.g., "database connection refused")

### When the user asks to create a scheduled health check:

Use the `cron` tool to create a recurring job that:
1. Runs every 2 minutes (or as specified)
2. Calls `logs_error_count` with `time_range="2m"`
3. If errors found, calls `logs_search` and optionally `traces_get`
4. Posts a short summary to the chat

Example cron job creation:
```
cron({"action": "add", "name": "health-check", "schedule": "*/2 * * * *", "messages": [...]})
```

The messages should include a prompt like:
"Check for LMS backend errors in the last 2 minutes. Use logs_error_count with time_range='2m'. If errors found, search logs and inspect a trace. Post a short summary."

### When the user asks about system health or performance:

1. **Use `logs_search`** with a recent time range to check for any issues
2. **Use `traces_list`** to see recent trace durations
3. **Report status** based on findings

## Query Examples

**Find LMS backend errors in the last 2 minutes:**
```
_time:2m service.name:"Learning Management Service" severity:ERROR
```

**Find database connection errors:**
```
_time:5m service.name:"Learning Management Service" event:db_query severity:ERROR
```

**Find all errors across services:**
```
_time:10m severity:ERROR
```

## Response Guidelines

- **Be concise** — summarize findings, don't dump raw JSON
- **Include timestamps** — mention when errors occurred
- **Identify root cause** — if a trace shows the failure point, explain it
- **Cite evidence** — explicitly mention both log evidence AND trace evidence
- **Suggest next steps** — if appropriate, suggest what to investigate next
- **Scope queries narrowly** — use `_time:2m` or `_time:5m` for recent issues

## Example Workflow

**User:** "What went wrong?"

**You:**
1. Call `logs_error_count` with `time_range="5m"`
2. If errors found for "Learning Management Service", call `logs_search` with:
   - `query='service.name:"Learning Management Service" severity:ERROR'`
   - `time_range="5m"`
3. Extract `otelTraceID` from the log entry
4. Call `traces_get` with that trace ID
5. Summarize: "The LMS backend failed due to [error from logs]. The trace shows the failure occurred in the [span name] operation when [trace evidence]. Root cause: [specific failure like 'database connection refused']."

**User:** "Create a health check that runs every 2 minutes"

**You:**
1. Call `cron` with action "add" to create a scheduled job
2. The job should check for errors every 2 minutes and post a summary
3. Confirm the job was created

**User:** "List scheduled jobs"

**You:**
1. Call `cron` with action "list"
2. Show the user their scheduled jobs
