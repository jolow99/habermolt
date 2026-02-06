# Habermas Machine dataset

This repository contains the Habermas Machine dataset, used in
[Tessler, M. H.<sup>\*</sup>, Bakker, M. A.<sup>\*</sup>, Jarret, D., Sheahan, H., Chadwick, M. J., Koster, R., Evans, G., Campbell-Gillingham, L., Collins, T., Parkes, D. C., Botvinick, M., & Summerfield C. (2024). "AI can help humans find common ground in democratic deliberation". *Science*.](https://www.science.org/doi/10.1126/science.adq2852)
to train and evaluate the Habermas Machine.


## Download data files from Google Cloud Storage

You can download the data from Google Cloud Storage (total size ~450 MB):

```shell
wget https://storage.googleapis.com/habermas_machine/datasets/hm_all_candidate_comparisons.parquet
wget https://storage.googleapis.com/habermas_machine/datasets/hm_all_final_preference_rankings.parquet
wget https://storage.googleapis.com/habermas_machine/datasets/hm_all_position_statement_ratings.parquet
wget https://storage.googleapis.com/habermas_machine/datasets/hm_all_round_survey_responses.parquet
```

## Load into Python

[![Open In
Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/google-deepmind/habermas_machine/blob/master/analysis/habermas_machine_data_preprocessing.ipynb)

You can load the data into a Python colab using the following:

```python
import io
import requests
import pandas as pd

file_location = (
    'https://storage.googleapis.com/habermas_machine/datasets/hm_all_candidate_comparisons.parquet'
)
response = requests.get(file_location)
with io.BytesIO(response.content) as f:
  df = pd.read_parquet(f)
```

# Prompted Habermas Machine
In `habermas_machine/` we provide a prompted version of the Habermas Machine.
 The package can be installed using the following command:

```shell
pip install --upgrade git+https://github.com/google-deepmind/habermas_machine.git
```

For a demo of the prompted Habermas Machine, see the following colab:
[![Open In
Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/google-deepmind/habermas_machine/blob/master/habermas_machine/example_ai_studio.ipynb)

There are a few key differences between the prompted version of the Habermas
Machine and the fine-tuned Habermas Machine in the paper:

1. The prompted version of the Habermas Machine is not fine-tuned on the
 dataset that we provide but instead uses a more elaborate prompt and
 chain-of-thought to generate the candidate statements and preferences.

2. The prompted version of the Habermas Machine currently uses AI Studio with a
 Gemini backend. However, other LLM backends can be used and added to
 `habermas_machine/llm_client/`.

3. The reward model used in the prompted version of the Habermas Machine is
 generating the full ranking over statements given an opinion (and critique)
 rather than a score like is done in the paper. However, more reward models
 can be added to `habermas_machine/reward_model/`.

# License and disclaimer

Copyright 2024 DeepMind Technologies Limited

All software is licensed under the Apache License, Version 2.0 (Apache 2.0);
you may not use this file except in compliance with the Apache 2.0 license.
You may obtain a copy of the Apache 2.0 license at:
https://www.apache.org/licenses/LICENSE-2.0

All other materials are licensed under the Creative Commons Attribution 4.0
International License (CC-BY). You may obtain a copy of the CC-BY license at:
https://creativecommons.org/licenses/by/4.0/legalcode

Unless required by applicable law or agreed to in writing, all software and
materials distributed here under the Apache 2.0 or CC-BY licenses are
distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the licenses for the specific language governing
permissions and limitations under those licenses.

This is not an official Google product.
