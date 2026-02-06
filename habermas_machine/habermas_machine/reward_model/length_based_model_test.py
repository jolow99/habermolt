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

from habermas_machine import types
from habermas_machine.reward_model import length_based_model


class LongestStatementRankingModelTest(parameterized.TestCase):

  @parameterized.named_parameters(
      {
          'testcase_name': 'no_ties',
          'statements': ['a', 'aa', 'aaa'],
          'expected_ranking': np.array([2, 1, 0]),
      },
      {
          'testcase_name': 'with_ties',
          'statements': ['a', 'aa', 'aa', 'aaa', 'a'],
          'expected_ranking': np.array([2, 1, 1, 0, 2]),
      },
  )
  def test_predict_ranking(self, statements, expected_ranking):
    """Tests predict_ranking."""
    model = length_based_model.LongestStatementRankingModel()
    actual_ranking, explanation = model.predict_ranking(
        llm_client=types.LLMCLient.MOCK.get_client('mock_url'),
        question='mock_question',
        opinion='mock_opinion',
        statements=statements,
    )
    np.testing.assert_array_equal(actual_ranking, expected_ranking)
    self.assertEqual(explanation, 'Longest statement ranking.')


if __name__ == '__main__':
  absltest.main()
