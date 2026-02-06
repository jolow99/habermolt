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

import dataclasses

from absl.testing import absltest
from absl.testing import parameterized
import numpy as np

from habermas_machine.social_choice import schulze_method
from habermas_machine.social_choice import utils


@dataclasses.dataclass
class SchulzeTestData:
  testcase_name: str
  rankings: np.ndarray
  pairwise_defeats: np.ndarray
  strongest_path_strengths: np.ndarray
  social_ranking: np.ndarray


# Test cases taken from https://electowiki.org/wiki/Schulze_method.
schulze_test_cases = [
    SchulzeTestData(
        testcase_name='Example 1 (30 voters, 4 candidates)',
        rankings=np.int32(
            5 * [[0, 2, 1, 3]]
            + 2 * [[0, 3, 1, 2]]
            + 3 * [[0, 3, 2, 1]]
            + 4 * [[1, 0, 2, 3]]
            + 3 * [[3, 1, 0, 2]]
            + 3 * [[3, 2, 0, 1]]
            + 1 * [[1, 3, 2, 0]]
            + 5 * [[2, 1, 3, 0]]
            + 4 * [[3, 2, 1, 0]]
        ),
        pairwise_defeats=np.int32([
            [0, 11, 20, 14],
            [19, 0, 9, 12],
            [10, 21, 0, 17],
            [16, 18, 13, 0],
        ]),
        strongest_path_strengths=np.int32([
            [0, 20, 20, 17],
            [19, 0, 19, 17],
            [19, 21, 0, 17],
            [18, 18, 18, 0],
        ]),
        social_ranking=np.int32([1, 3, 2, 0]),
    ),
    SchulzeTestData(
        testcase_name='Example 2 (9 voters, 4 candidates)',
        rankings=np.int32(
            3 * [[0, 1, 2, 3]]
            + 2 * [[1, 2, 3, 0]]
            + 2 * [[3, 1, 2, 0]]
            + 2 * [[3, 1, 0, 2]]
        ),
        pairwise_defeats=np.int32([
            [0, 5, 5, 3],
            [4, 0, 7, 5],
            [4, 2, 0, 5],
            [6, 4, 4, 0],
        ]),
        strongest_path_strengths=np.int32([
            [0, 5, 5, 5],
            [5, 0, 7, 5],
            [5, 5, 0, 5],
            [6, 5, 5, 0],
        ]),
        social_ranking=np.int32([1, 0, 1, 0]),  # Ties.
    ),
    SchulzeTestData(
        testcase_name='Example 3 (2 voters, 4 candidates)',
        rankings=np.int32([[0, 0, 1, 2], [0, 1, 3, 2]]),
        pairwise_defeats=np.int32([
            [0, 1, 2, 2],
            [0, 0, 2, 2],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
        ]),
        strongest_path_strengths=np.int32([
            [0, 1, 2, 2],
            [0, 0, 2, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]),
        social_ranking=np.int32([0, 1, 2, 2]),
    ),
    SchulzeTestData(
        testcase_name='Example from MH (5 voters, 4 candidates)',
        rankings=np.int32(
            2 * [[0, 1, 3, 2]]
            + [[1, 3, 2, 0]]
            + [[2, 3, 0, 1]]
            + [[2, 0, 3, 1]]
        ),
        pairwise_defeats=np.int32([
            [0, 4, 4, 2],
            [1, 0, 3, 3],
            [1, 2, 0, 1],
            [3, 2, 4, 0],
        ]),
        strongest_path_strengths=np.int32([
            [0, 4, 4, 3],
            [3, 0, 3, 3],
            [0, 0, 0, 0],
            [3, 3, 4, 0],
        ]),
        social_ranking=np.int32([0, 1, 2, 0]),
    ),
    SchulzeTestData(
        testcase_name='Example for TBRC check (2 voters, 2 candidates)',
        rankings=np.int32([[0, 1], [1, 0]]),
        pairwise_defeats=np.int32([[0, 1], [1, 0]]),
        strongest_path_strengths=np.int32([[0, 0], [0, 0]]),
        social_ranking=np.int32([0, 0]),
    )
]


class SchulzeTest(parameterized.TestCase):

  @parameterized.named_parameters(
      {
          'testcase_name': 'Figure 1 opinion round',
          'rankings': np.int32(
              [[1, 2, 3, 4]]
              + [[2, 1, 4, 3]]
              + [[4, 1, 2, 3]]
              + [[2, 3, 4, 1]]
              + [[3, 2, 4, 1]]
          ),
          'social_ranking': np.int32([3, 1, 4, 2]),
      },
      {
          'testcase_name': 'Figure 1 critique round',
          'rankings': np.int32(
              [[3, 1, 2, 2]]
              + [[1, 3, 2, 2]]
              + [[3, 2, 2, 1]]
              + [[2, 3, 1, 1]]
              + [[4, 2, 1, 3]]
          ),
          'social_ranking': np.int32([3, 2, 1, 1]),
      },
  )
  def test_for_fig_1(self, rankings, social_ranking):
    """Tests the Schulze method for the example from Figure 1."""
    rankings = rankings - rankings.min()
    social_ranking = social_ranking - social_ranking.min()
    np.testing.assert_array_equal(
        schulze_method.Schulze(utils.TieBreakingMethod.TIES_ALLOWED).aggregate(
            rankings
        )[0],
        social_ranking,
    )

  @parameterized.named_parameters(
      [dataclasses.asdict(test_case) for test_case in schulze_test_cases]
  )
  def test_schulze_method(
      self,
      rankings: np.ndarray,
      pairwise_defeats: np.ndarray,
      strongest_path_strengths: np.ndarray,
      social_ranking: np.ndarray,
  ):
    """Tests the Schulze method."""
    # Test _compute_pairwise_defeats.
    np.testing.assert_array_equal(
        schulze_method.Schulze(
            utils.TieBreakingMethod.TIES_ALLOWED
        )._compute_pairwise_defeats(rankings),
        pairwise_defeats,
    )

    # Test _compute_strongest_path_strengths.
    np.testing.assert_array_equal(
        schulze_method.Schulze(
            utils.TieBreakingMethod.TIES_ALLOWED
        )._compute_strongest_path_strengths(
            pairwise_defeats
        ),
        strongest_path_strengths,
    )

    # Test _rank_candidates.
    np.testing.assert_array_equal(
        schulze_method.Schulze(
            utils.TieBreakingMethod.TIES_ALLOWED
        )._rank_candidates(strongest_path_strengths),
        social_ranking,
    )

    # Test aggregate.
    np.testing.assert_array_equal(
        schulze_method.Schulze(
            utils.TieBreakingMethod.TIES_ALLOWED
        ).aggregate_with_ties(rankings),
        social_ranking,
    )

  @parameterized.named_parameters([
      {
          'testcase_name': schulze_test_cases[0].testcase_name + '_RANDOM',
          'rankings': schulze_test_cases[0].rankings,
          'target_social_ranking': schulze_test_cases[0].social_ranking,
          'seed': 0,
          'tie_breaking_method': utils.TieBreakingMethod.RANDOM,
          'target_untied_ranking': schulze_test_cases[0].social_ranking,
      },
      {
          'testcase_name': schulze_test_cases[0].testcase_name + '_TBRC',
          'rankings': schulze_test_cases[0].rankings,
          'target_social_ranking': schulze_test_cases[0].social_ranking,
          'seed': 0,
          'tie_breaking_method': utils.TieBreakingMethod.TBRC,
          'target_untied_ranking': schulze_test_cases[0].social_ranking,
      },
      {
          'testcase_name': schulze_test_cases[3].testcase_name + '_TBRC',
          'rankings': schulze_test_cases[3].rankings,
          'target_social_ranking': schulze_test_cases[3].social_ranking,
          'seed': 1,
          'tie_breaking_method': utils.TieBreakingMethod.TBRC,
          'target_untied_ranking': np.int32([1, 2, 3, 0]),
      },
      {
          'testcase_name': schulze_test_cases[3].testcase_name + '_RANDOM',
          'rankings': schulze_test_cases[3].rankings,
          'target_social_ranking': schulze_test_cases[3].social_ranking,
          'seed': 1,
          'tie_breaking_method': utils.TieBreakingMethod.RANDOM,
          'target_untied_ranking': np.int32([0, 2, 3, 1]),
      },
      {
          'testcase_name': schulze_test_cases[4].testcase_name + '_TBRC_0',
          'rankings': schulze_test_cases[4].rankings,
          'target_social_ranking': schulze_test_cases[4].social_ranking,
          'seed': 0,
          'tie_breaking_method': utils.TieBreakingMethod.TBRC,
          'target_untied_ranking': np.int32([0, 1]),
      },
      {
          'testcase_name': schulze_test_cases[4].testcase_name + '_TBRC_3',
          'rankings': schulze_test_cases[4].rankings,
          'target_social_ranking': schulze_test_cases[4].social_ranking,
          'seed': 3,
          'tie_breaking_method': utils.TieBreakingMethod.TBRC,
          'target_untied_ranking': np.int32([1, 0]),
      },
      {
          'testcase_name': schulze_test_cases[4].testcase_name + '_RANDOM_0',
          'rankings': schulze_test_cases[4].rankings,
          'target_social_ranking': schulze_test_cases[4].social_ranking,
          'seed': 0,
          'tie_breaking_method': utils.TieBreakingMethod.RANDOM,
          'target_untied_ranking': np.int32([0, 1]),
      },
      {
          'testcase_name': schulze_test_cases[4].testcase_name + '_RANDOM_3',
          'rankings': schulze_test_cases[4].rankings,
          'target_social_ranking': schulze_test_cases[4].social_ranking,
          'seed': 3,
          'tie_breaking_method': utils.TieBreakingMethod.RANDOM,
          'target_untied_ranking': np.int32([1, 0]),
      },
  ])
  def test_schulze_aggregate(
      self,
      rankings: np.ndarray,
      target_social_ranking: np.ndarray,
      seed: int,
      tie_breaking_method: utils.TieBreakingMethod,
      target_untied_ranking: np.ndarray,
  ):
    """Tests Schulze().aggregate method."""
    social_ranking, untied_social_ranking = schulze_method.Schulze(
        tie_breaking_method
    ).aggregate(rankings, seed)
    np.testing.assert_array_equal(
        social_ranking,
        target_social_ranking,
    )
    np.testing.assert_array_equal(
        untied_social_ranking,
        target_untied_ranking,
    )

  @parameterized.named_parameters(
      ('Non-zero diagonal', np.int32([[0, 1, 1], [1, 1, 1], [1, 1, 0]])),
      (
          'Wrong dimensions',
          np.int32([[0, 1, 1], [1, 0, 1]]),
      ),
  )
  def test_rank_compute_strongest_path_strengths(self, pairwise_defeats):
    """Tests the Valueerrors of Schulze()._compute_strongest_path_strengths."""
    with self.assertRaises(ValueError):
      _ = schulze_method.Schulze(
          utils.TieBreakingMethod.TIES_ALLOWED
      )._compute_strongest_path_strengths(pairwise_defeats)

  @parameterized.named_parameters(
      ('Non-zero diagonal', np.int32([[0, 1, 1], [1, 1, 1], [1, 1, 0]])),
      (
          'Wrong dimensions',
          np.int32([[0, 1, 1], [1, 0, 1]]),
      ),
  )
  def test_rank_candidates(self, path_strengths):
    """Tests the ValueErrors of Schulze()._rank_candidates."""
    with self.assertRaises(ValueError):
      _ = schulze_method.Schulze(
          utils.TieBreakingMethod.TIES_ALLOWED)._rank_candidates(path_strengths)


if __name__ == '__main__':
  absltest.main()
