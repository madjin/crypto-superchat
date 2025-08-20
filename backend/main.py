"""
Simple FastAPI server for stream overlay donations.
"""

import os
import asyncio
import time
import json
import logging
import requests
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

try:
    from .database import (
        init_db, create_event, get_pending_events, 
        approve_event, skip_event, clear_events, is_memo_banned
    )
    from .listener import start_listener_task
except ImportError:
    from database import (
        init_db, create_event, get_pending_events,
        approve_event, skip_event, clear_events, is_memo_banned
    )
    try:
        from listener import start_listener_task
    except ImportError:
        start_listener_task = None

load_dotenv()

# Simple FastAPI app
app = FastAPI(title="Crypto Stream Overlay", version="1.0.0")

# CORS middleware with WebSocket support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket clients
overlay_clients: set[WebSocket] = set()
dashboard_clients: set[WebSocket] = set()

# Simple settings
AUTO_MODE = os.getenv("AUTO_MODE", "false").lower() == "true"

# API Models
class EventAction(BaseModel):
    event_id: str
    action: str  # "approve" or "skip"

class TokenMetadata(BaseModel):
    mint: str
    symbol: Optional[str] = None
    name: Optional[str] = None
    logo: Optional[str] = None
    decimals: int = 6

@app.get("/health")
async def health():
    return {"ok": True, "timestamp": int(time.time())}

@app.get("/api/events/pending")
async def get_pending():
    """Get pending events for dashboard."""
    events = get_pending_events()
    return events  # Already converted to dicts

@app.post("/api/events/action")
async def moderate_event(action: EventAction):
    """Approve or skip an event."""
    if action.action == "approve":
        event = approve_event(action.event_id)
        if event:
            # Broadcast to overlay for display
            await broadcast_to_overlay({
                "type": "show_donation",
                "event": event
            })
            # Notify dashboard
            await broadcast_to_dashboard({
                "type": "event_approved", 
                "event_id": action.event_id
            })
            return {"success": True, "action": "approved"}
    
    elif action.action == "skip":
        event = skip_event(action.event_id)
        if event:
            await broadcast_to_dashboard({
                "type": "event_skipped",
                "event_id": action.event_id  
            })
            return {"success": True, "action": "skipped"}
    
    return {"success": False, "error": "Invalid action or event not found"}

@app.delete("/api/events")
async def clear_all_events():
    """Clear all events."""
    count = clear_events()
    await broadcast_to_dashboard({"type": "events_cleared", "count": count})
    return {"success": True, "cleared": count}

def get_token_metadata_from_helius(mint_address: str) -> Optional[Dict[str, Any]]:
    """Fetch token metadata from Helius DAS API and cache it."""
    helius_api_key = os.getenv('HELIUS_API_KEY')
    if not helius_api_key:
        return None
        
    try:
        # Try to use database cache first (would need to implement)
        # For now, just fetch directly from Helius
        
        helius_url = f"https://mainnet.helius-rpc.com/?api-key={helius_api_key}"
        
        # Fetch from Helius DAS API
        payload = {
            "jsonrpc": "2.0",
            "id": f"token-metadata-{mint_address}",
            "method": "getAsset",
            "params": {
                "id": mint_address
            }
        }
        
        response = requests.post(helius_url, json=payload)
        response.raise_for_status()
        asset_data = response.json()
        
        if 'error' in asset_data or not asset_data.get('result'):
            return None
        
        asset = asset_data['result']
        
        # Extract metadata
        symbol = None
        name = None
        decimals = 6  # Default for SPL tokens
        logo_uri = None
        cdn_uri = None
        
        # Get symbol and name from token_info or content
        if asset.get('token_info'):
            symbol = asset['token_info'].get('symbol')
            decimals = asset['token_info'].get('decimals', 6)
        
        if asset.get('content'):
            content = asset['content']
            if not symbol and content.get('metadata'):
                symbol = content['metadata'].get('symbol')
                name = content['metadata'].get('name')
            
            # Get image URLs
            if content.get('files') and len(content['files']) > 0:
                first_file = content['files'][0]
                logo_uri = first_file.get('uri')
                cdn_uri = first_file.get('cdn_uri')
        
        return {
            'symbol': symbol or mint_address[:8],
            'name': name,
            'decimals': decimals,
            'logo': cdn_uri or logo_uri,  # prefer CDN
            'mint': mint_address
        }
        
    except Exception as e:
        print(f"Error fetching token metadata for {mint_address}: {e}")
        return None

