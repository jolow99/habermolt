"""
Authentication service for API key generation and validation.
"""

import secrets
import hashlib
from typing import Optional
from sqlalchemy.orm import Session

from app.models import Agent
from app.config import settings


def generate_api_key() -> str:
    """
    Generate a secure random API key.

    Returns:
        str: A URL-safe 32-byte random API key
    """
    return secrets.token_urlsafe(32)


def hash_api_key(api_key: str) -> str:
    """
    Hash an API key for secure storage.

    Uses SHA-256 with a salt from settings.

    Args:
        api_key: The plaintext API key

    Returns:
        str: Hexadecimal hash of the API key
    """
    salted = f"{api_key}{settings.API_KEY_SALT}".encode()
    return hashlib.sha256(salted).hexdigest()


def verify_api_key(db: Session, api_key: str) -> Optional[Agent]:
    """
    Verify an API key and return the associated agent.

    Args:
        db: Database session
        api_key: The plaintext API key to verify

    Returns:
        Agent if the key is valid, None otherwise
    """
    hashed = hash_api_key(api_key)
    agent = db.query(Agent).filter(Agent.api_key == hashed).first()
    return agent


def create_agent_with_api_key(
    db: Session,
    name: str,
    human_name: str
) -> tuple[Agent, str]:
    """
    Create a new agent with a generated API key.

    Args:
        db: Database session
        name: Agent's display name
        human_name: Name of the human the agent represents

    Returns:
        tuple: (Agent instance, plaintext API key)
               The plaintext key is only returned once and must be stored by the caller.
    """
    # Generate and hash API key
    plaintext_key = generate_api_key()
    hashed_key = hash_api_key(plaintext_key)

    # Create agent
    agent = Agent(
        name=name,
        human_name=human_name,
        api_key=hashed_key
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    # Return agent and plaintext key (only time it's available)
    return agent, plaintext_key
