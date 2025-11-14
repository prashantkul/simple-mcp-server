"""
Simple test client for MCP Customer Management Server.
Tests the MCP protocol endpoints.
"""

import requests
import json
import sys


class MCPClient:
    """Simple MCP protocol client for testing."""

    def __init__(self, base_url: str):
        """
        Initialize MCP client.

        Args:
            base_url: Base URL of the MCP server (e.g., http://localhost:8080)
        """
        self.base_url = base_url.rstrip('/')
        self.mcp_url = f"{self.base_url}/mcp"

    def send_message(self, method: str, params: dict = None, message_id: int = 1):
        """
        Send an MCP message to the server.

        Args:
            method: MCP method name
            params: Method parameters
            message_id: Message ID

        Returns:
            Parsed response or None if error
        """
        message = {
            "jsonrpc": "2.0",
            "id": message_id,
            "method": method
        }

        if params:
            message["params"] = params

        print(f"\n{'='*60}")
        print(f"REQUEST: {method}")
        print(f"{'='*60}")
        print(json.dumps(message, indent=2))

        try:
            response = requests.post(
                self.mcp_url,
                json=message,
                headers={'Content-Type': 'application/json'},
                stream=True,
                timeout=10
            )

            # Parse SSE response
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data = json.loads(line_str[6:])

                        print(f"\nRESPONSE:")
                        print(json.dumps(data, indent=2))

                        return data

        except Exception as e:
            print(f"\nERROR: {e}")
            return None

    def health_check(self):
        """Check server health."""
        print(f"\n{'='*60}")
        print("HEALTH CHECK")
        print(f"{'='*60}")

        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            print(json.dumps(response.json(), indent=2))
            return response.status_code == 200
        except Exception as e:
            print(f"ERROR: {e}")
            return False

    def initialize(self):
        """Initialize MCP connection."""
        return self.send_message(
            method="initialize",
            params={
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            },
            message_id=1
        )

    def list_tools(self):
        """List available tools."""
        return self.send_message(method="tools/list", message_id=2)

    def list_customers(self, status: str = None):
        """List customers."""
        arguments = {}
        if status:
            arguments["status"] = status

        return self.send_message(
            method="tools/call",
            params={
                "name": "list_customers",
                "arguments": arguments
            },
            message_id=3
        )

    def get_customer(self, customer_id: int):
        """Get customer by ID."""
        return self.send_message(
            method="tools/call",
            params={
                "name": "get_customer",
                "arguments": {"customer_id": customer_id}
            },
            message_id=4
        )

    def add_customer(self, name: str, email: str = None, phone: str = None):
        """Add new customer."""
        arguments = {"name": name}
        if email:
            arguments["email"] = email
        if phone:
            arguments["phone"] = phone

        return self.send_message(
            method="tools/call",
            params={
                "name": "add_customer",
                "arguments": arguments
            },
            message_id=5
        )


def main():
    """Run test suite."""
    # Get server URL from command line or use default
    server_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"

    print(f"\nTesting MCP Server at: {server_url}")
    print("="*60)

    client = MCPClient(server_url)

    # Test 1: Health check
    if not client.health_check():
        print("\nFailed to connect to server!")
        sys.exit(1)

    # Test 2: Initialize
    init_response = client.initialize()
    if not init_response or 'error' in init_response:
        print("\nInitialization failed!")
        sys.exit(1)

    # Test 3: List tools
    tools_response = client.list_tools()
    if tools_response and 'result' in tools_response:
        tools = tools_response['result']['tools']
        print(f"\nFound {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")

    # Test 4: List all customers
    client.list_customers()

    # Test 5: Get specific customer
    client.get_customer(customer_id=1)

    # Test 6: List active customers only
    client.list_customers(status="active")

    # Test 7: Add new customer
    client.add_customer(
        name="Test Customer",
        email="test@example.com",
        phone="+1-555-TEST"
    )

    print(f"\n{'='*60}")
    print("ALL TESTS COMPLETED")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