@app.get("/api/tokens/metadata/{mint_address}")
async def get_token_metadata(mint_address: str):
    """Get token metadata for a given mint address."""
    
    # Handle special cases for well-known tokens
    well_known_tokens = {
        "So11111111111111111111111111111111111111112": {
            "symbol": "SOL",
            "name": "Solana",
            "decimals": 9,
            "logo": "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/So11111111111111111111111111111111111111112/logo.png",
            "mint": "So11111111111111111111111111111111111111112"
        },
        "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC": {
            "symbol": "AI16Z",
            "name": "ai16z",
            "decimals": 6,
            "logo": "https://arweave.net/yPPLSRJCJBpj0teCRvwJKYNj1Z5K7vCLZfqxjWaKpjE",
            "mint": "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"
        },
        "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": {
            "symbol": "USDC",
            "name": "USD Coin",
            "decimals": 6,
            "logo": "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v/logo.png",
            "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        }
    }
    
    # Check if it's a well-known token first
    if mint_address in well_known_tokens:
        return well_known_tokens[mint_address]
    
    # Otherwise fetch from Helius
    metadata = get_token_metadata_from_helius(mint_address)
    if metadata:
        return metadata
    else:
        raise HTTPException(status_code=404, detail="Token metadata not found")

@app.get("/api/tokens/popular")
async def get_popular_tokens():
    """Get list of popular tokens with metadata."""
    popular_tokens = [
        "So11111111111111111111111111111111111111112",  # SOL
        "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC",  # AI16Z
        "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
        "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",  # BONK
        "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",  # USDT
        "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",  # ETH (Wormhole)
    ]
    
    tokens = []
    for mint in popular_tokens:
        try:
            metadata = await get_token_metadata(mint)
            tokens.append(metadata)
        except:
            continue
    
    return tokens

@app.websocket("/ws/overlay")
async def overlay_websocket(websocket: WebSocket):
    """WebSocket for OBS overlay display."""
    print(f"Overlay WebSocket connection attempt from: {websocket.client}")
    try:
        await websocket.accept()
        overlay_clients.add(websocket)
        print(f"✅ Overlay WebSocket connected. Total clients: {len(overlay_clients)}")
        
        await websocket.send_json({"type": "connected", "client": "overlay"})
        
        while True:
            # Keep connection alive and handle any messages
            try:
                data = await websocket.receive_text()
                print(f"Overlay message: {data}")
            except Exception as e:
                print(f"Overlay WebSocket receive error: {e}")
                break
                
    except WebSocketDisconnect:
        print("Overlay WebSocket disconnected normally")
    except Exception as e:
        print(f"Overlay WebSocket error: {e}")
    finally:
        overlay_clients.discard(websocket)
        print(f"Overlay WebSocket cleaned up. Remaining clients: {len(overlay_clients)}")

@app.websocket("/ws/dashboard")  
async def dashboard_websocket(websocket: WebSocket):
    """WebSocket for moderation dashboard."""
    print(f"Dashboard WebSocket connection attempt from: {websocket.client}")
    try:
        await websocket.accept()
        dashboard_clients.add(websocket)
        print(f"✅ Dashboard WebSocket connected. Total clients: {len(dashboard_clients)}")
        
        # Send initial data
        pending = get_pending_events()
        await websocket.send_json({
            "type": "dashboard_init",
            "pending_events": pending,  # Already converted to dicts
            "auto_mode": AUTO_MODE
        })
        
        # Handle dashboard actions
        while True:
            try:
                data = await websocket.receive_json()
                print(f"Dashboard message: {data}")
                await handle_dashboard_message(websocket, data)
            except Exception as e:
                print(f"Dashboard WebSocket receive error: {e}")
                break
                
    except WebSocketDisconnect:
        print("Dashboard WebSocket disconnected normally")
    except Exception as e:
        print(f"Dashboard WebSocket error: {e}")
    finally:
        dashboard_clients.discard(websocket)
        print(f"Dashboard WebSocket cleaned up. Remaining clients: {len(dashboard_clients)}")

async def handle_dashboard_message(websocket: WebSocket, data: dict):
    """Handle dashboard WebSocket messages."""
    msg_type = data.get("type")
    
    if msg_type == "approve":
        event = approve_event(data.get("event_id"))
        if event:
            await broadcast_to_overlay({"type": "show_donation", "event": event.to_dict()})
            await broadcast_to_dashboard({"type": "event_approved", "event_id": event.id})
    
    elif msg_type == "skip":
        event = skip_event(data.get("event_id"))
        if event:
            await broadcast_to_dashboard({"type": "event_skipped", "event_id": event.id})
    
    elif msg_type == "toggle_auto":
        global AUTO_MODE
        AUTO_MODE = not AUTO_MODE
        await broadcast_to_dashboard({"type": "auto_mode_changed", "auto_mode": AUTO_MODE})

async def broadcast_to_overlay(message: Dict[str, Any]):
    """Send message to all overlay clients (OBS)."""
    for client in list(overlay_clients):
        try:
            await client.send_json(message)
        except:
            overlay_clients.discard(client)

async def broadcast_to_dashboard(message: Dict[str, Any]):
    """Send message to all dashboard clients."""
    for client in list(dashboard_clients):
        try:
            await client.send_json(message)
        except:
            dashboard_clients.discard(client)

async def handle_new_donation(donation_data: dict):
    """Process new donation from listener."""
    # Extract data
    signature = donation_data.get("signature", "")
    sender = donation_data.get("from", "")
    amount = float(donation_data.get("amount", 0))
    memo = donation_data.get("memo", "")
    
    # Classify tier (simple version)
    if amount >= 100000:
        tier = "whale"
    elif amount >= 10000: 
        tier = "high"
    elif amount >= 1000:
        tier = "mid"
    else:
        tier = "low"
    
    # Create event in database
    event = create_event(signature, sender, amount, memo, tier)
    
    # Notify dashboard of new event
    await broadcast_to_dashboard({
        "type": "new_event",
        "event": event.to_dict()
    })
    
    # Auto-approve if in auto mode and not banned
    if AUTO_MODE and not event.auto_filtered:
        approved_event = approve_event(event.id)
        await broadcast_to_overlay({
            "type": "show_donation",
            "event": approved_event.to_dict()
        })

@app.on_event("startup")
async def startup():
    """Initialize on startup."""
    print("Starting AI16Z Stream Overlay Backend...")
    init_db()
    print("Database ready")
    
    # Start blockchain listener if configured
    if start_listener_task and os.getenv("HELIUS_API_KEY") and os.getenv("PRIZE_WALLET_ADDRESS"):
        asyncio.create_task(start_listener_task(handle_new_donation))
        print("Blockchain listener started")
    
    print("Backend ready!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)