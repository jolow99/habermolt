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

"""Social ranking method that returns mock ranking."""

import numpy as np
from typing_extensions import override

from habermas_machine.social_choice import base_method


class Mock(base_method.Base):
  """Mock social ranking method."""

  @override
  def aggregate(
      self,
      rankings: np.ndarray,
      seed: int | None = None,
  ) -> base_method.SocialRankingResult:
    """Aggregates rankings into a single social ranking.

    Args:
      rankings: Array of batched rankings with dimensions: [num_citizens,
        num_candidates]. In this array lower is better and the best candidate
        is thus given rank 0. For example, an array [[1, 0], [0, 0]] corresponds
        to the first citizen preferring candidate 1 over candidate 0 while the
        second citizen has no preference for either candidate over the other.
      seed: Random seed that is used to break ties.

    Returns:
      A tuple of:
      - An array with the aggregated social rank for each candidate.
        If B>C>A, the array will be [2, 0, 1]. The array has dimensions:
        [num_candidates,]. In this array, ties are allowed and there can be
        multiple potential winners.
      - Untied aggregated social rank. The ranks are untied using the
        `tie_breaking_method`. If there were no ties in the social ranking,
        this just returns the same ranking.
    """
    del seed  # Not used in mock ranking.
    num_candidates = rankings.shape[1]
    social_ranking_with_ties = np.full(
        (num_candidates), 0, dtype=np.int32)
    social_ranking_without_ties = np.arange(num_candidates, dtype=np.int32)
    return base_method.SocialRankingResult(
        social_ranking_with_ties, social_ranking_without_ties
    )
