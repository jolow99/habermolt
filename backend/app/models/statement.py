"""
Statement model for storing generated group statements from Habermas Machine.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.database import Base


class Statement(Base):
    """
    Represents a generated group statement from the Habermas Machine.

    The Habermas Machine generates ~16 candidate statements per round.
    Agents rank these statements, and social choice determines the winner.
    """

    __tablename__ = "statements"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys
    deliberation_id = Column(UUID(as_uuid=True), ForeignKey("deliberations.id"), nullable=False, index=True)

    # Round Information
    round_number = Column(Integer, nullable=False)  # 0 = opinion round, 1+ = critique rounds

    # Content
    statement_text = Column(Text, nullable=False)

    # Social Choice Results
    social_ranking = Column(Integer, nullable=True)  # 1 = winner, 2 = second place, etc.

    # Timestamp
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Metadata (JSONB)
    # Store: explanation, chain-of-thought reasoning, generation parameters, etc.
    metadata = Column(JSONB, default=dict)

    # Relationships
    deliberation = relationship("Deliberation", back_populates="statements")
    critiques = relationship("Critique", back_populates="winning_statement")
    human_feedback_entries = relationship("HumanFeedback", back_populates="final_statement")

    def __repr__(self) -> str:
        return f"<Statement(round={self.round_number}, ranking={self.social_ranking}, text='{self.statement_text[:50]}...')>"

    def is_winner(self) -> bool:
        """Check if this statement won its round."""
        return self.social_ranking == 1
