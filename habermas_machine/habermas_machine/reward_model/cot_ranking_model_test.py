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

from habermas_machine.reward_model import cot_ranking_model


class COTRankingModelTest(parameterized.TestCase):

  def test_check_response_format(self):
    """Tests the _check_response_format method."""
    self.assertTrue(
        cot_ranking_model._check_response_format(
            '<answer>Explanation\n<sep>\nA > B > C</answer>'
        )
    )
    self.assertFalse(
        cot_ranking_model._check_response_format(
            'Explanation\nA > B > C'
        )
    )

  def test_check_arrow_format(self):
    """Tests the _check_arrow_format method."""
    correct_formats = ['A>B>C', 'A=B>C>D', 'A>B=C=D>E', 'A=B=C']
    incorrect_formats = [
        'A<B>C',
        'A>>B>C',
        'A>B>A',
        'A>B=B>C',
        'A>B>C>B',
        'A>>B',
        'A>B>>C',
        'A=>B',
        'A>B>',
        '>A>B',
        'A=B=>C',
        'A>B=',
        'A=>B>C',
    ]
    for format_ in correct_formats:
      self.assertTrue(
          cot_ranking_model._check_arrow_format(format_)
      )
    for format_ in incorrect_formats:
      self.assertFalse(
          cot_ranking_model._check_arrow_format(format_)
      )

  @parameterized.named_parameters(
      {
          'testcase_name': 'Correct format',
          'text': 'Explanation\nA > B > C',
          'expected_ranking': 'A>B>C',
      },
      {
          'testcase_name': 'Correct format with extra spaces',
          'text': 'Explanation\n  A  >  B  >  C',
          'expected_ranking': 'A>B>C',
      },
      {
          'testcase_name': 'Correct format with extra spaces and =',
          'text': 'Explanation\n  A  =  B  >  C',
          'expected_ranking': 'A=B>C',
      },
      {
          'testcase_name': 'Incorrect format',
          'text': 'Explanation\nA > B < C > D',
          'expected_ranking': 'A>B',
      },
      {
          'testcase_name': 'No ranking',
          'text': 'Explanation',
          'expected_ranking': None,
      },
  )
  def test_extract_arrow_ranking(self, text, expected_ranking):
    """Tests the _extract_arrow_ranking method."""
    self.assertEqual(
        cot_ranking_model._extract_arrow_ranking(text),
        expected_ranking,
    )

  @parameterized.named_parameters(
      {
          'testcase_name': 'Correct answer',
          'response': '<answer>Explanation\n<sep>\nB>A=D>C</answer>',
          'expected_ranking': np.array([1, 0, 2, 1]),
          'expected_explanation': (
              '<answer>Explanation\n<sep>\nB>A=D>C</answer>'
          ),
      },
      {
          'testcase_name': 'Incorrect template',
          'response': 'Explanation\nB>A=D>C',
          'expected_ranking': None,
          'expected_explanation': 'INCORRECT_TEMPLATE: Explanation\nB>A=D>C',
      },
      {
          'testcase_name': 'Incorrect arrow ranking',
          'response': '<answer>Explanation\n<sep>\nB<A=D>C</answer>',
          'expected_ranking': None,
          'expected_explanation': (
              'INCORRECT_ARROW_RANKING: '
              '<answer>Explanation\n<sep>\nB<A=D>C</answer>'
          ),
      },
      {
          'testcase_name': 'Backup template',
          'response': 'Final ranking: B>A=D>C',
          'expected_ranking': np.array([1, 0, 2, 1]),
          'expected_explanation': 'Final ranking: B>A=D>C',
      },
      {
          'testcase_name': 'All tied',
          'response': '<answer>Explanation\n<sep>\nA=B=C=D</answer>',
          'expected_ranking': np.array([0, 0, 0, 0]),
          'expected_explanation': (
              '<answer>Explanation\n<sep>\nA=B=C=D</answer>'
          ),
      }
  )
  def test_process_model_response(
      self, response, expected_ranking, expected_explanation):
    """Tests the _process_model_response method."""
    if expected_ranking is None:
      num_statements = 0
    else:
      num_statements = len(expected_ranking)
    ranking_result = (
        cot_ranking_model._process_model_response(response, num_statements)
    )
    np.testing.assert_array_equal(ranking_result.ranking, expected_ranking)
    self.assertEqual(ranking_result.explanation, expected_explanation)


if __name__ == '__main__':
  absltest.main()
