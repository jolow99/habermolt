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

"""Library for loading human data batches.

  Typical usage example for creating a dataset with pairwise rating comparisons:

  live_loading.check_consistent_tuple_lengths_in_grouped_columns(df)
  df = live_loading.unnest_nested_columns(df)
  df = live_loading.filter_on_response_provenances(
      df,
      provenance_column=DFKeys.OWN_OPINION_PROVENANCE,
      valid_provenances=(hm_types.ResponseProvenance.HUMAN_CITIZEN,),
  )
  df = live_loading.filter_on_response_provenances(
      df,
      provenance_column=DFKeys.CANDIDATES_PROVENANCE,
      valid_provenances=(hm_types.ResponseProvenance.MODEL_MEDIATOR,),
  )
  df = live_loading.filter_out_mock_ratings(
      df, rating_type=live_loading.RatingTypes.AGREEMENT)
  df = live_loading.add_numerical_ratings(df)
  df = live_loading.filter_groups_with_repeat_participants(df)
  df = live_loading.nest_columns_as_tuples(df)
"""

import dataclasses
import enum
from typing import Any, Callable, List, Sequence, Union

from absl import logging
import pandas as pd

from habermas_machine.analysis import serialise
from habermas_machine.analysis import types as hm_types

DFKeys = serialise.SerialisedComparisonKeys
DFGroupedKeys = serialise.GroupedSerialisedComparisonKeys()
SELECTED_CANDIDATE = 'selected_candidate'
NUMERICAL_RATINGS_AGREEMENT = 'numerical_ratings.agreement'
NUMERICAL_RATINGS_QUALITY = 'numerical_ratings.quality'
NUMERICAL_RATINGS_IMPORTANCE = 'numerical_ratings.importance'
NUMERICAL_RATINGS_AVERAGE_AGREEMENT = 'numerical_ratings.average.agreement'
NUMERICAL_RATINGS_AVERAGE_QUALITY = 'numerical_ratings.average.quality'
NUMERICAL_RATINGS_AVERAGE_IMPORTANCE = 'numerical_ratings.average.importance'
BINARIZED_RATINGS_AGREEMENT = 'binarized_ratings.agreement'
BINARIZED_RATINGS_QUALITY = 'binarized_ratings.quality'
BINARIZED_RATINGS_IMPORTANCE = 'binarized_ratings.importance'
NEW_PROMPT_TEXT = 'new_prompt_text'
ONE_MILLION = 1_000_000
MONOTONIC_TIMESTAMP = 'monotonic_timestamp'
NROWS = 'n_rows'

CANDIDATE_COLS_INC_NUMERICAL = DFGroupedKeys.CANDIDATES + [
    NUMERICAL_RATINGS_AGREEMENT, NUMERICAL_RATINGS_QUALITY] + [
        NUMERICAL_RATINGS_AVERAGE_AGREEMENT,
        NUMERICAL_RATINGS_AVERAGE_QUALITY,
    ] + [DFKeys.RANKINGS_NUMERICAL_RANKS, DFKeys.RANKINGS_CANDIDATE_IDS] + [
        DFKeys.RATINGS_AGREEMENT, DFKeys.RATINGS_QUALITY]


class GroupMinSizeParameters(enum.Enum):
  """Pre-registered minimum group sizes and number of groups."""
  ITERATION_EVAL_ABLATION_IID_V1 = {
      'min_num_citizens': 4,
      'min_num_iterations': 2,
      'min_num_rounds': 3,
      'num_groups': 100
  }
  ITERATION_EVAL_ABLATION_IID_V2 = {
      'min_num_citizens': 4,
      'min_num_iterations': 2,
      'min_num_rounds': 3,
      'num_groups': 150
  }
  ITERATION_EVAL_CRITIQUE_EXCLUSION = {
      'min_num_citizens': 4,
      'min_num_iterations': 2,
      'min_num_rounds': 3,
      'num_groups': 50
  }
  ITERATION_EVAL_ABLATION_OOD_V1 = {
      'min_num_citizens': 4,
      'min_num_iterations': 2,
      'min_num_rounds': 3,
      'num_groups': 100
  }
  ITERATION_EVAL_HUMAN_MEDIATOR = {
      'min_num_citizens': 4,
      'min_num_iterations': 1,
      'min_num_rounds': 2,
      'num_groups': 75
  }
  ITERATION_EVAL_OPINION_EXPOSURE = {
      'min_num_citizens': 4,
      'min_num_iterations': 1,
      'min_num_rounds': 2,
      'num_groups': 75
  }


