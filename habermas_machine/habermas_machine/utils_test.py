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

from habermas_machine import utils


class ArrowRankingToStringTest(parameterized.TestCase):

  @parameterized.parameters([
      ([1, 2, 2, 0], "4 > 1 > 2 = 3"),
      ([2, 1, 0, 2], "3 > 2 > 1 = 4"),
      ([0, 1, 2, 3], "1 > 2 > 3 > 4"),
      ([3, 3, 3, 3], "1 = 2 = 3 = 4"),
      ([3, 2, 1, 0], "4 > 3 > 2 > 1"),
      ([0], "1"),
      ([0, 0], "1 = 2"),
      ([1, 0], "2 > 1"),
  ])
  def test_numerical_ranking_to_ordinal_text(
      self, ranking_array, expected_string):
    result = utils.numerical_ranking_to_ordinal_text(np.array(ranking_array))
    self.assertEqual(result, expected_string)

  @parameterized.parameters([
      (None,),
      ("Not an array",),
      ([1.0, 2.0, 3.0],),
      ([1, "a", 3],)
  ])
  def test_numerical_ranking_to_ordinal_text_invalid_input(self, invalid_input):
    with self.assertRaises(ValueError):
      _ = utils.numerical_ranking_to_ordinal_text(np.array(invalid_input))

if __name__ == "__main__":
  absltest.main()
