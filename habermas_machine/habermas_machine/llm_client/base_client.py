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

"""Base class for LLM clients."""

import abc
from collections.abc import Collection

DEFAULT_TEMPERATURE = 0.8
DEFAULT_TERMINATORS = ()
DEFAULT_TIMEOUT_SECONDS = 60
# We truncate the response if we detect the terminator string before the max
# tokens so we set a high default value for max tokens.
DEFAULT_MAX_TOKENS = 4096


class LLMClient(abc.ABC):
  """Language model client base class."""

  @abc.abstractmethod
  def sample_text(
      self,
      prompt: str,
      *,
      max_tokens: int = DEFAULT_MAX_TOKENS,
      terminators: Collection[str] = DEFAULT_TERMINATORS,
      temperature: float = DEFAULT_TEMPERATURE,
      timeout: float = DEFAULT_TIMEOUT_SECONDS,
      seed: int | None = None,
  ) -> str:
    """Samples text from the model.

    Args:
      prompt: The input text that the model conditions on.
      max_tokens: The maximum number of tokens in the response.
      terminators: The response will be terminated before any of these
        characters.
      temperature: Model temperature.
      timeout: Timeout for the request.
      seed: Optional seed for the sampling. If None a random seed will be used.

    Returns:
      The sampled response (i.e. does not include the prompt).

    Raises:
      TimeoutError: if the operation times out.
    """
    raise NotImplementedError('sample_text method is not implemented.')
