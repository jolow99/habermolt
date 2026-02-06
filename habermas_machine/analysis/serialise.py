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

"""Library for serialisation and deserialisation."""

import dataclasses
from typing import List


@dataclasses.dataclass(frozen=True)
class SerialisedComparisonKeys:
  """Serialised comparison keys; used, for example, when working with pandas."""

  # pylint: disable=invalid-name
  ROUND_ID: str = 'round_id'
  LAUNCH_ID: str = 'launch_id'
  ITERATION_ID: str = 'iteration_id'
  ITERATION_INDEX: str = 'iteration_index'
  COMPARISON_ID: str = 'metadata.id'
  COMPARISON_TASK_DURATION: str = 'metadata.task_duration'
  COMPARISON_RESPONSE_DURATION: str = 'metadata.response_duration'
  COMPARISON_CREATED: str = 'metadata.created'
  COMPARISON_UPDATED: str = 'metadata.updated'
  COMPARISON_STATUS: str = 'metadata.status'
  COMPARISON_PARTICIPANT_ID: str = 'metadata.participant_id'
  COMPARISON_VERSION: str = 'metadata.version'
  COMPARISON_PROVENANCE: str = 'metadata.provenance'

  RATINGS_ID: str = 'ratings.metadata.id'
  RATINGS_AGREEMENT: str = 'ratings.agreement'
  RATINGS_QUALITY: str = 'ratings.quality'
  RATINGS_PROVENANCE: str = 'ratings.metadata.provenance'
  RATINGS_PARTICIPANT_ID: str = 'ratings.metadata.participant_id'
  RATINGS_RESPONSE_DURATION: str = 'ratings.metadata.response_duration'
  RATINGS_CREATED: str = 'ratings.metadata.created'
  RATINGS_STATUS: str = 'ratings.metadata.status'

  RANKINGS_ID: str = 'rankings.metadata.id'
  RANKINGS_CANDIDATE_IDS: str = 'rankings.candidate_ids'
  RANKINGS_NUMERICAL_RANKS: str = 'rankings.numerical_ranks'
  RANKINGS_EXPLANATION: str = 'rankings.explanation'
  RANKINGS_PROVENANCE: str = 'rankings.metadata.provenance'
  RANKINGS_PARTICIPANT_ID: str = 'rankings.metadata.participant_id'
  RANKINGS_RESPONSE_DURATION: str = 'rankings.metadata.response_duration'
  RANKINGS_CREATED: str = 'rankings.metadata.created'
  RANKINGS_STATUS: str = 'rankings.metadata.status'

  QUESTION_ID: str = 'question.id'
  QUESTION_TEXT: str = 'question.text'
  SPLIT: str = 'question.split'
  QUESTION_PROVENANCE: str = 'question.provenance'
  QUESTION_TOPIC: str = 'question.topic'
  QUESTION_AFFIRMING_STATEMENT: str = 'question.affirming_statement'
  QUESTION_NEGATING_STATEMENT: str = 'question.negating_statement'

  OWN_OPINION_ID: str = 'own_opinion.metadata.id'
  OWN_OPINION_TEXT: str = 'own_opinion.text'
  OWN_OPINION_PROVENANCE: str = 'own_opinion.metadata.provenance'
  OWN_OPINION_DISPLAY_LABEL: str = 'own_opinion.display_label'
  OWN_OPINION_PARTICIPANT_ID: str = 'own_opinion.metadata.participant_id'
  OWN_OPINION_RESPONSE_DURATION: str = 'own_opinion.metadata.response_duration'
  OWN_OPINION_CREATED: str = 'own_opinion.metadata.created'
  OWN_OPINION_UPDATED: str = 'own_opinion.metadata.updated'
  OWN_OPINION_STATUS: str = 'own_opinion.metadata.status'

  OTHER_OPINIONS_ID: str = 'other_opinions.metadata.id'
  OTHER_OPINIONS_TEXT: str = 'other_opinions.text'
  OTHER_OPINIONS_PROVENANCE: str = 'other_opinions.metadata.provenance'
  OTHER_OPINIONS_DISPLAY_LABEL: str = 'other_opinions.display_label'
  OTHER_OPINIONS_PARTICIPANT_ID: str = 'other_opinions.metadata.participant_id'
  OTHER_OPINIONS_RESPONSE_DURATION: str = (
      'other_opinions.metadata.response_duration'
  )
  OTHER_OPINIONS_CREATED: str = 'other_opinions.metadata.created'
  OTHER_OPINIONS_UPDATED: str = 'other_opinions.metadata.updated'
  OTHER_OPINIONS_STATUS: str = 'other_opinions.metadata.status'

  CANDIDATES_ID: str = 'candidates.metadata.id'
  CANDIDATES_TEXT: str = 'candidates.text'
  CANDIDATES_PROVENANCE: str = 'candidates.metadata.provenance'
  CANDIDATES_DISPLAY_LABEL: str = 'candidates.display_label'
  CANDIDATES_PROMPT_TEXT: str = 'candidates.prompt_text'
  CANDIDATES_TOTAL_PROMPT_TEXT: str = 'candidates.total_prompt_text'
  CANDIDATES_AGGREGATION_METHOD: str = 'candidates.aggregation.method'
  CANDIDATES_REWARD_DATA_PREDICTIONS: str = (
      'candidates.reward_data.reward_predictions'
  )
  CANDIDATES_REWARD_DATA_WELFARE_OR_RANK: str = (
      'candidates.reward_data.welfare_or_rank')
  CANDIDATES_ALL_REWARD_DATA_PREDICTIONS: str = (
      'candidates.all_reward_predictions'
  )
  CANDIDATES_ALL_REWARD_DATA_WELFARE_OR_RANK: str = (
      'candidates.all_welfare_or_rank')
  CANDIDATES_ALL_TEXTS: str = 'candidates.all_texts'
  CANDIDATES_PARENT_STATEMENT_IDS: str = 'candidates.parent_statement_ids'
  CANDIDATES_PARTICIPANT_ID: str = 'candidates.metadata.participant_id'
  CANDIDATES_GENERATIVE_MODEL_API_VERSION: str = (
      'candidates.metadata.generative_model.api_version'
  )
  CANDIDATES_REWARD_MODEL_API_VERSION: str = (
      'candidates.metadata.reward_model.api_version'
  )
  CANDIDATES_GENERATIVE_MODEL_TEMPLATE_NAME: str = (
      'candidates.metadata.generative_model.template_name'
  )
  CANDIDATES_REWARD_MODEL_TEMPLATE_NAME: str = (
      'candidates.metadata.reward_model.template_name'
  )
  CANDIDATES_RESPONSE_DURATION: str = 'candidates.metadata.response_duration'
  CANDIDATES_CREATED: str = 'candidates.metadata.created'
  CANDIDATES_STATUS: str = 'candidates.metadata.status'
  CANDIDATES_VERSION: str = 'candidates.metadata.version'

  CRITIQUE_ID: str = 'critique.metadata.id'
  CRITIQUE_TEXT: str = 'critique.text'
  CRITIQUE_PROVENANCE: str = 'critique.metadata.provenance'
  CRITIQUE_SENTIMENT: str = 'critique.sentiment'
  CRITIQUE_DISPLAY_LABEL: str = 'critique.display_label'
  CRITIQUE_PARTICIPANT_ID: str = 'critique.metadata.participant_id'
  CRITIQUE_RESPONSE_DURATION: str = 'critique.metadata.response_duration'
  CRITIQUE_CREATED: str = 'critique.metadata.created'
  CRITIQUE_STATUS: str = 'critique.metadata.status'

  TOP_CANDIDATE_ID: str = 'top_candidate.metadata.id'
  TOP_CANDIDATE_TEXT: str = 'top_candidate.text'
  TOP_CANDIDATE_PROVENANCE: str = 'top_candidate.metadata.provenance'
  TOP_CANDIDATE_DISPLAY_LABEL: str = 'top_candidate.display_label'
  TOP_CANDIDATE_PROMPT_TEXT: str = 'top_candidate.prompt_text'
  TOP_CANDIDATE_TOTAL_PROMPT_TEXT: str = 'top_candidate.total_prompt_text'
  TOP_CANDIDATE_AGGREGATION_METHOD: str = 'top_candidate.aggregation.method'
  TOP_CANDIDATE_REWARD_DATA_PREDICTIONS: str = (
      'top_candidate.reward_data.reward_predictions'
  )
  TOP_CANDIDATE_REWARD_DATA_WELFARE_OR_RANK: str = (
      'top_candidate.reward_data.welfare_or_rank')
  TOP_CANDIDATE_ALL_REWARD_DATA_PREDICTIONS: str = (
      'top_candidate.all_reward_predictions'
  )
  TOP_CANDIDATE_ALL_REWARD_DATA_WELFARE_OR_RANK: str = (
      'top_candidate.all_welfare_or_rank')
  TOP_CANDIDATE_ALL_TEXTS: str = 'top_candidate.all_texts'
  TOP_CANDIDATE_PARENT_STATEMENT_IDS: str = 'top_candidate.parent_statement_ids'
  TOP_CANDIDATE_PARTICIPANT_ID: str = 'top_candidate.metadata.participant_id'
  TOP_CANDIDATE_GENERATIVE_MODEL_API_VERSION: str = (
      'top_candidate.metadata.generative_model.api_version'
  )
  TOP_CANDIDATE_REWARD_MODEL_API_VERSION: str = (
      'top_candidate.metadata.reward_model.api_version'
  )
  TOP_CANDIDATE_GENERATIVE_MODEL_TEMPLATE_NAME: str = (
      'top_candidate.metadata.generative_model.template_name'
  )
  TOP_CANDIDATE_REWARD_MODEL_TEMPLATE_NAME: str = (
      'top_candidate.metadata.reward_model.template_name'
  )
  TOP_CANDIDATE_RESPONSE_DURATION: str = (
      'top_candidate.metadata.response_duration'
  )
  TOP_CANDIDATE_CREATED: str = 'top_candidate.metadata.created'
  TOP_CANDIDATE_STATUS: str = 'top_candidate.metadata.status'
  # pylint: enable=invalid-name


