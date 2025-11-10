# 🎓 Educational MCP Server Demo: Customer Management System

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/prashantkul/simple-mcp-server/blob/claude/mcp-colab-customer-demo-011CUyKnnHZc4KxRNuBxQry3/mcp_customer_demo.ipynb)

An interactive Jupyter notebook for teaching students how to build MCP (Model Context Protocol) servers. This hands-on tutorial demonstrates building a complete customer management system with MCP integration.

## 📚 What is This?

This is an educational resource designed to teach the **Model Context Protocol (MCP)** through a practical, working example. Students will build a full-stack MCP server that exposes customer management tools to AI assistants.

## 🎯 Learning Objectives

By completing this tutorial, students will learn:

- **MCP Protocol Fundamentals** - JSON-RPC 2.0 message structure and SSE streaming
- **Server Implementation** - Building HTTP-based MCP servers with Flask
- **Tool Definition** - Creating MCP tools with proper JSON schemas
- **Database Integration** - Connecting MCP tools to SQLite databases
- **Error Handling** - Implementing robust error responses
- **Testing & Debugging** - Using MCP Inspector for interactive testing
- **Real-World Application** - Building practical AI-integrated systems

## ✨ Features

### 🔧 Complete MCP Server Implementation
- **6 MCP Tools** for customer management (get, list, add, update, disable, activate)
- **Flask-based HTTP server** with Server-Sent Events (SSE) support
- **SQLite database** with sample data
- **Proper error handling** and validation
- **MCP protocol compliance** (specification 2024-11-05)

### 🌐 Public Access & Testing
- **Automatic ngrok tunnel** for public URL generation
- **MCP Inspector integration** - Test directly from the web
- **Local testing** included in the notebook
- **Background server threading** keeps Colab responsive

### 📖 Educational Design
- **Step-by-step instructions** with clear explanations
- **💡 Learning points** throughout the notebook
- **Interactive demonstrations** - 10 test cases included
- **Visual output** with colored terminal display
- **Code comments** explaining MCP-specific concepts
- **Architecture diagrams** and protocol explanations

## 🚀 Quick Start

### For Students:

