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

"""Common types for the Habermas Machine."""

import enum

from habermas_machine.llm_client import aistudio_client
from habermas_machine.llm_client import base_client
from habermas_machine.llm_client import mock_client
from habermas_machine.reward_model import base_model
from habermas_machine.reward_model import cot_ranking_model
from habermas_machine.reward_model import length_based_model
from habermas_machine.reward_model import mock_ranking_model
from habermas_machine.social_choice import base_method
from habermas_machine.social_choice import mock_method
from habermas_machine.social_choice import schulze_method
from habermas_machine.social_choice import utils as sc_utils
from habermas_machine.statement_model import base_model as statement_base_model
from habermas_machine.statement_model import cot_model
from habermas_machine.statement_model import mock_statement_model


RANKING_MOCK = sc_utils.RANKING_MOCK
TieBreakingMethod = sc_utils.TieBreakingMethod


@enum.unique
class LLMCLient(enum.Enum):
  """LLM client."""
  AISTUDIO = 'aistudio'
  MOCK = 'mock'

  def get_client(self, model: str) -> base_client.LLMClient:
    if self is self.MOCK:
      del model
      return mock_client.MockClient()
    elif self is self.AISTUDIO:
      return aistudio_client.AIStudioClient(model_name=model)
    else:
      raise ValueError('Unknown LLM client was specified.')


@enum.unique
class RewardModel(enum.Enum):
  """Reward model."""
  MOCK = 'mock'
  LENGTH_BASED = 'length_based'
  CHAIN_OF_THOUGHT_RANKING = 'chain_of_thought_ranking'

  def get_model(self) -> base_model.BaseRankingModel:
    if self is self.MOCK:
      return mock_ranking_model.MockRankingModel()
    elif self is self.LENGTH_BASED:
      return length_based_model.LongestStatementRankingModel()
    elif self is self.CHAIN_OF_THOUGHT_RANKING:
      return cot_ranking_model.COTRankingModel()
    else:
      raise ValueError('Unknown reward model was specified.')


@enum.unique
class StatementModel(enum.Enum):
  """Statement model."""
  MOCK = 'mock'
  CHAIN_OF_THOUGHT = 'chain_of_thought'

  def get_model(self) -> statement_base_model.BaseStatementModel:
    if self is self.MOCK:
      return mock_statement_model.MockStatementModel()
    elif self is self.CHAIN_OF_THOUGHT:
      return cot_model.COTModel()
    else:
      raise ValueError('Unknown statement model was specified.')


@enum.unique
class RankAggregation(enum.Enum):
  """Social ranking function for aggregating rankings from citizens."""
  MOCK = 'mock'
  SCHULZE = 'schulze'

  def get_method(
      self,
      tie_breaking_method: TieBreakingMethod,
  ) -> base_method.Base:
    """Returns the social ranking method."""
    if self is self.MOCK:
      return mock_method.Mock(tie_breaking_method)
    elif self is self.SCHULZE:
      return schulze_method.Schulze(tie_breaking_method)
    else:
      raise ValueError('Unknown social ranking function was specified.')
