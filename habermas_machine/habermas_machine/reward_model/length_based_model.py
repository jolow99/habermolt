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

"""A ranking model that always chooses the longest statement."""

from collections.abc import Sequence

import numpy as np
from typing_extensions import override

from habermas_machine.llm_client import base_client
from habermas_machine.reward_model import base_model
from habermas_machine.social_choice import utils


class LongestStatementRankingModel(base_model.BaseRankingModel):
  """A ranking model that always chooses the longest statement.

  This model demonstrates a simple ranking strategy based on the length of the
  statements. It will always assign the highest rank (lowest value) to the
  longest statement, and so on. This is a naive approach and is not expected
  to perform well in realistic scenarios.
  """

  @override
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
  ) -> base_model.RankingResult:
    """Ranks statements based on their length (see base class)."""
    del (
        llm_client,
        question,
        opinion,
        previous_winner,
        critique,
        seed,
        num_retries_on_error,
    )
    lengths = np.array([len(s) for s in statements])
    non_normalized_ranking = lengths.max() - lengths
    return base_model.RankingResult(
        ranking=utils.normalize_ranking(non_normalized_ranking),
        explanation='Longest statement ranking.',
    )
