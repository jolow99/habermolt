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

from habermas_machine.social_choice import mock_method
from habermas_machine.social_choice import utils


class MockTest(parameterized.TestCase):

  @parameterized.named_parameters(
      ('2 citizens, 2 candidates', 2, 2),
      ('3 citizens, 4 candidates', 3, 4),
  )
  def test_aggregate(self, num_citizens: int, num_candidates: int):
    """Tests aggregate."""
    rankings = np.random.randint(
        0, num_candidates, size=(num_citizens, num_candidates)
    )
    social_ranking, untied_social_ranking = mock_method.Mock(
        utils.TieBreakingMethod.TIES_ALLOWED
    ).aggregate(rankings)
    expected_social_ranking = np.full(
        (num_candidates), 0, dtype=np.int32
    )
    expected_untied_social_ranking = np.arange(num_candidates, dtype=np.int32)
    np.testing.assert_array_equal(social_ranking, expected_social_ranking)
    np.testing.assert_array_equal(
        untied_social_ranking, expected_untied_social_ranking
    )


if __name__ == '__main__':
  absltest.main()