@enum.unique
class RatingTypesNames(enum.Enum):
  """Names of the rating types. Used for Launchpad serialization."""
  AGREEMENT = 'agreement'
  QUALITY = 'quality'
  IMPORTANCE = 'importance'


@dataclasses.dataclass
class RatingType:
  """Properties for a specific rating type."""
  value_name: str
  mock: Union[
      hm_types.LikertQuality,
      hm_types.LikertAgreement,
      hm_types.LikertImportance,
  ]
  name_to_value: Callable[[str], int]
  name_column: str
  numerical_column: str
  numerical_average_column: str
  binarized_column: str


@enum.unique
class RatingTypes(enum.Enum):
  """Possible rating types."""
  AGREEMENT = RatingType(
      value_name=RatingTypesNames.AGREEMENT.value,
      mock=hm_types.LikertAgreement.MOCK,
      name_to_value=hm_types.LikertAgreement.name_to_value,
      name_column=DFKeys.RATINGS_AGREEMENT,
      numerical_column=NUMERICAL_RATINGS_AGREEMENT,
      numerical_average_column=NUMERICAL_RATINGS_AVERAGE_AGREEMENT,
      binarized_column=BINARIZED_RATINGS_AGREEMENT,
  )
  QUALITY = RatingType(
      value_name=RatingTypesNames.QUALITY.value,
      mock=hm_types.LikertQuality.MOCK,
      name_to_value=hm_types.LikertQuality.name_to_value,
      name_column=DFKeys.RATINGS_QUALITY,
      numerical_column=NUMERICAL_RATINGS_QUALITY,
      numerical_average_column=NUMERICAL_RATINGS_AVERAGE_QUALITY,
      binarized_column=BINARIZED_RATINGS_QUALITY,
  )
  IMPORTANCE = RatingType(
      value_name=RatingTypesNames.IMPORTANCE.value,
      mock=hm_types.LikertImportance.MOCK,
      name_to_value=hm_types.LikertImportance.name_to_value,
      name_column=serialise.SerialisedQuestionImportanceKeys.RATING_IMPORTANCE,
      numerical_column=NUMERICAL_RATINGS_IMPORTANCE,
      numerical_average_column=NUMERICAL_RATINGS_AVERAGE_IMPORTANCE,
      binarized_column=BINARIZED_RATINGS_IMPORTANCE,
  )

  @classmethod
  def select_rating_type_by_value_name(
      cls, name: RatingTypesNames) -> 'RatingTypes':
    items = [c for c in cls if c.value_name == name.value]
    if len(items) != 1:
      raise ValueError(
          f'Name {name.value} is an invalid name for selecting a rating type.')
    else:
      return items[0]

  @property
  def value_name(self) -> str:
    """Returns the value name of the rating type."""
    return self.value.value_name

  @property
  def mock(self) -> Union[
      hm_types.LikertQuality,
      hm_types.LikertAgreement,
      hm_types.LikertImportance,
  ]:
    """Returns the mock Likert of the rating type."""
    return self.value.mock

  def name_to_value(self, name: str) -> int:
    """Returns the value of the corresponding likert."""
    return self.value.name_to_value(name)

  @property
  def name_column(self) -> str:
    """Returns the name column of the rating type."""
    return self.value.name_column

  @property
  def numerical_column(self) -> str:
    """Returns the numerical column of the rating type."""
    return self.value.numerical_column

  @property
  def numerical_average_column(self) -> str:
    """Returns the numerical average column of the rating type."""
    return self.value.numerical_average_column

  @property
  def binarized_column(self) -> str:
    """Returns the binarized column of the rating type."""
    return self.value.binarized_column


def _map_if_series(f: Callable[..., Any]) -> Callable[..., Any]:
  """Decorator which makes f map itself to a pd.Series object if needed."""
  def g(x, *args, **kwargs):
    if isinstance(x, pd.Series):
      return x.apply(f, *args, **kwargs)
    else:
      return f(x, *args, **kwargs)
  return g


def _map_if_tuple(f: Callable[..., Any]) -> Callable[..., Any]:
  """Decorator which makes f map itself to a tuple if needed."""
  def g(x, *args, **kwargs):
    if isinstance(x, tuple):
      return tuple([f(y, *args, **kwargs) for y in x])
    else:
      return f(x, *args, **kwargs)
  return g


def check_if_columns_are_nested(
    df: pd.DataFrame,
    columns: Sequence[str] = (DFKeys.CANDIDATES_ID,),
) -> bool:
  """Check if the values in the columns are nested (lists, tuples, or sets).

  Args:
    df: Dataframe that holds the columns that need to be checked.
    columns: Names of the columns to check.

  Returns:
   A boolean indicating if there are nested values in the specified columns.
  """
  overlapping_columns = list(set(df.columns) & set(columns))
  check_value_unnested = lambda x: isinstance(x, (list, tuple, set))
  return df[overlapping_columns].applymap(check_value_unnested).any(axis=None)


