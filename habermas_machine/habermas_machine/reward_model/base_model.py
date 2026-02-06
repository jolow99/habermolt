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

"""Base class for reward models."""

import abc
from collections.abc import Sequence
from typing import NamedTuple

import numpy as np

from habermas_machine.llm_client import base_client


RankingResult = NamedTuple(
    'RankingResult',
    [
        ('ranking', np.ndarray | None),
        ('explanation', str | None),
    ],
)


class BaseRankingModel(abc.ABC):
  """Base class for reward models that rank multiple statements."""

  @abc.abstractmethod
  def predict_ranking(
      self,
      llm_client: base_client.LLMClient,
      question: str,
      opinion: str,
      statements: Sequence[str],
      previous_winner: str | None = None,
      critique: str | None = None,
      seed: int | None = None,
      num_retries_on_error: int = 1,
  ) -> RankingResult:
    """Samples text from the model.

    Args:
      llm_client: LLM client to use.
      question: Question that the citizen is responding to.
      opinion: Text-based opinion of the citizen.
      statements: Statements that are ranked.
      previous_winner: The statement that won the previous round.
      critique: Critique of the previous winner.
      seed: Optional seed for the model.
      num_retries_on_error: Number of retries when it hits an error. Default is
        1. If it runs out of retries, it returns the last result.

    Returns:
      A RankingResult tuple, consisting of:
        - Array of rankings with dimensions: [num_statements,]. In this array
          lower is better and the best candidate is thus given rank 0. For
          example, an array [0, 1, 0] corresponds to the first citizen
          preferring candidates 0 and 2 over candidate 1, while preferring
          candidates 0 and 2 equally. If the model has an error, None is
          returned.
        - Explanation for the ranking (for example the raw output including
          the chain-of-thought) or the error. None if there is no explanation.
    """
    raise NotImplementedError('predict_ranking method is not implemented.')
