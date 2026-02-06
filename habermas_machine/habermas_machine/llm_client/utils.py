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

"""LLM client utils."""

from collections.abc import Collection
import sys


def truncate(
    string: str,
    *,
    max_length: int = sys.maxsize,
    delimiters: Collection[str] = (),
) -> str:
  """Truncates a string to a maximum length up to a delimiter.

  Args:
    string: String to truncate
    max_length: Maximum length of the string.
    delimiters: Delimiters that must not be present in the truncated string.

  Returns:
    The longest prefix of string that does not exceed max_length and does not
    contain any delimiter.
  """
  truncated = string[:max_length]
  for delimiter in delimiters:
    truncated = truncated.split(delimiter, 1)[0] + delimiter
  return truncated
