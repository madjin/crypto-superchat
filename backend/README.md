# Backend - AI16Z Memo Overlay

FastAPI backend that monitors Solana blockchain for AI16Z token transfers, extracts memo messages, and delivers them to frontend overlays via WebSocket with moderation capabilities.

## Quick Start

1. **Install dependencies:**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Run the server:**
   ```bash
   uvicorn main:app --reload --port 8765
   ```

4. **Verify it's working:**
   - Health check: http://localhost:8765/health
   - WebSocket: ws://localhost:8765/ws

## Configuration

All configuration is done via the `.env` file.

### Required Environment Variables

```bash
# Solana/Helius Configuration
HELIUS_API_KEY=your_helius_api_key_here
AI16Z_WALLET_ADDRESS=HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC
AI16Z_MINT_ADDRESS=HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC

# Database
DATABASE_URL=sqlite:///./donations.db

# Server Configuration
PORT=8765
HOST=0.0.0.0

# Content Moderation
ENABLE_PROFANITY_FILTER=true
BANNED_WORDS=scam,spam,hack,fake
MIN_DONATION_AMOUNT_USD=1.0
MAX_MEMO_LENGTH=280

# Demo Mode (optional)
DEMO_MODE=false
DEMO_INTERVAL_SECONDS=8
```

### Optional Configuration

```bash
# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log

# Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=100

# WebSocket
MAX_CONNECTIONS=50
CONNECTION_TIMEOUT_SECONDS=300
```

## API Endpoints

### Health Check
```http
GET /health
```
Returns server status and configuration info.

### Admin Dashboard
```http
GET /
```
Serves the admin dashboard interface.

### WebSocket Connection
```
ws://localhost:8765/ws
```
Real-time message delivery to frontend overlays.

## Architecture

### Core Components

- **`main.py`** - FastAPI application with WebSocket server, health endpoints, and CORS configuration
- **`listener.py`** - Blockchain monitoring service that fetches AI16Z transactions and processes memos  
- **`models.py`** - SQLAlchemy database models for donation tracking and moderation queue

### Database Schema

**Donations Table:**
- `id` - Primary key
- `signature` - Transaction signature (unique)
- `amount_sol` - Donation amount in SOL
- `amount_usd` - Donation amount in USD  
- `memo` - Message content
- `sender` - Wallet address of sender
- `timestamp` - Transaction timestamp
- `is_approved` - Moderation status
- `tier` - Donation tier (low/mid/high/whale)

### Message Flow

1. **Blockchain Monitoring**: `listener.py` polls Helius API for new transactions
2. **Transaction Processing**: Extracts memo content and calculates USD amounts
3. **Content Filtering**: Applies profanity filter and validation rules
4. **Database Storage**: Stores donation with pending approval status
5. **Moderation Queue**: Admin can approve/reject via dashboard
6. **WebSocket Delivery**: Approved messages sent to connected overlays

## Moderation System

### Automatic Filtering
- **Profanity Filter**: Blocks messages containing banned words
- **Length Validation**: Enforces maximum memo length
- **Amount Threshold**: Filters donations below minimum USD amount
- **Duplicate Detection**: Prevents duplicate transaction processing

### Manual Moderation
- **Admin Dashboard**: Web interface for reviewing pending donations
- **Approve/Reject**: Real-time moderation with immediate overlay updates
- **Message History**: View all processed donations with timestamps
- **WebSocket Monitoring**: Live connection status and message delivery

### Content Policies
- Messages containing banned words are auto-rejected
- Donations below minimum threshold are filtered out
- Memos exceeding length limits are truncated or rejected
- Duplicate transactions are ignored

## WebSocket Protocol

### Message Types

**Donation Message:**
```json
{
    "type": "donation",
    "data": {
        "amount_sol": 0.5,
        "amount_usd": 25.50,
        "memo": "Great stream!",
        "sender": "wallet_address",
        "tier": "mid",
        "timestamp": "2024-01-01T12:00:00Z"
    }
}
```

