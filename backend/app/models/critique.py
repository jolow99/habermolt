"""
Critique model for storing agent critiques of winning statements.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Critique(Base):
    """
    Represents an agent's critique of a winning statement.

    After each round, agents critique the statement that won the social choice vote.
    These critiques become input to the next round of the Habermas Machine.
    """

    __tablename__ = "critiques"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys
    deliberation_id = Column(UUID(as_uuid=True), ForeignKey("deliberations.id"), nullable=False, index=True)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False, index=True)
    winning_statement_id = Column(UUID(as_uuid=True), ForeignKey("statements.id"), nullable=False)

    # Round Information
    round_number = Column(Integer, nullable=False)  # Which critique round this is for

    # Content
    critique_text = Column(Text, nullable=False)

    # Timestamp
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    deliberation = relationship("Deliberation", back_populates="critiques")
    agent = relationship("Agent", back_populates="critiques")
    winning_statement = relationship("Statement", back_populates="critiques")

    # Constraints (one critique per agent per deliberation per round)
    __table_args__ = (
        UniqueConstraint("deliberation_id", "agent_id", "round_number", name="uq_critique_deliberation_agent_round"),
    )

    def __repr__(self) -> str:
        return f"<Critique(agent_id={self.agent_id}, deliberation_id={self.deliberation_id}, round={self.round_number})>"
