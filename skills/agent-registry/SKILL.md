---
name: agent-registry
description: "Expertise in Google Cloud Agent Registry. Use when the user asks to manage, list, create, search or delete Agents, MCP Servers, and Endpoints on GCP."
metadata:
  author: "Srinandan"
  version: "1.0.0"
---

# Google Cloud Agent Registry Expert

You are an expert in managing Google Cloud's Agent Registry.

## 🚨 CRITICAL INSTRUCTIONS: MCP vs GCLOUD 🚨

1. **Check for the MCP Server**: Before performing any action, check if the `agentregistry` MCP server (and its tools like `list_agents`, `create_service`, `search_mcp_servers`, etc.) is available to you.
2. **Retrieve Project ID**: Every MCP tool requires a `parent` or `name` formatted with the Google Cloud Project ID (e.g. `projects/{project_id}/locations/us-central1`).
   - You MUST run `run_shell_command("gcloud config get-value project")` to fetch the default project.
   - If no project is set and the user didn't provide one, **ask the user for the project ID** before attempting to use an MCP tool. Do NOT guess the project ID.
3. **If the MCP server is ENABLED**: You MUST prioritize using these native MCP tools over running `gcloud` shell commands. This is the preferred, fastest, and safest method.
4. **Confirmation Guard for Destructive Operations**: For any destructive operation (e.g., delete) — via MCP OR gcloud — always summarize what will happen and ask: "Ready to proceed? (yes/no)" before executing.
5. **If the MCP server is NOT ENABLED**:
   - Briefly inform the user that they can enable the Agent Registry MCP Server in their global `~/.gemini/settings.json` for a better experience, and point them to the docs if needed. Only suggest enabling MCP if this is the first time this session the user has invoked the fallback path.
   - **FALLBACK**: Use the `run_shell_command` tool to execute the `gcloud alpha agent-registry` commands as detailed in the "Detailed Command Reference" section below.

### Example settings.json Configuration for Users

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

## Detailed Command Reference

All commands support `--location` (required) and `--project` (optional).

| Group | Commands |
|-------|----------|
| `agents` | `list`, `describe` |
| `mcp-servers` | `list`, `describe` |
| `endpoints` | `list`, `describe` |
| `services` | `create`, `list`, `describe`, `update`, `delete` |
| `operations` | `list`, `describe` |

### Pagination

If output appears truncated or contains a `nextPageToken`, inform the user and ask if they want to fetch the next page.

```bash
# List with pagination
gcloud alpha agent-registry agents list --location=LOCATION --page-size=50
```

### Service Creation Flags

| Flag | Description |
|------|-------------|
| `--display-name` | Human-readable name |
| `--description` | Brief summary of the service |
| `--interfaces` | JSON array of protocol bindings and URLs |
| `--mcp-server-spec-type` | Type: `no-spec`, `tool-spec` |
| `--mcp-server-spec-content`| JSON content of the spec |
| `--agent-spec-type` | Type: `no-spec`, `a2a-agent-card` |
| `--agent-spec-content` | JSON content for `a2a-agent-card` |
| `--endpoint-spec-type` | Type: `no-spec` |

---

## Natural Language → Command Examples

| User says | Command |
|-----------|---------|
| "List my MCP servers" | `gcloud alpha agent-registry mcp-servers list --location=us-central1` |
| "Show me information on agent X" | `gcloud alpha agent-registry agents describe X --location=us-central1` |
| "Register a new GitHub MCP server with this spec..." | `gcloud alpha agent-registry services create github ... --mcp-server-spec-content='...'` |
| "Check status of operation Y" | `gcloud alpha agent-registry operations describe Y --location=us-central1` |
| "List all registered services" | `gcloud alpha agent-registry services list --location=us-central1` |
| "Show all agents where the runtime is reasoningEngine" | `gcloud alpha agent-registry agents list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"` |
| "Show agents with identity containing 'service-432423'" | `gcloud alpha agent-registry agents list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeIdentity\".principal:service-432423"` |
| "Create a new A2A agent called my-a2a" | `gcloud alpha agent-registry services create my-a2a --agent-spec-type=a2a-agent-card ...` |
| "Show me all MCP servers where the runtime is my-runtime" | `gcloud alpha agent-registry mcp-servers list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:my-runtime"` |
| "List all global agents" | `gcloud alpha agent-registry agents list --location=global` |
| "List global MCP servers" | `gcloud alpha agent-registry mcp-servers list --location=global` |
| "show me a dashboard for my agents" | `/dashboard:agents` |
| "show me a dashboard for my mcp servers" | `/dashboard:mcp` |
| "Change display name of gemini-models to 'Vertex AI Model Garden'" | `gcloud alpha agent-registry services update gemini-models --display-name="..." --location=us-central1` |
| "Which agents in us-central1 are based on reasoning engine?" | `gcloud alpha agent-registry agents list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"` |
| "List all vertex ai agents" | `gcloud alpha agent-registry agents list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"` |
| "Show agents with agent engine runtime" | `gcloud alpha agent-registry agents list --location=us-central1 --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"` |
| "Which MCP Server has a tool named search_documents?" | `gcloud alpha agent-registry mcp-servers list --location=us-central1 --filter="tools.name:search_documents"` |
| "Find all servers with the get_document tool" | `gcloud alpha agent-registry mcp-servers list --location=us-central1 --filter="tools.name:get_document"` |

---

## Advanced Filtering

To filter resources based on nested attributes with special characters (like dots or slashes), use double quotes around the key segments in the `--filter` flag.

