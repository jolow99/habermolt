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

"""A ranking model that uses chain-of-thought reasoning."""

from collections.abc import Sequence
import re

import numpy as np
from typing_extensions import override

from habermas_machine.llm_client import base_client
from habermas_machine.reward_model import base_model


class COTRankingModel(base_model.BaseRankingModel):
  """A ranking model that uses chain-of-thought reasoning to rank statements."""

  @override
  def predict_ranking(
      self,
      llm_client: base_client.LLMClient,
      question: str,
      opinion: str,
      statements: Sequence[str],
      previous_winner: str | None = None,
      critique: str | None = None,
      seed: int | None = None,
      num_retries_on_error: int | None = None,
  ) -> base_model.RankingResult:
    """Ranks statements based on their length (see base class)."""
    if num_retries_on_error is None:
      num_retries_on_error = 0
    else:
      if num_retries_on_error < 0:
        raise ValueError('num_retries_on_error must be None or at least 0.')
    if previous_winner is None and critique is not None:
      raise ValueError(
          'If there is a previous_winner, there should be a critique.'
      )
    if len(statements) < 2:
      raise ValueError('There should be at least two statements to rank.')

    prompt = _generate_prompt(
        question, opinion, statements, previous_winner, critique
    )

    ranking_result = base_model.RankingResult(None, None)  # Dummy result.
    for _ in range(num_retries_on_error + 1):
      response = llm_client.sample_text(
          prompt, terminators=['</answer>'], seed=seed)
      ranking_result = _process_model_response(response, len(statements))

      if (
          ranking_result.ranking is not None
          and 'INCORRECT' not in ranking_result.explanation
      ):
        return ranking_result
      else:
        if seed is not None:
          seed += 1
          print(
              'Retrying with new seed. Explanation:'
              f' {ranking_result.explanation}'
          )

    # If we reach here, all retries failed. return the last result.
    return ranking_result


def _generate_opinion_critique_prompt(
    question: str,
    opinion: str,
    statements: Sequence[str],
    previous_winner: str,
    critique: str,
) -> str:
  """Generates a prompt for the LLM using opinion and critique."""
  prompt = f"""As an AI assistant, your job is to rank these statements in the order that the participant would most likely agree with them, based on their opinion and critique to a summary statement from a previous discussion round. Use Arrow notation for the ranking, where ">" means "preferred to". Ties are NOT allowed and items should be in descending order of preference so you can ONLY use ">" and the letters of the statements in the ranking. Examples of valid rankings: B > A, D > A > C > B. B > C > A > E > D.

Please think through this task step-by-step:

1. Analyze the participant's opinion and critique, noting key points and sentiments.
2. Analyze the critique to the summary statement from the previous discussion round.
3. Compare each statement to the participant's opinion and critique, considering how well it aligns with or supports their view.
4. Consider any nuances or implications in the statements that might appeal to or repel the participant based on their expressed opinion.
5. Rank the statements accordingly using only ">" and the letters of the statements.

Provide your answer in the following format:
<answer>
[Your step-by-step reasoning and explanation for the ranking]
<sep>
[Final ranking using arrow notation]
</answer>

For example for five statements A, B, C, D and E a valid response could be:
<answer>
1. The participant's opinion emphasizes the importance of environmental protection and the need for immediate action to address climate change. The critique of the previous winner highlights that it failed to offer specific solutions.

2. The critique emphasizes the need for concrete solutions to address climate change, indicating that the participant values action-oriented approaches.

3. - Statement A directly addresses the urgency of climate action and proposes concrete steps, aligning with both the participant's opinion and critique.
  - Statements B and D acknowledge the seriousness of climate change but offer less concrete solutions. B focuses on global cooperation, while D emphasizes economic considerations.
  - Statement C downplays the urgency of climate change, contradicting the participant's stance.
  - Statement E completely opposes the participant's view by denying the existence of climate change.

4.  The participant's emphasis on immediate action suggests a preference for proactive solutions and a dislike for approaches that downplay the issue or offer only abstract ideas.

5. Based on this analysis, the ranking is: A > D > B > C > E

<sep>
A > D > B > C > E
</answer>

It is important to follow the template EXACTLY. So ALWAYS start with <answer>, then the explanation, then <sep> then only the final ranking and then </answer>.


Below you will find the question, the participant's opinion, the statement from the previous round, and a critique of that statement. You will also find a list of statements to rank.

Question: {question}

Participant's Opinion: {opinion}

Statement from previous round: {previous_winner}

Critique: {critique}

Statements to rank:
"""
  for i, statement in enumerate(statements):
    letter = chr(ord('A') + i)  # A, B, C, D, etc.
    try:
      statement = (
          statement.strip().strip('').strip('""').strip('\n').strip()
      )
    except Exception as exc:
      raise ValueError(f'Issue with statement: {statement}') from exc
    prompt += f'{letter}. {statement}\n'

  return prompt.strip()


