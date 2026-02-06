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

"""Mock dataframes for use in tests."""

import pandas as pd

from habermas_machine.analysis import live_loading
from habermas_machine.analysis import serialise
from habermas_machine.analysis import types as hm_types

DFKeys = serialise.SerialisedComparisonKeys
DUMMY_DF = pd.DataFrame({
    DFKeys.COMPARISON_ID: ['N1', 'N1', 'N2', 'N2', 'N3', 'N4'],
    DFKeys.SPLIT:
        ([hm_types.Split.TRAIN.name] * 3 + [hm_types.Split.VALIDATION.name] * 3
        ),
    DFKeys.RATINGS_AGREEMENT: [
        (
            hm_types.LikertAgreement.STRONGLY_DISAGREE.name,
            hm_types.LikertAgreement.DISAGREE.name,
        ),
        (
            hm_types.LikertAgreement.STRONGLY_DISAGREE.name,
            hm_types.LikertAgreement.DISAGREE.name,
            hm_types.LikertAgreement.NEUTRAL.name,
        ),
        (
            hm_types.LikertAgreement.DISAGREE.name,
            hm_types.LikertAgreement.STRONGLY_DISAGREE.name,
        ),
        (
            hm_types.LikertAgreement.STRONGLY_DISAGREE.name,
            hm_types.LikertAgreement.MOCK.name,
        ),
        (
            hm_types.LikertAgreement.STRONGLY_DISAGREE.name,
            hm_types.LikertAgreement.STRONGLY_DISAGREE.name,
        ), (
            hm_types.LikertAgreement.MOCK.name,
            hm_types.LikertAgreement.MOCK.name,
        ),
    ],
    DFKeys.RANKINGS_NUMERICAL_RANKS: [
        (1, 0), (2, 1, 0), (0, 1), (-1, -1), (0, 0), (-1, -1)],
    DFKeys.CANDIDATES_ID: [(1, 2), (3, 4, 5), (6, 7), (8, 9), (10, 1),
                           (11, 12)],
})
NESTED_DUMMY_DF = pd.DataFrame({
    DFKeys.COMPARISON_PARTICIPANT_ID: [2, 2, 1],
    DFKeys.COMPARISON_ID: ['N1', 'N2', 'N3'],
    DFKeys.SPLIT:
        ([hm_types.Split.TRAIN.name] * 1 + [hm_types.Split.VALIDATION.name] * 2
        ),
    DFKeys.RATINGS_AGREEMENT: [
        (
            hm_types.LikertAgreement.STRONGLY_DISAGREE.name,
            hm_types.LikertAgreement.DISAGREE.name,
            hm_types.LikertAgreement.SOMEWHAT_DISAGREE.name,
        ),
        (
            hm_types.LikertAgreement.AGREE.name,
            hm_types.LikertAgreement.DISAGREE.name,
            hm_types.LikertAgreement.STRONGLY_DISAGREE.name,
        ),
        (
            hm_types.LikertAgreement.STRONGLY_DISAGREE.name,
            hm_types.LikertAgreement.STRONGLY_AGREE.name,
        ),
    ],
    DFKeys.RATINGS_QUALITY: [
        (
            hm_types.LikertQuality.NEUTRAL.name,
            hm_types.LikertQuality.TERRIBLE_QUALITY.name,
            hm_types.LikertQuality.POOR_QUALITY.name,
        ),
        (
            hm_types.LikertQuality.TERRIBLE_QUALITY.name,
            hm_types.LikertQuality.SOMEWHAT_POOR_QUALITY.name,
            hm_types.LikertQuality.POOR_QUALITY.name,
        ),
        (
            hm_types.LikertQuality.NEUTRAL.name,
            hm_types.LikertQuality.TERRIBLE_QUALITY.name,
        ),
    ],
    DFKeys.RANKINGS_NUMERICAL_RANKS: [(2, 1, 0), (0, 1, 2), (1, 0)],
    DFKeys.CANDIDATES_ID: [(1, 2, 2), (3, 3, 3), (4, 4)],
})
UNNESTED_DUMMY_DF = pd.DataFrame({
    DFKeys.COMPARISON_PARTICIPANT_ID: [2, 2, 2, 2, 2, 2, 1, 1],
    DFKeys.COMPARISON_ID: ['N1', 'N1', 'N1', 'N2', 'N2', 'N2', 'N3', 'N3'],
    DFKeys.SPLIT:
        ([hm_types.Split.TRAIN.name] * 3 + [hm_types.Split.VALIDATION.name] * 5
        ),
    DFKeys.RATINGS_AGREEMENT: [
        hm_types.LikertAgreement.STRONGLY_DISAGREE.name,
        hm_types.LikertAgreement.DISAGREE.name,
        hm_types.LikertAgreement.SOMEWHAT_DISAGREE.name,
        hm_types.LikertAgreement.AGREE.name,
        hm_types.LikertAgreement.DISAGREE.name,
        hm_types.LikertAgreement.STRONGLY_DISAGREE.name,
        hm_types.LikertAgreement.STRONGLY_DISAGREE.name,
        hm_types.LikertAgreement.STRONGLY_AGREE.name,
    ],
    DFKeys.RATINGS_QUALITY: [
        hm_types.LikertQuality.NEUTRAL.name,
        hm_types.LikertQuality.TERRIBLE_QUALITY.name,
        hm_types.LikertQuality.POOR_QUALITY.name,
        hm_types.LikertQuality.TERRIBLE_QUALITY.name,
        hm_types.LikertQuality.SOMEWHAT_POOR_QUALITY.name,
        hm_types.LikertQuality.POOR_QUALITY.name,
        hm_types.LikertQuality.NEUTRAL.name,
        hm_types.LikertQuality.TERRIBLE_QUALITY.name,
    ],
    DFKeys.RANKINGS_NUMERICAL_RANKS: [2, 1, 0, 0, 1, 2, 1, 0],
    DFKeys.CANDIDATES_ID: [1, 2, 2, 3, 3, 3, 4, 4],
})
UNNESTED_NUMERICAL_RATINGS = pd.DataFrame({
    live_loading.NUMERICAL_RATINGS_AGREEMENT:
        [1, 2, 3, 6, 2, 1, 1, 7],
    live_loading.NUMERICAL_RATINGS_QUALITY:
        [4, 1, 2, 1, 3, 2, 4, 1],
    DFKeys.COMPARISON_ID: [1, 1, 1, 2, 2, 2, 3, 3],
})
DF_FOR_CANDIDATE_PROVENANCE = pd.DataFrame({
    DFKeys.COMPARISON_ID: ['a', 'a', 'a', 'a', 'c', 'd', 'd'],
    DFKeys.CANDIDATES_ID: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    DFKeys.CANDIDATES_PROVENANCE: [
        hm_types.ResponseProvenance.MOCK.name,
        hm_types.ResponseProvenance.EXAMPLE.name,
        hm_types.ResponseProvenance.BOT_CITIZEN.name,
        hm_types.ResponseProvenance.HUMAN_CITIZEN.name,
        hm_types.ResponseProvenance.HUMAN_MEDIATOR.name,
        hm_types.ResponseProvenance.MODEL_MEDIATOR.name,
        hm_types.ResponseProvenance.POSITION_STATEMENT.name,
    ],
    DFKeys.OWN_OPINION_PROVENANCE: [
        hm_types.ResponseProvenance.POSITION_STATEMENT.name,
        hm_types.ResponseProvenance.MOCK.name,
        hm_types.ResponseProvenance.EXAMPLE.name,
        hm_types.ResponseProvenance.BOT_CITIZEN.name,
        hm_types.ResponseProvenance.HUMAN_CITIZEN.name,
        hm_types.ResponseProvenance.HUMAN_MEDIATOR.name,
        hm_types.ResponseProvenance.MODEL_MEDIATOR.name,
    ],
})