**Status Update:**
```json
{
    "type": "status",
    "data": {
        "connected_clients": 3,
        "messages_pending": 5,
        "last_transaction": "2024-01-01T12:00:00Z"
    }
}
```

**Error Message:**
```json
{
    "type": "error",
    "data": {
        "message": "Connection error",
        "code": "WS_ERROR"
    }
}
```

## Development

### Running in Development Mode

```bash
# Install in development mode
pip install -e .

# Run with auto-reload
uvicorn main:app --reload --port 8765 --log-level debug

# Run listener separately (optional)
python listener.py
```

### Testing

```bash
# Run tests
pytest tests/

# Test WebSocket connection
python tests/test_websocket.py

# Test blockchain integration
python tests/test_blockchain.py
```

### Database Management

```bash
# Create database tables
python -c "from models import create_tables; create_tables()"

# Reset database
rm donations.db
python -c "from models import create_tables; create_tables()"

# View database contents
sqlite3 donations.db ".schema"
sqlite3 donations.db "SELECT * FROM donations LIMIT 10;"
```

## Deployment

### Production Configuration

```bash
# Use production WSGI server
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8765

# Or with uvicorn for single process
uvicorn main:app --host 0.0.0.0 --port 8765 --workers 1
```

### Environment Variables for Production

```bash
# Security
SECRET_KEY=your_secret_key_here
DEBUG=false
CORS_ORIGINS=https://yourdomain.com

# Database (consider PostgreSQL for production)
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Monitoring
SENTRY_DSN=your_sentry_dsn_here
```

### Systemd Service (Linux)

```ini
# /etc/systemd/system/crypto-superchat.service
[Unit]
Description=Crypto SuperChat Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/crypto-superchat/backend
Environment=PATH=/path/to/crypto-superchat/backend/.venv/bin
ExecStart=/path/to/crypto-superchat/backend/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8765
Restart=always

[Install]
WantedBy=multi-user.target
```

## Troubleshooting

### Common Issues

**Server won't start:**
- Check if port 8765 is available: `netstat -tuln | grep 8765`
- Verify Python virtual environment is activated
- Check `.env` file exists and has correct format

**No blockchain data:**
- Verify `HELIUS_API_KEY` is valid and has credits
- Check wallet and mint addresses in `.env`
- Monitor logs for API errors: `tail -f app.log`

**WebSocket connections failing:**
- Check firewall settings for port 8765
- Verify CORS settings in production
- Test connection with WebSocket client

**Database errors:**
- Ensure SQLite file permissions are correct
- Check disk space for database growth
- Consider PostgreSQL for high-volume production use

### Monitoring

**Health Check:**
```bash
curl http://localhost:8765/health
```

**WebSocket Status:**
```bash
# Check connected clients
curl http://localhost:8765/status
```

**Log Analysis:**
```bash
# Monitor real-time logs
tail -f app.log

# Search for errors
grep ERROR app.log

# Monitor WebSocket connections
grep "WebSocket" app.log
```

### Performance Tuning

**Database Optimization:**
- Add indexes for frequent queries
- Set up connection pooling for PostgreSQL
- Regular cleanup of old donations

**Memory Usage:**
- Monitor WebSocket client connections
- Implement connection limits
- Use connection pooling for external APIs

**Rate Limiting:**
- Configure rate limits for API endpoints
- Implement backoff for blockchain polling
- Cache frequently accessed data

## Security Considerations

### API Security
- Use HTTPS in production
- Implement proper CORS policies
- Add rate limiting to prevent abuse
- Validate all input data

### Content Security
- Sanitize memo content before display
- Implement comprehensive profanity filtering
- Monitor for spam patterns
- Add manual review capabilities

### Database Security
- Use environment variables for credentials
- Regular backups of donation data
- Encrypt sensitive data at rest
- Implement proper access controls

For frontend integration details, see `/frontend/README.md` and the main project documentation.