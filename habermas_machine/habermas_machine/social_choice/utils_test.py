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

from absl.testing import absltest
from absl.testing import parameterized
import numpy as np

from habermas_machine.social_choice import utils


class UtilsTest(parameterized.TestCase):

  @parameterized.named_parameters(
      {
          'testcase_name': 'Normal ranking inc negative.',
          'ranking': np.int32([0, 5, -1]),
          'target_ranking': np.int32([1, 2, 0]),
          'should_raise': False,
      },
      {
          'testcase_name': 'Normal ranking.',
          'ranking': np.int32([0, 20, 10]),
          'target_ranking': np.int32([0, 2, 1]),
          'should_raise': False,
      },
      {
          'testcase_name': 'All tied.',
          'ranking': np.int32([99, 99, 99]),
          'target_ranking': np.int32([0, 0, 0]),
          'should_raise': False,
      },
      {
          'testcase_name': 'Wrong shape.',
          'ranking': np.int32([[0, 1], [0, 0]]),
          'target_ranking': None,
          'should_raise': True,
      },
  )
  def test_normalize_ranking(self, ranking, target_ranking, should_raise):
    """Tests _normalize_ranking method."""
    if should_raise:
      with self.assertRaises(ValueError):
        _ = utils.normalize_ranking(ranking)
    else:
      np.testing.assert_array_equal(
          utils.normalize_ranking(ranking),
          target_ranking,
      )

  @parameterized.named_parameters(
      {
          'testcase_name': 'Tied ranking.',
          'ranking': np.int32([0, 0, 1]),
          'is_untied': False,
          'should_raise': False,
      },
      {
          'testcase_name': 'Untied ranking.',
          'ranking': np.int32([0, 2, 1]),
          'is_untied': True,
          'should_raise': False,
      },
      {
          'testcase_name': 'Wrong shape.',
          'ranking': np.int32([[0, 1], [0, 0]]),
          'is_untied': None,
          'should_raise': True,
      },
  )
  def test_is_untied_ranking(self, ranking, is_untied, should_raise):
    """Tests _is_untied_ranking method."""
    if should_raise:
      with self.assertRaises(ValueError):
        _ = utils.is_untied_ranking(ranking)
    else:
      self.assertEqual(
          utils.is_untied_ranking(ranking),
          is_untied,
      )

  @parameterized.named_parameters(
      {
          'testcase_name': 'Already untied ranking.',
          'ranking': np.int32([0, 1, 2]),
          'ballot': np.int32([0, 5, 10]),
          'target_ranking': np.int32([0, 1, 2]),
          'should_raise': False,
      },
      {
          'testcase_name': 'Partially untie ranking.',
          'ranking': np.int32([0, 0, 0]),
          'ballot': np.int32([0, 0, 1]),
          'target_ranking': np.int32([0, 0, 1]),
          'should_raise': False,
      },
      {
          'testcase_name': 'Untie ranking.',
          'ranking': np.int32([0, 1, 1]),
          'ballot': np.int32([2, 1, 0]),
          'target_ranking': np.int32([0, 2, 1]),
          'should_raise': False,
      },
      {
          'testcase_name': 'Wrong ranking shape.',
          'ranking': np.int32([[0, 1], [0, 0]]),
          'ballot': np.int32([2, 1, 0]),
          'target_ranking': None,
          'should_raise': True,
      },
      {
          'testcase_name': 'No matching shape.',
          'ranking': np.int32([0, 1, 1]),
          'ballot': np.int32([2, 1, 0, 0]),
          'target_ranking': None,
          'should_raise': True,
      },
  )
  def test_untie_ranking_with_ballot(
      self, ranking, ballot, target_ranking, should_raise):
    """Tests _untie_ranking_with_ballot method."""
    if should_raise:
      with self.assertRaises(ValueError):
        _ = utils.untie_ranking_with_ballot(ranking, ballot)
    else:
      np.testing.assert_array_equal(
          utils.untie_ranking_with_ballot(ranking, ballot),
          target_ranking,
      )

  @parameterized.named_parameters(
      {
          'testcase_name': 'Ok rankings.',
          'rankings': np.int32([[0, 1], [0, 0]]),
          'should_raise': False,
          'allow_ties': True,
      },
      {
          'testcase_name': 'Wrong data type.',
          'rankings': np.array([[0.1, 1], [1, 0]]),
          'should_raise': True,
          'allow_ties': True,
      },
      {
          'testcase_name': 'Contains mock ranking.',
          'rankings': np.array([
              [utils.RANKING_MOCK, utils.RANKING_MOCK],
              [1, 0],
          ]),
          'should_raise': True,
          'allow_ties': True,
      },
      {
          'testcase_name': 'Best ranking is non-zero.',
          'rankings': np.int32([[0, 1], [1, 2]]),
          'should_raise': True,
          'allow_ties': True,
      },
      {
          'testcase_name': 'Ranking is non-zero.',
          'rankings': np.int32([[0, 1], [0, 3]]),
          'should_raise': True,
          'allow_ties': True,
      },
      {
          'testcase_name': 'Ranking ties while not allowed.',
          'rankings': np.int32([[0, 1], [0, 0]]),
          'should_raise': True,
          'allow_ties': False,
      },
      {
          'testcase_name': 'No ranking ties and not allowed.',
          'rankings': np.int32([[0, 1], [0, 1]]),
          'should_raise': False,
          'allow_ties': False,
      },
  )
  def test_check_rankings(self, rankings, should_raise, allow_ties):
    """Tests check_rankings method."""
    if should_raise:
      with self.assertRaises(ValueError):
        utils.check_rankings(rankings, allow_ties=allow_ties)
    else:
      utils.check_rankings(rankings, allow_ties=allow_ties)

  @parameterized.named_parameters(
      {
          'testcase_name': 'Wrong data type.',
          'rankings': np.array([[0.1, 1], [1, 0]]),
          'filtered_rankings': None,
          'should_raise': True,
      },
      {
          'testcase_name': 'Partial mock rankings.',
          'rankings': np.int32([[utils.RANKING_MOCK, 1], [1, 0]]),
          'filtered_rankings': None,
          'should_raise': True,
      },
      {
          'testcase_name': 'No mocks.',
          'rankings': np.int32([[0, 1], [0, 0]]),
          'filtered_rankings': np.int32([[0, 1], [0, 0]]),
          'should_raise': False,
      },
      {
          'testcase_name': 'All mocks.',
          'rankings': np.int32([
              [utils.RANKING_MOCK, utils.RANKING_MOCK],
              [utils.RANKING_MOCK, utils.RANKING_MOCK],
          ]),
          'filtered_rankings': np.empty(shape=(0, 2), dtype=np.int32),
          'should_raise': False,
      },
      {
          'testcase_name': 'Mocks for one citizen.',
          'rankings': np.int32([
              [0, 1],
              [utils.RANKING_MOCK, utils.RANKING_MOCK],
          ]),
          'filtered_rankings': np.int32([[0, 1]]),
          'should_raise': False,
      },
  )
  def test_filter_out_mocks(
      self, rankings, filtered_rankings, should_raise
  ):
    """Tests filter_out_mocks method."""
    if should_raise:
      with self.assertRaises(ValueError):
        utils.filter_out_mocks(rankings)
    else:
      np.testing.assert_array_equal(
          utils.filter_out_mocks(rankings), filtered_rankings
      )


if __name__ == '__main__':
  absltest.main()
