# Variables in Candidate Comparisons dataset

| Variable Name                                      | Description                                                                                       |
|----------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `monotonic_timestamp`                              | Timestamp indicating the moment of the data entry or event.                                       |

### Candidate Statements

| Variable Name                                      | Description                                                                                       |
|----------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `candidates.aggregation.method`                    | Method used for aggregating candidate statements (e.g., Schulze).                                 |
| `candidates.all_reward_predictions`                | List of reward model predictions from one run of the Habermas Machine (e.g., when it samples 16 statements and chooses the top 1). |
| `candidates.all_texts`                             | List of all candidate statement texts generated from one run of the Habermas Machine.             |
| `candidates.display_label`                         | Display label associated with the candidate statements shown to participants.                     |
| `candidates.metadata.*`                            | Metadata related to the candidate statement (created, ID, participant ID, provenance, etc.).       |
| `candidates.text`                                  | Full text of the candidate statements.                                                            |
| `candidates.reward_data.reward_predictions`        | Predicted reward scores for the candidate statements shown to participants.                       |
| `candidates.parent_statement_ids`                  | List of parent statement IDs linked to the candidate statement (e.g., the opinions).              |

### Top Candidate

| Variable Name                                      | Description                                                                                       |
|----------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `top_candidate.*`                                  | Fields similar to `candidates`, representing the top-ranked candidate statement.                  |

### Critique

| Variable Name                                      | Description                                                                                       |
|----------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `critique.text`                                    | Full text of the critique provided by the participant.                                            |
| `critique.metadata.*`                              | Metadata for critiques (created, ID, participant ID, provenance, etc.).                            |

### Opinions

| Variable Name                                      | Description                                                                                       |
|----------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `own_opinion.text`                                 | Full text of the participant's own opinion.                                                       |
| `own_opinion.metadata.*`                           | Metadata for the participant's own opinion (created, ID, participant ID, provenance, etc.).        |
| `other_opinions.text`                              | Text of opinions shared by other participants.                                                    |
| `other_opinions.metadata.*`                        | Metadata for opinions shared by others (created, ID, participant ID, provenance, etc.).            |

### Questions

| Variable Name                                      | Description                                                                                       |
|----------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `question.id`                                      | Unique identifier for the question.                                                               |
| `question.text`                                    | Full text of the deliberation question.                                                           |
| `question.affirming_statement`                     | Position statement expressing the supporting position on the question.                            |
| `question.negating_statement`                      | Position statement expressing the opposing position on the question.                              |
| `question.topic`                                   | Topic ID of the question.                                                                         |
| `question.split`                                   | Dataset split identifier (e.g., train, test, validation).                                         |

### Rankings and Ratings

| Variable Name                                      | Description                                                                                       |
|----------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `rankings.candidate_ids`                           | List of candidate statement IDs ranked by the participant.                                        |
| `rankings.numerical_ranks`                         | Numerical ranks assigned by the participant to each candidate statement.                          |
| `ratings.agreement`                                | Participant’s endorsement rating for the candidate statement.                                      |
| `ratings.quality`                                  | Quality rating provided by the participant for the candidate statement.                           |

### Metadata and Identifiers

| Variable Name                                      | Description                                                                                       |
|----------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `iteration_id`                                     | Unique identifier for the deliberation iteration.                                                 |
| `iteration_index`                                  | Index number of the iteration within the deliberation process (e.g., pre-critique, post-critique). |
| `launch_id`                                        | Identifier for the specific group of participants.                                                |
| `metadata.*`                                       | General metadata fields (created, ID, participant ID, provenance, response duration, etc.).       |
| `round_id`                                         | Unique identifier for the deliberation round.                                                     |
| `worker_id`                                        | Unique identifier for the participant.                                                            |

## Metadata Characteristics

The following metadata fields provide additional context and details for various elements within the dataset (e.g., candidates, critiques, own opinions):

| Variable Name                                      | Description                                                                                       |
|----------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `metadata.created`                                 | Timestamp when the entry (e.g., candidate statement, critique) was created.                       |
| `metadata.generative_model.api_version`            | Version of the generative model API used for creating the text.                                   |
| `metadata.generative_model.template_name`          | Template name used by the generative model for text generation.                                   |
| `metadata.id`                                      | Unique identifier for the entry (e.g., candidate statement, critique).                            |
| `metadata.participant_id`                          | Identifier of the participant associated with the entry.                                          |
| `metadata.provenance`                              | Provenance information indicating the source or process that created the entry.                   |
| `metadata.response_duration`                       | Time taken (in seconds) by the participant to respond.                                            |
| `metadata.reward_model.api_version`                | Version of the reward model API used for predicting participant preferences.                      |
| `metadata.reward_model.template_name`              | Template name used by the reward model for generating predictions.                                |
