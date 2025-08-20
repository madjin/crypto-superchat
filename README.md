# 🎮 Crypto SuperChat - AI16Z Memo Overlay

**Browser-based OBS overlay that displays memo messages from AI16Z token transfers on Solana in real-time.**

Stream-ready overlay that shows donation alerts when viewers send AI16Z tokens with memo messages to your wallet. Features automatic filtering, manual moderation, and seamless OBS integration with zero build requirements.

## ✨ Features

- **🎯 Zero-Install Overlay** - Single HTML file, no dependencies or build process
- **💰 Real-time Blockchain Monitoring** - Live Solana transaction monitoring via Helius API  
- **🎛️ Moderation Dashboard** - Approve/reject donations before they appear on stream
- **🔧 URL Parameter Configuration** - No config files needed, customize everything via URL
- **🎨 Tier-based Styling** - Visual styling based on donation amounts (low/mid/high/whale)
- **🔊 Audio & TTS Support** - Notification sounds and text-to-speech for donations
- **⚡ WebSocket Communication** - Real-time updates between backend and overlay
- **🛡️ Content Filtering** - Automatic profanity filtering and manual moderation
- **📱 Demo Mode** - Test the overlay without real blockchain transactions

## 🚀 Quick Start

### 1. **Start the Backend**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your API keys
uvicorn main:app --reload --port 8765
```

### 2. **Start the Frontend**
```bash
cd frontend  
python -m http.server 8000
```

### 3. **Add to OBS**
- **Add Browser Source**
- **URL**: `http://localhost:8000/overlay.html?demo=true`
- **Width**: 1920, **Height**: 1080
- **Enable**: "Control audio via OBS" and unmute in mixer

### 4. **Test with Demo Mode**
```bash
# Test overlay positioning and audio
http://localhost:8000/overlay.html?demo=true&audio=true&position=top-right
```

## 📁 Project Structure

```
crypto-superchat/
├── frontend/                    # 🎨 Browser-based overlay
│   ├── overlay.html            # Main OBS overlay (single file, ~500 lines)
│   ├── dashboard.html          # Admin moderation interface
│   ├── media/                  # Static assets
│   │   ├── alert.gif           # Visual notification
│   │   └── notification.mp3    # Audio notification
│   └── README.md               # Frontend documentation
├── backend/                     # ⚡ FastAPI server with SQLite
│   ├── main.py                 # FastAPI application with WebSocket
│   ├── models.py               # SQLAlchemy database models
│   ├── listener.py             # Blockchain monitoring service
│   ├── database.py             # Database utilities
│   ├── requirements.txt        # Python dependencies
│   └── README.md               # Backend documentation
├── tests/                       # 🧪 Testing environment
│   ├── frontend/               # Frontend test files
│   │   ├── overlay_test.html   # Interactive overlay testing
│   │   ├── test_dashboard.html # Dashboard testing
│   │   └── simple_dashboard.html
│   ├── backend/                # Backend API tests
│   │   ├── test_api.py         # API endpoint tests
│   │   └── test_donations.py   # Database tests
│   └── README.md               # Testing documentation
├── old/                        # 🗄️ Legacy modular architecture
│   ├── frontend/js/            # Original modular ES6 system
│   ├── settings.json           # Old config files
│   └── prepros.config          # Build tool config (unused)
├── .env.example               # Environment configuration template
├── CLAUDE.md                  # Development guidance
└── README.md                  # This file
```

## ⚙️ Configuration

### Backend Environment Variables (.env file)
```bash
# Required: Blockchain API
HELIUS_API_KEY=your_helius_api_key_here
AI16Z_WALLET_ADDRESS=HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC
AI16Z_MINT_ADDRESS=HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC

# Database
DATABASE_URL=sqlite:///./donations.db

# Server
PORT=8765
HOST=0.0.0.0

# Content Moderation
ENABLE_PROFANITY_FILTER=true
BANNED_WORDS=scam,spam,hack,fake
MIN_DONATION_AMOUNT_USD=1.0
MAX_MEMO_LENGTH=280
```

