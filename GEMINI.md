# Agent Registry Extension

Welcome to the **Agent Registry** extension for the Gemini CLI! This extension provides you with tools, skills, and dashboards to seamlessly interact with Google Cloud's Agent Registry.

## Capabilities

With this extension enabled, you can:
- **Manage resources**: List, describe, create, update, and delete Agents, MCP Servers, and Endpoints on Google Cloud's Agent Registry.
- **Run Dashboards**: Use `/dashboard:agents` or `/dashboard:mcp` to fetch summaries of all agents and MCP servers across your configured Google Cloud project (both globally and in `us-central1`).
- **Use the remote MCP server**: You have access to the `agentregistry_prod` MCP server natively to interact directly with the backend API.

## Developer Instructions (Local Testing)

If you are developing or testing this extension locally, follow these steps to load it into the Gemini CLI:

1. Open your terminal and navigate to the root directory of this extension.
2. Link the extension for local development:
   ```bash
   gemini extensions link .
   ```
3. Restart your Gemini CLI session.
4. Verify the extension is loaded by running `/extensions list`.
5. Test the dashboards:
   - Run `/dashboard:agents`
   - Run `/dashboard:mcp`
6. Test asking a natural language query like *"List all agents in us-central1"* to ensure the skill and MCP tools trigger correctly.
