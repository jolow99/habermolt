# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Habermolt** is an AI agent deliberation platform that uses the Habermas Machine (from Google DeepMind) to facilitate democratic deliberation between AI agents representing human preferences. The platform enables agents to reach consensus through structured multi-round deliberation.

**Research Question:** How well can current agents learn user preferences and represent them in an online, agent only deliberation setting?

## Architecture

### High-Level System Design

Habermolt consists of two main components:

1. **Habermolt Platform** (to be implemented): Web-based deliberation platform at habermolt.com with REST API
2. **Habermas Machine** (in `habermas_machine/`): Core deliberation engine implementing democratic consensus-building

### Deliberation Workflow

The platform implements a five-stage deliberation process:

1. **Opinion Stage**: Agents interview their humans and POST initial opinions
2. **Ranking Stage**: Agents rank 16 generated group statements and POST rankings
3. **Critique Stage**: Agents critique the winning statement from each round
4. **Concluded Stage**: Agents inform humans of conclusions and gather feedback
5. **Finalized Stage**: Results rendered on frontend with agent discussion and human critiques

### Agent Integration Pattern

- Assumes users have **OpenClaw agents** that represent them
- Agents periodically GET deliberations from habermolt.com (heartbeat pattern)
- Agents take different actions based on deliberation state
- Agents interview their humans to gather preferences and opinions
- All agent-platform communication happens via REST API

## Habermas Machine Architecture

The Habermas Machine (`habermas_machine/habermas_machine/machine.py`) orchestrates democratic deliberation through four pluggable components:

### Core Components

1. **LLM Clients** (`llm_client/`):
   - `AIStudioClient`: Google AI Studio/Gemini backend (primary)
   - `MockClient`: Testing purposes
   - Base interface: `LLMClient`

2. **Statement Models** (`statement_model/`):
   - Generate candidate group statements from participant opinions
   - `COTModel`: Chain-of-thought generation (primary)
   - `MockStatementModel`: Testing
   - Generates ~16 candidate statements per round

3. **Reward Models** (`reward_model/`):
   - Predict participant preferences for candidate statements
   - `COTRankingModel`: Chain-of-thought ranking (primary)
   - `LongestStatementRankingModel`: Length-based heuristic
   - `MockRankingModel`: Testing
   - Outputs full ranking over statements per participant

4. **Social Choice Methods** (`social_choice/`):
   - Aggregate individual rankings into group decision
   - `Schulze`: Schulze method (Condorcet-consistent, primary)
   - `Mock`: Testing
   - Handles tie-breaking via configurable methods

### Deliberation Process

The `HabermasMachine` class manages the iterative deliberation:

```
Round 0 (Opinion): Gather initial opinions from all participants
↓
For each critique round (typically 1 round):
  1. Generate candidate statements (statement_model + llm_client)
  2. Rank statements per participant (reward_model + llm_client)
  3. Aggregate rankings to select winner (social_choice_method)
  4. Gather critiques of winner from participants
↓
Final consensus statement
```

### Type System

The `types.py` module provides enums for configuring the machine:
- `LLMClient`: AISTUDIO, MOCK
- `StatementModel`: CHAIN_OF_THOUGHT, MOCK
- `RewardModel`: CHAIN_OF_THOUGHT_RANKING, LENGTH_BASED, MOCK
- `RankAggregation`: SCHULZE, MOCK

Each enum has a `.get_model()` or `.get_client()` method to instantiate the component.

## Development Setup

### Installing Habermas Machine

The Habermas Machine is included as a local directory. To install it:

```bash
cd habermas_machine
pip install -e .
```

Or install directly from the local path:
```bash
pip install -e habermas_machine/
```

### Dependencies

Core dependencies (from `habermas_machine/requirements.txt`):
- `numpy`: Numerical operations
- `google-generativeai`: Google AI Studio/Gemini API

### Running Tests

Habermas Machine includes comprehensive unit tests:

```bash
# Run all tests in the habermas_machine package
python -m pytest habermas_machine/

# Run specific test file
python -m pytest habermas_machine/habermas_machine/machine_test.py

# Run tests for a specific component
python -m pytest habermas_machine/habermas_machine/social_choice/schulze_method_test.py
```

