"""
Opinion model for storing initial agent opinions.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Opinion(Base):
    """
    Represents an agent's initial opinion on a deliberation question.

    Each agent can submit exactly one opinion per deliberation.
    Opinions are used as input to the Habermas Machine's first round.
    """

    __tablename__ = "opinions"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys
    deliberation_id = Column(UUID(as_uuid=True), ForeignKey("deliberations.id"), nullable=False, index=True)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False, index=True)

    # Content
    opinion_text = Column(Text, nullable=False)

    # Timestamp
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    deliberation = relationship("Deliberation", back_populates="opinions")
    agent = relationship("Agent", back_populates="opinions")

    # Constraints
    __table_args__ = (
        UniqueConstraint("deliberation_id", "agent_id", name="uq_opinion_deliberation_agent"),
    )

    def __repr__(self) -> str:
        return f"<Opinion(agent_id={self.agent_id}, deliberation_id={self.deliberation_id})>"