@dataclasses.dataclass
class GroupedSerialisedComparisonKeys:
  """Grouped serialised comparison keys.

  Used when working with Pandas.
  """

  # pylint: disable=invalid-name
  COMPARISON_METADATA: List[str] = dataclasses.field(default_factory=list)
  QUESTION: List[str] = dataclasses.field(default_factory=list)
  OWN_OPINION: List[str] = dataclasses.field(default_factory=list)
  OTHER_OPINIONS: List[str] = dataclasses.field(default_factory=list)
  CANDIDATES: List[str] = dataclasses.field(default_factory=list)
  CRITIQUE: List[str] = dataclasses.field(default_factory=list)
  RANKINGS: List[str] = dataclasses.field(default_factory=list)
  RATINGS: List[str] = dataclasses.field(default_factory=list)
  TOP_CANDIDATE: List[str] = dataclasses.field(default_factory=list)
  CANDIDATES_AND_RATINGS: List[str] = dataclasses.field(default_factory=list)
  CANDIDATES_RANKINGS_AND_RATINGS: List[str] = dataclasses.field(
      default_factory=list)

  # Values are assigned post initialization as lists are needed for indexing
  # while mutable objects cannot be assigned as defaults in dataclasses.
  def __post_init__(self):
    self.COMPARISON_METADATA = [
        SerialisedComparisonKeys.COMPARISON_ID,
        SerialisedComparisonKeys.ROUND_ID,
        SerialisedComparisonKeys.LAUNCH_ID,
        SerialisedComparisonKeys.ITERATION_ID,
        SerialisedComparisonKeys.ITERATION_INDEX,
        SerialisedComparisonKeys.COMPARISON_TASK_DURATION,
        SerialisedComparisonKeys.COMPARISON_RESPONSE_DURATION,
        SerialisedComparisonKeys.COMPARISON_PARTICIPANT_ID,
        SerialisedComparisonKeys.COMPARISON_CREATED,
        SerialisedComparisonKeys.COMPARISON_UPDATED,
        SerialisedComparisonKeys.COMPARISON_STATUS,
        SerialisedComparisonKeys.COMPARISON_VERSION,
        SerialisedComparisonKeys.COMPARISON_PROVENANCE,
    ]
    self.QUESTION = [
        SerialisedComparisonKeys.QUESTION_ID,
        SerialisedComparisonKeys.QUESTION_TEXT,
        SerialisedComparisonKeys.SPLIT,
        SerialisedComparisonKeys.QUESTION_PROVENANCE,
        SerialisedComparisonKeys.QUESTION_TOPIC,
        SerialisedComparisonKeys.QUESTION_AFFIRMING_STATEMENT,
        SerialisedComparisonKeys.QUESTION_NEGATING_STATEMENT,
    ]
    self.OWN_OPINION = [
        SerialisedComparisonKeys.OWN_OPINION_ID,
        SerialisedComparisonKeys.OWN_OPINION_TEXT,
        SerialisedComparisonKeys.OWN_OPINION_PROVENANCE,
        SerialisedComparisonKeys.OWN_OPINION_DISPLAY_LABEL,
        SerialisedComparisonKeys.OWN_OPINION_PARTICIPANT_ID,
        SerialisedComparisonKeys.OWN_OPINION_RESPONSE_DURATION,
        SerialisedComparisonKeys.OWN_OPINION_CREATED,
        SerialisedComparisonKeys.OWN_OPINION_UPDATED,
        SerialisedComparisonKeys.OWN_OPINION_STATUS,
    ]
    self.OTHER_OPINIONS = [
        SerialisedComparisonKeys.OTHER_OPINIONS_ID,
        SerialisedComparisonKeys.OTHER_OPINIONS_TEXT,
        SerialisedComparisonKeys.OTHER_OPINIONS_PROVENANCE,
        SerialisedComparisonKeys.OTHER_OPINIONS_DISPLAY_LABEL,
        SerialisedComparisonKeys.OTHER_OPINIONS_PARTICIPANT_ID,
        SerialisedComparisonKeys.OTHER_OPINIONS_RESPONSE_DURATION,
        SerialisedComparisonKeys.OTHER_OPINIONS_CREATED,
        SerialisedComparisonKeys.OTHER_OPINIONS_UPDATED,
        SerialisedComparisonKeys.OTHER_OPINIONS_STATUS,
    ]
    self.CANDIDATES = [
        SerialisedComparisonKeys.CANDIDATES_ID,
        SerialisedComparisonKeys.CANDIDATES_TEXT,
        SerialisedComparisonKeys.CANDIDATES_PROVENANCE,
        SerialisedComparisonKeys.CANDIDATES_DISPLAY_LABEL,
        SerialisedComparisonKeys.CANDIDATES_PROMPT_TEXT,
        SerialisedComparisonKeys.CANDIDATES_TOTAL_PROMPT_TEXT,
        SerialisedComparisonKeys.CANDIDATES_AGGREGATION_METHOD,
        SerialisedComparisonKeys.CANDIDATES_REWARD_DATA_PREDICTIONS,
        SerialisedComparisonKeys.CANDIDATES_REWARD_DATA_WELFARE_OR_RANK,
        SerialisedComparisonKeys.CANDIDATES_ALL_REWARD_DATA_PREDICTIONS,
        SerialisedComparisonKeys.CANDIDATES_ALL_REWARD_DATA_WELFARE_OR_RANK,
        SerialisedComparisonKeys.CANDIDATES_ALL_TEXTS,
        SerialisedComparisonKeys.CANDIDATES_GENERATIVE_MODEL_API_VERSION,
        SerialisedComparisonKeys.CANDIDATES_REWARD_MODEL_API_VERSION,
        SerialisedComparisonKeys.CANDIDATES_PARENT_STATEMENT_IDS,
        SerialisedComparisonKeys.CANDIDATES_PARTICIPANT_ID,
        SerialisedComparisonKeys.CANDIDATES_GENERATIVE_MODEL_TEMPLATE_NAME,
        SerialisedComparisonKeys.CANDIDATES_REWARD_MODEL_TEMPLATE_NAME,
        SerialisedComparisonKeys.CANDIDATES_RESPONSE_DURATION,
        SerialisedComparisonKeys.CANDIDATES_CREATED,
        SerialisedComparisonKeys.CANDIDATES_STATUS,
        SerialisedComparisonKeys.CANDIDATES_VERSION,
    ]
    self.CRITIQUE = [
        SerialisedComparisonKeys.CRITIQUE_ID,
        SerialisedComparisonKeys.CRITIQUE_TEXT,
        SerialisedComparisonKeys.CRITIQUE_PROVENANCE,
        SerialisedComparisonKeys.CRITIQUE_SENTIMENT,
        SerialisedComparisonKeys.CRITIQUE_DISPLAY_LABEL,
        SerialisedComparisonKeys.CRITIQUE_PARTICIPANT_ID,
        SerialisedComparisonKeys.CRITIQUE_RESPONSE_DURATION,
        SerialisedComparisonKeys.CRITIQUE_CREATED,
        SerialisedComparisonKeys.CRITIQUE_STATUS,
    ]
    self.TOP_CANDIDATE = [
        SerialisedComparisonKeys.TOP_CANDIDATE_ID,
        SerialisedComparisonKeys.TOP_CANDIDATE_TEXT,
        SerialisedComparisonKeys.TOP_CANDIDATE_PROVENANCE,
        SerialisedComparisonKeys.TOP_CANDIDATE_DISPLAY_LABEL,
        SerialisedComparisonKeys.TOP_CANDIDATE_PROMPT_TEXT,
        SerialisedComparisonKeys.TOP_CANDIDATE_TOTAL_PROMPT_TEXT,
        SerialisedComparisonKeys.TOP_CANDIDATE_AGGREGATION_METHOD,
        SerialisedComparisonKeys.TOP_CANDIDATE_REWARD_DATA_PREDICTIONS,
        SerialisedComparisonKeys.TOP_CANDIDATE_REWARD_DATA_WELFARE_OR_RANK,
        SerialisedComparisonKeys.TOP_CANDIDATE_ALL_REWARD_DATA_PREDICTIONS,
        SerialisedComparisonKeys.TOP_CANDIDATE_ALL_REWARD_DATA_WELFARE_OR_RANK,
        SerialisedComparisonKeys.TOP_CANDIDATE_ALL_TEXTS,
        SerialisedComparisonKeys.TOP_CANDIDATE_PARENT_STATEMENT_IDS,
        SerialisedComparisonKeys.TOP_CANDIDATE_PARTICIPANT_ID,
        SerialisedComparisonKeys.TOP_CANDIDATE_GENERATIVE_MODEL_API_VERSION,
        SerialisedComparisonKeys.TOP_CANDIDATE_GENERATIVE_MODEL_TEMPLATE_NAME,
        SerialisedComparisonKeys.TOP_CANDIDATE_REWARD_MODEL_API_VERSION,
        SerialisedComparisonKeys.TOP_CANDIDATE_REWARD_MODEL_TEMPLATE_NAME,
        SerialisedComparisonKeys.TOP_CANDIDATE_RESPONSE_DURATION,
        SerialisedComparisonKeys.TOP_CANDIDATE_CREATED,
        SerialisedComparisonKeys.TOP_CANDIDATE_STATUS,
    ]
    self.RATINGS = [
        SerialisedComparisonKeys.RATINGS_ID,
        SerialisedComparisonKeys.RATINGS_AGREEMENT,
        SerialisedComparisonKeys.RATINGS_QUALITY,
        SerialisedComparisonKeys.RATINGS_PROVENANCE,
        SerialisedComparisonKeys.RATINGS_PARTICIPANT_ID,
        SerialisedComparisonKeys.RATINGS_RESPONSE_DURATION,
        SerialisedComparisonKeys.RATINGS_CREATED,
        SerialisedComparisonKeys.RATINGS_STATUS,
    ]
    self.RANKINGS = [
        SerialisedComparisonKeys.RANKINGS_ID,
        SerialisedComparisonKeys.RANKINGS_CANDIDATE_IDS,
        SerialisedComparisonKeys.RANKINGS_NUMERICAL_RANKS,
        SerialisedComparisonKeys.RANKINGS_EXPLANATION,
        SerialisedComparisonKeys.RANKINGS_PROVENANCE,
        SerialisedComparisonKeys.RANKINGS_PARTICIPANT_ID,
        SerialisedComparisonKeys.RANKINGS_RESPONSE_DURATION,
        SerialisedComparisonKeys.RANKINGS_CREATED,
        SerialisedComparisonKeys.RANKINGS_STATUS,
    ]
    self.CANDIDATES_AND_RATINGS = [*self.CANDIDATES, *self.RATINGS]
    self.CANDIDATES_RANKINGS_AND_RATINGS = [
        *self.CANDIDATES, *self.RANKINGS, *self.RATINGS]
  # pylint: enable=invalid-name