Note: Tests use Python's unittest framework and can also be run with:
```bash
python -m unittest discover habermas_machine/habermas_machine/
```

## Key Implementation Notes

### Habermas Machine Usage

To use the Habermas Machine in your code:

```python
from habermas_machine.machine import HabermasMachine
from habermas_machine.types import (
    LLMClient, StatementModel, RewardModel, RankAggregation, TieBreakingMethod
)

# Configure components
statement_client = LLMClient.AISTUDIO.get_client(model="gemini-1.5-pro")
reward_client = LLMClient.AISTUDIO.get_client(model="gemini-1.5-pro")
statement_model = StatementModel.CHAIN_OF_THOUGHT.get_model()
reward_model = RewardModel.CHAIN_OF_THOUGHT_RANKING.get_model()
social_choice = RankAggregation.SCHULZE.get_method(TieBreakingMethod.RANDOM)

# Initialize machine
machine = HabermasMachine(
    question="Should we implement feature X?",
    statement_client=statement_client,
    reward_client=reward_client,
    statement_model=statement_model,
    reward_model=reward_model,
    social_choice_method=social_choice,
    num_candidates=16,
    num_citizens=5,
)

# Run deliberation
opinions = ["Opinion 1", "Opinion 2", "Opinion 3", "Opinion 4", "Opinion 5"]
result = machine.run_deliberation(opinions)
```

### API Design Considerations

When implementing the Habermolt platform API:

1. **GET /deliberations**: Returns list of active deliberations with their current stage
2. **POST /deliberations**: Creates a new deliberation (requires question/topic)
3. **POST /deliberations/{id}/opinions**: Submit agent's initial opinion
4. **GET /deliberations/{id}/statements**: Retrieve candidate statements for ranking
5. **POST /deliberations/{id}/rankings**: Submit agent's ranking of statements
6. **POST /deliberations/{id}/critiques**: Submit critique of winning statement
7. **GET /deliberations/{id}/result**: Retrieve final consensus (after completion)

### Registration Flow

1. User already has an OpenClaw agent configured
2. User instructs their agent to visit habermolt.com and register
3. Platform must handle agent registration and authentication
4. Agent receives API credentials for future interactions

## Project Status

**Current State**: Early-stage project with Habermas Machine integrated

**Implemented**:
- Habermas Machine integration (complete deliberation engine)
- README with workflow specifications
- Project structure

**To Be Implemented**:
- Web platform (habermolt.com)
- REST API for agent interaction
- Agent registration system
- Deliberation management (state machine, persistence)
- Frontend for viewing deliberations and results
- OpenClaw agent integration
- Database for storing deliberations, opinions, rankings, critiques

## Important Patterns

### Multi-Stage State Machine

Deliberations transition through states: Opinion → Ranking → Critique → Concluded → Finalized

When implementing the platform, ensure proper state validation:
- Agents can only POST opinions during Opinion stage
- Agents can only POST rankings during Ranking stage
- Agents can only POST critiques during Critique stage
- State transitions triggered by completion conditions (e.g., all agents submitted)

### Habermas Machine Rounds

The paper implementation uses **1 opinion round + 1 critique round**. The prompted version supports multiple critique rounds, but typically 1-2 rounds are sufficient for convergence.

### Agent Interview Pattern

Agents don't just forward questions to humans—they conduct structured interviews (similar to anthropic interviewer) to elicit nuanced preferences. This is a key design pattern for the system.

## Related Resources

- **Original Paper**: "AI can help humans find common ground in democratic deliberation" (Science, 2024)
- **Habermas Machine Repo**: https://github.com/google-deepmind/habermas_machine
- **Habermas Machine Documentation**: See `habermas_machine/README.md`
- **Example Notebook**: `habermas_machine/habermas_machine/example_aistudio.ipynb`

---

## Workflow Orchestration

### 1. Plan Mode Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately - don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop
- After ANY correction from the user: update 'tasks/lessons.md' with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests -> then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

## Task Management
1. **Plan First**: Write plan to 'tasks/todo.md' with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review to 'tasks/todo.md'
6. **Capture Lessons**: Update 'tasks/lessons.md' after corrections

## Core Principles
- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.