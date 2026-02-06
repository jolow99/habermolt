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
import pandas as pd

from habermas_machine.analysis import live_loading
from habermas_machine.analysis import mocks
from habermas_machine.analysis import serialise
from habermas_machine.analysis import types as hm_types

DFKeys = serialise.SerialisedComparisonKeys
DFGroupedKeys = serialise.GroupedSerialisedComparisonKeys()


class LiveLoadingTest(parameterized.TestCase):

  @parameterized.parameters([
      dict(
          rating_type_name=live_loading.RatingTypesNames.AGREEMENT,
          rating_type_direct=live_loading.RatingTypes.AGREEMENT,
          value_name='agreement',
          test_likert=hm_types.LikertAgreement.AGREE,
          name_column=DFKeys.RATINGS_AGREEMENT,
          numerical_column=live_loading.NUMERICAL_RATINGS_AGREEMENT,
          numerical_average_column=(
              live_loading.NUMERICAL_RATINGS_AVERAGE_AGREEMENT
          ),
      ),
      dict(
          rating_type_name=live_loading.RatingTypesNames.QUALITY,
          rating_type_direct=live_loading.RatingTypes.QUALITY,
          value_name='quality',
          test_likert=hm_types.LikertQuality.POOR_QUALITY,
          name_column=DFKeys.RATINGS_QUALITY,
          numerical_column=live_loading.NUMERICAL_RATINGS_QUALITY,
          numerical_average_column=(
              live_loading.NUMERICAL_RATINGS_AVERAGE_QUALITY
          ),
      ),
      dict(
          rating_type_name=live_loading.RatingTypesNames.IMPORTANCE,
          rating_type_direct=live_loading.RatingTypes.IMPORTANCE,
          value_name='importance',
          test_likert=hm_types.LikertImportance.NOT_IMPORTANT,
          name_column=(
              serialise.SerialisedQuestionImportanceKeys.RATING_IMPORTANCE
          ),
          numerical_column=live_loading.NUMERICAL_RATINGS_IMPORTANCE,
          numerical_average_column=(
              live_loading.NUMERICAL_RATINGS_AVERAGE_IMPORTANCE
          ),
      ),
  ])
  def test_rating_types(
      self,
      rating_type_name,
      rating_type_direct,
      test_likert,
      value_name,
      name_column,
      numerical_column,
      numerical_average_column,
  ):
    """Tests rating_types enum."""
    rating_type_from_name = (
        live_loading.RatingTypes.select_rating_type_by_value_name(
            rating_type_name
        )
    )
    for rating_type in [rating_type_from_name, rating_type_direct]:
      self.assertEqual(rating_type.value_name, value_name)
      self.assertEqual(rating_type.name_column, name_column)
      self.assertEqual(rating_type.numerical_column, numerical_column)
      self.assertEqual(
          rating_type.numerical_average_column, numerical_average_column
      )
      self.assertEqual(
          rating_type.name_to_value(test_likert.name), test_likert.value
      )

  def test_unnest_nested_columns(self):
    """Tests unnest_nested_columns method."""
    # Add None dummy to test if exploding the dataframe preserves the `None`.
    nested_df = mocks.NESTED_DUMMY_DF.copy()
    nested_df = nested_df.replace({DFKeys.COMPARISON_ID: 'N1'}, None)
    unnested_df = mocks.UNNESTED_DUMMY_DF.copy()
    unnested_df = unnested_df.replace({DFKeys.COMPARISON_ID: 'N1'}, None)
    df = live_loading.unnest_nested_columns(
        df=nested_df,
        nested_columns=[
            DFKeys.RATINGS_AGREEMENT,
            DFKeys.RATINGS_QUALITY,
            DFKeys.RANKINGS_NUMERICAL_RANKS,
            DFKeys.CANDIDATES_ID,
        ],
    )
    pd.testing.assert_frame_equal(df, unnested_df, check_dtype=False)

  def test_nest_columns_as_tuples(self):
    """Tests nest_columns_as_tuples method."""
    df = live_loading.nest_columns_as_tuples(
        df=mocks.UNNESTED_DUMMY_DF.copy(),
        nesting_columns=[
            DFKeys.RATINGS_AGREEMENT,
            DFKeys.RATINGS_QUALITY,
            DFKeys.CANDIDATES_ID,
            DFKeys.RANKINGS_NUMERICAL_RANKS,
        ],
        column_for_grouping=DFKeys.COMPARISON_ID,
    )
    pd.testing.assert_frame_equal(df, mocks.NESTED_DUMMY_DF)

  @parameterized.parameters(
      (mocks.UNNESTED_DUMMY_DF, False), (mocks.NESTED_DUMMY_DF, True)
  )
  def test_check_if_columns_are_nested(self, frame, is_nested):
    """Tests check_if_columns_are_nested method."""
    self.assertEqual(live_loading.check_if_columns_are_nested(frame), is_nested)

  def test_check_consistent_tuple_lengths_in_grouped_columns(self):
    """Tests check_consistent_tuple_lengths_in_grouped_columns method."""
    live_loading.check_consistent_tuple_lengths_in_grouped_columns(
        pd.DataFrame({'a': [(1,), (1, 2)], 'b': [(3,), (4, 5)]}), [['a', 'b']]
    )
    with self.assertRaises(ValueError):
      live_loading.check_consistent_tuple_lengths_in_grouped_columns(
          pd.DataFrame({'a': [(1,), (1, 2, 3)], 'b': [(3,), (4, 5)]}),
          [['a', 'b']],
      )

  @parameterized.parameters([
      dict(
          valid_provenances=(hm_types.ResponseProvenance.MODEL_MEDIATOR,),
          valid_statements=['f'],
          provenance_column=DFKeys.CANDIDATES_PROVENANCE,
      ),
      dict(
          valid_provenances=(
              hm_types.ResponseProvenance.MOCK,
              hm_types.ResponseProvenance.MODEL_MEDIATOR,
          ),
          valid_statements=['a', 'f'],
          provenance_column=DFKeys.CANDIDATES_PROVENANCE,
      ),
      dict(
          valid_provenances=(hm_types.ResponseProvenance.MODEL_MEDIATOR,),
          valid_statements=['g'],
          provenance_column=DFKeys.OWN_OPINION_PROVENANCE,
      ),
      dict(
          valid_provenances=(
              hm_types.ResponseProvenance.MOCK,
              hm_types.ResponseProvenance.MODEL_MEDIATOR,
          ),
          valid_statements=['b', 'g'],
          provenance_column=DFKeys.OWN_OPINION_PROVENANCE,
      ),
  ])
  def test_filter_on_response_provenances(
      self,
      valid_provenances,
      valid_statements,
      provenance_column,
  ):
    """Tests filter_on_response_provenances method."""
    df = live_loading.filter_on_response_provenances(
        df=mocks.DF_FOR_CANDIDATE_PROVENANCE.copy(),
        valid_provenances=valid_provenances,
        provenance_column=provenance_column,
    )
    target_frame = mocks.DF_FOR_CANDIDATE_PROVENANCE[
        mocks.DF_FOR_CANDIDATE_PROVENANCE[DFKeys.CANDIDATES_ID].isin(
            valid_statements
        )
    ]
    pd.testing.assert_frame_equal(df, target_frame)

  @parameterized.parameters(
      (mocks.DUMMY_DF.copy(), ['N1', 'N1', 'N2', 'N3']),
      (
          live_loading.unnest_nested_columns(
              mocks.DUMMY_DF.copy(),
              [DFKeys.RATINGS_AGREEMENT, DFKeys.CANDIDATES_ID],
          ),
          ['N1', 'N1', 'N1', 'N1', 'N1', 'N2', 'N2', 'N2', 'N3', 'N3'],
      ),
  )
  def test_filter_out_mock_ratings(self, dataframe, target_comparison_ids):
    """Tests filter_out_mock_ratings method."""
    df = live_loading.filter_out_mock_ratings(dataframe)
    np.testing.assert_array_equal(
        df[DFKeys.COMPARISON_ID], target_comparison_ids
    )

  @parameterized.parameters(
      (mocks.DUMMY_DF.copy(), ['N1', 'N1', 'N2', 'N3']),
      (
          live_loading.unnest_nested_columns(
              mocks.DUMMY_DF.copy(),
              [
                  DFKeys.RATINGS_AGREEMENT,
                  DFKeys.CANDIDATES_ID,
                  DFKeys.RANKINGS_NUMERICAL_RANKS,
              ],
          ),
          ['N1', 'N1', 'N1', 'N1', 'N1', 'N2', 'N2', 'N3', 'N3'],
      ),
  )
  def test_filter_out_mock_rankings(self, dataframe, target_comparison_ids):
    """Tests filter_out_mock_rankings method."""
    df = live_loading.filter_out_mock_rankings(dataframe)
    np.testing.assert_array_equal(
        df[DFKeys.COMPARISON_ID], target_comparison_ids
    )

  @parameterized.parameters(
      (
          [live_loading.RatingTypes.QUALITY],
          [live_loading.NUMERICAL_RATINGS_QUALITY],
      ),
      (
          [live_loading.RatingTypes.AGREEMENT],
          [live_loading.NUMERICAL_RATINGS_AGREEMENT],
      ),
      (
          [
              live_loading.RatingTypes.QUALITY,
              live_loading.RatingTypes.AGREEMENT,
          ],
          [
              live_loading.NUMERICAL_RATINGS_QUALITY,
              live_loading.NUMERICAL_RATINGS_AGREEMENT,
          ],
      ),
  )
  def test_add_numerical_ratings(self, rating_types, numerical_columns):
    """Tests add_numerical_ratings method."""
    df = live_loading.add_numerical_ratings(
        mocks.UNNESTED_DUMMY_DF.copy(), rating_types=rating_types
    )

    # Assert correct columns.
    self.assertSameElements(
        set(df) - set(mocks.UNNESTED_DUMMY_DF.columns), numerical_columns
    )

    # Check if the numerical ratings have the correct values.
    pd.testing.assert_frame_equal(
        df[numerical_columns],
        mocks.UNNESTED_NUMERICAL_RATINGS[numerical_columns],
    )

    # Check correct behavior when ratings are nested in tuples.
    df = live_loading.add_numerical_ratings(
        mocks.NESTED_DUMMY_DF.copy(), rating_types=rating_types
    )
    nested_numerical_ratings = live_loading.nest_columns_as_tuples(
        df=mocks.UNNESTED_NUMERICAL_RATINGS.copy(),
        nesting_columns=[
            live_loading.NUMERICAL_RATINGS_QUALITY,
            live_loading.NUMERICAL_RATINGS_AGREEMENT,
        ],
        column_for_grouping=DFKeys.COMPARISON_ID,
    )
    pd.testing.assert_frame_equal(
        df[numerical_columns], nested_numerical_ratings[numerical_columns]
    )

  @parameterized.parameters(
      (
          pd.DataFrame({
              DFKeys.LAUNCH_ID: ['a', 'd', 'c', 'd'],
              DFKeys.COMPARISON_PARTICIPANT_ID: ['wa', 'wb', 'wc', 'wd'],
              live_loading.MONOTONIC_TIMESTAMP: [1, 2, 3, 4],
              'worker_id': ['a', 'b', 'c', 'c'],
          }),
          ['wa', 'wc'],
      ),
      (  # More data contributed for 'wd' than 'wc' instance of 'c'.
          pd.DataFrame({
              DFKeys.LAUNCH_ID: ['a', 'd', 'c', 'd', 'd'],
              DFKeys.COMPARISON_PARTICIPANT_ID: ['wa', 'wb', 'wc', 'wd', 'wd'],
              live_loading.MONOTONIC_TIMESTAMP: [1, 2, 3, 4, 5],
              'worker_id': ['a', 'b', 'c', 'c', 'c'],
          }),
          ['wa', 'wb', 'wd'],
      ),
  )
  def test_filter_groups_with_repeat_participants(
      self,
      df_data,
      remaining_ids,
  ):
    """Tests filter_groups_with_repeat_participants method."""
    df = live_loading.filter_groups_with_repeat_participants(df_data)
    self.assertSameElements(
        list(df[DFKeys.COMPARISON_PARTICIPANT_ID]), remaining_ids
    )

  @parameterized.parameters(
      (
          pd.DataFrame({
              DFKeys.COMPARISON_PARTICIPANT_ID: [
                  'y', 'z', 'y', 'z',
                  'y', 'z', 'y', 'z',
                  'g', 'h', 'g', 'h',
              ],
              DFKeys.LAUNCH_ID: [
                  'a', 'a', 'a', 'a',
                  'a', 'a', 'a', 'a',
                  'b', 'b', 'b', 'b',
              ],
              DFKeys.ROUND_ID: [
                  'wa', 'wa', 'wa', 'wa',
                  'wb', 'wb', 'wb', 'wb',
                  'wa', 'wa', 'wa', 'wa',   # Not enough rounds in b.
              ],
              DFKeys.ITERATION_INDEX: [
                  0, 0, 1, 1,
                  0, 0, 1, 1,
                  0, 0, 1, 1,
              ],
          }),
          {
              'min_num_citizens': 2,
              'min_num_iterations': 2,
              'min_num_rounds': 2,
              'num_groups': 2,
          },
          ['a'],
      ),
      (
          pd.DataFrame({
              DFKeys.COMPARISON_PARTICIPANT_ID: [
                  'y', 'z', 'y', 'z',
                  'y', 'z', 'y', 'z',
                  'g', 'h', 'g', 'h',
              ],
              DFKeys.LAUNCH_ID: [
                  'a', 'a', 'a', 'a',
                  'a', 'a', 'a', 'a',
                  'b', 'b', 'b', 'b',
              ],
              DFKeys.ROUND_ID: [
                  'wa', 'wa', 'wa', 'wa',
                  'wb', 'wb', 'wb', 'wb',
                  'wa', 'wa', 'wa', 'wa',
              ],
              DFKeys.ITERATION_INDEX: [
                  0, 0, 1, 1,
                  0, 0, 1, 1,
                  0, 0, 1, 1,
              ],
          }),
          {
              'min_num_citizens': 2,
              'min_num_iterations': 2,
              'min_num_rounds': 1,
              'num_groups': 2,
          },
          ['a', 'b'],
      ),
      (
          pd.DataFrame({
              DFKeys.COMPARISON_PARTICIPANT_ID: [
                  'y', 'z', 'y', 'z',
                  'y', 'z', 'y', 'z',
                  'g', 'g', 'g', 'g',  # Not enough citizens in b.
              ],
              DFKeys.LAUNCH_ID: [
                  'a', 'a', 'a', 'a',
                  'a', 'a', 'a', 'a',
                  'b', 'b', 'b', 'b',
              ],
              DFKeys.ROUND_ID: [
                  'wa', 'wa', 'wa', 'wa',
                  'wb', 'wb', 'wb', 'wb',
                  'wa', 'wb', 'wa', 'wb',
              ],
              DFKeys.ITERATION_INDEX: [
                  0, 0, 1, 1,
                  0, 0, 1, 1,
                  0, 0, 1, 1,
              ],
          }),
          {
              'min_num_citizens': 2,
              'min_num_iterations': 2,
              'min_num_rounds': 1,
              'num_groups': 2,
          },
          ['a'],
      ),
      (
          pd.DataFrame({
              DFKeys.COMPARISON_PARTICIPANT_ID: [
                  'y', 'z', 'y', 'z',
                  'y', 'z', 'y', 'z',
                  'g', 'h', 'g', 'h',
              ],
              DFKeys.LAUNCH_ID: [
                  'a', 'a', 'a', 'a',
                  'a', 'a', 'a', 'a',
                  'b', 'b', 'b', 'b',
              ],
              DFKeys.ROUND_ID: [
                  'wa', 'wa', 'wa', 'wa',
                  'wb', 'wb', 'wb', 'wb',
                  'wa', 'wa', 'wa', 'wa',
              ],
              DFKeys.ITERATION_INDEX: [
                  0, 0, 1, 1,
                  0, 0, 1, 1,
                  0, 0, 0, 0,  # Not enough iterations in b.
              ],
          }),
          {
              'min_num_citizens': 2,
              'min_num_iterations': 2,
              'min_num_rounds': 1,
              'num_groups': 2,
          },
          ['a'],
      ),
      (
          pd.DataFrame({
              DFKeys.COMPARISON_PARTICIPANT_ID: [
                  'y', 'z', 'y', 'z',
                  'y', 'z', 'y', 'z',
                  'g', 'h', 'g', 'h',
              ],
              DFKeys.LAUNCH_ID: [
                  'a', 'a', 'a', 'a',
                  'a', 'a', 'a', 'a',
                  'b', 'b', 'b', 'b',
              ],
              DFKeys.ROUND_ID: [
                  'wa', 'wa', 'wa', 'wa',
                  'wb', 'wb', 'wb', 'wb',
                  'wa', 'wa', 'wa', 'wa',
              ],
              DFKeys.ITERATION_INDEX: [
                  0, 0, 1, 1,
                  0, 0, 1, 1,
                  0, 0, 1, 1,
              ],
          }),
          {
              'min_num_citizens': 2,
              'min_num_iterations': 2,
              'min_num_rounds': 1,
              'num_groups': 1,  # Only keeping max 1 group.
          },
          ['a'],
      ),
  )
  def test_filter_by_number_of_groups_of_min_size(
      self,
      df,
      group_min_size_parameters,
      target_launch_ids,
  ):
    """Tests filter_by_number_of_groups_of_min_size method."""
    df = live_loading.filter_by_number_of_groups_of_min_size(
        df, **group_min_size_parameters)
    self.assertSameElements(
        list(df[DFKeys.LAUNCH_ID].drop_duplicates()),
        target_launch_ids
    )

if __name__ == '__main__':
  absltest.main()
