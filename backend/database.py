"""
Simple database operations for stream overlay.
"""

import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import List

try:
    from .models import Base, Event, BannedWord
except ImportError:
    from models import Base, Event, BannedWord

# Simple SQLite setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///overlay.db")
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Create tables and add default banned words."""
    Base.metadata.create_all(bind=engine)
    
    # Add some default banned words
    with get_session() as db:
        if not db.query(BannedWord).first():
            default_words = ["scam", "fake", "spam", "bot", "rug"]
            for word in default_words:
                db.add(BannedWord(word=word))
            db.commit()

@contextmanager
def get_session():
    """Simple database session context manager."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def get_banned_words() -> List[str]:
    """Get list of active banned words."""
    with get_session() as db:
        words = db.query(BannedWord).filter(BannedWord.active == True).all()
        return [word.word.lower() for word in words]

def is_memo_banned(memo: str) -> bool:
    """Simple banned word check."""
    banned_words = get_banned_words()
    memo_lower = memo.lower()
    return any(word in memo_lower for word in banned_words)

def create_event(signature: str, sender: str, amount: float, memo: str, tier: str) -> Event:
    """Create a new donation event."""
    with get_session() as db:
        # Check if already exists
        existing = db.query(Event).filter(Event.id == signature).first()
        if existing:
            return existing
            
        # Auto-filter check
        auto_filtered = is_memo_banned(memo)
        
        # Create event
        event = Event(
            id=signature,
            signature=signature,
            sender=sender,
            amount=amount,
            memo=memo,
            tier=tier,
            status="pending" if auto_filtered else "pending",  # Always pending for now
            created_at=int(time.time()),
            auto_filtered=auto_filtered
        )
        
        db.add(event)
        db.commit()
        db.refresh(event)
        # Convert to dict to avoid session issues
        result = event.to_dict()
        db.expunge(event)
        return event

def get_pending_events() -> List[dict]:
    """Get all pending events for moderation."""
    with get_session() as db:
        events = db.query(Event).filter(Event.status == "pending").order_by(Event.created_at.asc()).all()
        # Convert to dicts while session is active
        return [event.to_dict() for event in events]

def approve_event(event_id: str) -> dict:
    """Approve an event."""
    with get_session() as db:
        event = db.query(Event).filter(Event.id == event_id).first()
        if event:
            event.status = "approved"
            event.decided_at = int(time.time())
            db.commit()
            db.refresh(event)
            return event.to_dict()
        return None

def skip_event(event_id: str) -> dict:
    """Skip an event."""
    with get_session() as db:
        event = db.query(Event).filter(Event.id == event_id).first()
        if event:
            event.status = "skipped" 
            event.decided_at = int(time.time())
            db.commit()
            db.refresh(event)
            return event.to_dict()
        return None

def clear_events():
    """Clear all events (for testing)."""
    with get_session() as db:
        count = db.query(Event).count()
        db.query(Event).delete()
        db.commit()
        return count