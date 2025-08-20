# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an AI16Z Memo Overlay project - a browser-based OBS overlay that displays memo messages from AI16Z token transfers on Solana. The project consists of a zero-install frontend with a FastAPI backend for real-time message delivery.

## Project Structure

The project is organized into two main components:

- **frontend/** - Browser-based overlay (single HTML file, no build step required)
- **backend/** - FastAPI backend with WebSocket support and SQLite database

## Frontend Architecture

### Core Technologies
- Single HTML file with embedded CSS and JavaScript
- Direct browser deployment via simple HTTP server
- WebSocket client for real-time communication with backend
- URL parameter-based configuration

### File Structure
- **overlay.html** - Main overlay display with embedded JavaScript for WebSocket communication, message display, and audio handling
- **dashboard.html** - Admin dashboard for moderation (embedded JavaScript for WebSocket management and approval/rejection interface)
- **media/** - Static assets (alert.gif, notification.mp3)

### Configuration System
- URL parameters for all configuration (host, demo mode, audio settings, positioning)
- Environment variables via backend (.env file)
- Hard-coded defaults with URL parameter overrides
- No separate config files - all configuration via URL parameters

### Display System
- WebSocket-based real-time message display
- Tier-based styling (low/mid/high/whale) with amount thresholds
- Integrated audio with text-to-speech and sound effects
- Toast notification system with CSS animations

## Backend Architecture

### Core Technologies
- FastAPI with async/await patterns
- SQLite database with SQLAlchemy ORM
- WebSocket support for real-time communication
- Helius API integration for Solana blockchain monitoring

### Components
- **main.py** - FastAPI application with WebSocket endpoints, health checks, and moderation API
- **listener.py** - Blockchain monitoring service that fetches transactions and processes memos
- **models.py** - SQLAlchemy database models for donation tracking and moderation

### API Design
- Health check endpoint at `/health`
- WebSocket endpoint at `/ws` for real-time updates
- Admin dashboard endpoints for moderation
- CORS enabled for cross-origin frontend communication
- SQLite database for persistent storage

## Common Development Tasks

### Frontend Development
```bash
# Serve frontend locally
cd frontend
python -m http.server 8000
# Access at http://localhost:8000/overlay.html
```

### Backend Development  
```bash
# Set up Python environment
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv/Scripts/activate on Windows
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys and configuration

# Run development server
uvicorn main:app --reload --port 8765
```

### Configuration Setup
1. Backend configuration via .env file:
   - Copy `.env.example` to `.env`
   - Set `HELIUS_API_KEY` for blockchain monitoring
   - Configure `AI16Z_WALLET_ADDRESS` and `AI16Z_MINT_ADDRESS`
   - Set database and server configuration

2. Frontend configuration via URL parameters:
   - `?demo=true` - Enable demo mode with test messages
   - `?host=localhost` - Set WebSocket host
   - `?audio=false` - Disable audio
   - See overlay.html for full parameter list

### OBS Integration
- Add Browser Source pointing to frontend URL: `http://localhost:8000/overlay.html`
- Enable "Refresh browser when scene becomes active"
- For audio: enable "Control audio via OBS" and unmute in mixer
- Set canvas dimensions to match overlay requirements (typically 1920x1080)

## Key Implementation Patterns

### Single-File Architecture
- No build step required - HTML files are served directly
- Embedded CSS and JavaScript in HTML files for zero dependencies
- URL parameter-based configuration system

### Configuration-Driven Behavior
- URL parameter overrides for all settings
- Environment variable configuration for backend
- Demo mode vs live mode switching
- Tier-based styling and behavior

### Blockchain Integration
- Helius API for Solana RPC and enhanced transaction data
- Token transfer parsing with memo extraction
- SQLite database for persistent storage and moderation queue
- Real-time WebSocket updates from backend listener

### Audio Management
- Browser audio context unlocking via user gestures
- Text-to-speech integration with configurable voices
- Sound effects coordination with visual notifications

### Real-time Communication
- WebSocket-based message delivery from backend to frontend
- Moderation queue with approval/rejection workflow
- Dashboard interface for real-time content moderation

## Development Workflow

### Live Mode Testing
1. Configure backend with real Helius API key in `.env`
2. Set correct wallet and mint addresses in `.env`
3. Start backend and frontend servers
4. Monitor real blockchain transactions and memo displays

### Demo Mode Testing  
1. Access overlay with `?demo=true` parameter
2. Use demo mode to test display, audio, and positioning
3. Test moderation workflow via dashboard

### Moderated Flow
The current implementation includes:
- Backend moderation queue with SQLite database
- Admin dashboard at `/dashboard.html` for approval/rejection
- WebSocket-based approved content delivery to overlay
- Configurable content filtering and tier-based display

## Build Tools Integration

The project includes Prepros configuration for optional asset processing:
- CSS minification and autoprefixing  
- JavaScript minification for distribution
- Image optimization for media assets
- Live reload during development

Note: The core overlay works without any build step - Prepros is purely optional for optimization.
- when it comes to testing assume that i will start / stop the server from now on
- Let the user run python commands to start / stop the server