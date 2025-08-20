#!/usr/bin/env python3
"""
Test script to simulate donations for the overlay system.
"""

import asyncio
import time
from database import create_event, get_pending_events

def test_create_donations():
    """Create some test donation events."""
    print("Creating test donations...")
    
    # Test donations with different amounts and content
    donations = [
        ("sig1", "wallet123", 500, "Thanks for the stream!", "low"),
        ("sig2", "wallet456", 5000, "Great content as always", "mid"), 
        ("sig3", "wallet789", 50000, "This is a scam message", "high"),  # Should be auto-filtered
        ("sig4", "walletWhale", 200000, "Whale donation incoming!", "whale"),
    ]
    
    for sig, sender, amount, memo, tier in donations:
        event = create_event(sig, sender, amount, memo, tier)
        event_dict = event.to_dict()
        print(f"Created event: {event_dict['memo'][:30]}... (filtered: {event_dict['auto_filtered']})")
    
    # Check pending events
    pending = get_pending_events()
    print(f"\nPending events: {len(pending)}")
    for event in pending:
        print(f"- {event.memo[:30]}... (${event.amount:.0f})")

if __name__ == "__main__":
    test_create_donations()