def check_consistent_tuple_lengths_in_grouped_columns(
    df: pd.DataFrame,
    groups_columns: Sequence[List[str]] = (
        DFGroupedKeys.OTHER_OPINIONS, DFGroupedKeys.CANDIDATES),
) -> None:
  """Checks if all tuple lengths within groups are consistent across rows.

  Args:
    df: Dataframe that holds the columns that are checked.
    groups_columns: The groups of columns that are checked. Within each group
      of columns, the tuple lengths should be consistent.
  """
  df = df.copy()  # Copy dataframe to ensure the main frame does not change.
  for group_columns in groups_columns:
    overlapping_group_columns = list(set(df.columns) & set(group_columns))
    length_df = df[overlapping_group_columns].apply(_map_if_series(len), axis=1)
    if not (length_df.nunique(axis=1) == 1).all():
      raise ValueError(
          'All sequences with a group of columns should have the same length. '
          f'The group that is causing the error is {group_columns}.')


def unnest_nested_columns(
    df: pd.DataFrame,
    nested_columns: Sequence[str] = (
        DFGroupedKeys.CANDIDATES_RANKINGS_AND_RATINGS),
)-> pd.DataFrame:
  """Unnests (aka explodes) the columns that contain nested sequences.

  This method inverts the `nest_columns_as_tuples` method.

  Args:
    df: Dataframe that contains the nested sequences.
    nested_columns: Columns that currently contain the nested values.

  Returns:
    A dataframe that is unnested. It has a single row per value in the
      sequence in the nested columns.
  """
  df = df.reset_index(drop=True)  # Ensure no index collisions for `pd.join`.
  fixed_columns = [
      column for column in df.columns if column not in nested_columns]  # pytype: disable=attribute-error  # typed-pandas
  nested_columns = [
      column for column in df.columns if column in nested_columns]  # pytype: disable=attribute-error  # typed-pandas
  # Explode only the nested columns and rejoin dataframes on index.
  df = df[fixed_columns].join(df[nested_columns].apply(pd.Series.explode))
  return df.reset_index(drop=True)


def nest_columns_as_tuples(
    df: pd.DataFrame,
    nesting_columns: Sequence[str] = CANDIDATE_COLS_INC_NUMERICAL,
    column_for_grouping: str = DFKeys.COMPARISON_ID,
)-> pd.DataFrame:
  """Nests values in specific columns as tuples.

  This method inverts the `unnest_nested_columns` method.

  Args:
    df: Dataframe that contains the nested sequences.
    nesting_columns: Columns that should contain the nested sequences.
    column_for_grouping: Column name of the column that is used to identify
      rows that should be nested together.

  Returns:
    A dataframe that is nested. It has a single row per unique value in the
      column for grouping.
  """
  fixed_columns = [
      column for column in df.columns if column not in nesting_columns]
  nesting_columns_in_df = [
      column for column in df.columns if column in nesting_columns]
  aggregations = {
      column: tuple for column in nesting_columns_in_df}
  nested_df = df.groupby(column_for_grouping).agg(aggregations).reset_index()
  fixed_columns_df = df[fixed_columns].drop_duplicates([column_for_grouping])
  merged_df = pd.merge(
      fixed_columns_df, nested_df, how='inner', on=column_for_grouping)
  return merged_df


def filter_on_response_provenances(
    df: pd.DataFrame,
    valid_provenances: Sequence[hm_types.ResponseProvenance] = (
        hm_types.ResponseProvenance.MODEL_MEDIATOR,),
    provenance_column: str = DFKeys.CANDIDATES_PROVENANCE,
)-> pd.DataFrame:
  """Filters the dataframe for candidate statements with specific provenances.

  Args:
    df: Dataframe that should be filtered.
    valid_provenances: The candidate provenances that are valid.
    provenance_column: Provenance column used for filtering.

  Returns:
    The filtered dataframe.
  """
  if check_if_columns_are_nested(df, columns=(provenance_column,)):
    raise ValueError('The input dataframe should be first unnested.')

  valid_provenance_names = [provenance.name for provenance in valid_provenances]
  mask = df[provenance_column].isin(valid_provenance_names)
  df = df[mask]
  logging.info(
      '[filter_on_response_provenances] Provenance column=%s. Kept %d/%d rows.',
      provenance_column, len(df), len(mask))
  return df