def _generate_opinion_only_prompt(
    question: str,
    opinion: str,
    statements: Sequence[str],
) -> str:
  """Generates a prompt for the LLM using only the opinion."""
  prompt = f"""
Task: As an AI assistant, your job is to rank these statements in the order that the participant would most likely agree with them, based on their opinion. Use Arrow notation for the ranking, where ">" means "preferred to". Ties are NOT allowed and items should be in descending order of preference so you can ONLY use ">" and the letters of the statements in the final ranking. Examples of valid final rankings: B > A, D > A > C > D. B > C > A > E > D.

Please think through this task step-by-step:

1. Analyze the participant's opinion, noting key points and sentiments.
2. Compare each statement to the participant's opinion, considering how well it aligns with or supports their view.
3. Consider any nuances or implications in the statements that might appeal to or repel the participant based on their expressed opinion.
4. Rank the statements accordingly using only ">" and the letters of the statements.

Provide your answer in the following format:
<answer>
[Your step-by-step reasoning and explanation for the ranking]
<sep>
[Final ranking using arrow notation]
</answer>

For example for five statements A, B, C, D and E a valid response could be:
<answer>
1. The participant's opinion emphasizes the importance of environmental protection and the need for immediate action to address climate change.

2. - Statement A directly addresses the urgency of climate action and proposes concrete steps, aligning with the participant's opinion.
   - Statements B and D acknowledge the seriousness of climate change but offer less concrete solutions. B focuses on global cooperation, while D emphasizes economic considerations.
   - Statement C downplays the urgency of climate change, contradicting the participant's stance.
   - Statement E completely opposes the participant's view by denying the existence of climate change.

3.  The participant's emphasis on immediate action suggests a preference for proactive solutions and a dislike for approaches that downplay the issue or offer only abstract ideas.

4. Based on this analysis, the ranking is: A > D > B > C > E

<sep>
A > D > B > C > E
</answer>

It is important to follow the template EXACTLY. So ALWAYS start with <answer>, then the explanation, then <sep> then only the final ranking and then </answer>.


Below you will find the question and the participant's opinion. You will also find a list of statements to rank.

Question: {question}

Participant's Opinion: {opinion}

Statements to rank:
"""
  for i, statement in enumerate(statements):
    letter = chr(ord('A') + i)  # A, B, C, D, etc.
    try:
      statement = (
          statement.strip().strip('').strip('""').strip('\n').strip()
      )
    except Exception as exc:
      raise ValueError(f'Issue with statement: {statement}') from exc
    prompt += f'{letter}. {statement}\n'

  return prompt.strip()


def _generate_prompt(
    question: str,
    opinion: str,
    statements: Sequence[str],
    previous_winner: str | None = None,
    critique: str | None = None,
) -> str:
  """Generates a prompt for the LLM."""
  if previous_winner is None:
    return _generate_opinion_only_prompt(
        question, opinion, statements
    )
  else:
    return _generate_opinion_critique_prompt(
        question, opinion, statements, previous_winner, critique
    )


def _check_response_format(response: str) -> bool:
  """Checks if the response is in a correct format with <answer> and <sep>.

  Args:
    response: The model's raw response

  Returns:
    bool: True if the format is correct, False otherwise
  """
  # Made more lenient - some models omit the opening <answer> tag
  pattern = r'(?:<answer>\s*)?.*?\s*<sep>\s*.*?\s*</answer>'
  return bool(re.search(pattern, response, re.DOTALL))


