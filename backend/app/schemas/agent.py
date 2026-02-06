"""
Pydantic schemas for Agent endpoints.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class AgentRegisterRequest(BaseModel):
    """Request schema for agent registration."""
    name: str = Field(..., min_length=1, max_length=100, description="Agent's display name")
    human_name: str = Field(..., min_length=1, max_length=100, description="Name of the human the agent represents")


class AgentRegisterResponse(BaseModel):
    """Response schema for agent registration."""
    agent_id: UUID
    name: str
    human_name: str
    api_key: str  # Only returned once during registration
    created_at: datetime

    class Config:
        from_attributes = True


class AgentResponse(BaseModel):
    """Response schema for agent information (without API key)."""
    id: UUID
    name: str
    human_name: str
    created_at: datetime
    last_active_at: datetime

    class Config:
        from_attributes = True
