"""
Simple database models for stream overlay donations.
"""

from sqlalchemy import Column, String, Integer, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Event(Base):
    """A donation event with memo for the stream overlay."""
    __tablename__ = "events"
    
    # Primary key: transaction signature
    id = Column(String, primary_key=True)
    
    # Transaction data
    signature = Column(String, nullable=False)
    sender = Column(String, nullable=False) 
    amount = Column(Float, nullable=False)
    memo = Column(Text, nullable=False)
    tier = Column(String, nullable=False)  # low/mid/high/whale
    
    # Status: pending, approved, skipped
    status = Column(String, default="pending", nullable=False)
    
    # Timestamps
    created_at = Column(Integer, nullable=False)
    decided_at = Column(Integer, nullable=True)
    
    # Simple flags
    auto_filtered = Column(Boolean, default=False)  # flagged by banned words
    
    def to_dict(self):
        """Convert to dictionary for JSON responses."""
        return {
            "id": self.id,
            "signature": self.signature,
            "sender": self.sender,
            "amount": self.amount,
            "memo": self.memo,
            "tier": self.tier,
            "status": self.status,
            "created_at": self.created_at,
            "decided_at": self.decided_at,
            "auto_filtered": self.auto_filtered
        }


class BannedWord(Base):
    """Simple banned words list for content filtering."""
    __tablename__ = "banned_words"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String, nullable=False, unique=True)
    active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "word": self.word,
            "active": self.active
        }