def filter_out_mock_ratings(
    df: pd.DataFrame,
    *,
    rating_type: RatingTypes = RatingTypes.AGREEMENT,
    ) -> pd.DataFrame:
  """Removes rows that use mock ratings, as they come from worker bots.

  Args:
    df: dataframe to filter. The dataframe could be nested or unnested.
    rating_type: the type of rating to apply the filter to. Must be either
      RatingTypes.AGREEMENT, RatingTypes.QUALITY, or RatingTypes.IMPORTANCE.

  Returns:
    A new filtered dataframe.
  """

  if check_if_columns_are_nested(df):
    def find_mock_likert(df_rating) -> bool:
      return rating_type.mock.name not in df_rating
    mask = df[rating_type.name_column].apply(find_mock_likert)
  else:
    mask = df[rating_type.name_column] != rating_type.mock.name
  df = df[mask]
  logging.info(
      '[filter_out_mock_ratings] Kept %d/%d rows.', len(df), len(mask))
  return df


def filter_out_mock_rankings(
    df: pd.DataFrame,
    *,
    ranking_col: str = DFKeys.RANKINGS_NUMERICAL_RANKS,
    ) -> pd.DataFrame:
  """Removes rows that use mock rankings, as they come from worker bots.

  Args:
    df: dataframe to filter. The dataframe could be nested or unnested.
    ranking_col: the column name in which we can find the rankings.

  Returns:
    A new filtered dataframe.
  """

  if check_if_columns_are_nested(df):
    mask = df[ranking_col].apply(lambda x: hm_types.RANKING_MOCK not in x)
  else:
    mask = df[ranking_col] != hm_types.RANKING_MOCK
  df = df[mask]
  logging.info(
      '[filter_out_mock_rankings] Kept %d/%d rows.', len(df), len(mask))
  return df


def add_numerical_ratings(
    df: pd.DataFrame,
    rating_types: Sequence[RatingTypes] = (
        RatingTypes.AGREEMENT, RatingTypes.QUALITY),
)-> pd.DataFrame:
  """Add numerical ratings to dataframe.

  Args:
    df: Dataframe to add numerical ratings to. The dataframe can contain
      ratings that are nested (tuples or lists) or flattened ratings.
    rating_types: The types of ratings to apply the conversion to.  Must contain
      RatingTypes.AGREEMENT, RatingTypes.QUALITY, and/or RatingTypes.IMPORTANCE.

  Returns:
    The dataframe with numerical ratings.
  """
  for rating_type in rating_types:
    df[rating_type.numerical_column] = df[rating_type.name_column].apply(
        _map_if_tuple(rating_type.name_to_value))
  return df


def filter_groups_with_repeat_participants(
    df: pd.DataFrame,
    id_column: str = 'worker_id',
) -> pd.DataFrame:
  """Removes groups with participants who did the task multiple times.

  Participant IDs are based on self-reported IDs entered at the
  start of the task, which are then anonymized. For participants who got passed
  the start page more than once, we look to see which workerid they were
  assigned is associated with more data. That is, if participants tried to
  connect once, but failed, and tried again, then did the task, this would keep
  their second instance's worth of data. If a paricipant did the entire
  experiment, and returned to the start page, and re-entered their worker id
  accidentally, this would keep their first instance's worth of data.

  Note DFKeys.COMPARISON_PARTICIPANT_ID is assigned to a participant each time
  they do the task, so it denotes an instance of doing the task for one
  participant, whereas id_column column denotes the participant id that is
  constant across instances.

  Args:
    df: Dataframe containing main data.
    id_column: Column name containing participant self-reported platform IDs,
      anonymized.

  Returns:
    Dataframe without groups who have repeat participants.
  """
  # Find IDs where participants began the task multiple times.
  df_ids_counts = (
      df[id_column]
      .value_counts()
      .reset_index()
      .set_axis([id_column, 'count'], axis=1)
  )
  repeat_ids = df_ids_counts[df_ids_counts['count'] > 1]
  logging.info(
      '[filter_groups_with_repeat_participants] %d repeat ids found',
      len(repeat_ids))
  repeat_workerids = df[
      df[id_column].isin(repeat_ids[id_column])
  ]

  # For each repeat worker id, determine the time they provided the most data.
  data_counts = []
  for worker_id in repeat_workerids[id_column].drop_duplicates():
    worker_instance_ids = repeat_workerids[
        repeat_workerids[id_column] == worker_id
    ][DFKeys.COMPARISON_PARTICIPANT_ID].drop_duplicates()
    for worker_instance_id in worker_instance_ids:
      df_worker_instance = df[
          df[DFKeys.COMPARISON_PARTICIPANT_ID] == worker_instance_id]
      n_rows = len(df_worker_instance)  # Number of rows of data contributed.
      if n_rows > 0:  # Participant submitted some amount of data.
        # Timestamp to determine when this data was contributed.
        monotonic_timestamp = min(df_worker_instance[MONOTONIC_TIMESTAMP])
      else:  # Participant submitted no data.
        monotonic_timestamp = 0
      data_counts.append({
          id_column: worker_id,
          DFKeys.COMPARISON_PARTICIPANT_ID: worker_instance_id,
          MONOTONIC_TIMESTAMP: monotonic_timestamp,
          NROWS: n_rows
      })
  df_data_counts = pd.DataFrame(data_counts)

  # Remove empty data.
  df_data_counts = df_data_counts[df_data_counts[NROWS] > 0]

  # Sort by NROWS in descending order and timestamp as ascending order.
  df_data_counts = df_data_counts.sort_values(
      by=[id_column, NROWS, MONOTONIC_TIMESTAMP],
      ascending=[False, False, True])

  # Group by id_column and take first row of each group.
  worker_instance_ids_to_keep = df_data_counts.groupby(
      id_column, as_index=False).first()
  worker_instance_ids_to_remove = repeat_workerids[
      ~repeat_workerids[DFKeys.COMPARISON_PARTICIPANT_ID].isin(
          worker_instance_ids_to_keep[DFKeys.COMPARISON_PARTICIPANT_ID])
  ][DFKeys.COMPARISON_PARTICIPANT_ID]

  # Remove groups with repeat participants.
  groups_with_repeating_participants = df[
      df[DFKeys.COMPARISON_PARTICIPANT_ID].isin(worker_instance_ids_to_remove)
  ][DFKeys.LAUNCH_ID].drop_duplicates()
  df = df[~df[DFKeys.LAUNCH_ID].isin(groups_with_repeating_participants)]

  logging.info(
      '[filter_groups_with_repeat_participants] '
      'Removed %d groups with repeat participants. Rows remaining = %d',
      len(groups_with_repeating_participants),
      len(df))
  return df


