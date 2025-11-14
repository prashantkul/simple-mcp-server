# MCP Customer Management Server

A production-ready MCP (Model Context Protocol) server for customer management, implementing MCP protocol over HTTP using Server-Sent Events (SSE). This server exposes customer management tools through the MCP protocol.

## Features

- **MCP Protocol Support**: Implements MCP 2024-11-05 specification
- **Server-Sent Events**: Streaming responses using SSE
- **RESTful API**: HTTP-based MCP communication
- **SQLite Database**: Lightweight customer data storage
- **6 Customer Management Tools**:
  - `get_customer`: Retrieve customer by ID
  - `list_customers`: List all customers (with optional status filter)
  - `add_customer`: Create new customer
  - `update_customer`: Update customer information
  - `disable_customer`: Disable customer account
  - `activate_customer`: Activate customer account

## Architecture

```
app.py          - Main Flask application and MCP protocol implementation
database.py     - Database manager with all CRUD operations
config.py       - Configuration management
Dockerfile      - Container definition for Cloud Run
requirements.txt - Python dependencies
```

## Local Development

### Prerequisites

- Python 3.11 or higher
- pip

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python app.py
```

The server will start on `http://localhost:8080` by default.

### Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | Server port |
| `HOST` | `0.0.0.0` | Server host |
| `DEBUG` | `false` | Debug mode |
| `DB_PATH` | `./data/customers.db` | SQLite database path |
| `LOG_LEVEL` | `INFO` | Logging level |

### Testing Locally

Test the health endpoint:
```bash
curl http://localhost:8080/health
```

Test MCP initialize:
```bash
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "test-client", "version": "1.0.0"}
    }
  }'
```

## Cloud Run Deployment

### Prerequisites

- Google Cloud account
- `gcloud` CLI installed and configured
- Docker installed (for local testing)

### Deployment Steps

#### 1. Set up Google Cloud project

```bash
# Set your project ID
export PROJECT_ID="your-project-id"
export REGION="us-central1"
export SERVICE_NAME="mcp-customer-server"

# Configure gcloud
gcloud config set project $PROJECT_ID
```

#### 2. Enable required APIs

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

#### 3. Build and deploy to Cloud Run

```bash
# Build and deploy in one command
gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10 \
  --timeout 300
```

Or build separately:

```bash
# Build container image
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1
```

#### 4. Get the service URL

```bash
gcloud run services describe $SERVICE_NAME \
  --region $REGION \
  --format 'value(status.url)'
```

### Environment Variables for Cloud Run

Set environment variables during deployment:

```bash
gcloud run deploy $SERVICE_NAME \
  --set-env-vars LOG_LEVEL=INFO \
  --set-env-vars DEBUG=false
```

Or update existing service:

```bash
gcloud run services update $SERVICE_NAME \
  --region $REGION \
  --set-env-vars LOG_LEVEL=DEBUG
```

### Persistent Storage (Optional)

For persistent SQLite database, you can mount Cloud Storage:

1. Create a bucket:
```bash
gcloud storage buckets create gs://${PROJECT_ID}-mcp-data --location=$REGION
```

2. Mount during deployment (requires Cloud Run with persistent volumes - preview feature)

Alternatively, consider using Cloud SQL for production workloads.

## MCP Inspector Testing

After deployment, test with MCP Inspector:

1. Install MCP Inspector:
```bash
npx @modelcontextprotocol/inspector
```

2. Open in browser and connect to your deployed URL:
```
https://your-service-url.run.app/mcp
```

3. Test the available tools through the inspector UI

## API Endpoints

### MCP Endpoint
- **POST** `/mcp` - Main MCP protocol endpoint (SSE streaming)

### Utility Endpoints
- **GET** `/` - Server information
- **GET** `/health` - Health check

## MCP Protocol Messages

### Initialize
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "client", "version": "1.0.0"}
  }
}
```

### List Tools
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

### Call Tool (Example: List Customers)
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "list_customers",
    "arguments": {"status": "active"}
  }
}
```

## Database Schema

### Customers Table
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

The database is automatically initialized with 10 sample customers on first run.

## Monitoring

### View Logs
```bash
gcloud run services logs read $SERVICE_NAME \
  --region $REGION \
  --limit 50
```

### Follow Logs in Real-time
```bash
gcloud run services logs tail $SERVICE_NAME \
  --region $REGION
```

## Security Considerations

1. **Authentication**: The default deployment allows unauthenticated access. For production:
   ```bash
   gcloud run deploy $SERVICE_NAME \
     --no-allow-unauthenticated
   ```

2. **CORS**: Currently allows all origins. Modify `app.py` to restrict origins:
   ```python
   CORS(app, origins=["https://your-domain.com"])
   ```

3. **Rate Limiting**: Consider implementing rate limiting for production use

4. **Database**: SQLite is suitable for development. For production, consider Cloud SQL

## Troubleshooting

### Check service status
```bash
gcloud run services describe $SERVICE_NAME --region $REGION
```

### Test health endpoint
```bash
curl https://your-service-url.run.app/health
```

### View recent errors
```bash
gcloud run services logs read $SERVICE_NAME \
  --region $REGION \
  --filter="severity>=ERROR" \
  --limit 20
```

## Cost Optimization

Cloud Run pricing is based on:
- CPU and memory allocation
- Number of requests
- Request duration

To optimize costs:
1. Set appropriate min/max instances
2. Configure auto-scaling properly
3. Use smaller memory allocation if possible
4. Monitor usage with Cloud Monitoring

## License

MIT License - Feel free to use this for your projects

## Support

For issues or questions:
- Check Cloud Run logs
- Review MCP protocol specification
- Test locally before deploying

## Next Steps

1. Implement authentication
2. Add more customer management features
3. Integrate with external CRM systems
4. Add data validation and sanitization
5. Implement request rate limiting
6. Add metrics and monitoring
7. Set up CI/CD pipeline
