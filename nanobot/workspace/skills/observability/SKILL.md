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

## Strategy

### When the user asks about errors or failures:

1. **Start with `logs_error_count`** to see if there are recent errors and which services are affected
2. **Use `logs_search`** to inspect the error details for the relevant service
   - Include `service.name:"Learning Management Service"` to focus on the LMS backend
   - Include `severity:ERROR` to filter for errors
   - Use a narrow time range like `_time:10m` for recent issues
3. **Extract trace_id** from error logs if available
4. **Use `traces_get`** to fetch the full trace and understand the failure path
5. **Summarize findings** concisely — don't dump raw JSON

### When the user asks about system health or performance:

1. **Use `logs_search`** with a recent time range to check for any issues
2. **Use `traces_list`** to see recent trace durations
3. **Report status** based on findings

## Query Examples

**Find LMS backend errors in the last 10 minutes:**
```
_time:10m service.name:"Learning Management Service" severity:ERROR
```

**Find all errors across services:**
```
_time:1h severity:ERROR
```

**Find database-related errors:**
```
_time:1h service.name:"Learning Management Service" event:db_query severity:ERROR
```

## Response Guidelines

- **Be concise** — summarize findings, don't dump raw JSON
- **Include timestamps** — mention when errors occurred
- **Identify root cause** — if a trace shows the failure point, explain it
- **Suggest next steps** — if appropriate, suggest what to investigate next
- **Scope queries narrowly** — use `_time:10m` for recent issues, not `_time:1h` which may include unrelated historical errors

## Example Workflow

**User:** "Any LMS backend errors in the last 10 minutes?"

**You:**
1. Call `logs_error_count` with `time_range="10m"`
2. If errors found for "Learning Management Service", call `logs_search` with:
   - `query='service.name:"Learning Management Service" severity:ERROR'`
   - `time_range="10m"`
3. If logs show a trace_id, call `traces_get` with that ID
4. Summarize: "Found X errors in the LMS backend in the last 10 minutes. The errors show [brief description]. The trace shows the failure occurred at [span/service]."

**User:** "Show me recent traces for the backend"

**You:**
1. Call `traces_list` with `service="Learning Management Service"`
2. Summarize the traces showing duration and span count
3. Offer to fetch details for a specific trace ID
