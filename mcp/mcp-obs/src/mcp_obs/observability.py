"""Observability API clients for VictoriaLogs and VictoriaTraces."""

import json
import httpx

# VictoriaLogs API base URL (port 9428)
VICTORIALOGS_BASE_URL = "http://victorialogs:9428"

# VictoriaTraces API base URL (port 10428, Jaeger-compatible)
VICTORIATRACES_BASE_URL = "http://victoriatraces:10428/select/jaeger/api"


async def logs_search(query: str = "", time_range: str = "1h", limit: int = 20) -> str:
    """Search VictoriaLogs using LogsQL query.

    Args:
        query: LogsQL query string
        time_range: Time range like "1h", "10m", "1d"
        limit: Maximum number of entries

    Returns:
        JSON-formatted log entries
    """
    # Build LogsQL query with time range
    logsql_query = f"_time:{time_range}"
    if query:
        logsql_query += f" {query}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{VICTORIALOGS_BASE_URL}/select/logsql/query",
            params={"query": logsql_query, "limit": limit},
        )
        response.raise_for_status()
        # VictoriaLogs returns newline-delimited JSON
        lines = response.text.strip().split('\n')
        entries = [json.loads(line) for line in lines if line.strip()]
        return json.dumps(entries, indent=2)


async def logs_error_count(time_range: str = "1h") -> dict:
    """Count errors per service over a time window.

    Args:
        time_range: Time range like "1h", "10m", "1d"

    Returns:
        Dictionary mapping service names to error counts
    """
    logsql_query = f"_time:{time_range} severity:ERROR"

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{VICTORIALOGS_BASE_URL}/select/logsql/query",
            params={"query": logsql_query, "limit": 1000},
        )
        response.raise_for_status()
        # VictoriaLogs returns newline-delimited JSON
        lines = response.text.strip().split('\n')
        entries = [json.loads(line) for line in lines if line.strip()]

    # Count errors by service
    error_counts: dict[str, int] = {}
    for entry in entries:
        # Extract service name from log entry
        service = entry.get("service.name", "unknown")
        error_counts[service] = error_counts.get(service, 0) + 1

    return error_counts


async def traces_list(service: str = "Learning Management Service", limit: int = 10) -> list:
    """List recent traces for a service.

    Args:
        service: Service name to filter
        limit: Maximum number of traces

    Returns:
        List of trace summaries
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{VICTORIATRACES_BASE_URL}/traces",
            params={"service": service, "limit": limit},
        )
        response.raise_for_status()
        data = response.json()

    # Extract trace summaries
    traces = []
    if "data" in data and "traces" in data["data"]:
        for trace in data["data"]["traces"]:
            traces.append({
                "trace_id": trace.get("traceID", ""),
                "duration_ms": trace.get("duration", 0),
                "span_count": len(trace.get("spans", [])),
                "start_time": trace.get("startTime", 0),
            })

    return traces


async def traces_get(trace_id: str) -> dict:
    """Fetch a specific trace by ID.

    Args:
        trace_id: The trace ID

    Returns:
        Full trace data with spans
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{VICTORIATRACES_BASE_URL}/traces/{trace_id}",
        )
        response.raise_for_status()
        return response.json()