1. **Click the "Open in Colab" badge** at the top of this README
2. **Set up ngrok** (see [Ngrok Setup](#-ngrok-setup) section below for details)
3. **Run cells 1-11** to set up the server
4. **Run test cells 14-32** to see MCP in action
5. **Copy the public URL** from the output (e.g., `https://xxxx.ngrok.io/mcp`)
6. **Run MCP Inspector**: `npx @modelcontextprotocol/inspector`
7. **Connect and test** your MCP server!

### For Instructors:

This notebook is ready to use in:
- Computer Science courses on API design
- AI/ML courses covering LLM integration
- Software Engineering courses on protocols
- Workshops on building AI tools

**Duration**: ~30-45 minutes to complete all cells

## 📋 What's Included

### Notebook Structure

```
1. 📚 Introduction & MCP Concepts
2. 🔧 Installation & Setup
3. 🗄️ Database Creation (SQLite)
4. 🛠️ CRUD Functions (Python)
5. 🌐 MCP Server Implementation (Flask + SSE)
6. 🚀 Server Startup (with ngrok)
7. 🧪 Interactive Tests (10 demonstrations)
8. 🔍 MCP Inspector Guide
9. 🎯 Server Management Utilities
10. 📝 Summary & Next Steps
```

### Customer Management Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_customer` | Retrieve customer by ID | `customer_id` (int) |
| `list_customers` | List all or filtered customers | `status` (optional: 'active', 'disabled') |
| `add_customer` | Create new customer | `name` (required), `email`, `phone` (optional) |
| `update_customer` | Update customer info | `customer_id` (int), `name`, `email`, `phone` (optional) |
| `disable_customer` | Deactivate account | `customer_id` (int) |
| `activate_customer` | Reactivate account | `customer_id` (int) |

## 🛠️ Technical Stack

- **Python 3.9+** - Core language
- **Flask** - HTTP server framework
- **SQLite** - Embedded database
- **Server-Sent Events (SSE)** - Streaming protocol
- **pyngrok** - Public URL tunneling
- **termcolor** - Colored terminal output
- **JSON-RPC 2.0** - Message protocol

## 🔍 Testing with MCP Inspector

### Launch MCP Inspector

MCP Inspector is a CLI tool that provides a visual interface for testing MCP servers. To launch it:

1. Open a terminal on your local machine (not in Colab)
2. Run the following command:
   ```bash
   npx @modelcontextprotocol/inspector
   ```
3. This will automatically:
   - Download the MCP Inspector tool (if not already installed)
   - Start the inspector server
   - Open your browser to the MCP Inspector interface

### Connect to Your Server

1. Start the server in the notebook (Cell 11)
2. Copy the public URL from the output (e.g., `https://abc123.ngrok.io/mcp`)
3. In the MCP Inspector browser interface:
   - Paste the URL in the "Server URL" field
   - Click "Connect"
4. Explore and test all 6 customer management tools interactively!

### Benefits

- **Visual interface** for testing MCP tools
- **No coding required** - point and click testing
- **See full protocol messages** - great for learning
- **Real-time testing** - immediate feedback
- **Debug easily** - see requests and responses

## 📊 Database Schema

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'disabled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Sample Data:** 10 customers (8 active, 2 disabled)

## 💡 Key Concepts Covered

### MCP Protocol Basics
- JSON-RPC 2.0 message format
- Three core methods: `initialize`, `tools/list`, `tools/call`
- Tool definition with JSON Schema
- Server capabilities negotiation

### Server-Sent Events (SSE)
- Real-time streaming communication
- SSE message formatting: `data: {json}\n\n`
- Generator functions in Flask
- Request context management

### Error Handling
- Proper MCP error responses
- Database error handling
- Input validation
- Meaningful error messages for AI

## 🌐 Ngrok Setup

To enable public access to your MCP server (required for testing with MCP Inspector), you need to set up ngrok:

### 1. Get Ngrok Auth Token

1. Go to [https://ngrok.com](https://ngrok.com)
2. Sign up for a free account
3. Go to your dashboard and copy your auth token

### 2. Add Token to Google Colab Secrets

1. Open your Colab notebook
2. Click the **🔑 (Secrets)** icon in the left sidebar
3. Click **+ Add new secret**
4. Set:
   - **Name**: `NGROK_AUTHTOKEN`
   - **Value**: Paste your auth token from ngrok
5. Toggle **Notebook access** to ON
6. Run Cell 11 to start the server with public URL

### 3. Verify Setup

When Cell 11 runs successfully, you should see:
```
✅ Ngrok authenticated
✅ Public URL: https://xxxx.ngrok.io
📍 MCP Endpoint: https://xxxx.ngrok.io/mcp
```

If you see a warning about missing token, double-check that:
- The secret name is exactly `NGROK_AUTHTOKEN`
- Notebook access is enabled
- You've re-run Cell 11 after adding the secret

### Without Ngrok

If you don't set up ngrok, the server will still work locally within the Colab environment, but you won't be able to test with MCP Inspector.

## 🔗 Resources

- **MCP Specification**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **MCP Python SDK**: [GitHub](https://github.com/modelcontextprotocol/python-sdk)
- **MCP Inspector**: Run with `npx @modelcontextprotocol/inspector`
- **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **SQLite Tutorial**: [sqlite.org/docs.html](https://sqlite.org/docs.html)

## 📝 Testing Summary

See [TESTING_SUMMARY.md](TESTING_SUMMARY.md) for detailed testing documentation including:
- All tests performed
- Issues found and fixed
- Component verification
- Colab compatibility checks

## ⚠️ Known Limitations (Colab-Specific)

- **Temporary Storage**: Database deleted when runtime resets
- **Thread Persistence**: Server continues until runtime reset
- **Localhost Binding**: Direct local access limited to Colab environment
- **No Persistence**: State not saved between sessions

These are **by design** for educational purposes and clearly documented in the notebook.

## 🤝 Contributing

This is an educational resource. Contributions welcome for:
- Additional exercises
- Bug fixes
- Documentation improvements
- Translation to other languages
- Additional MCP examples

## 📄 License

This educational resource is provided as-is for teaching and learning purposes.

## 🙏 Acknowledgments

- **Anthropic** - For the Model Context Protocol specification
- **Flask Community** - For the excellent web framework
- **ngrok** - For tunneling capabilities
- **Google Colab** - For free computing resources

## 📧 Questions or Feedback?

Open an issue in this repository or contribute improvements via pull request!

---

**Happy Learning!** 🚀

*Last Updated: 2025-11-10*
*Notebook Version: v1.0.0*
