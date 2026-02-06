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

from habermas_machine.llm_client import mock_client
from habermas_machine.statement_model import cot_model


class COTModelTest(parameterized.TestCase):

  def test_generate_opinion_only_prompt(self):
    """Tests the _generate_opinion_only_prompt method."""
    question = "What is the best way to improve public transport?"
    opinions = [
        "Invest in more buses.",
        "Reduce fares.",
        "Improve the train network."
    ]
    prompt = cot_model._generate_opinion_only_prompt(question, opinions)
    self.assertIn(question, prompt)
    for opinion in opinions:
      self.assertIn(opinion, prompt)
    self.assertIn("<answer>", prompt)
    self.assertIn("<sep>", prompt)

  def test_generate_opinion_critique_prompt(self):
    """Tests the _generate_opinion_critique_prompt method."""
    question = "How can we make our city greener?"
    opinions = [
        "Plant more trees.",
        "Create more parks.",
        "Reduce car usage."
    ]
    previous_winner = "We should plant more trees in the city center."
    critiques = [
        "Planting trees is not enough.",
        "We need more parks, not just trees."
    ]
    prompt = cot_model._generate_opinion_critique_prompt(
        question, opinions, previous_winner, critiques
    )
    self.assertIn(question, prompt)
    for opinion in opinions:
      self.assertIn(opinion, prompt)
    self.assertIn(previous_winner, prompt)
    for critique in critiques:
      self.assertIn(critique, prompt)
    self.assertIn("<answer>", prompt)
    self.assertIn("<sep>", prompt)

  def test_generate_prompt(self):
    """Tests the _generate_prompt method."""
    question = "What is the meaning of life?"
    opinions = ["42", "To be happy", "To help others"]

    # Test with only opinions
    prompt = cot_model._generate_prompt(question, opinions)
    self.assertEqual(
        prompt, cot_model._generate_opinion_only_prompt(question, opinions)
    )

    # Test with previous winner and critiques
    previous_winner = "42 is the answer."
    critiques = ["That's not helpful", "What about happiness?"]
    prompt = cot_model._generate_prompt(
        question, opinions, previous_winner, critiques
    )
    self.assertEqual(
        prompt,
        cot_model._generate_opinion_critique_prompt(
            question, opinions, previous_winner, critiques
        ),
    )

  def test_process_model_response(self):
    """Tests the _process_model_response method."""
    # Test correct format
    response = (
        "<answer>This is the explanation.\n<sep>\nThis is the"
        " statement.</answer>"
    )
    statement, explanation = cot_model._process_model_response(response)
    self.assertEqual(statement, "This is the statement.")
    self.assertEqual(explanation, "This is the explanation.")

    # Test incorrect format
    response = "This is just some text."
    statement, explanation = cot_model._process_model_response(response)
    self.assertEqual(statement, "")
    self.assertEqual(explanation, "INCORRECT_TEMPLATE")

  def test_generate_statement(self):
    """Tests the generate_statement method."""

    model = cot_model.COTModel()
    llm_client = mock_client.MockClient(
        response="<answer>Mock explanation<sep>Mock statement</answer>")
    question = "Test question?"
    opinions = ["Opinion 1", "Opinion 2"]
    statement, explanation = model.generate_statement(
        llm_client, question, opinions
    )
    self.assertEqual(statement, "Mock statement")
    self.assertEqual(explanation, "Mock explanation")


if __name__ == "__main__":
  absltest.main()
