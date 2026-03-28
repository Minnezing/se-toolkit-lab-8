"""MCP server for observability tools (VictoriaLogs and VictoriaTraces)."""

from mcp.server.fastmcp import FastMCP

from . import observability as obs

mcp = FastMCP("mcp-obs")


@mcp.tool()
async def logs_search(
    query: str = "Errors in the last hour",
    time_range: str = "1h",
    limit: int = 20,
) -> str:
    """Search VictoriaLogs for log entries matching a LogsQL query.

    Args:
        query: LogsQL query string (e.g., "severity:ERROR service.name:backend")
        time_range: Time range like "1h", "10m", "1d" (default: "1h")
        limit: Maximum number of log entries to return (default: 20)

    Returns:
        JSON-formatted log entries
    """
    return await obs.logs_search(query, time_range, limit)


@mcp.tool()
async def logs_error_count(
    time_range: str = "1h",
) -> dict:
    """Count errors per service over a time window.

    Args:
        time_range: Time range like "1h", "10m", "1d" (default: "1h")

    Returns:
        Dictionary mapping service names to error counts
    """
    return await obs.logs_error_count(time_range)


@mcp.tool()
async def traces_list(
    service: str = "Learning Management Service",
    limit: int = 10,
) -> list:
    """List recent traces for a service from VictoriaTraces.

    Args:
        service: Service name to filter traces (default: "Learning Management Service")
        limit: Maximum number of traces to return (default: 10)

    Returns:
        List of trace summaries with trace_id, duration, and span count
    """
    return await obs.traces_list(service, limit)


@mcp.tool()
async def traces_get(trace_id: str) -> dict:
    """Fetch a specific trace by ID from VictoriaTraces.

    Args:
        trace_id: The trace ID to fetch (hex string)

    Returns:
        Full trace data with span hierarchy and timing information
    """
    return await obs.traces_get(trace_id)


if __name__ == "__main__":
    mcp.run()