### Frontend URL Parameters
Configure the overlay without editing files:

```bash
# Demo mode for testing
overlay.html?demo=true&audio=true&position=top-right

# Live mode with custom settings  
overlay.html?host=yourserver.com&port=8765&showAmount=false

# Silent mode for positioning tests
overlay.html?demo=true&audio=false&demoInterval=3000
```

**Available Parameters:**
- `demo=true` - Enable demo mode with test messages
- `host=localhost` - WebSocket server host (default: window.location.hostname)
- `port=8765` - WebSocket server port (default: 8765)
- `audio=false` - Disable all audio
- `tts=false` - Disable text-to-speech only  
- `sfx=false` - Disable sound effects only
- `showAmount=false` - Hide donation amounts
- `position=top-right` - Toast position (top-left/top-right/bottom-left/bottom-right)
- `offsetX=50` - Horizontal offset in pixels
- `offsetY=50` - Vertical offset in pixels
- `demoInterval=5000` - Time between demo messages in ms

## 🧪 Testing

### Demo Mode Testing
```bash
# Test overlay with fake donations
http://localhost:8000/overlay.html?demo=true&audio=true

# Test dashboard moderation flow
http://localhost:8000/dashboard.html
```

### Backend API Testing
```bash
cd tests/backend
python test_api.py
python test_donations.py
```

### Interactive Frontend Testing
```bash
# Open test environments in browser
tests/frontend/overlay_test.html
tests/frontend/test_dashboard.html
```

See `tests/README.md` for comprehensive testing documentation.

## 🎯 Usage Workflows

### For Streamers
1. **Backend Setup**: Start backend server with your API keys in `.env`
2. **Moderation Dashboard**: Open `http://localhost:8000/dashboard.html`
3. **OBS Integration**: Add browser source with `http://localhost:8000/overlay.html`  
4. **Go Live**: Approve/reject donations in real-time via dashboard
5. **Demo First**: Test with `?demo=true` before going live

### For Developers  
1. **Development**: Edit single HTML files directly, no build process
2. **Testing**: Use demo mode and automated tests
3. **Deployment**: Host static frontend files anywhere, deploy backend to server

## 🔧 Development

### Backend Development
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8765
```

### Frontend Development  
**Zero build process** - edit HTML files directly:
- **Overlay**: Edit `frontend/overlay.html` (embedded CSS/JS)
- **Dashboard**: Edit `frontend/dashboard.html` (embedded CSS/JS)
- **Assets**: Replace files in `frontend/media/`

### Architecture
- **Single-file frontend**: No modules, imports, or build steps
- **URL parameter config**: No config files, everything via URL parameters
- **WebSocket communication**: Real-time backend ↔ frontend updates
- **SQLite database**: Simple, file-based persistence

## 🛡️ Security

- **Environment Variables**: API keys in `.env` file only
- **Content Filtering**: Automatic banned word detection and manual moderation
- **Input Validation**: Pydantic models validate all API inputs
- **CORS**: Configured for cross-origin frontend communication
- **Memo Sanitization**: User-generated content is filtered before display

## 📦 Deployment

### Local Development
```bash
# Start backend (Terminal 1)
cd backend && uvicorn main:app --reload --port 8765

# Start frontend server (Terminal 2)  
cd frontend && python -m http.server 8000

# Access overlay
http://localhost:8000/overlay.html?demo=true
```

### Production Deployment
```bash
# Backend: Deploy to VPS/cloud with public IP
uvicorn main:app --host 0.0.0.0 --port 8765

# Frontend: Host static files anywhere (Netlify, GitHub Pages, etc.)
# Update overlay URL: overlay.html?host=yourserver.com&port=8765
```

### OBS Studio Integration
1. **Add Browser Source**
2. **URL**: `http://localhost:8000/overlay.html?demo=true`
3. **Size**: 1920x1080 (match your canvas)
4. **Audio**: Enable "Control audio via OBS" + unmute in mixer
5. **Settings**: Enable "Refresh browser when scene becomes active"

