"""
MCP (Model Context Protocol) Server for Customer Management.
Implements MCP protocol over HTTP using Server-Sent Events (SSE).
"""

from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import json
import logging
import sys
from typing import Dict, Any

from config import Config
from database import DatabaseManager

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize database
db_manager = DatabaseManager(Config.get_db_path())

# MCP Tools Definition
MCP_TOOLS = [
    {
        "name": "get_customer",
        "description": "Retrieve a specific customer by their ID. Returns customer details including name, email, phone, and status.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "The unique ID of the customer to retrieve"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "list_customers",
        "description": "List all customers in the database. Can optionally filter by status (active or disabled).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["active", "disabled"],
                    "description": "Optional filter by customer status"
                }
            }
        }
    },
    {
        "name": "add_customer",
        "description": "Add a new customer to the database. Name is required, email and phone are optional.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Customer's full name (required)"
                },
                "email": {
                    "type": "string",
                    "description": "Customer's email address (optional)"
                },
                "phone": {
                    "type": "string",
                    "description": "Customer's phone number (optional)"
                }
            },
            "required": ["name"]
        }
    },
    {
        "name": "update_customer",
        "description": "Update an existing customer's information. Provide the customer ID and the fields to update.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "The unique ID of the customer to update"
                },
                "name": {
                    "type": "string",
                    "description": "New name (optional)"
                },
                "email": {
                    "type": "string",
                    "description": "New email (optional)"
                },
                "phone": {
                    "type": "string",
                    "description": "New phone (optional)"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "disable_customer",
        "description": "Disable a customer account by setting their status to 'disabled'.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "The unique ID of the customer to disable"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "activate_customer",
        "description": "Activate a customer account by setting their status to 'active'.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "The unique ID of the customer to activate"
                }
            },
            "required": ["customer_id"]
        }
    }
]


def create_sse_message(data: Dict[str, Any]) -> str:
    """
    Format a message for Server-Sent Events (SSE).
    SSE format: 'data: {json}\n\n'
    """
    return f"data: {json.dumps(data)}\n\n"


def handle_initialize(message: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle MCP initialize request.
    This is the first message in the MCP protocol handshake.
    """
    logger.info("Handling initialize request")
    return {
        "jsonrpc": "2.0",
        "id": message.get("id"),
        "result": {
            "protocolVersion": Config.PROTOCOL_VERSION,
            "capabilities": {
                "tools": {},  # We support tools
            },
            "serverInfo": {
                "name": Config.SERVER_NAME,
                "version": Config.SERVER_VERSION
            }
        }
    }


def handle_tools_list(message: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle tools/list request.
    Returns the list of available tools.
    """
    logger.info("Handling tools/list request")
    return {
        "jsonrpc": "2.0",
        "id": message.get("id"),
        "result": {
            "tools": MCP_TOOLS
        }
    }


def handle_tools_call(message: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle tools/call request.
    Executes the requested tool and returns the result.
    """
    params = message.get("params", {})
    tool_name = params.get("name")
    arguments = params.get("arguments", {})

    logger.info(f"Handling tools/call request for tool: {tool_name}")

    # Map tool names to database manager methods
    tool_functions = {
        "get_customer": db_manager.get_customer,
        "list_customers": db_manager.list_customers,
        "add_customer": db_manager.add_customer,
        "update_customer": db_manager.update_customer,
        "disable_customer": db_manager.disable_customer,
        "activate_customer": db_manager.activate_customer,
    }

    if tool_name not in tool_functions:
        logger.warning(f"Tool not found: {tool_name}")
        return {
            "jsonrpc": "2.0",
            "id": message.get("id"),
            "error": {
                "code": -32601,
                "message": f"Tool not found: {tool_name}"
            }
        }

    try:
        # Call the tool function with the provided arguments
        result = tool_functions[tool_name](**arguments)

        return {
            "jsonrpc": "2.0",
            "id": message.get("id"),
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2)
                    }
                ]
            }
        }
    except TypeError as e:
        logger.error(f"Invalid arguments for tool {tool_name}: {e}")
        return {
            "jsonrpc": "2.0",
            "id": message.get("id"),
            "error": {
                "code": -32602,
                "message": f"Invalid arguments: {str(e)}"
            }
        }
    except Exception as e:
        logger.error(f"Tool execution error for {tool_name}: {e}", exc_info=True)
        return {
            "jsonrpc": "2.0",
            "id": message.get("id"),
            "error": {
                "code": -32603,
                "message": f"Tool execution error: {str(e)}"
            }
        }


def process_mcp_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process an MCP message and route it to the appropriate handler.
    """
    method = message.get("method")

    if method == "initialize":
        return handle_initialize(message)
    elif method == "tools/list":
        return handle_tools_list(message)
    elif method == "tools/call":
        return handle_tools_call(message)
    else:
        logger.warning(f"Unknown method: {method}")
        return {
            "jsonrpc": "2.0",
            "id": message.get("id"),
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            }
        }


# Flask Routes

@app.route('/mcp', methods=['POST'])
def mcp_endpoint():
    """
    Main MCP endpoint for MCP communication.
    Receives MCP messages and streams responses using Server-Sent Events.
    """
    # Get the MCP message from the request
    try:
        message = request.get_json()
        if not message:
            raise ValueError("Empty request body")
    except Exception as e:
        logger.error(f"Failed to parse request: {e}")
        return jsonify({
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": -32700,
                "message": f"Parse error: {str(e)}"
            }
        }), 400

    def generate():
        try:
            logger.info(f"Received MCP message: {message.get('method')}")

            # Process the message
            response = process_mcp_message(message)

            logger.debug(f"Sending response: {response}")

            # Send the response as SSE
            yield create_sse_message(response)

        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            error_response = {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            yield create_sse_message(error_response)

    return Response(generate(), mimetype='text/event-stream')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify server is running."""
    return jsonify({
        "status": "healthy",
        "server": Config.SERVER_NAME,
        "version": Config.SERVER_VERSION,
        "protocol": Config.PROTOCOL_VERSION
    })


@app.route('/', methods=['GET'])
def index():
    """Root endpoint with server information."""
    return jsonify({
        "name": Config.SERVER_NAME,
        "version": Config.SERVER_VERSION,
        "protocol": Config.PROTOCOL_VERSION,
        "endpoints": {
            "mcp": "/mcp (POST)",
            "health": "/health (GET)"
        },
        "tools": [tool["name"] for tool in MCP_TOOLS]
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "error": "Not found",
        "message": "The requested endpoint does not exist"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500


if __name__ == '__main__':
    try:
        # Validate configuration
        Config.validate()

        logger.info(f"Starting {Config.SERVER_NAME} v{Config.SERVER_VERSION}")
        logger.info(f"MCP Protocol Version: {Config.PROTOCOL_VERSION}")
        logger.info(f"Database: {Config.get_db_path()}")
        logger.info(f"Available tools: {len(MCP_TOOLS)}")

        # Run the Flask application
        app.run(
            host=Config.HOST,
            port=Config.PORT,
            debug=Config.DEBUG
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        sys.exit(1)
