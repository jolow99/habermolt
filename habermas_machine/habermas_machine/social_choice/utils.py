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

"""Utils for social choice methods."""

import enum
import numpy as np


RANKING_MOCK = -1


class TieBreakingMethod(enum.Enum):
  """Method for breaking ties."""
  TIES_ALLOWED = 'ties_allowed'
  RANDOM = 'random'
  TBRC = 'tbrc'  # Schulze tie-breaking ranking of the candidates (TBRC).


def filter_out_mocks(rankings: np.ndarray) -> np.ndarray:
  """Filters out mock rankings and checks whether mocks are correctly used."""
  if not np.issubdtype(rankings.dtype, np.integer):
    raise ValueError(
        f'The array should be an integer array but is {rankings.dtype}.'
    )
  is_mock = rankings == RANKING_MOCK
  any_mock = is_mock.any(axis=1)
  all_mock = is_mock.all(axis=1)
  if not (any_mock == all_mock).all():
    raise ValueError(
        'If a citizen uses a mock rank for one candidate'
        'it should use a mock rank for all candidates.'
    )
  return rankings[np.logical_not(any_mock)]


def normalize_ranking(ranking: np.ndarray) -> np.ndarray:
  """Normalizes ranking so e.g. [0, 2, 5, 5] -> [0, 1, 2, 2]."""
  if ranking.ndim != 1:
    raise ValueError('The input array should be a single ranking so `ndim=1`')
  _, normalized_ranking = np.unique(ranking, return_inverse=True)
  return normalized_ranking


def is_untied_ranking(ranking: np.ndarray) -> bool:
  """Checks if the ranking is untied."""
  if ranking.ndim != 1:
    raise ValueError('The input array should be a single ranking so `ndim=1`')
  return np.unique(ranking).size == ranking.size


def check_rankings(rankings: np.ndarray, allow_ties: bool = True) -> None:
  """Checks if a ranking array is a valid ranking array.

  Args:
    rankings: Array of batched rankings with dimensions: [num_citizens,
        num_candidates]. In this array lower is better and the best candidate
        is thus given rank 0. For example, an array [[1, 0], [0, 0]] corresponds
        to the first citizen preferring candidate 1 over candidate 0 while the
        second citizen has no preference for either candidate over the other.
        We assume that the mock ranks have been filtered out.
    allow_ties: If True, rating ties are allowed.
  """
  if not np.issubdtype(rankings.dtype, np.integer):
    raise ValueError(
        f'The array should be an integer array but is {rankings.dtype}.')

  sorted_rankings = np.sort(rankings, axis=1)
  if np.any(sorted_rankings[:, 0] != 0):
    raise ValueError('All rankings should have a 0 as highest ranking')

  diff_sorted_rankings = np.diff(sorted_rankings, axis=1)

  if allow_ties:
    if not np.all(
        np.logical_or(diff_sorted_rankings == 1, diff_sorted_rankings == 0)):
      raise ValueError(
          'Incorrect ratings, the step size between ratings should be 0 or 1.')
  else:
    if not np.all(diff_sorted_rankings == 1):
      raise ValueError('Incorrect ratings, the step size between ratings should'
                       ' be 1 as ties are not allowed.')


def untie_ranking_with_ballot(
    ranking: np.ndarray, ballot: np.ndarray) -> np.ndarray:
  """Unties ranking with extra ballot and renormalizes rankings."""
  if ranking.ndim != 1:
    raise ValueError('The input array should be a single ranking so `ndim=1`')
  if ranking.shape != ballot.shape:
    raise ValueError('The ranking and ballot should have the same shape.')
  # We multiply the rankings with the number of candidates to ensure that we do
  # not change the order of the already sorted candidates. We then add a ballot
  # to untie the social ranking.
  ranking = normalize_ranking(
      ranking) * len(ranking) + normalize_ranking(ballot)

  # Renormalize the social ranking to make sure ranks are consecutive.
  return normalize_ranking(ranking)
