# Agent Registry Extension

Welcome to the **Agent Registry** extension for the Gemini CLI! This extension provides you with direct access to Google Cloud's Agent Registry via the remote `agentregistry_prod` MCP server.

## Capabilities & Instructions

With this extension enabled, you can manage resources on Google Cloud's Agent Registry using native MCP tools. **You must prefer these MCP tools over running `gcloud` shell commands.**

Available MCP tools provided by `agentregistry_prod`:
- `list_agents`: Lists Agents in a given project and location (`parent` format: `projects/{project}/locations/{location}`).
- `get_agent`: Gets details of a single Agent (`name` format: `projects/{project}/locations/{location}/agents/{agent}`).
- `search_agents`: Search for Agents in a given project and location.
- `list_mcp_servers`: Lists MCP Servers.
- `get_mcp_server`: Gets details of an MCP Server.
- `search_mcp_servers`: Search for MCP Servers.
- `list_endpoints`: Lists Endpoints.
- `get_endpoint`: Gets details of an Endpoint.
- `list_services`: Lists Services.
- `get_service`: Gets details of a Service.
- `create_service`: Creates a new Service (Agent, Endpoint, or MCP Server).
- `update_service`: Updates a Service.
- `delete_service`: Deletes a Service.

### Quick Commands

- **Dashboards**: Run `/dashboard:agents` or `/dashboard:mcp` to run bash scripts that output quick consolidated views.

## Developer Instructions (Local Testing)

1. Open your terminal and navigate to the root directory of this extension.
2. Link the extension for local development:
   ```bash
   gemini extensions link .
   ```
3. Restart your Gemini CLI session.
4. Verify the extension is loaded by running `/extensions list` and test using `list_agents` with `parent: projects/{project}/locations/{location}`.
