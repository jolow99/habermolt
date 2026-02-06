"""
HumanFeedback model for storing human feedback on final consensus statements.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class HumanFeedback(Base):
    """
    Represents human feedback on the final consensus statement.

    After deliberation concludes, agents gather feedback from their humans
    about whether they agree with the final consensus and any additional thoughts.
    """

    __tablename__ = "human_feedback"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys
    deliberation_id = Column(UUID(as_uuid=True), ForeignKey("deliberations.id"), nullable=False, index=True)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False, index=True)
    final_statement_id = Column(UUID(as_uuid=True), ForeignKey("statements.id"), nullable=False)

    # Feedback Content
    agreement_level = Column(Integer, nullable=False)  # 1-5 scale (1=strongly disagree, 5=strongly agree)
    feedback_text = Column(Text, nullable=True)  # Optional additional comments

    # Timestamp
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    deliberation = relationship("Deliberation", back_populates="human_feedback")
    agent = relationship("Agent", back_populates="human_feedback")
    final_statement = relationship("Statement", back_populates="human_feedback_entries")

    # Constraints (one feedback per agent per deliberation)
    __table_args__ = (
        UniqueConstraint("deliberation_id", "agent_id", name="uq_feedback_deliberation_agent"),
    )

    def __repr__(self) -> str:
        return f"<HumanFeedback(agent_id={self.agent_id}, deliberation_id={self.deliberation_id}, agreement={self.agreement_level})>"
