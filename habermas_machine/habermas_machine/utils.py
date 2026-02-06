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

"""Top-level utils for Habermas Machine."""


import numpy as np


def numerical_ranking_to_ordinal_text(ranking_array):
  """Converts a numerical ranking array to ordinal text representation.

  Elements with the same rank are ordered ascendingly by their original index.
  For example:
      * [1, 1, 0, 0] becomes "3 = 4 > 0 = 1"
      * [1, 2, 2, 0] becomes "4 > 1 > 2 = 3"
      * [0, 0, 2, 1] becomes "1 = 2 > 4 > 3"

  Args:
      ranking_array: The NumPy array of rankings.

  Returns:
      A string representing the arrow ranking or None if input is invalid.
  """

  if not isinstance(ranking_array, np.ndarray) or not np.issubdtype(
      ranking_array.dtype, np.integer
  ):
    raise ValueError(
        f"The array should be an integer array but is {ranking_array.dtype}."
    )

  n = len(ranking_array)
  ranked_elements = sorted(  # Use original indices
      zip(ranking_array, range(n)))

  result = []
  current_rank = -1  # Initialize to an invalid rank.
  current_group = []

  for rank, original_index in ranked_elements:
    if rank != current_rank:  # Start a new group
      if current_group:  # Append the previous group if it exists
        result.append(
            # Adjust the rank to start from 1.
            " = ".join(str(i + 1) for i in sorted(current_group)))
      current_rank = rank
      current_group = [original_index]
    else:
      current_group.append(original_index)

  result.append(" = ".join(str(i + 1) for i in sorted(current_group)))

  return " > ".join(result)
