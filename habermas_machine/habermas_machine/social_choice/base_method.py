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

"""Base social ranking method for aggregating ranked preferences."""

import abc
from typing import NamedTuple

import numpy as np

from habermas_machine.social_choice import utils


RANKING_MOCK = utils.RANKING_MOCK


SocialRankingResult = NamedTuple(
    'SocialRankingResult',
    [
        ('social_ranking', np.ndarray),
        ('untied_social_ranking', np.ndarray),
    ],
)


class Base(abc.ABC):
  """Social ranking base class."""

  def __init__(self, tie_breaking_method: utils.TieBreakingMethod):
    """Initialize the Base class.

    Args:
        tie_breaking_method: Method that is used to break ties.
    """
    self._tie_breaking_method = tie_breaking_method

  @abc.abstractmethod
  def aggregate(
      self,
      rankings: np.ndarray,
      seed: int | None = None,
  ) -> SocialRankingResult:
    """Aggregates a set of rankings into a single social ranking.

    Args:
      rankings: Array of batched rankings with dimensions: [num_citizens,
        num_candidates]. In this array lower is better and the best candidate
        is thus given rank 0. For example, an array [[1, 0], [0, 0]] corresponds
        to the first citizen preferring candidate 1 over candidate 0 while the
        second citizen has no preference for either candidate over the other.
      seed: Optional seed for tie breaking.

    Return:
      A tuple of:
      - An array with the aggregated social rank for each candidate.
        If B>C>A, the array will be [2, 0, 1]. The array has dimensions:
        [num_candidates,]. In this array, ties are allowed and there can be
        multiple potential winners.
      - Untied aggregated social rank. The ranks are untied using the
        `tie_breaking_method`. If there were no ties in the social ranking,
        this just returns the same ranking.
    """
    raise NotImplementedError('Base class is not implemented.')
