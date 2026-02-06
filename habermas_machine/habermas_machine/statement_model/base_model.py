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

"""Base class for statement models."""

import abc
from collections.abc import Sequence
from typing import NamedTuple

from habermas_machine.llm_client import base_client

StatementResult = NamedTuple(
    'StatementResult',
    [
        ('statement', str),
        ('explanation', str),
    ],
)


class BaseStatementModel(abc.ABC):
  """Base class for reward models that rank multiple statements."""

  @abc.abstractmethod
  def generate_statement(
      self,
      llm_client: base_client.LLMClient,
      question: str,
      opinions: Sequence[str],
      previous_winner: str | None = None,
      critiques: Sequence[str] | None = None,
      seed: int | None = None,
      num_retries_on_error: int = 1,
  ) -> StatementResult:
    """Samples text from the model.

    Args:
      llm_client: The LLM client used to generate the statement.
      question: Question that the citizens are responding to.
      opinions: Text-based opinions of the citizens.
      previous_winner: The statement that won the previous round.
      critiques: Critiques of the previous winner.
      seed: Optional seed for the sampling. If None a random seed will be used.
      num_retries_on_error: Number of retries when it hits an error. Default is
        1. If it runs out of retries, it returns the last result.

    Returns:
      A tuple containing:
        - The predicted statement.
        - The explanation (e.g. chain-of-thought)
    """
    raise NotImplementedError('generate_statement method is not implemented.')