def filter_by_number_of_groups_of_min_size(
    df: pd.DataFrame,
    *,
    min_num_citizens: int = 4,
    min_num_iterations: int = 2,
    min_num_rounds: int = 3,
    num_groups: int = 100,
) -> pd.DataFrame:
  """Filter by pre-registered number of groups with sufficient data."""
  logging.info(
      '[filter_by_number_of_groups_of_min_size] Filtering by group size '
      'parameters: (citizens >= %d) & (iterations >= %d) & (rounds >= %d)',
      min_num_citizens, min_num_iterations, min_num_rounds)
  # Count number of rows for each group in each iteration of each round.
  group_round_iteration_row_counts = (
      df[[DFKeys.LAUNCH_ID, DFKeys.ROUND_ID, DFKeys.ITERATION_INDEX]]
      .value_counts()
      .rename('count')
      .reset_index()
  )

  # Count iterations with sufficient number of citizens for each group & round.
  group_round_iteration_counts = (
      group_round_iteration_row_counts[
          group_round_iteration_row_counts['count'] >= min_num_citizens
      ][[DFKeys.LAUNCH_ID, DFKeys.ROUND_ID]]
      .value_counts()
      .rename('count')
      .reset_index()
  )

  # Count rounds with sufficient number of iterations for each group.
  group_round_counts = (
      group_round_iteration_counts[
          group_round_iteration_counts['count'] >= min_num_iterations
      ][DFKeys.LAUNCH_ID]
      .value_counts()
      .reset_index()
      .set_axis([DFKeys.LAUNCH_ID, 'count'], axis=1)
  )

  # Filter groups for those with sufficient number of rounds.
  groups_with_min_complete_rounds = group_round_counts[
      group_round_counts['count'] >= min_num_rounds
  ][DFKeys.LAUNCH_ID]

  logging.info(
      '[filter_by_number_of_groups_of_min_size] Found %d groups with '
      'specified criteria. Keeping %d.',
      len(groups_with_min_complete_rounds), num_groups)
  # Keep only max number of groups that we pre-registered.
  groups_with_min_complete_rounds = groups_with_min_complete_rounds.head(
      num_groups)

  # Filter data set to contain just those groups.
  df = df[df[DFKeys.LAUNCH_ID].isin(groups_with_min_complete_rounds)]
  logging.info(
      '[filter_by_number_of_groups_of_min_size] Filtered by stipulated group '
      'size. Each group has %d rounds of %d iterations with data from %d '
      'citizens. Rows remaining = %d',
      min_num_rounds, min_num_iterations, min_num_citizens, len(df))

  return df
