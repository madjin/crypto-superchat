# Frontend - AI16Z Memo Overlay

Browser-based OBS overlay that displays memo messages from AI16Z token transfers on Solana in real-time.

## Quick Start

1. **Start a local server:**
   ```bash
   cd frontend
   python -m http.server 8000
   ```

2. **Access the overlay:**
   - **Overlay**: http://localhost:8000/overlay.html
   - **Dashboard**: http://localhost:8000/dashboard.html

3. **Add to OBS:**
   - Add Browser Source with URL: `http://localhost:8000/overlay.html?demo=true`
   - Enable "Control audio via OBS" and unmute in mixer for audio
   - Set dimensions to 1920x1080 (or your canvas size)

## Files

- **`overlay.html`** - Main overlay display for OBS
- **`dashboard.html`** - Admin moderation interface  
- **`media/`** - Static assets (alert.gif, notification.mp3)

## Configuration

All configuration is done via URL parameters. No separate config files needed.

### Overlay Parameters

Add parameters to the overlay URL: `overlay.html?param1=value1&param2=value2`

#### Core Settings
- **`demo=true`** - Enable demo mode with test messages (default: false)
- **`host=localhost`** - WebSocket server host (default: window.location.hostname)
- **`port=8765`** - WebSocket server port (default: 8765)

#### Display Settings  
- **`audio=false`** - Disable all audio (default: true)
- **`tts=false`** - Disable text-to-speech only (default: true)
- **`sfx=false`** - Disable sound effects only (default: true)
- **`showAmount=false`** - Hide donation amounts (default: true)

#### Positioning
- **`position=top-right`** - Toast position (options: top-left, top-right, bottom-left, bottom-right)
- **`offsetX=50`** - Horizontal offset in pixels (default: 20)
- **`offsetY=50`** - Vertical offset in pixels (default: 20)

#### Demo Mode Settings
- **`demoInterval=5000`** - Time between demo messages in ms (default: 8000)
- **`demoCount=10`** - Number of demo messages to show (default: unlimited)

### Example URLs

```bash
# Demo mode for testing
overlay.html?demo=true&audio=true&position=top-right

# Live mode with custom positioning
overlay.html?host=localhost&offsetX=100&offsetY=50&showAmount=false

# Silent mode for testing positioning
overlay.html?demo=true&audio=false&demoInterval=3000
```

## Display Features

### Tier-Based Styling
Messages are styled based on donation amount:
- **Whale** (≥$1000): Gold border, special effects
- **High** (≥$100): Purple border, enhanced animation  
- **Mid** (≥$10): Blue border, medium animation
- **Low** (<$10): Gray border, basic animation

### Audio Features
- **Text-to-Speech**: Reads donation amount and memo message
- **Sound Effects**: Notification sound for each donation
- **Audio Unlock**: Automatic handling of browser audio policies

### Visual Effects
- **Toast Notifications**: Sliding animations with tier-based colors
- **Media Integration**: GIF and sound effects based on donation tier
- **Responsive Positioning**: Configurable overlay positioning

## Demo Mode

Perfect for testing without a live backend:

```bash
# Access demo overlay
http://localhost:8000/overlay.html?demo=true
```

Demo mode features:
- Generates fake donations with random amounts and memos
- Tests all tier levels and audio features
- Configurable timing and message count
- Perfect for OBS setup and positioning

## Dashboard (Moderation)

Access the admin dashboard at `http://localhost:8000/dashboard.html`

Features:
- **Real-time message queue** - See incoming donations awaiting approval
- **Approve/Reject** - Moderate content before it appears on overlay
- **Live monitoring** - View approved messages as they display
- **Message history** - Track all processed donations

The dashboard connects to the same backend WebSocket and provides real-time moderation capabilities.

## OBS Integration

### Setup Steps
1. **Add Browser Source** in OBS
2. **Set URL**: `http://localhost:8000/overlay.html?demo=true`
3. **Set Dimensions**: 1920x1080 (match your canvas)
4. **Enable Audio**: Check "Control audio via OBS" 
5. **Unmute Source**: In OBS audio mixer
6. **Refresh Setting**: Enable "Refresh browser when scene becomes active"

### Audio Configuration
- **For Audio**: Must enable "Control audio via OBS" and unmute in mixer
- **For Silent**: Use `?audio=false` parameter
- **TTS Only**: Use `?sfx=false` to disable sound effects but keep speech
- **SFX Only**: Use `?tts=false` to disable speech but keep notification sounds

### Positioning Tips
- Use `?position=top-right` for corner placement
- Use `offsetX` and `offsetY` for fine-tuning
- Test with `?demo=true` to see positioning before going live
- Consider your game/content layout when positioning

## Troubleshooting

### Common Issues

**No messages appearing:**
- Check WebSocket connection (F12 → Network → WS tab)
- Verify backend is running on port 8765
- Try demo mode first: `?demo=true`

**Audio not working in OBS:**
- Enable "Control audio via OBS" in Browser Source properties
- Unmute the source in OBS audio mixer
- Test with `?demo=true&audio=true`

**Messages positioned incorrectly:**
- Use `?position=` parameter to set corner
- Fine-tune with `offsetX=` and `offsetY=` parameters
- Test positioning with demo mode

**WebSocket connection failed:**
- Ensure backend is running: `uvicorn main:app --port 8765`
- Check firewall/antivirus blocking connections
- Try different host: `?host=127.0.0.1`

### Browser Compatibility
- **Brave**: Full support (recommended)
- **Chrome**: Full support
- **Firefox**: Full support
- **OBS Browser**: Full support (Chromium-based)
- **Safari**: Limited (WebSocket may need configuration)

## Development

The frontend is a single HTML file with embedded CSS and JavaScript - no build process required.

### File Structure
```
frontend/
├── overlay.html      # Main overlay (500+ lines with CSS/JS embedded)
├── dashboard.html    # Admin interface (300+ lines with CSS/JS embedded)  
├── media/
│   ├── alert.gif     # Visual notification
│   └── notification.mp3  # Audio notification
└── README.md         # This file
```

### Architecture Notes
- **Single-file design** for zero-dependency deployment
- **WebSocket client** for real-time backend communication
- **URL parameter configuration** eliminates config file management
- **Embedded assets** for maximum portability

For advanced development, see the main project CLAUDE.md for full architectural details.