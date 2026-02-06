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
from habermas_machine.reward_model import mock_ranking_model


class MockRankingModelTest(parameterized.TestCase):

  def test_predict_ranking(self):
    """Tests predict_ranking."""
    model = mock_ranking_model.MockRankingModel()
    statements = ['a', 'b', 'c']
    expected_ranking = np.array(
        [types.RANKING_MOCK] * len(statements)
    )
    actual_ranking, explanation = model.predict_ranking(
        llm_client=types.LLMCLient.MOCK.get_client('mock_url'),
        question='mock_question',
        opinion='mock_opinion',
        statements=statements,
    )
    np.testing.assert_array_equal(actual_ranking, expected_ranking)
    self.assertEqual(explanation, 'Mock ranking.')

if __name__ == '__main__':
  absltest.main()