def _check_arrow_format(arrow_ranking):
  """Checks if the arrow ranking format is correct.

  Args:
    arrow_ranking: The arrow ranking string (eg A > B > C)

  Returns:
  bool: True if the format is correct, False otherwise
  """
  if len(arrow_ranking) < 3:
    return False

  # Remove whitespace and replace multiple spaces with single spaces.
  arrow_ranking = re.sub(r'\s+', ' ', arrow_ranking.strip())

  # Remove spaces around '>' and '=' symbols.
  arrow_ranking = re.sub(r'\s*(>|=)\s*', r'\1', arrow_ranking)

  # Check if the ranking contains only allowed characters.
  if not re.match(r'^[A-Z>=]+$', arrow_ranking):
    return False

  # Check for consecutive '>' symbols, '=' at the start/end,
  # or '=' immediately before '>'.
  if (
      '>>' in arrow_ranking
      or arrow_ranking.startswith('=')
      or arrow_ranking.endswith('=')
      or '=>' in arrow_ranking
  ):
    return False

  # Split by '>' and check each group
  groups = arrow_ranking.split('>')

  if len(groups) < 1:
    return False

  seen_letters = set()
  for group in groups:
    # Check if the group is empty.
    if not group:
      return False
    # Check if each group contains only unique letters separated by '='.
    letters = group.split('=')
    if len(letters) != len(set(letters)):
      return False
    # Check if any letter in this group has been seen before.
    if any(letter in seen_letters for letter in letters):
      return False
    seen_letters.update(letters)

  return True


def _extract_arrow_ranking(text: str) -> str | None:
  """Extracts the arrow ranking from a given string.

  Args:
    text: The input string containing the arrow ranking.

  Returns:
    The extracted arrow ranking or None if not found.
  """
  # Regular expression to match a full arrow ranking pattern
  match = re.search(r'\b([A-Z](?:\s*(?:>|=)\s*[A-Z])*)\b', text)

  if match:
    return match.group(1).replace(' ', '')  # Removes any extra spaces
  else:
    return None


def _process_model_response(
    response: str, num_statements: int) -> base_model.RankingResult:
  """Processes the model's response, extract the explanation and arrow ranking.

  Args:
    response: The raw model response.
    num_statements: The number of statements to rank.

  Returns:
    A base_model.RankingResult of:
    - np.ndarray: The arrow ranking if it is correct, None otherwise.
    - str: The explanation if it is correct, "INCORRECT_TEMPLATE" if the
    response format is incorrect, or "INCORRECT_ARROW_RANKING" if the arrow
    ranking is incorrect.
  """
  if _check_response_format(response):
    # Try with opening <answer> tag first
    match = re.search(
        r'<answer>\s*(.*?)\s*<sep>\s*(.*?)\s*</answer>', response, re.DOTALL
    )
    # If not found, try without opening tag (some models omit it)
    if match is None:
      match = re.search(
          r'(.*?)\s*<sep>\s*(.*?)\s*</answer>', response, re.DOTALL
      )
    if match is None:
      return base_model.RankingResult(None, f'INCORRECT_TEMPLATE: {response}')
    else:
      explanation = match.group(1).strip()
      arrow_ranking = _extract_arrow_ranking(
          match.group(2).strip())
  else:
    # Backup as it sometimes returns "final ranking:" in a different format.
    match = re.search(r'(?i)final ranking:\s*(.*)', response)
    if match is None:
      return base_model.RankingResult(None, f'INCORRECT_TEMPLATE: {response}')
    else:
      explanation = response
      arrow_ranking = _extract_arrow_ranking(match.group(1))

  if arrow_ranking is None or not _check_arrow_format(
      arrow_ranking
  ):
    # Check if the ranking is in the explanation.
    arrow_ranking = _extract_arrow_ranking(
        explanation.strip()
    )
    if arrow_ranking is None or not _check_arrow_format(
        arrow_ranking
    ):
      return base_model.RankingResult(
          None, f'INCORRECT_ARROW_RANKING: {response}')

  # Convert arrow ranking to numpy array.
  elements = re.findall(r'[A-Z]', arrow_ranking)
  unique_elements = sorted(set(elements))
  ranking_dict = {element: 0 for element in unique_elements}

  groups = arrow_ranking.split('>')
  for rank, group in enumerate(groups):
    tied_elements = group.strip().split('=')
    for element in tied_elements:
      ranking_dict[element.strip()] = rank

  result = np.array([ranking_dict[element] for element in unique_elements])

  if len(result) != num_statements:
    return base_model.RankingResult(
        None, f'INCORRECT_RANKING_LENGTH: {response}')

  return base_model.RankingResult(result, response)
