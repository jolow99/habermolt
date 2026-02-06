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

"""Social ranking method that implements the Schulze method."""

import numpy as np
from typing_extensions import override

from habermas_machine.social_choice import base_method
from habermas_machine.social_choice import utils


class Schulze(base_method.Base):
  """Schulze social ranking method (Schulze, M. 2011).

  We follow the steps from https://electowiki.org/wiki/Schulze_method.
  """

  @override
  def aggregate(
      self,
      rankings: np.ndarray,
      seed: int | None = None,
  ) -> base_method.SocialRankingResult:
    """Aggregates rankings into a single social ranking and unties the ranking.

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
    rng = np.random.default_rng(seed)

    rankings = utils.filter_out_mocks(rankings)
    if rankings.size == 0:
      social_ranking_with_ties = np.full(
          (rankings.shape[1]), utils.RANKING_MOCK, dtype=np.int32)
      social_ranking_without_ties = rng.permutation(
          np.arange(rankings.shape[1])).astype(np.int32)
      return base_method.SocialRankingResult(
          social_ranking_with_ties, social_ranking_without_ties
      )
    social_ranking = self.aggregate_with_ties(rankings)

    # Return if there are no ties or the method is TIES_ALLOWED.
    if (
        utils.is_untied_ranking(social_ranking)
        or self._tie_breaking_method == utils.TieBreakingMethod.TIES_ALLOWED
    ):
      return base_method.SocialRankingResult(social_ranking, social_ranking)
    # If not, we need to break the ties.
    else:
      tied_social_ranking = social_ranking.copy()

      # Schulze tie-breaking ranking of the candidates (TBRC).
      if self._tie_breaking_method == utils.TieBreakingMethod.TBRC:
        # Copy and shuffle rankings so we can randomly select ballots.
        random_ballots = rankings.copy()
        rng.shuffle(random_ballots)

        # Each iteration, we try one random ballot and keep track of already
        # untied positions.
        for random_ballot in random_ballots:  # Loop over shuffled ballots.
          # Untie social ranking with random ballot.
          social_ranking = utils.untie_ranking_with_ballot(
              social_ranking, random_ballot
          )
          # Exit the while loop if there are no more ties.
          if utils.is_untied_ranking(social_ranking):
            return base_method.SocialRankingResult(
                tied_social_ranking,
                social_ranking,
            )

      # If there are still ties or the method is random, break ties randomly.
      if self._tie_breaking_method in [
          utils.TieBreakingMethod.RANDOM,
          utils.TieBreakingMethod.TBRC,
      ]:
        # New random ballot that can be added to untie rankings.
        random_ballot = np.arange(social_ranking.size)
        rng.shuffle(random_ballot)
        social_ranking = utils.untie_ranking_with_ballot(
            social_ranking, random_ballot
        )
        return base_method.SocialRankingResult(
            tied_social_ranking,
            social_ranking,
        )
      raise ValueError(
          f'tie_breaking_method {self._tie_breaking_method.name} is not'
          ' supported.'
      )

  def aggregate_with_ties(
      self,
      rankings: np.ndarray,
  ) -> np.ndarray:
    """Aggregates rankings into a single social ranking with potential ties."""

    utils.check_rankings(rankings)

    pairwise_defeats = self._compute_pairwise_defeats(rankings)
    strongest_path_strengths = self._compute_strongest_path_strengths(
        pairwise_defeats)
    social_ranking = self._rank_candidates(
        strongest_path_strengths)
    return social_ranking

  def _compute_pairwise_defeats(self, rankings: np.ndarray) -> np.ndarray:
    """Computes the number of votes who prefer one over the other candidate.

    Args:
      rankings: Array of batched rankings with dimensions: [num_citizens,
        num_candidates].

    Returns:
      An array with the number of voters who prefer candidate x to candidate y.
        Dimensions [num_candidates, num_candidates].
    """
    num_citizens, num_candidates = rankings.shape
    pairwise_defeats = np.zeros(
        (num_candidates, num_candidates), dtype=np.int32)
    for citizen_id in range(num_citizens):
      for idx in range(num_candidates):
        for idy in range(num_candidates):
          # Lower is better as the higest rank is 0.
          if rankings[citizen_id, idx] < rankings[citizen_id, idy]:
            pairwise_defeats[idx, idy] += 1
    return pairwise_defeats

  def _compute_strongest_path_strengths(
      self, pairwise_defeats: np.ndarray) -> np.ndarray:
    """Computes the strength of the strongest path between candidates.

    Args:
      pairwise_defeats: An array with the number of voters who prefer candidate
          x to candidate y. Dimensions [num_candidates, num_candidates].
    Returns:
      An array with the strength of the strongest path between candidate x and
      candidate y. Dimensions [num_candidates, num_candidates].
    """
    if len(set(pairwise_defeats.shape)) != 1:
      raise ValueError('pairwise_defeats should be a square array.')
    if np.any(np.diag(pairwise_defeats) != 0):
      raise ValueError('pairwise_defeats should have an all zero diagonal.')

    num_candidates = pairwise_defeats.shape[0]
    path_strengths = np.zeros((num_candidates, num_candidates), dtype=np.int32)
    for idx in range(num_candidates):
      for idy in range(num_candidates):
        if idx != idy:
          if pairwise_defeats[idx, idy] > pairwise_defeats[idy, idx]:
            path_strengths[idx, idy] = pairwise_defeats[idx, idy]

    for idx in range(num_candidates):
      for idy in range(num_candidates):
        if idx != idy:
          for idz in range(num_candidates):
            if idx != idz and idy != idz:
              path_strengths[idy, idz] = max(
                  path_strengths[idy, idz],
                  min(path_strengths[idy, idx], path_strengths[idx, idz]),
              )

    return path_strengths

  def _rank_candidates(self, path_strengths: np.ndarray) -> np.ndarray:
    """Rank the candidates by winning path strength.

    Args:
      path_strengths: An array with the strength of the strongest path between
        candidate x and candidate y. Dimensions [num_candidates,
        num_candidates].
    Returns:
      An array with the aggregated social rank for each candidate. Dimensions
        [num_candidates,]. Note that this social rank can contain ties.
    """

    if len(set(path_strengths.shape)) != 1:
      raise ValueError('The path_strengths array should be square.')
    if np.any(np.diag(path_strengths) != 0):
      raise ValueError('path_strengths should have an all zero diagonal.')

    # Compute the margin array and determine pairwise weak preferences.
    pairwise_dominance = (path_strengths - path_strengths.T) >= 0

    # Potential winners are those are preferred (weakly) most often.
    weakly_preferred_count = pairwise_dominance.sum(axis=1)

    # We can compute the rankings from the weakly preferred count as the binary
    # relationships (A >= B) from Schulze are transitive (see page 200 from
    # https://arxiv.org/pdf/1804.02973.pdf).
    _, rankings = np.unique(-1 * weakly_preferred_count, return_inverse=True)
    return rankings