## 🎨 Customization

### Donation Tiers
Tiers are defined in frontend code (overlay.html):
```javascript
// Lines ~200-220 in overlay.html
const tiers = {
  whale: 1000,    // ≥$1000 = Gold
  high: 100,      // ≥$100 = Purple  
  mid: 10,        // ≥$10 = Blue
  low: 0          // <$10 = Gray
};
```

### Visual Styling
Modify CSS in overlay.html:
```css
/* Lines ~50-150 in overlay.html */
.tier-whale { border-color: #ffd700; /* Gold */ }
.tier-high { border-color: #a855f7;  /* Purple */ }
.tier-mid { border-color: #3b82f6;   /* Blue */ }
.tier-low { border-color: #6b7280;   /* Gray */ }
```

### Audio & Media
- **Notification Sound**: Replace `frontend/media/notification.mp3`
- **Alert Animation**: Replace `frontend/media/alert.gif`
- **TTS Voices**: Configure in overlay.html WebSpeechAPI settings

## 🐛 Troubleshooting

### Common Issues

**Overlay not showing donations:**
- Check backend is running: `curl http://localhost:8765/health`
- Verify WebSocket connection in browser console (F12 → Network → WS tab)
- Test with demo mode first: `?demo=true`
- Check browser console for error messages

**Audio not working in OBS:**
- Enable "Control audio via OBS" in Browser Source properties
- Unmute the source in OBS audio mixer  
- Test with: `?demo=true&audio=true`

**Backend connection issues:**
- Verify `.env` file has correct API keys
- Check Helius API key is valid and has credits
- Ensure backend port 8765 is not blocked by firewall
- Try different host: `?host=127.0.0.1`

**WebSocket connection failed:**
- Backend not running or wrong port (should be 8765)
- Browser blocking WebSocket connections (check console)
- Network/firewall blocking connections
- Try restarting both backend and frontend servers

**No real donations appearing:**
- Check `HELIUS_API_KEY` is valid in `.env`  
- Verify `AI16Z_WALLET_ADDRESS` and `AI16Z_MINT_ADDRESS` are correct
- Check backend logs for blockchain API errors
- Ensure donations meet minimum amount threshold

### Debug Steps

1. **Test Demo Mode**: `?demo=true` - should show fake donations
2. **Check Backend Health**: Visit `http://localhost:8765/health`  
3. **Monitor WebSocket**: Browser F12 → Network → WS tab
4. **Check Backend Logs**: Look for errors in terminal running uvicorn
5. **Test Dashboard**: Open `http://localhost:8000/dashboard.html`

## 🤝 Contributing

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/amazing-feature`)
3. **Test** your changes:
   ```bash
   # Test backend
   cd tests/backend && python test_api.py
   
   # Test frontend
   open overlay.html?demo=true
   ```
4. **Commit** changes (`git commit -m 'Add amazing feature'`)
5. **Push** to branch (`git push origin feature/amazing-feature`)
6. **Open** Pull Request

### Development Guidelines
- **Frontend**: Single-file architecture, no modules or build process
- **Backend**: FastAPI with async patterns, SQLAlchemy models
- **Testing**: Use demo mode for frontend, pytest for backend
- **Documentation**: Update component READMEs when adding features

## 📚 Documentation

- **`/frontend/README.md`** - Frontend setup, configuration, and OBS integration
- **`/backend/README.md`** - Backend API, database, and deployment
- **`/tests/README.md`** - Testing procedures and environments  
- **`/CLAUDE.md`** - Development guidance for Claude Code

## 📄 License

This project is licensed under the MIT License.

## 🙋‍♂️ Support

For issues and questions:
- Check the troubleshooting section above
- Review component READMEs for detailed setup
- Test with demo mode before reporting issues
- Include browser console logs when reporting frontend issues

---

**Built for streamers, by developers** 💜

*Zero-dependency OBS overlay for the AI16Z community*