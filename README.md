# 🎮 AI16Z Stream Overlay

**Professional-grade OBS overlay system for displaying AI16Z crypto donations with real-time moderation.**

Stream-ready overlay that shows donation alerts when viewers send AI16Z tokens with memo messages to your wallet. Features automatic filtering, manual moderation, and seamless OBS integration.

## ✨ Features

- **🎯 OBS-Ready Overlay** - Single HTML file, zero dependencies
- **💰 Real-time Donations** - Live blockchain monitoring via Helius API
- **🎛️ Moderation Dashboard** - Approve/skip donations before showing
- **🔧 Configurable** - URL parameters for easy customization
- **🎨 Tier-based Styling** - Different colors/animations for donation amounts
- **🔊 Audio Support** - Notification sounds with each donation
- **⚡ WebSocket Real-time** - Instant updates between backend and overlay
- **🛡️ Content Filtering** - Automatic banned word detection

## 🚀 Quick Start

### 1. **Start the Backend**
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. **Add to OBS**
- **Add Browser Source**
- **URL**: `file:///path/to/frontend/overlay.html?obs=true`
- **Width**: 1920, **Height**: 1080
- **Custom CSS**: None needed

### 3. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 4. **Test the System**
```bash
# Open test environment
open tests/frontend/overlay_test.html
```

## 📁 Project Structure

```
chainchat/
├── frontend/                    # 🎨 Production web interface
│   ├── overlay.html            # Main OBS overlay (single file)
│   ├── dashboard.html          # Streamer moderation dashboard
│   └── media/alert.gif         # Notification media
├── backend/                     # ⚡ API server & WebSocket
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Database models  
│   ├── database.py             # SQLite operations
│   └── requirements.txt        # Python dependencies
├── tests/                       # 🧪 Testing environment
│   ├── frontend/
│   │   ├── overlay_test.html   # Interactive overlay testing
│   │   └── simple_dashboard.html # Manual moderation testing
│   └── backend/
│       └── test_api.py         # Automated API tests
├── old/                        # 🗄️ Legacy code (reference only)
├── .env.example               # Configuration template
└── README.md                  # This file
```

## ⚙️ Configuration

### Environment Variables
```bash
# Required: Blockchain API
HELIUS_API_KEY=your_helius_api_key
PRIZE_WALLET_ADDRESS=your_wallet_address

# Optional: Customization  
AI16Z_MINT=HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC
DATABASE_URL=sqlite:///overlay.db
AUTO_MODE=false

# Overlay Display Settings
OVERLAY_POSITION=bottom-right
DONATION_DURATION_MS=5000
TIER_MID=1000
TIER_HIGH=10000
TIER_WHALE=100000
```

### URL Parameters
Configure the overlay without touching code:

```bash
# Basic configuration
frontend/overlay.html?host=localhost&port=8000&duration=3000

# Position and styling
frontend/overlay.html?position=top-left&debug=true

# OBS production mode
frontend/overlay.html?obs=true&host=yourserver.com
```

**Available Parameters:**
- `host` - Backend host (default: localhost)
- `port` - Backend port (default: 8000) 
- `duration` - Display duration in ms (default: 5000)
- `position` - Toast position (default: bottom-right)
- `debug` - Show connection status (default: false)
- `demo` - Demo mode with test donation (default: false)
- `obs` - OBS mode, minimal UI (default: false)

## 🧪 Testing

### Automated Tests
```bash
# Backend API tests
cd tests/backend
python test_api.py
```

### Interactive Testing
```bash
# Visual overlay testing
open tests/frontend/overlay_test.html

# Manual dashboard testing  
open tests/frontend/simple_dashboard.html
```

See `tests/README.md` for detailed testing instructions.

## 🎯 Usage Workflows

### For Streamers
1. **Setup**: Start backend, configure API keys
2. **Dashboard**: Open `frontend/dashboard.html` for moderation
3. **OBS**: Add `frontend/overlay.html` as browser source  
4. **Moderation**: Use dashboard to approve/skip donations
5. **Go Live**: Donations appear automatically on stream

### For Developers
1. **Development**: Use test environment for development
2. **Testing**: Run automated tests before deployment
3. **Deployment**: Single HTML file for easy hosting

## 🔧 Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### Frontend Development  
The overlay is a single HTML file with no build process. Edit `frontend/overlay.html` directly.

### Adding Features
- **Backend**: Add endpoints to `main.py`
- **Frontend**: Modify overlay.html
- **Tests**: Add tests to `tests/` directory

## 🛡️ Security

- **Environment Variables**: Keep API keys in `.env` (not in code)
- **Content Filtering**: Automatic banned word detection
- **Input Validation**: All user inputs are validated
- **CORS**: Configured for local development only

## 📦 Deployment

### Local Development
```bash
# Start backend
cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Use overlay
frontend/overlay.html?host=localhost&port=8000
```

### Production
```bash
# Deploy backend to your server
# Update overlay URL: frontend/overlay.html?host=yourserver.com&port=8000
```

### OBS Studio Setup
1. **Add Browser Source**
2. **URL**: `file:///absolute/path/to/frontend/overlay.html?obs=true`
3. **Size**: 1920x1080 (or your canvas size)
4. **Properties**: Check "Refresh browser when scene becomes active"

## 🎨 Customization

### Donation Tiers
Edit tier thresholds in `.env`:
```bash
TIER_MID=1000      # $1,000+ = Mid tier (blue)
TIER_HIGH=10000    # $10,000+ = High tier (purple)  
TIER_WHALE=100000  # $100,000+ = Whale tier (orange)
```

### Styling
The overlay uses CSS custom properties for easy theming:
```css
:root {
  --tier-low: #10b981;    /* Green */
  --tier-mid: #3b82f6;    /* Blue */ 
  --tier-high: #a855f7;   /* Purple */
  --tier-whale: #f59e0b;  /* Orange */
}
```

### Media Assets
Replace `frontend/media/alert.gif` with your own notification media.

## 🐛 Troubleshooting

**Overlay not showing donations:**
- Check backend is running on port 8000
- Verify WebSocket connection in browser console
- Test with `tests/frontend/overlay_test.html`

**Backend connection issues:**
- Check `.env` file has correct API keys
- Verify Helius API key is valid
- Check firewall/port settings

**OBS not displaying overlay:**
- Use absolute file path in browser source
- Check OBS browser source size matches canvas
- Enable "Refresh browser when scene becomes active"

## 🤝 Contributing

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/amazing-feature`)
3. **Test** your changes (`python tests/backend/test_api.py`)
4. **Commit** changes (`git commit -m 'Add amazing feature'`)
5. **Push** to branch (`git push origin feature/amazing-feature`)
6. **Open** Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Documentation**: See `tests/README.md` for detailed testing info

---

**Built for streamers, by developers** 💜

*Professional stream overlay system for the AI16Z community*