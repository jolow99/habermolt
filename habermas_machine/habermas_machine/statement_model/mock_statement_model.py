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

"""Mock statement model."""

from collections.abc import Sequence

from habermas_machine.llm_client import base_client
from habermas_machine.statement_model import base_model


class MockStatementModel(base_model.BaseStatementModel):
  """Mock statement model that just concatenates the inputs."""

  def generate_statement(
      self,
      llm_client: base_client.LLMClient,
      question: str,
      opinions: Sequence[str],
      previous_winner: str | None = None,
      critiques: Sequence[str] | None = None,
      seed: int | None = None,
      num_retries_on_error: int = 1,
  ) -> base_model.StatementResult:
    """Samples text from the model (see base class)."""
    del llm_client, seed, num_retries_on_error
    parts = [question, *opinions]
    if previous_winner is not None:
      parts.extend([previous_winner, *critiques])
    statement = '\n'.join(parts)
    return base_model.StatementResult(
        statement=statement,
        explanation='Mock statement joining all inputs.',
    )
