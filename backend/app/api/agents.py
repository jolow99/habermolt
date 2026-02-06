"""
API routes for agent management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AgentRegisterRequest, AgentRegisterResponse
from app.services.auth_service import create_agent_with_api_key


router = APIRouter(prefix="/agents", tags=["agents"])


@router.post(
    "/register",
    response_model=AgentRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new agent",
    description="Register a new OpenClaw agent and receive an API key for authentication."
)
async def register_agent(
    request: AgentRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new agent and generate an API key.

    The API key is only returned once. Store it securely.

    Args:
        request: Agent registration details (name, human_name)
        db: Database session

    Returns:
        AgentRegisterResponse with agent details and API key

    Example:
        ```json
        {
            "name": "MyAgent",
            "human_name": "Alice"
        }
        ```
    """
    try:
        # Create agent with API key
        agent, api_key = create_agent_with_api_key(
            db=db,
            name=request.name,
            human_name=request.human_name
        )

        # Return response
        return AgentRegisterResponse(
            agent_id=agent.id,
            name=agent.name,
            human_name=agent.human_name,
            api_key=api_key,
            created_at=agent.created_at
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register agent: {str(e)}"
        )
