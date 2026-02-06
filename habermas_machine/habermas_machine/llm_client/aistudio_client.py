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

"""Language Model that uses GDM AI Studio API."""

from collections.abc import Collection, Mapping, Sequence
import os
import time

import google.generativeai as genai
from typing_extensions import override

from habermas_machine.llm_client import base_client
from habermas_machine.llm_client import utils


DEFAULT_SAFETY_SETTINGS = (
    {
        'category': 'HARM_CATEGORY_HARASSMENT',
        'threshold': 'BLOCK_ONLY_HIGH',
    },
    {
        'category': 'HARM_CATEGORY_HATE_SPEECH',
        'threshold': 'BLOCK_ONLY_HIGH',
    },
    {
        'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
        'threshold': 'BLOCK_ONLY_HIGH',
    },
    {
        'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
        'threshold': 'BLOCK_ONLY_HIGH',
    },
)


class AIStudioClient(base_client.LLMClient):
  """Language Model that uses AI Studio API."""

  def __init__(
      self,
      model_name: str,
      *,
      safety_settings: Sequence[Mapping[str, str]] = DEFAULT_SAFETY_SETTINGS,
      sleep_periodically: bool = False,
  ) -> None:
    """Initializes the instance.

    Args:
      model_name: which language model to use. For more details, see
        https://aistudio.google.com/.
      safety_settings: Gemini safety settings. For more details, see
        https://ai.google.dev/gemini-api/docs/safety.
      sleep_periodically: sleep between API calls to avoid rate limit.
    """
    self._api_key = os.environ['GOOGLE_API_KEY']
    self._model_name = model_name
    self._safety_settings = safety_settings
    self._sleep_periodically = sleep_periodically

    genai.configure(api_key=self._api_key)
    self._model = genai.GenerativeModel(
        model_name=self._model_name,
        safety_settings=safety_settings,
    )

    self._calls_between_sleeping = 10
    self._n_calls = 0

  @override
  def sample_text(
      self,
      prompt: str,
      *,
      max_tokens: int = base_client.DEFAULT_MAX_TOKENS,
      terminators: Collection[str] = base_client.DEFAULT_TERMINATORS,
      temperature: float = base_client.DEFAULT_TEMPERATURE,
      timeout: float = base_client.DEFAULT_TIMEOUT_SECONDS,
      seed: int | None = None,
  ) -> str:
    del timeout
    del seed  # AI Studio does not support seeds.

    self._n_calls += 1
    if self._sleep_periodically and (
        self._n_calls % self._calls_between_sleeping == 0):
      print('Sleeping for 10 seconds...')
      time.sleep(10)

    sample = self._model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            stop_sequences=terminators,
        ),
        safety_settings=self._safety_settings,
        stream=False,
    )
    try:
      # AI Studio returns a list of parts, but we only use the first one.
      response = sample.candidates[0].content.parts[0].text
    except (ValueError, IndexError) as e:
      print('An error occurred: ', e)
      print(f'prompt: {prompt}')
      print(f'sample: {sample}')
      print(f'sample.prompt_feedback: {sample.prompt_feedback}')
      # Check if blocked by safety filters
      if hasattr(sample, 'prompt_feedback'):
        print(f'Safety ratings: {sample.prompt_feedback}')
      response = ''
    return utils.truncate(response, delimiters=terminators)

