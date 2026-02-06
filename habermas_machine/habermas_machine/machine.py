# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Habermas Machine."""

from collections.abc import Sequence

import numpy as np

from habermas_machine import types
from habermas_machine import utils
from habermas_machine.llm_client import base_client
from habermas_machine.reward_model import base_model as base_reward_model
from habermas_machine.social_choice import base_method as base_social_choice
from habermas_machine.statement_model import base_model as base_statement_model


class HabermasMachine:
  """Mediates caucus deliberation among participants.

  The Habermas Machine facilitates AI-mediated deliberation among a group of
  participants on a given question. It acts as a "mediator," iteratively
  refining a group statement that aims to capture the common ground of the
  participants' opinions.

  The process involves:

  1. Gathering initial opinions from participants.
  2. Generating candidate group statements using a Large Language Model (LLM).
  3. Evaluating these statements using a personalized reward model, predicting
     the order of preference of each participant for each statement.
  4. Aggregating individual preferences using a social choice method to select
     a winning statement.
  5. Gathering critiques of the winning statement from participants.
  6. Generating revised statements based on the critiques and previous opinions.
  7. Optionally, repeating steps 3-6 for multiple rounds, refining the statement
     iteratively. In the paper, we use one opinion and one critique round.

  This class manages the entire deliberation process, including interaction with
  the LLM, the reward model, and the social choice mechanism.  It maintains the
  history of opinions, critiques, candidate statements, and winning statements
  for each round.
  """

  def __init__(
      self,
      question: str,
      statement_client: base_client.LLMClient,
      reward_client: base_client.LLMClient,
      statement_model: base_statement_model.BaseStatementModel,
      reward_model: base_reward_model.BaseRankingModel,
      social_choice_method: base_social_choice.Base,
      num_candidates: int = 16,
      num_citizens: int = 5,
      seed: int | None = None,
      verbose: bool = False,
      num_retries_on_error: int | None = 8,
  ):
    """Initializes the Habermas Machine."""
    self._question = question  # Question to be answered.
    self._round = 0  # Current round (round 0 is the opinion round).
    self._critiques = []  # Critiques from current and previous rounds.
    self._statement_client = statement_client
    self._reward_client = reward_client
    self._statement_model = statement_model
    self._reward_model = reward_model
    self._social_choice_method = social_choice_method
    self._num_candidates = num_candidates  # Number of candidates to generate.
    self._rng = np.random.default_rng(seed)  # Random number generator.
    self._num_citizens = num_citizens
    self._previous_winners = []  # Winning statements from previous rounds.
    self._ranking_explanations = []  # Explanations for the rankings.
    self._previous_tied_rankings = []  # Rankings from previous rounds.
    self._previous_untied_rankings = []  # Untied rankings from previous rounds.
    self._statement_explanations = []  # Explanations for the statements.
    self._previous_candidates = []  # Candidates from previous rounds.
    self._verbose = verbose  # Whether to print round information.
    self._opinions = []  # Initial opinions.
    # Number of retries when the model returns an erroroneous response.
    self._num_retries_on_error = num_retries_on_error

  def _get_new_seed(self):
    """Generates a new random seed."""
    return self._rng.integers(np.iinfo(np.int32).max)

  def _generate_statements(
      self,
  ) -> tuple[list[str], list[str]]:  # statements, explanations.
    """Generates candidate statements."""
    statements = []
    explanations = []
    for _ in range(self._num_candidates):
      # Shuffle the opinions and critiques to avoid ordering bias.
      indices = self._rng.permutation(self._num_citizens)
      shuffled_opinions = [self._opinions[j] for j in indices]
      shuffled_critiques = (
          [self._critiques[-1][i] for i in indices] if self._critiques else None
      )
      statement, explanation = self._statement_model.generate_statement(
          llm_client=self._statement_client,
          question=self._question,
          opinions=shuffled_opinions,
          previous_winner=(
              self._previous_winners[-1] if self._previous_winners else None),
          critiques=shuffled_critiques,
          seed=self._get_new_seed(),
          num_retries_on_error=self._num_retries_on_error,
      )
      statements.append(statement)
      explanations.append(explanation)
    return statements, explanations

  def _get_rankings(
      self, statements: list[str]) -> tuple[np.ndarray, list[None | str]]:
    """Gets rankings over all candidates for each citizen."""
    all_rankings = []
    explanations = []
    for i in range(self._num_citizens):
      # Shuffle the statements to avoid ordering bias.
      indices = self._rng.permutation(self._num_candidates)
      shuffled_statements = [statements[j] for j in indices]

      ranking, explanation = self._reward_model.predict_ranking(
          llm_client=self._reward_client,
          question=self._question,
          opinion=self._opinions[i],
          statements=shuffled_statements,
          previous_winner=(
              self._previous_winners[-1] if self._round > 0 else None
          ),
          critique=self._critiques[-1][i] if self._round > 0 else None,
          seed=self._get_new_seed(),
          num_retries_on_error=self._num_retries_on_error,
      )

      if ranking is None:
        raise ValueError(
            f"Ranking is None for citizen {i+1}. Explanation: {explanation}")

      unshuffled_ranking = np.full_like(ranking, fill_value=types.RANKING_MOCK)
      unshuffled_ranking[indices] = ranking
      all_rankings.append(unshuffled_ranking)
      explanations.append(explanation)
    return np.array(all_rankings), explanations

  def overwrite_previous_winner(self, winner: str):
    """Overwrites the last winner."""
    if self._round == 0:
      raise ValueError("There is no previous winner before the opinion round.")
    else:
      if self._verbose:
        print("\nOverwriting last winner.")
        print(f"Previous winner: {self._previous_winners[-1]}")
        print(f"New winner: {winner}")
      self._previous_winners[-1] = winner

  def mediate(
      self, opinions_or_critiques: Sequence[str]) -> tuple[str, list[str]]:
    """Runs a single medatiation step and returns the winning statement."""
    if len(opinions_or_critiques) != self._num_citizens:
      raise ValueError(
          f"Expected {self._num_citizens} opinions or critiques, got"
          f" {len(opinions_or_critiques)}."
      )

    if self._round == 0:
      self._opinions = list(opinions_or_critiques)
    else:
      self._critiques.append(list(opinions_or_critiques))

    if self._verbose:
      if self._round == 0:
        print("\n\nOpinion round.")
      else:
        print(f"\n\nCritique round {self._round}.")
      print(f"\nQuestion: {self._question}")
      print("\nOpinions:")
      for i, opinion in enumerate(self._opinions):
        print(f"\tCitizen {i + 1}: {opinion}")
      if self._round > 0:
        print(f"\nPrevious winner: {self._previous_winners[-1]}")
        print("\nCritiques:")
        for i, critique in enumerate(self._critiques[-1]):
          print(f"\tCitizen {i + 1}: {critique}")

    statements, statement_explanations = self._generate_statements()

    if self._verbose:
      print("\nStatements generated:")
      for i, statement in enumerate(statements):
        print(f"\tStatement {i+1}: {statement}")

    all_rankings, ranking_explanations = self._get_rankings(statements)
    if self._verbose:
      print("\nRankings:")
      for i, ranking in enumerate(all_rankings):
        print(
            f"\tCitizen {i + 1}:"
            f" {utils.numerical_ranking_to_ordinal_text(ranking)}"
        )

    tied_social_ranking, untied_social_ranking = (
        self._social_choice_method.aggregate(
            all_rankings, seed=self._get_new_seed()
        )
    )

    if self._verbose:
      print("\nUntied social ranking:")
      print(utils.numerical_ranking_to_ordinal_text(untied_social_ranking))
      print("\nPotentially tied social ranking:")
      print(utils.numerical_ranking_to_ordinal_text(tied_social_ranking))

    # Record the statements with tied and untied rankings.
    statements_with_tied_rankings = []
    statements_with_untied_rankings = []
    for idx, statement in enumerate(statements):
      statements_with_untied_rankings.append((
          statement,
          untied_social_ranking[idx],
      ))
      statements_with_tied_rankings.append((
          statement,
          tied_social_ranking[idx],
      ))
    self._previous_tied_rankings.append(statements_with_tied_rankings)
    self._previous_untied_rankings.append(statements_with_untied_rankings)

    # Get the sorted indices based on the social_ranking.
    sorted_indices = np.argsort(untied_social_ranking)

    # Reorder the statements based on the sorted indices.
    sorted_statements = [statements[i] for i in sorted_indices]
    sorted_statement_explanations = [
        statement_explanations[i] for i in sorted_indices
    ]
    winner = sorted_statements[0]
    self._ranking_explanations.append(ranking_explanations)
    self._statement_explanations.append(sorted_statement_explanations)
    self._previous_winners.append(winner)
    self._previous_candidates.append(sorted_statements)

    if self._verbose:
      print(f"\nWinning statement: {winner}")

    self._round += 1
    return winner, sorted_statements
