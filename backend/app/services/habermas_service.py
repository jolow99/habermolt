"""
Habermas Machine service - wrapper for async integration with FastAPI.

Provides high-level methods for running opinion and critique rounds.
"""

import asyncio
from typing import List, Tuple
from sqlalchemy.orm import Session

from habermas_machine.machine import HabermasMachine
from habermas_machine import types
from habermas_machine.social_choice import utils as sc_utils

from app.config import settings
from app.models import Deliberation, Statement


class HabermasService:
    """
    Service for integrating Habermas Machine with the platform.

    Handles asynchronous execution of deliberation rounds and stores
    generated statements in the database.
    """

    def __init__(self):
        """Initialize Habermas service with configuration from settings."""
        self.num_candidates = settings.HABERMAS_NUM_CANDIDATES
        self.verbose = settings.HABERMAS_VERBOSE
        self.num_retries = settings.HABERMAS_NUM_RETRIES
        self.llm_model = settings.HABERMAS_LLM_MODEL

    def _create_machine(self, question: str, num_citizens: int) -> HabermasMachine:
        """
        Create a configured HabermasMachine instance.

        Args:
            question: The deliberation question
            num_citizens: Number of participating agents

        Returns:
            Configured HabermasMachine instance
        """
        # Configure LLM clients
        statement_client = types.LLMClient.AISTUDIO.get_client(model=self.llm_model)
        reward_client = types.LLMClient.AISTUDIO.get_client(model=self.llm_model)

        # Configure models
        statement_model = types.StatementModel.CHAIN_OF_THOUGHT.get_model()
        reward_model = types.RewardModel.CHAIN_OF_THOUGHT_RANKING.get_model()

        # Configure social choice (Schulze method with TBRC tie-breaking)
        social_choice = types.RankAggregation.SCHULZE.get_method(
            sc_utils.TieBreakingMethod.TBRC
        )

        # Create machine
        machine = HabermasMachine(
            question=question,
            statement_client=statement_client,
            reward_client=reward_client,
            statement_model=statement_model,
            reward_model=reward_model,
            social_choice_method=social_choice,
            num_candidates=self.num_candidates,
            num_citizens=num_citizens,
            verbose=self.verbose,
            num_retries_on_error=self.num_retries,
        )

        return machine

    async def run_opinion_round(
        self,
        db: Session,
        deliberation: Deliberation,
        opinions: List[str]
    ) -> Tuple[Statement, List[Statement]]:
        """
        Run the initial opinion round using the Habermas Machine.

        Args:
            db: Database session
            deliberation: The deliberation instance
            opinions: List of opinion texts from all agents

        Returns:
            tuple: (winning_statement, all_statements)
                   All statements are already stored in the database.
        """
        # Create machine
        machine = self._create_machine(deliberation.question, len(opinions))

        # Run mediate in thread (blocking operation)
        def _run_mediate():
            return machine.mediate(opinions)

        # Execute in thread pool to avoid blocking async event loop
        results = await asyncio.to_thread(_run_mediate)

        # Store statements in database
        statements = []
        for idx, (statement_text, rank) in enumerate(zip(results.statements, results.social_ranking)):
            statement = Statement(
                deliberation_id=deliberation.id,
                round_number=0,  # Opinion round is round 0
                statement_text=statement_text,
                social_ranking=int(rank),  # Convert numpy int to Python int
                meta_data={
                    "explanations": results.explanations[idx] if results.explanations else None,
                }
            )
            db.add(statement)
            statements.append(statement)

        db.commit()

        # Return winner (rank 1) and all statements
        winner = next(s for s in statements if s.social_ranking == 1)
        return winner, statements

    async def run_critique_round(
        self,
        db: Session,
        deliberation: Deliberation,
        opinions: List[str],
        critiques: List[str],
        round_number: int
    ) -> Tuple[Statement, List[Statement]]:
        """
        Run a critique round using the Habermas Machine.

        Args:
            db: Database session
            deliberation: The deliberation instance
            opinions: List of original opinion texts (needed by HM)
            critiques: List of critique texts from all agents
            round_number: The critique round number (1-indexed)

        Returns:
            tuple: (winning_statement, all_statements)
                   All statements are already stored in the database.
        """
        # Create machine
        machine = self._create_machine(deliberation.question, len(opinions))

        # Run mediate with critiques in thread (blocking operation)
        def _run_mediate():
            # First run with opinions to set up the machine
            machine.mediate(opinions)
            # Then run with critiques
            return machine.mediate(critiques)

        # Execute in thread pool
        results = await asyncio.to_thread(_run_mediate)

        # Store statements in database
        statements = []
        for idx, (statement_text, rank) in enumerate(zip(results.statements, results.social_ranking)):
            statement = Statement(
                deliberation_id=deliberation.id,
                round_number=round_number,
                statement_text=statement_text,
                social_ranking=int(rank),  # Convert numpy int to Python int
                meta_data={
                    "explanations": results.explanations[idx] if results.explanations else None,
                }
            )
            db.add(statement)
            statements.append(statement)

        db.commit()

        # Return winner (rank 1) and all statements
        winner = next(s for s in statements if s.social_ranking == 1)
        return winner, statements


# Global service instance
habermas_service = HabermasService()