@dataclasses.dataclass(frozen=True)
class SerialisedQuestionImportanceKeys:
  """Serialised question importance data keys; used e.g. for data analysis."""

  # pylint: disable=invalid-name
  LAUNCH_ID: str = 'launch_id'
  QUESTION_INDEX: str = 'question_index'
  RATING_INDEX: str = 'rating_index'
  METADATA_ID: str = 'metadata.id'
  METADATA_TASK_DURATION: str = 'metadata.task_duration'
  METADATA_RESPONSE_DURATION: str = 'metadata.response_duration'
  METADATA_CREATED: str = 'metadata.created'
  METADATA_STATUS: str = 'metadata.status'
  METADATA_PARTICIPANT_ID: str = 'metadata.participant_id'
  METADATA_GENERATIVE_MODEL_API_VERSION: str = (
      'metadata.generative_model.api_version'
  )
  METADATA_GENERATIVE_MODEL_TEMPLATE_NAME: str = (
      'metadata.generative_model.template_name'
  )
  METADATA_REWARD_MODEL_API_VERSION: str = 'metadata.reward_model.api_version'
  METADATA_REWARD_MODEL_TEMPLATE_NAME: str = (
      'metadata.reward_model.template_name'
  )
  METADATA_VERSION: str = 'metadata.version'
  METADATA_PROVENANCE: str = 'metadata.provenance'

  RATING_IMPORTANCE: str = 'importance_rating'

  QUESTION_ID: str = 'question.id'
  QUESTION_TEXT: str = 'question.text'
  SPLIT: str = 'question.split'
  QUESTION_PROVENANCE: str = 'question.provenance'
  QUESTION_TOPIC: str = 'question.topic'
  QUESTION_AFFIRMING_STATEMENT: str = 'question.affirming_statement'
  QUESTION_NEGATING_STATEMENT: str = 'question.negating_statement'
  # pylint: enable=invalid-name
