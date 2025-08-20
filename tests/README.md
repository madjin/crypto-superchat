# 🧪 AI16Z Stream Overlay Tests

This directory contains all test files for the AI16Z stream overlay system.

## 📁 Structure

```
tests/
├── backend/
│   ├── test_api.py           # Automated backend API tests
│   ├── test_donations.py     # Legacy donation testing (moved from backend/)
│   └── test_dashboard.html   # Legacy dashboard (moved from frontend/)
├── frontend/
│   ├── overlay_test.html     # Interactive overlay testing environment
│   ├── simple_dashboard.html # Simple dashboard for manual testing
│   └── test_overlay.html     # Legacy overlay test (moved from frontend/)
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Start the Backend
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Run Tests

**Automated Backend Tests:**
```bash
cd tests/backend
python test_api.py
```

**Interactive Frontend Tests:**
```bash
# Open in browser
open tests/frontend/overlay_test.html
```

**Manual Dashboard Testing:**
```bash
# Open in browser  
open tests/frontend/simple_dashboard.html
```

## 🧪 Test Descriptions

### Backend Tests (`test_api.py`)
- ✅ Health check endpoint
- ✅ WebSocket connections (overlay & dashboard)
- ✅ API endpoint functionality
- ✅ Event creation and approval flow

**Usage:**
```bash
python test_api.py
```

### Overlay Test Environment (`overlay_test.html`)
- 🎮 Interactive overlay testing with visual interface
- 🎯 Different overlay modes (demo, debug, production, OBS)  
- 📱 Quick donation buttons with different tiers
- 🔌 Real-time backend connection status
- 🎨 Visual overlay preview in iframe

**Features:**
- Test donations with preset amounts
- Switch between overlay modes
- Backend connection monitoring
- Direct overlay communication

### Simple Dashboard (`simple_dashboard.html`)
- 🎛️ Manual donation management
- 📊 Pending events list with approve/skip actions
- 💰 Custom donation creation
- 📈 Real-time status monitoring
- 🧹 Event management (clear all, refresh)

**Features:**
- Send test donations (all tiers)
- Approve/skip pending donations  
- Custom donation amounts and messages
- Activity logging
- Backend status monitoring

## 📋 Testing Workflow

### For Developers
1. **Start backend** (`uvicorn main:app`)
2. **Run automated tests** (`python test_api.py`)
3. **Test overlay visually** (`overlay_test.html`)
4. **Test dashboard flows** (`simple_dashboard.html`)

### For Streamers  
1. **Start backend**
2. **Open overlay test** to see how it looks
3. **Use simple dashboard** to practice moderation
4. **Test in OBS** with overlay.html

## 🎯 Test Scenarios

### Basic Functionality
- [ ] Backend starts without errors
- [ ] WebSocket connections work  
- [ ] Overlay displays test donations
- [ ] Dashboard can approve/skip events

### Overlay Modes
- [ ] Demo mode shows test donation automatically
- [ ] Debug mode shows connection status
- [ ] Production mode connects to backend
- [ ] OBS mode hides debug info

### Donation Flow
- [ ] Different tier donations display correctly
- [ ] Custom donations work with any amount
- [ ] Pending events show in dashboard
- [ ] Approve action triggers overlay display
- [ ] Skip action removes from queue

### Error Handling  
- [ ] Overlay handles backend disconnection gracefully
- [ ] Dashboard shows connection status
- [ ] Failed API calls are logged properly
- [ ] WebSocket reconnection works

## 🔧 Configuration

### Environment Variables
Set these in `.env` file or environment:
```bash
# Backend connection
HOST=localhost
PORT=8000

# Overlay settings  
DISPLAY_DURATION=5000
OVERLAY_POSITION=bottom-right

# Debug settings
DEBUG_MODE=true
```

### URL Parameters
Overlay supports configuration via URL parameters:
- `?demo=true` - Demo mode with test donation
- `?debug=true` - Show debug information
- `?obs=true` - OBS mode (minimal UI)
- `?host=localhost&port=8000` - Backend connection
- `?duration=3000` - Display duration in ms

## 🐛 Troubleshooting

**Backend not connecting:**
- Check if uvicorn is running on port 8000
- Verify no firewall blocking localhost:8000
- Check browser console for CORS errors

**Overlay not showing donations:**
- Check WebSocket connection in browser dev tools
- Verify backend is processing events
- Test with simple dashboard first

**Dashboard not working:**
- Check backend API endpoints are responding
- Verify JavaScript console for errors
- Try refreshing the connection

## 📝 Adding New Tests

### Backend Tests
Add new test methods to `test_api.py`:
```python
def test_new_feature(self):
    """Test description"""
    # Test implementation
    pass
```

### Frontend Tests
Create new HTML test files following the pattern:
- Use consistent styling
- Include connection status indicators  
- Add console logging for debugging
- Handle errors gracefully

## 🎯 Production Testing

Before going live:
1. **Run all automated tests**
2. **Test overlay in OBS Studio**  
3. **Practice with dashboard**
4. **Test with real donations** (small amounts)
5. **Verify audio works** 
6. **Check different donation tiers**

Remember: Tests are in a separate directory to keep production code clean! 🧹