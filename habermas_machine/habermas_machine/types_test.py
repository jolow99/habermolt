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


class TypesTest(parameterized.TestCase):

  def test_llm_client(self):
    """Tests the LLMCLient type."""
    self.assertEqual(
        types.LLMCLient.MOCK.get_client('mock_url').sample_text('mock_prompt'),
        'Mock response.'
    )

  def test_reward_model(self):
    """Tests the RewardModel type."""
    np.testing.assert_array_equal(
        types.RewardModel.MOCK.get_model().predict_ranking(
            llm_client=types.LLMCLient.MOCK.get_client('mock_url'),
            question='mock_question',
            opinion='mock_opinion',
            statements=['mock_statement_1', 'mock_statement_2'],
        )[0],
        np.array([types.RANKING_MOCK, types.RANKING_MOCK]),
    )

  def test_statement_model(self):
    """Tests the StatementModel type."""
    self.assertEqual(
        types.StatementModel.MOCK.get_model().generate_statement(
            llm_client=types.LLMCLient.MOCK.get_client('mock_url'),
            question='mock_question',
            opinions=['mock_opinion_1', 'mock_opinion_2'],
            previous_winner='mock_previous_winner',
            critiques=['mock_critique_1', 'mock_critique_2'],
        ),
        (
            '\n'.join([
                'mock_question',
                'mock_opinion_1',
                'mock_opinion_2',
                'mock_previous_winner',
                'mock_critique_1',
                'mock_critique_2',
            ]),
            'Mock statement joining all inputs.',
        )
    )


if __name__ == '__main__':
  absltest.main()
