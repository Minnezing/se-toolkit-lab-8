#!/usr/bin/env python3
"""
Nanobot gateway entrypoint for Docker.

Resolves environment variables into the config at runtime,
then launches `nanobot gateway`.
"""

import json
import os
import sys
from pathlib import Path


def main():
    # Paths
    config_dir = Path(__file__).parent
    config_path = config_dir / "config.json"
    resolved_path = config_dir / "config.resolved.json"
    workspace_dir = config_dir / "workspace"

    # Read base config
    with open(config_path) as f:
        config = json.load(f)

    # Override from environment variables
    # LLM provider settings
    if llm_api_key := os.environ.get("LLM_API_KEY"):
        config["providers"]["custom"]["apiKey"] = llm_api_key

    if llm_api_base := os.environ.get("LLM_API_BASE_URL"):
        config["providers"]["custom"]["apiBase"] = llm_api_base

    if llm_model := os.environ.get("LLM_API_MODEL"):
        config["agents"]["defaults"]["model"] = llm_model

    # Gateway settings
    if gateway_host := os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS"):
        config["gateway"]["host"] = gateway_host

    if gateway_port := os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT"):
        config["gateway"]["port"] = int(gateway_port)

    # Webchat channel settings
    if webchat_host := os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS"):
        if "channels" not in config:
            config["channels"] = {}
        config["channels"]["webchat"] = {
            "enabled": True,
            "host": webchat_host,
            "port": int(os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765")),
            "allowFrom": ["*"],
        }

    # MCP LMS server settings
    if lms_backend_url := os.environ.get("NANOBOT_LMS_BACKEND_URL"):
        if "tools" not in config or "mcpServers" not in config["tools"]:
            config["tools"] = config.get("tools", {})
            config["tools"]["mcpServers"] = config["tools"].get("mcpServers", {})
        if "lms" not in config["tools"]["mcpServers"]:
            config["tools"]["mcpServers"]["lms"] = {
                "command": "python",
                "args": ["-m", "mcp_lms"],
            }
        if "env" not in config["tools"]["mcpServers"]["lms"]:
            config["tools"]["mcpServers"]["lms"]["env"] = {}
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = (
            lms_backend_url
        )

    if lms_api_key := os.environ.get("NANOBOT_LMS_API_KEY"):
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = lms_api_key

    # MCP Webchat server settings (for structured UI)
    if webchat_ui_url := os.environ.get("NANOBOT_WEBSOCKET_UI_RELAY_URL"):
        if "tools" not in config:
            config["tools"] = {}
        if "mcpServers" not in config["tools"]:
            config["tools"]["mcpServers"] = {}
        config["tools"]["mcpServers"]["webchat"] = {
            "command": "python",
            "args": ["-m", "mcp_webchat"],
            "env": {
                "NANOBOT_WEBSOCKET_UI_RELAY_URL": webchat_ui_url,
                "NANOBOT_WEBSOCKET_UI_TOKEN": os.environ.get(
                    "NANOBOT_WEBSOCKET_UI_TOKEN", ""
                ),
            },
        }

    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Using config: {resolved_path}", file=sys.stderr)

    # Launch nanobot gateway
    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--config",
            str(resolved_path),
            "--workspace",
            str(workspace_dir),
        ],
    )


if __name__ == "__main__":
    main()
