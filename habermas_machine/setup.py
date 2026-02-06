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

"""Setup.py for the habermas_machine package."""

import setuptools

with open('requirements.txt', 'r') as reqs_f:
  requirements = reqs_f.read().split()

with open('LICENSE', 'r') as lf:
  LICENSE = lf.read()

setuptools.setup(
    name='habermas_machine',
    version='0.1',
    description=(
        'Gemini-based version of the "Habermas Machine" introduced in the '
        'Science 2024 publication "AI can help humans find common ground in '
        'democratic deliberation".'
    ),
    url='https://www.science.org/stoken/author-tokens/ST-2196/full',
    author='Google DeepMind',
    author_email='miba@google.com',
    license=LICENSE,
    install_requires=requirements,
    packages=[
        'habermas_machine',
        'habermas_machine.llm_client',
        'habermas_machine.reward_model',
        'habermas_machine.social_choice',
        'habermas_machine.statement_model'
    ],
    zip_safe=False,
)
