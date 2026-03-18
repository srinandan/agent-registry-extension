# Google Cloud Agent Registry Extension for Gemini CLI

[![CI](https://github.com/srinandan/agent-registry-extension/actions/workflows/ci.yml/badge.svg)](https://github.com/srinandan/agent-registry-extension/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/srinandan/agent-registry-extension)](https://github.com/srinandan/agent-registry-extension/releases)
[![License](https://img.shields.io/github/license/srinandan/agent-registry-extension)](LICENSE)

An extension for the Gemini CLI to interact with Google Cloud's Agent Registry using the `agentregistry` MCP server and fallback `gcloud alpha agent-registry` commands.

## Features

- **Direct MCP Server Integration**: Configure the native MCP server in your `~/.gemini/settings.json` to leverage fast and native tool interactions for Agent Registry.
- **Automated Authentication**: Helps with `gcloud auth login` and project configuration when using shell tools.
- **Resource Management**: Create, list, describe, and delete Agents, MCP Servers, and Endpoints.
- **Dashboards**: Generate quick views of your Agents and MCP servers using `/dashboard:agents` and `/dashboard:mcp`.
- **Python ADK Integration**: Specialized support and snippets for the Google Agent Development Kit (ADK).

## Installation

Install the extension by running the following command from your terminal:

```bash
gemini extensions install https://github.com/srinandan/agent-registry-extension
```

You can confirm the installation by starting `gemini` and typing `/extensions list`. The response should include `agent-registry` similar to this:

```
/extensions list

Installed extensions:
  agent-registry (v1.0.0) -
```

## Recommended Setup (Enable MCP Server)

To get the most out of this extension, we highly recommend enabling the native Agent Registry MCP Server in your global `~/.gemini/settings.json`:

```json
"mcpServers": {
  "agentregistry": {
    "httpUrl": "https://agentregistry.googleapis.com/mcp",
    "authProviderType": "google_credentials",
    "oauth": {
      "scopes": [
        "https://www.googleapis.com/auth/agentregistry.read-write"
      ]
    }
  }
}
```

## Fallback Usage (Gcloud)

If you choose not to configure the MCP server, this extension acts as a standard Agent Skill, driving the Gemini CLI to execute standard `gcloud` shell commands.

-   *"List my agents in us-central1"*
-   *"Describe the MCP server named github-mcp"*
-   *"Register a new Salesforce agent at https://api.salesforce.com/v1"*

## Prerequisites

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) version **560.0.0** or higher (minimum).
- `gcloud alpha` component version **2026.03.09** or higher (minimum).
- **Google ADK** version **1.26.0** or higher (minimum) for Python integration.
- Proper permissions to access Agent Registry in your Google Cloud project.

## Support
This demo is NOT endorsed by Google or Google Cloud. The repo is intended for educational/hobbyists use only.

## License
This project is licensed under the terms of the [LICENSE](LICENSE) file.
