# Agent Registry Extension

Welcome to the **Agent Registry** extension for the Gemini CLI! This extension provides you with direct access to Google Cloud's Agent Registry via the remote `agentregistry_prod` MCP server and a set of rich `gcloud` shell command fallback skills.

## 🚨 CRITICAL INSTRUCTIONS: MCP vs GCLOUD 🚨

1. **Check for the MCP Server**: Before performing any action, check if the `agentregistry_prod` MCP server (and its tools like `list_agents`, `create_service`, `search_mcp_servers`, etc.) is available to you.
2. **If the MCP server is ENABLED**: You MUST prioritize using these native MCP tools over running `gcloud` shell commands. This is the preferred, fastest, and safest method.
3. **If the MCP server is NOT ENABLED**:
   - Briefly inform the user that they can enable the Agent Registry MCP Server in their global `~/.gemini/settings.json` for a better experience, and point them to the docs if needed. (See the example configuration below).
   - **FALLBACK**: Use the `run_shell_command` tool to execute the `gcloud alpha agent-registry` commands as detailed in the `SKILL.md`.

### Example settings.json Configuration for Users

```json
"mcpServers": {
  "agentregistry_prod": {
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

### Quick Commands

- **Dashboards**: Run `/dashboard:agents` or `/dashboard:mcp` to run bash scripts that output quick consolidated views.

## Developer Instructions (Local Testing)

1. Open your terminal and navigate to the root directory of this extension.
2. Link the extension for local development:
   ```bash
   gemini extensions link .
   ```
3. Restart your Gemini CLI session.
4. Verify the extension is loaded by running `/extensions list`.
