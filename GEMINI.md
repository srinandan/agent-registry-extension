# Agent Registry Extension

Welcome to the **Agent Registry** extension for the Gemini CLI! This extension provides you with direct access to Google Cloud's Agent Registry via the remote `agentregistry` MCP server and a set of rich `gcloud` shell command fallback skills.

## 🚨 CRITICAL INSTRUCTIONS: MCP vs GCLOUD 🚨

1. **Check for the MCP Server**: Before performing any action, check if the `agentregistry` MCP server is available to you. Check your available tools. If `list_agents`, `create_service`, or `search_mcp_servers` are present, the MCP path is active.
2. **Retrieve Project ID**: Every MCP tool requires a `parent` or `name` formatted with the Google Cloud Project ID (e.g. `projects/{project_id}/locations/us-central1`).
   - You MUST run `run_shell_command("gcloud config get-value project")` to fetch the default project.
   - If no project is set and the user didn't provide one, **ask the user for the project ID** before attempting to use an MCP tool. Do NOT guess the project ID.
3. **If the MCP server is ENABLED**: You MUST prioritize using these native MCP tools over running `gcloud` shell commands. This is the preferred, fastest, and safest method.
4. **Confirmation Guard for Destructive Operations**: For any destructive operation (e.g., delete) — via MCP OR gcloud — always summarize what will happen and ask: "Ready to proceed? (yes/no)" before executing.
5. **If the MCP server is NOT ENABLED**:
   - Briefly inform the user that they can enable the Agent Registry MCP Server in their global `~/.gemini/settings.json` for a better experience, and point them to the docs if needed. Only suggest enabling MCP if this is the first time this session the user has invoked the fallback path.
   - **FALLBACK**: Use the `run_shell_command` tool to execute the `gcloud alpha agent-registry` commands as detailed in the `SKILL.md`.

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

### Quick Commands

- **Dashboards**: Run `/dashboard:agents` or `/dashboard:mcp` to run bash scripts that output quick consolidated views.

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

## Developer Instructions (Local Testing)

1. Open your terminal and navigate to the root directory of this extension.
2. Link the extension for local development:
   ```bash
   gemini extensions link .
   ```
3. Restart your Gemini CLI session.
4. Verify the extension is loaded by running `/extensions list`.