> [!WARNING]
> The double-quote escaping shown below (`\"`) works in bash/zsh. Windows CMD or PowerShell users may need different escaping (e.g., `"` or ``` `"` ``) for nested attribute keys.

**Mapping Tips**:
- Map **"runtime"** to `attributes."agentregistry.googleapis.com/system/RuntimeReference".uri`.
- Map **"identity"** to `attributes."agentregistry.googleapis.com/system/RuntimeIdentity".principal`.
- Map **"tool name"** or **"tool"** to `tools.name` for MCP Server list commands.
- **Synonyms**: "agent engine", "reasoning engine", and "vertex ai" all refer to the runtime value **`reasoningEngine`**.
- **Context Filtering**: If the user asks about "agents", use the `agents` resource group (e.g., `gcloud alpha agent-registry agents list`), not `mcp-servers` or `endpoints`.

```bash
# Example: Show all agents where the runtime is reasoningEngine
gcloud alpha agent-registry agents list \
  --location=us-central1 \
  --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeReference\".uri:reasoningEngine"

# Example: Show agents where identity contains a specific service account ID
gcloud alpha agent-registry agents list \
  --location=us-central1 \
  --filter="attributes.\"agentregistry.googleapis.com/system/RuntimeIdentity\".principal:service-432423"
```

---

## GKE Based Agents

When a user asks to configure, annotate, or manage **GKE based agents** or GKE deployments for the Agent Registry, you should assist them by annotating their Kubernetes Deployment YAML files with the `apphub.cloud.google.com/functional-type` annotation.

Follow these steps:
1. **Ask for the Folder**: Ask the user if they want to process files in the current directory (`.`) or provide a specific folder path.
2. **Ask for the Type**: Ask whether the functional type should be `AGENT` or `MCP_SERVER`.
3. **Run the Script**: Once you have both inputs, use the `run_shell_command` tool to execute the provided pure-Python script:
   ```bash
   python3 scripts/annotate_gke.py <folder> <TYPE>
   ```
4. **Warn the User**: Inform the user that the script modifies the files in-place and preserves their formatting and comments.

---

## Python ADK Integration

The Google Agent Development Kit (ADK) allows seamless integration with the Agent Registry.

### 1. Requirements & Setup
- **ADK Version**: 1.26.0 or higher (minimum).
- **Installation**:
  ```bash
  # Using pip
  pip install --upgrade google-adk

  # Using uv
  uv add google-adk
  ```

### 2. Import & Usage
Add the following import to your Python code:
```python
from google.adk.integrations.agent_registry import AgentRegistry
```

### 3. Invoking an MCP Server from Registry
Use this snippet to retrieve and use an MCP toolset:
```python
import os
from google.adk.integrations.agent_registry import AgentRegistry

# Initialize registry client
registry = AgentRegistry(project_id=SESSION_PROJECT, location=SESSION_LOCATION)

# Retrieve MCP Toolset using the full resource name
# Example resource name: projects/PRJ/locations/LOC/mcpServers/SERVER_NAME
mcp_toolset = registry.get_mcp_toolset(
    f"projects/{SESSION_PROJECT}/locations/{SESSION_LOCATION}/mcpServers/{MCP_SERVER_NAME}"
)
```

### 4. Integrating a Remote A2A Agent
Use this snippet to use a registry agent as a sub-agent:
```python
from google.adk import Agent, Gemini, types
from google.adk.integrations.agent_registry import AgentRegistry

# Initialize registry client
registry = AgentRegistry(project_id=SESSION_PROJECT, location=SESSION_LOCATION)

# Retrieve Remote A2A Agent
remote_agent = registry.get_remote_a2a_agent(
    f"projects/{SESSION_PROJECT}/locations/{SESSION_LOCATION}/agents/{AGENT_NAME}"
)

# Define a new Agent with the remote agent as a sub-agent
help_agent = Agent(
    name="help_agent",
    description="Helpful AI Assistant that uses a remote agent.",
    model=Gemini(model="gemini-2.5-flash"),
    sub_agents=[remote_agent]
)
```

---

## Interactive Prompts

Only ask if still missing after checking session context:
- **location**: "Which region? (e.g. `us-central1`)" — only if `compute/region` was not set
- **project**: "Which project?" — only if `project` was not set in gcloud config
- **A2A Agent Card**: For A2A agents, explicitly ask: _"Please paste the contents of your `agent_card.json` file."_ and use it for `--agent-spec-content`.
- **MCP Server Spec**: For MCP servers, explicitly ask: _"Please paste the contents of your MCP server spec JSON file."_ and use it for `--mcp-server-spec-content`.

Only ask for what's strictly needed — don't overwhelm the user.

---

## Error Handling

If a command fails:
1. Check if `gcloud alpha` component is installed.
   - Required (minimum): **Google Cloud SDK 560.0.0 or higher**
   - Required (minimum): **alpha component 2026.03.09 or higher**
2. Verify the `--location` (some resources may be in `global` or specific regions).
3. Ensure JSON payloads for `--interfaces` or specs are correctly quoted for the shell.
4. Check project permissions for `agentregistry.googleapis.com`.

### Bug Reporting

If you encounter an unexpected problem, bug, or a failure that you cannot resolve:
1. Ask the user if they would like to create a GitHub issue for this bug.
2. If the user agrees, generate a descriptive title and body for the issue based on the error context.
3. Show the user the proposed issue content and the command to create it.
4. Ask for final approval before running the command.
5. Once approved, use the `gh` CLI to create the issue in the repository. For example:
   ```bash
   gh issue create --repo srinandan/agent-registry-extension --title "Title of the bug" --body "Description of the bug, including error messages and steps to reproduce."
   ```

---

## ADK Reference

If the user asks about ADK, read `references/adk-docs.md` for instructions
on which URL to fetch.
