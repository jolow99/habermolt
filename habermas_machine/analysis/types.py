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

"""Common types.

This module contains commons types used throughout habermas_machine/.
"""

import enum

import numpy as np

RANKING_MOCK = -1


@enum.unique
class Split(enum.IntEnum):
  """Dataset splits for questions."""
  MOCK = -1  # Used for writing data on blank questions in human_tasks.
  TRAIN = 1
  VALIDATION = 2
  IID_TEST = 3  # "Easy" within distribution test on the same topics/clusters.
  OOD_TEST = 4  # "Hard" out-of-distribution test on unseen topics/clusters.


@enum.unique
class LikertAgreement(enum.Enum):
  """Seven-point Likert scale for agreement ratings."""
  MOCK = -1
  STRONGLY_DISAGREE = 1
  DISAGREE = 2
  SOMEWHAT_DISAGREE = 3
  NEUTRAL = 4
  SOMEWHAT_AGREE = 5
  AGREE = 6
  STRONGLY_AGREE = 7

  @classmethod
  def valid(cls):
    """Returns all valid Likert enums (not the Mock)."""
    return [likert for likert in cls if likert is not cls.MOCK]

  @classmethod
  def random_sample(cls, *, num: int, include_mock=False):
    """Returns 'num' many random samples from valid Likert enums (not the Mock)."""
    if include_mock:
      values = tuple(np.random.choice(cls, size=num))
    else:
      values = tuple(np.random.choice(cls.valid(), size=num))
    return tuple([cls(value) for value in values])

  @classmethod
  def name_to_value(cls, name):
    return getattr(cls, name).value

  def to_text(self):
    """Returns an enum as a pair of strings for use with Loupe radio buttons."""
    return str(self.value), self.name.lower().replace('_', ' ')


@enum.unique
class LikertQuality(enum.Enum):
  """Seven-point Likert scale for quality ratings."""
  MOCK = -1
  TERRIBLE_QUALITY = 1
  POOR_QUALITY = 2
  SOMEWHAT_POOR_QUALITY = 3
  NEUTRAL = 4
  SOMEWHAT_GOOD_QUALITY = 5
  GOOD_QUALITY = 6
  EXCELLENT_QUALITY = 7

  @classmethod
  def valid(cls):
    """Returns all valid Likert enums (not the Mock)."""
    return [likert for likert in cls if likert is not cls.MOCK]

  @classmethod
  def random_sample(cls, *, num: int, include_mock=False):
    """Returns 'num' many random samples from valid Likert enums (not the Mock)."""
    if include_mock:
      values = tuple(np.random.choice(cls, size=num))
    else:
      values = tuple(np.random.choice(cls.valid(), size=num))
    return tuple([cls(value) for value in values])

  @classmethod
  def name_to_value(cls, name):
    return getattr(cls, name).value

  def to_text(self):
    """Returns an enum as a pair of strings for use with Loupe radio buttons."""
    return str(self.value), self.name.lower().replace('_', ' ')


@enum.unique
class LikertImportance(enum.Enum):
  """Five-point Likert scale for importance ratings."""
  MOCK = -1
  NOT_IMPORTANT = 1
  SLIGHTLY_IMPORTANT = 2
  MODRATELY_IMPORTANT = 3  # Name with typo, corrected in to_text below.
  IMPORTANT = 4
  VERY_IMPORTANT = 5

  @classmethod
  def valid(cls):
    """Returns all valid Likert enums (not the Mock)."""
    return [likert for likert in cls if likert is not cls.MOCK]

  @classmethod
  def random_sample(cls, *, num: int, include_mock=False):
    """Returns 'num' many random samples from valid Likert enums (not the Mock)."""
    if include_mock:
      values = tuple(np.random.choice(cls, size=num))
    else:
      values = tuple(np.random.choice(cls.valid(), size=num))
    return tuple([cls(value) for value in values])

  @classmethod
  def name_to_value(cls, name):
    return getattr(cls, name).value

  def to_text(self):
    """Returns an enum as a pair of strings for use with Loupe radio buttons."""
    corrected_name = ('MODERATELY_IMPORTANT'
                      if self == self.MODRATELY_IMPORTANT else self.name)
    return str(self.value), ' '.join(
        [x.capitalize() for x in corrected_name.split('_')]
    )


@enum.unique
class ResponseProvenance(enum.Enum):
  """Sources that Statement and CandidateComparison responses can come from."""
  MOCK = 'mock'  # For use in testing only.
  DUMMY = 'dummy'  # A dummy value to complete an object (for serialisation).
  EXAMPLE = 'example'  # Handcrafted example datasets of opinions.
  BOT_CITIZEN = 'bot_citizen'  # A bot that replaces a human citizen worker.
  HUMAN_CITIZEN = 'human_citizen'
  HUMAN_MEDIATOR = 'human_mediator'
  MODEL_MEDIATOR = 'model_mediator'
  POSITION_STATEMENT = 'position_statement'  # Derived from the question itself.

  @classmethod
  def human_members(cls):
    """Returns all human provenances including mocks and examples."""
    return (
        cls.HUMAN_CITIZEN,
        cls.HUMAN_MEDIATOR,
        cls.BOT_CITIZEN,
        cls.MOCK,
        cls.EXAMPLE,
        cls.DUMMY,
    )

  @classmethod
  def model_members(cls):
    """Returns all model provenances including mocks and examples."""
    return (
        cls.MODEL_MEDIATOR,
        cls.MOCK,
        cls.EXAMPLE,
        cls.DUMMY,
    )

  @classmethod
  def position_members(cls):
    """Returns all position statement provenances including mocks."""
    return (cls.POSITION_STATEMENT, cls.MOCK)
