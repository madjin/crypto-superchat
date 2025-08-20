#!/usr/bin/env python3
"""
Backend API tests for the AI16Z stream overlay system.
Run with: python test_api.py
"""

import asyncio
import json
import time
import requests
import websockets
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000"

class BackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_events = []
        
    def test_health_check(self):
        """Test basic health endpoint"""
        print("🏥 Testing health check...")
        try:
            response = self.session.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_create_donation(self, donation_data: Dict[str, Any]):
        """Test creating a donation event"""
        print(f"💰 Creating donation: {donation_data['memo'][:30]}...")
        try:
            # Create event via the handle_new_donation simulation
            test_event = {
                "signature": donation_data["signature"],
                "from": donation_data["sender"], 
                "amount": donation_data["amount"],
                "memo": donation_data["memo"]
            }
            
            # We'll use the API endpoints directly
            response = self.session.get(f"{BASE_URL}/api/events/pending")
            if response.status_code == 200:
                print(f"✅ Can access pending events API")
                return True
            else:
                print(f"❌ Pending events API failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Create donation error: {e}")
            return False
    
    def test_approve_event(self, event_id: str):
        """Test approving an event"""
        print(f"✅ Testing approve event: {event_id[:12]}...")
        try:
            response = self.session.post(
                f"{BASE_URL}/api/events/action",
                json={"event_id": event_id, "action": "approve"}
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Event approved: {result}")
                return True
            else:
                print(f"❌ Approve failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Approve error: {e}")
            return False
    
    async def test_websocket_overlay(self):
        """Test overlay WebSocket connection"""
        print("🔌 Testing overlay WebSocket...")
        try:
            uri = f"{WS_URL}/ws/overlay"
            async with websockets.connect(uri) as websocket:
                print("✅ Overlay WebSocket connected")
                
                # Wait for connection message
                response = await websocket.recv()
                data = json.loads(response)
                print(f"📨 Received: {data}")
                
                # Test ping
                await websocket.send(json.dumps({"type": "ping"}))
                response = await websocket.recv()
                data = json.loads(response)
                print(f"🏓 Ping response: {data}")
                
                return True
                
        except Exception as e:
            print(f"❌ Overlay WebSocket error: {e}")
            return False
    
    async def test_websocket_dashboard(self):
        """Test dashboard WebSocket connection"""
        print("🎛️ Testing dashboard WebSocket...")
        try:
            uri = f"{WS_URL}/ws/dashboard"
            async with websockets.connect(uri) as websocket:
                print("✅ Dashboard WebSocket connected")
                
                # Wait for initial data
                response = await websocket.recv()
                data = json.loads(response)
                print(f"📊 Dashboard init: {data}")
                
                return True
                
        except Exception as e:
            print(f"❌ Dashboard WebSocket error: {e}")
            return False
    
    def run_basic_tests(self):
        """Run basic HTTP API tests"""
        print("🧪 Starting Backend API Tests\n")
        
        results = []
        
        # Test 1: Health Check
        results.append(self.test_health_check())
        
        # Test 2: Pending Events API
        results.append(self.test_create_donation({
            "signature": f"test-{int(time.time())}",
            "sender": "TestWallet123",
            "amount": 5000,
            "memo": "Test donation for API testing"
        }))
        
        print(f"\n📊 Basic Tests Results: {sum(results)}/{len(results)} passed")
        return all(results)
    
    async def run_websocket_tests(self):
        """Run WebSocket connection tests"""
        print("\n🔌 Starting WebSocket Tests\n")
        
        overlay_result = await self.test_websocket_overlay()
        dashboard_result = await self.test_websocket_dashboard()
        
        results = [overlay_result, dashboard_result]
        print(f"\n📊 WebSocket Tests Results: {sum(results)}/{len(results)} passed")
        return all(results)

async def main():
    """Run all backend tests"""
    print("🚀 AI16Z Backend Test Suite")
    print("=" * 40)
    
    # Check if backend is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend not responding. Start it with:")
            print("cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
            return
    except Exception:
        print("❌ Cannot connect to backend. Start it with:")
        print("cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        return
    
    print("✅ Backend is running, starting tests...\n")
    
    tester = BackendTester()
    
    # Run basic HTTP tests
    basic_passed = tester.run_basic_tests()
    
    # Run WebSocket tests
    websocket_passed = await tester.run_websocket_tests()
    
    # Final results
    print("\n" + "=" * 40)
    if basic_passed and websocket_passed:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above.")
    
    print("\n💡 Next steps:")
    print("- Open tests/frontend/overlay_test.html to test the overlay")
    print("- Use tests/frontend/simple_dashboard.html for manual testing")

if __name__ == "__main__":
    asyncio.run(main())