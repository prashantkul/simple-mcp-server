"""Customer Management Agent Configuration"""
import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

# Get MCP server URL from environment variable
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")

if not MCP_SERVER_URL:
    raise ValueError(
        "MCP_SERVER_URL environment variable is required. "
        "Set it to your MCP server endpoint (e.g., https://xxxx.ngrok.io/mcp)"
    )

# Create the agent
root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="customer_management_agent",
    description="An AI agent that helps manage customer data using MCP tools",
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=MCP_SERVER_URL
            )
        )
    ],
    system_instruction="""You are a helpful customer management assistant.

You have access to a customer database through MCP tools. Use these tools to help users:
- Get information about specific customers
- List all customers or filter by status
- Add new customers
- Update customer information
- Disable or activate customer accounts

Always provide clear, friendly responses. When performing operations, explain what you're doing.
Format customer information in a clear, readable way."""
)
