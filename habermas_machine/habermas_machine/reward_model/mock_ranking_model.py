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

"""Mock ranking model."""

from collections.abc import Sequence

import numpy as np
from typing_extensions import override

from habermas_machine.llm_client import base_client
from habermas_machine.reward_model import base_model
from habermas_machine.social_choice import utils


class MockRankingModel(base_model.BaseRankingModel):
  """Ranking model that always returns the mock ranking for each item."""

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
    """Samples text from the model (see base class)."""
    del (
        llm_client,
        question,
        opinion,
        previous_winner,
        critique,
        seed,
        num_retries_on_error,
    )
    return base_model.RankingResult(
        ranking=np.array([utils.RANKING_MOCK] * len(statements)),
        explanation='Mock ranking.',
    )
