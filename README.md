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
2. **Run cells 1-11** to set up the server
3. **Run test cells 14-32** to see MCP in action
4. **Copy the public URL** from the output
5. **Open [MCP Inspector](https://inspector.anthropic.com)**
6. **Connect and test** your MCP server!

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

The notebook includes automatic public URL generation via ngrok, allowing students to test with [MCP Inspector](https://inspector.anthropic.com):

1. Start the server in the notebook (Cell 11)
2. Copy the public URL (e.g., `https://abc123.ngrok.io/sse`)
3. Open MCP Inspector
4. Enter the URL and click "Connect"
5. Explore and test all tools interactively!

**Benefits:**
- Visual interface for testing
- No additional coding required
- See full MCP protocol messages
- Great for debugging and demonstrations

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

## 🎓 Educational Use Cases

### For Students
- Learn by doing with immediate feedback
- See MCP protocol messages in action
- Experiment with modifications
- Build portfolio projects

### For Instructors
- Ready-to-use teaching material
- No setup required (runs in Colab)
- Includes all necessary explanations
- Can be extended with exercises

### Suggested Exercises

1. **Add Search Tool** - Implement `search_customers(query)`
2. **Add Pagination** - Modify `list_customers` to support pagination
3. **Add Validation** - Enhance email/phone format validation
4. **Add Statistics** - Create tool for customer analytics
5. **Add Authentication** - Implement API key validation

## 🔗 Resources

- **MCP Specification**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **MCP Python SDK**: [GitHub](https://github.com/modelcontextprotocol/python-sdk)
- **MCP Inspector**: [inspector.anthropic.com](https://inspector.anthropic.com)
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
