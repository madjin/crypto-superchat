# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an AI16Z Memo Overlay project - a browser-based OBS overlay that displays memo messages from AI16Z token transfers on Solana. The project consists of a zero-install frontend with an optional FastAPI backend for moderated flows.

## Project Structure

The project is organized into two main components:

- **memo_overlay/frontend/** - Browser-based overlay (ES modules, no build step required)
- **memo_overlay/backend/** - Optional FastAPI backend for WebSocket and moderated flows

## Frontend Architecture

### Core Technologies
- Vanilla JavaScript with ES6 modules (no bundler/transpilation)
- Direct browser deployment via simple HTTP server
- Modular architecture under `frontend/js/`

### Module Structure
- **boot.js** - Entry point that initializes the main module
- **main.js** - Core overlay logic, queue management, and display coordination
- **config.js** - Configuration loading from JSON files and URL parameters
- **helius.js** - Solana blockchain interaction via Helius API (RPC calls, memo extraction, token amount parsing)
- **positioning.js** - CSS positioning and offset management for overlay elements
- **media.js** - Dynamic media handling (images/videos) with tier-based overrides  
- **audio.js** - Text-to-speech and sound effects with browser audio unlock handling
- **demo.js** - Test/demo mode with fake transaction generation
- **utils.js** - Shared utilities (JSON loading, DOM helpers, string formatting)
- **constants.js** - Default configuration and API endpoints

### Configuration System
- **settings.json** - Display settings, positioning, media, tiers, and behavior config
- **keys.json** - API credentials (Helius API key, wallet address, mint address)
- URL parameter overrides supported for all settings
- Auto-detection of live vs demo mode based on placeholder key detection

### Display System
- Queue-based message display with toast notifications
- Tier-based styling (low/mid/high/whale) with amount thresholds
- Per-tier media overrides (GIFs, videos with different properties)
- TTS and SFX integration with audio unlock patterns

## Backend Architecture

### Core Technologies
- FastAPI with async/await patterns
- WebSocket support for real-time communication
- Optional listener integration for blockchain monitoring

### Components
- **main.py** - FastAPI application with WebSocket endpoints and health checks
- **listener.py** - Blockchain monitoring task (referenced but implementation varies)

### API Design
- Health check endpoint at `/health`
- WebSocket endpoint at `/ws` for real-time updates
- CORS enabled for cross-origin frontend communication

## Common Development Tasks

### Frontend Development
```bash
# Serve frontend locally
cd memo_overlay/frontend
python -m http.server 5500
# Access at http://localhost:5500/index.html
```

### Backend Development  
```bash
# Set up Python environment
cd memo_overlay/backend
python -m venv .venv
source .venv/bin/activate  # or .venv/Scripts/activate on Windows
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --port 8765
```

### Configuration Setup
1. Copy configuration templates and customize:
   - Create `keys.json` with real API credentials for live mode
   - Modify `settings.json` for display preferences and behavior
   - Use placeholder values in `keys.json` for demo/test mode

### OBS Integration
- Add Browser Source pointing to frontend URL
- Enable "Refresh browser when scene becomes active"
- For audio: enable "Control audio via OBS" and unmute in mixer
- Set canvas dimensions to match overlay requirements

## Key Implementation Patterns

### Modular ES6 Architecture
- No build step required - files are served directly
- Import/export pattern for clean module boundaries
- Dynamic imports for optional functionality

### Configuration-Driven Behavior
- JSON-based configuration with URL parameter overrides
- Runtime detection of live vs demo mode
- Tier-based theming and media selection

### Blockchain Integration
- Helius API for Solana RPC and enhanced transaction data
- Token transfer parsing with memo extraction
- Associated Token Account (ATA) resolution
- Deduplication and state management for real-time updates

### Audio Management
- Browser audio context unlocking via user gestures
- TTS integration with tier-based voice selection
- Sound effects coordination with visual animations

### Real-time Display
- Queue-based processing with configurable timing
- Toast notification system with CSS transitions  
- Position management for multiple simultaneous elements

## Development Workflow

### Live Mode Testing
1. Configure real Helius API key and wallet address in `keys.json`
2. Set `live: true` in `settings.json` or let auto-detection handle it
3. Monitor real blockchain transactions and memo displays

### Demo Mode Testing  
1. Use placeholder values in `keys.json` (e.g., `YOUR_API_KEY`)
2. Enable demo controls via `settings.json` or URL parameters
3. Use test controls to simulate various transaction scenarios

### Moderated Flow (Planned)
Reference `MODERATED_FLOW.md` for planned architecture that adds:
- Backend moderation queue with approval/rejection workflow
- Streamer dashboard for real-time moderation
- WebSocket-based approved content delivery to overlay

## Build Tools Integration

The project includes Prepros configuration for optional asset processing:
- CSS minification and autoprefixing  
- JavaScript minification for distribution
- Image optimization for media assets
- Live reload during development

Note: The core overlay works without any build step - Prepros is purely optional for optimization.
- when it comes to testing assume that i will start / stop the server from now on
- Let the user run python commands to start / stop the server