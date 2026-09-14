# ARC Prize 2026: ARC-AGI-3

**Languages:** [English](README.md) | [简体中文](README.zh-CN.md)

This repository is a reproducible research workspace for the **ARC Prize 2026 - ARC-AGI-3** Kaggle competition. The project studies how an AI agent can enter a previously unseen interactive environment, discover its controls and objectives, form a compact model of the environment, and complete increasingly difficult levels with as few actions as possible.

The development strategy is evidence-driven: understand the benchmark and evaluation protocol first, build reliable local tooling, establish simple baselines, inspect failures, and introduce more complex methods only when controlled experiments justify them.

## Official Links

| Resource | Link |
| --- | --- |
| Kaggle competition | [ARC Prize 2026 - ARC-AGI-3](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3) |
| Kaggle rules | [Competition Rules](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/rules) |
| Kaggle data | [Competition Data](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/data) |
| Kaggle notebooks | [Competition Code](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/code) |
| Kaggle leaderboard | [Competition Leaderboard](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/leaderboard) |
| ARC Prize competition page | [ARC-AGI-3 Competition](https://arcprize.org/competitions/2026/arc-agi-3) |
| ARC-AGI-3 benchmark | [Benchmark Overview](https://arcprize.org/arc-agi/3) |
| Official documentation and SDK | [ARC-AGI-3 Documentation](https://docs.arcprize.org/) |
| Scoring methodology | [Relative Human Action Efficiency](https://docs.arcprize.org/methodology) |
| Technical report | [ARC-AGI-3 Technical Report](https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf) |
| Official toolkit | [arcprize/ARC-AGI](https://github.com/arcprize/ARC-AGI) |
| Official agent framework | [arcprize/ARC-AGI-3-Agents](https://github.com/arcprize/ARC-AGI-3-Agents) |
| Official Kaggle starter | [arcprize/ARC-AGI-3-Kaggle-Starter](https://github.com/arcprize/ARC-AGI-3-Kaggle-Starter) |

## Status Snapshot

Verified on **September 13, 2026**:

- The Kaggle account associated with this workspace has accepted the competition rules: `userHasEntered=True`.
- The final submission deadline is **November 2, 2026 at 23:59 UTC**.
- The entry and team merger deadline is **October 26, 2026 at 23:59 UTC**.
- Kaggle reports a total prize pool of **USD 850,000** for the ARC-AGI-3 track.
- The competition is notebook-only and allows at most one submission per team per day.
- This project has not submitted to Kaggle yet.
- The local public-game toolkit, inventory, recording pipeline, visualization pipeline, and random smoke baseline are operational.

Live participation counts, leaderboard scores, rules, and deadlines can change. Always re-check the official Kaggle pages before a submission or prize-eligibility decision.

## Contents

1. [Competition Overview](#competition-overview)
2. [What ARC-AGI-3 Measures](#what-arc-agi-3-measures)
3. [How an Environment Works](#how-an-environment-works)
4. [Dataset and Evaluation Split](#dataset-and-evaluation-split)
5. [Scoring](#scoring)
6. [Prize Structure](#prize-structure)
7. [Competition Timeline](#competition-timeline)
8. [Submission and Team Rules](#submission-and-team-rules)
9. [Knowledge Required](#knowledge-required)
10. [Reference Agent Architecture](#reference-agent-architecture)
11. [Research Strategy](#research-strategy)
12. [Repository Structure](#repository-structure)
13. [Local Setup on Windows](#local-setup-on-windows)
14. [Current Commands](#current-commands)
15. [Experiment Protocol](#experiment-protocol)
16. [Collaboration Workflow](#collaboration-workflow)
17. [Current Baseline](#current-baseline)
18. [Known Risks and Open Questions](#known-risks-and-open-questions)
19. [Glossary](#glossary)

## Competition Overview

ARC-AGI-3 is the first interactive benchmark in the ARC-AGI series. Earlier ARC-AGI benchmarks primarily presented static input-output grid transformations. ARC-AGI-3 places the test taker inside an unfamiliar, turn-based environment and requires learning through interaction.

No natural-language instructions, control descriptions, or explicit goals are provided. An agent must discover:

- which visible structures matter;
- which actions are legal;
- what each action does;
- which state changes represent progress;
- what constitutes failure or success;
- how knowledge transfers from early levels to later levels;
- how to reach the inferred goal efficiently.

The benchmark is intentionally easy enough for humans to learn from first exposure while remaining difficult for current AI systems. Every accepted environment was fully solved by at least two independent human participants during controlled testing. The benchmark therefore targets the gap between human skill acquisition and machine skill acquisition, rather than testing whether a task is solvable in principle.

### Why this is a machine learning problem

The system must map a history of observations and actions to a useful next action:

```text
observation history + action history + inferred rules -> next action
```

This combines several areas that are often studied separately:

- visual representation of a structured grid;
- sequential decision-making;
- active exploration;
- system identification;
- memory and state abstraction;
- goal inference;
- planning and search;
- online adaptation;
- generalization to unseen tasks.

An agent can use hand-written rules, classical search, probabilistic inference, learned models, language models, vision-language models, or a hybrid system. Large-scale model training is optional. A strong research process begins with the simplest method that can test a clearly stated hypothesis.

## What ARC-AGI-3 Measures

The official competition description emphasizes four broad capabilities.

### 1. Exploration

The agent must actively obtain information. An action may serve as an experiment rather than an immediate attempt to win. For example, pressing each available action once from a reset state can reveal control semantics, movement rules, irreversible transitions, or hazards.

Useful concepts include:

- exploration versus exploitation;
- information gain;
- reversible and irreversible actions;
- controlled interventions;
- uncertainty-aware action selection.

### 2. Modeling

The agent must turn raw frames into a model that predicts future states. The model may be symbolic, object-centric, neural, or hybrid.

A useful model should answer questions such as:

- Which cells belong to the same object?
- Which objects are controllable?
- Which features persist across frames?
- What changed after an action?
- Is the environment deterministic?
- Which variables track lives, inventory, progress, or level state?

### 3. Goal Acquisition

The agent is not told what to optimize inside an environment. It must infer desirable states from feedback, visual structure, level transitions, and repeated interactions.

Goal inference can use signals such as:

- a transition to the next level;
- the disappearance or collection of an object;
- changes in counters or status regions;
- terminal states such as `WIN` or `GAME_OVER`;
- consistent structural patterns across levels.

### 4. Planning and Execution

After inferring a goal and transition rules, the agent must choose an efficient action sequence. It must also revise the plan when observations contradict its current model.

Planning quality matters because the score rewards both completion and action efficiency.

## How an Environment Works

### Core interaction loop

```text
Reset environment
       |
       v
Receive frame and available actions
       |
       v
Parse objects, changes, and status
       |
       v
Update beliefs, memory, and candidate goals
       |
       v
Select and validate one action
       |
       v
Execute action and receive next frame
       |
       +---- repeat until WIN, GAME_OVER, or budget exhaustion
```

### Frames

The agent receives JSON-compatible frame objects containing the current grid and metadata.

- Maximum grid size: `64 x 64`.
- Cell values: integers from `0` through `15`.
- Coordinate origin: `(0, 0)` at the top-left corner.
- Environments may expose multiple levels of increasing difficulty.
- Common active and terminal states include `NOT_FINISHED`, `WIN`, and `GAME_OVER`.

The integer values behave like colors or symbolic states. Their meaning is environment-specific. A color may represent a wall in one environment and a movable object in another.

### Actions

An environment exposes a subset of the following action interface:

| Action | General interface |
| --- | --- |
| `RESET` | Start or restart an environment. |
| `ACTION1` to `ACTION5` | Simple actions. They may represent movement, interaction, rotation, or another environment-specific operation. |
| `ACTION6` | A complex action that accepts `(x, y)` coordinates. It is commonly used for click-like interaction. |
| `ACTION7` | An additional simple action when required by an environment. |

Action names do not reveal semantics. `ACTION1` cannot be assumed to mean the same thing across games. The agent must infer action meaning from observed transitions.

### Levels

Each game contains sequential levels. Later levels are normally harder and receive greater weight in the game score. Earlier levels can reveal reusable mechanics, but the agent must avoid overfitting to one level layout.

### What counts as an action

An action is a discrete interaction submitted to the environment. Internal computation, reasoning, parsing, search, tool calls, and retries that do not alter the environment do not count as environment actions. They still consume notebook runtime and compute resources.

## Dataset and Evaluation Split

The competition package contains three major components:

| Component | Purpose |
| --- | --- |
| `ARC-AGI-3-Agents/` | Local copy of the official agent framework and templates. |
| `arc_agi_3_wheels/` | Python package wheels used by the competition environment. |
| `environment_files/` | Python implementations and metadata for the 25 public environments. |

The benchmark split is:

| Split | Environments | Visibility | Purpose |
| --- | ---: | --- | --- |
| Public demonstration set | 25 | Public | Learn the interface, build tools, and demonstrate methods. |
| Semi-private evaluation set | 55 | Hidden | Used for the Kaggle Public Leaderboard portion. |
| Fully private evaluation set | 55 | Hidden | Used for final ranking on the Private Leaderboard. |
| Total hidden competition set | 110 | Hidden | Measures generalization beyond the public demonstrations. |

The public environments are intentionally easier and do not comprehensively represent private mechanics. Public-game success is useful for debugging and controlled research, but it is not a reliable estimate of hidden-game performance.

This distribution shift is central to the benchmark. A system that contains game-specific solutions can obtain impressive public results while learning little that transfers to unseen environments.

## Scoring

ARC-AGI-3 evaluates both **completion** and **efficiency**. The metric is called **Relative Human Action Efficiency**, abbreviated RHAE.

### Human baseline

Human baselines were collected from first-time players under controlled conditions. For each level, completed runs are ordered from fewest to most actions. An odd number of runs uses the middle entry; an even number uses the slower of the two middle entries. For example, both four and five completed runs use the third-ranked run. This upper-median rule represents proficient human play without letting a lucky speed-run determine the baseline.

Let:

- `H_l` be the human baseline action count for level `l`;
- `A_l` be the agent action count used to complete level `l`;
- `S_l` be the score for level `l`.

### Per-level score

The Kaggle competition data page currently describes the competition calculation as:

```text
efficiency_l = min(H_l / A_l, 1.0)
S_l = efficiency_l^2
```

An uncompleted level receives a score of zero.

Examples:

| Human actions | Agent actions | Efficiency ratio | Level score |
| ---: | ---: | ---: | ---: |
| 10 | 10 | 1.00 | 100% |
| 10 | 20 | 0.50 | 25% |
| 10 | 40 | 0.25 | 6.25% |
| 10 | 100 | 0.10 | 1% |

Squaring strongly penalizes inefficient exploration. Doubling the human action count produces 25%, rather than 50%, for that level.

### Per-game score

Levels are weighted by their one-indexed level number:

```text
weight_l = l
game_score = sum(weight_l * S_l) / sum(weight_l)
```

Uncompleted levels contribute zero. Later levels carry more weight, so completing only tutorial levels cannot produce a high game score.

### Total score

The final benchmark score is the arithmetic mean of the individual game scores across the evaluation set. The competition reports scores from 0% to 100%.

### Scoring-source discrepancy to monitor

The general ARC-AGI-3 methodology documentation currently discusses an up-to-`1.15` per-level cap for performance faster than the human baseline, while the Kaggle data page states a `1.0` cap before squaring. This repository treats the live Kaggle competition definition as operational for local competition checks. The rule must be re-verified before final submission, and local scoring utilities should be updated if Kaggle changes or clarifies the implementation.

## Prize Structure

Kaggle currently lists **USD 850,000** in total ARC-AGI-3 prizes.

### Progress prizes: USD 150,000

#### Final Leaderboard prizes: USD 75,000

| Final position | Prize |
| ---: | ---: |
| 1st | USD 40,000 |
| 2nd | USD 15,000 |
| 3rd | USD 10,000 |
| 4th | USD 5,000 |
| 5th | USD 5,000 |

#### Milestone prizes: USD 75,000

Each milestone distributes USD 37,500:

| Milestone position | Milestone 1 | Milestone 2 |
| ---: | ---: | ---: |
| 1st | USD 25,000 | USD 25,000 |
| 2nd | USD 7,500 | USD 7,500 |
| 3rd | USD 5,000 | USD 5,000 |

- Milestone 1 deadline: June 30, 2026 at 23:59 UTC.
- Milestone 2 deadline: September 30, 2026 at 23:59 UTC.
- A milestone notebook must be public under an eligible open-source license by the corresponding deadline.

The ARC Prize website has displayed a different second/third-place split in some revisions while preserving the same milestone total. The live Kaggle Prizes page is treated as the controlling operational source and should be checked again before a milestone submission.

### Bonus prize: USD 700,000

The bonus pool is unlocked if a team achieves a score of 100% on the competition leaderboard. Kaggle currently lists the following distribution among qualifying top teams:

| Position | Bonus prize |
| ---: | ---: |
| 1st | USD 350,000 |
| 2nd | USD 175,000 |
| 3rd | USD 70,000 |
| 4th | USD 70,000 |
| 5th | USD 35,000 |

Prize eligibility is subject to the official rules, identity and jurisdiction checks, reproducibility review, licensing obligations, and sponsor verification. Taxes are the responsibility of prize recipients.

## Competition Timeline

All deadlines below are listed by Kaggle at `23:59 UTC` on the corresponding date.

| Date | Event | Status as of 2026-09-13 |
| --- | --- | --- |
| March 25, 2026 | Competition start | Completed |
| June 30, 2026 | Optional Milestone 1 deadline | Completed |
| September 30, 2026 | Optional Milestone 2 deadline | Upcoming |
| October 26, 2026 | Entry deadline | Upcoming |
| October 26, 2026 | Team merger deadline | Upcoming |
| November 2, 2026 | Final submission deadline | Upcoming |
| December 4, 2026 | Winners announcement | Scheduled |

The organizers reserve the right to update the timeline. Check Kaggle before relying on a deadline.

## Submission and Team Rules

This section summarizes operational rules verified from the Kaggle competition pages. The full rules remain authoritative.

### Notebook submission requirements

- Submissions must be generated through Kaggle Notebooks.
- CPU notebook runtime must be no more than 9 hours.
- GPU notebook runtime must be no more than 9 hours.
- Internet access must be disabled during evaluation.
- Freely and publicly available external data is allowed.
- Publicly available pretrained models are allowed, subject to licensing and accessibility requirements.
- The competition submission artifact is generated automatically if the agent takes an action on any game.
- A team may submit at most one entry per day.
- A team may select at most two final submissions for judging.

### Team requirements

- Maximum team size: 8 people.
- Each person must use a separate Kaggle account.
- Each person must accept the competition rules before joining the team.
- A participant may join or form only one team in this competition.
- Team membership becomes official only after the invitation is accepted through Kaggle.
- Team mergers must be completed by October 26, 2026 at 23:59 UTC.
- A merge can be rejected if the combined submission history exceeds the permitted team submission count.
- Private sharing of competition code or competition data outside the official Kaggle team is prohibited.

Repository collaborator access should therefore be limited to people who have accepted the Kaggle rules and officially joined the same Kaggle team.

### Prize sharing

Kaggle's general rules state that a monetary team prize is divided equally among eligible team members unless all members unanimously choose another split and notify Kaggle before payment.

### Open-source and licensing obligations

- The repository may remain private during development.
- Prize-eligible milestone notebooks must be made public by the corresponding milestone deadline.
- Winning submissions and source code are subject to the competition's open-source requirements.
- The competition lists `CC-BY 4.0` as the winner license type.
- The competition data is listed under `Apache 2.0` access and use terms.
- Winners may be required to deliver training code, inference code, environment details, model information, and documentation sufficient to reproduce the result.
- Model, weight, data, and third-party software licenses must be reviewed before public release.

This repository does not currently declare a project-wide license. A compliant release license and third-party dependency audit must be completed before any public, milestone, or prize-eligible release.

## Knowledge Required

The project is suitable for incremental study. A new contributor does not need to master every topic before beginning.

### Level 1: Programming and data foundations

| Topic | Why it matters | Initial exercise |
| --- | --- | --- |
| Python functions, classes, and modules | The toolkit, engine, environments, and agents are implemented in Python. | Read `src/run_random_smoke.py` and identify setup, loop, and output stages. |
| Lists, dictionaries, and dataclasses | Frames, metadata, actions, and scorecards are structured objects. | Print one frame and label each field. |
| NumPy arrays | Grids and frame differences are naturally represented as arrays. | Count changed cells between two frames. |
| JSON and JSONL | Scorecards and recordings use structured serialized data. | Load a recording and inspect one step. |
| CSV | Public-game inventory and experiment summaries can be tabulated. | Sort games by level count or baseline actions. |
| Git and GitHub | Reproducible collaboration requires versioned code and reviewable changes. | Create a branch and make a documentation-only commit. |
| Virtual environments | Dependency isolation prevents machine-wide package conflicts. | Recreate `.venv` from the documented versions. |

### Level 2: Core machine learning concepts

| Topic | ARC-AGI-3 interpretation |
| --- | --- |
| State | The information required to predict future environment behavior. It may be larger or smaller than the visible frame. |
| Observation | The frame and metadata currently available to the agent. |
| Action | One environment interaction selected from the available action set. |
| Policy | A rule or model that maps interaction history to the next action. |
| Trajectory | The ordered sequence of observations, actions, and resulting states. |
| Reward or feedback | Progress indicators such as level completion, terminal state, or scorecard change. Feedback is sparse. |
| Exploration | Actions selected to learn controls, dynamics, hazards, or goals. |
| Exploitation | Actions selected to execute the best current plan. |
| Generalization | Applying a learning process to hidden environments with unfamiliar mechanics. |
| Overfitting | Building behavior that succeeds on public games but fails on hidden games. |

ARC-AGI-3 has a reinforcement-learning-style interaction loop, but reinforcement-learning training is not required. A deterministic search policy or symbolic model is still a valid agent.

### Level 3: Perception and representation

Relevant techniques include:

- connected-component analysis;
- color and shape statistics;
- object segmentation;
- bounding boxes and centroids;
- frame differencing;
- motion and controllability detection;
- persistent object tracking;
- coordinate transforms;
- object-centric state representations;
- scene graphs and relational representations.

The benchmark uses symbolic grids, so a small amount of structured vision can often provide more interpretable information than a large generic image encoder.

### Level 4: Search and planning

Relevant algorithms include:

- breadth-first search;
- depth-first search;
- iterative deepening;
- uniform-cost search;
- A* search;
- beam search;
- Monte Carlo Tree Search;
- model-predictive control;
- novelty search;
- state hashing and duplicate-state detection;
- reversible-action analysis.

Search requires a state representation, a transition model, candidate goals, and a budget. Blind search can waste actions and notebook runtime. Learned or inferred structure should reduce the search space.

### Level 5: Rule induction and world modeling

The agent must infer compact explanations from few interactions. Relevant ideas include:

- system identification;
- causal intervention;
- hypothesis generation and elimination;
- finite-state machines;
- program synthesis;
- Bayesian belief updating;
- latent-state models;
- transition prediction;
- test-time adaptation;
- hierarchical skills and reusable options.

### Level 6: Memory and context management

Saving every raw `64 x 64` frame indefinitely is expensive for model-based agents. A practical memory system may store:

- action-to-effect summaries;
- discovered objects and their properties;
- candidate goals and confidence values;
- failure states and forbidden transitions;
- compressed frame differences;
- level-specific facts;
- cross-level rules;
- unresolved questions.

Memory should preserve decision-relevant evidence while discarding redundant pixels and repeated observations.

### Level 7: Optional learned-model methods

Later experiments may evaluate:

- vision-language models for frame interpretation;
- language models for hypothesis generation and planning;
- small learned transition models;
- imitation learning from permitted human trajectories;
- test-time fine-tuning;
- ensembles or proposal-ranking systems;
- code-generating agents that build task-specific analysis tools during evaluation.

Any model used in a Kaggle notebook must fit the offline runtime, memory, licensing, and reproducibility constraints. Model scale alone is not an experimental hypothesis.

## Reference Agent Architecture

A modular agent can be organized as follows:

```text
ARC environment
    |
    v
Frame parser and object extractor
    |
    v
Frame-change and controllability analyzer
    |
    v
Belief state and compressed memory
    |
    +----------------------+
    |                      |
    v                      v
Goal inference       Transition model
    |                      |
    +----------+-----------+
               |
               v
        Planner or search policy
               |
               v
       Legal-action validator
               |
               v
          Selected action
               |
               v
      Recorder and local evaluator
```

### Module responsibilities

| Module | Responsibility | Evidence to record |
| --- | --- | --- |
| Frame parser | Convert grids into objects, regions, and features. | Parsed objects and masks. |
| Change analyzer | Compare before/after frames and attribute changes to actions. | Changed cells, bounding boxes, and candidate causes. |
| Belief state | Track uncertain rules and persistent variables. | Hypotheses with confidence and supporting transitions. |
| Goal inference | Rank candidate success conditions. | Goal candidates and progress signals. |
| Transition model | Predict likely next states for actions. | Predicted versus observed transitions. |
| Planner | Choose informative or goal-directed action sequences. | Candidate plans, cost, and selection rationale. |
| Action validator | Restrict actions to the current legal set and valid parameters. | Rejected invalid proposals. |
| Recorder | Save full trajectories and summaries. | JSONL recordings and scorecards. |
| Evaluator | Compute comparable experiment metrics. | Completion, action efficiency, runtime, and failure counts. |

The first implementation does not need every module. The architecture is a map for isolating hypotheses and failures, not a requirement to build a large framework immediately.

## Research Strategy

### Phase 0: Infrastructure and reproducibility

Current status: operational.

Deliverables:

- local Python 3.12 environment;
- official public environments;
- game inventory;
- scorecard extraction;
- trajectory recording;
- frame visualization;
- deterministic random baseline.

Exit criterion: the same seed produces the same action sequence and equivalent scorecard behavior from a clean environment.

### Phase 1: Deterministic action probing

Goal: discover action semantics and immediate transition structure without model training.

Experiments:

- reset to the same initial state;
- execute each available action independently;
- compare changed cells and metadata;
- test repeated actions;
- test inverse-action pairs;
- detect no-op, movement, click, hazard, and irreversible behavior;
- record hypotheses and counterexamples.

Exit criterion: produce a machine-readable action-effect report for at least one public game.

### Phase 2: Object-centric state representation

Goal: replace raw-frame reasoning with compact entities and relations.

Experiments:

- connected components by color;
- object persistence across frames;
- controllable-object detection;
- static versus dynamic region classification;
- counters, borders, and status-panel detection.

Exit criterion: the representation explains observed frame changes with fewer variables than the raw grid.

### Phase 3: Transition and goal inference

Goal: construct testable models of environment dynamics and progress.

Experiments:

- deterministic transition tables;
- finite-state-machine induction;
- candidate goal ranking;
- confidence updates after contradictory observations;
- separation of level-specific and cross-level rules.

Exit criterion: predict held-out transitions within a public game and identify at least one verified progress condition.

### Phase 4: Search-based policy

Goal: use the inferred model to plan efficiently.

Experiments:

- breadth-first or A* search over compact states;
- duplicate-state pruning;
- action-cost penalties;
- exploration bonuses for novel states;
- short-horizon replanning after every observation.

Exit criterion: complete at least one public level reproducibly and improve action count over an uninformed baseline.

### Phase 5: Generalization experiments

Goal: determine which components transfer across games.

Experiments:

- leave-one-game-out evaluation;
- freeze the policy before testing a held-out public game;
- compare game-specific and generic features;
- perform ablations on memory, perception, planning, and prompting;
- track variance across seeds and environments.

Exit criterion: demonstrate improvement on held-out public games without adding game-specific rules after inspection.

### Phase 6: Optional model-assisted agent

Goal: test whether a local offline model adds measurable value over structured baselines.

Requirements before adoption:

- a defined role for the model;
- a smaller non-model baseline;
- fixed prompts and decoding settings;
- legal-action validation;
- runtime and memory measurements;
- ablation evidence;
- compatible model and weight licenses;
- Kaggle notebook compatibility.

### Phase 7: Kaggle submission pipeline

Goal: produce a valid offline notebook submission without hidden network dependencies.

Checklist:

- attach all required packages, models, and assets;
- disable Internet access;
- run the notebook from a clean Kaggle session;
- stay within the 9-hour limit;
- verify that the agent acts on at least one game;
- inspect generated outputs and logs;
- record notebook version, code commit, dependencies, runtime, and leaderboard result;
- obtain explicit approval before consuming the daily submission slot.

## Repository Structure

```text
arc-prize-2026-arc-agi-3/
|-- README.md
|-- README.zh-CN.md
|-- requirements-local.txt
|-- data/
|   |-- raw/                 # Kaggle archive and extracted official files; ignored
|   `-- working/             # Derived local indexes; ignored
|-- docs/
|   |-- competition_check.md
|   |-- experiment_log.md
|   `-- public_games_inventory.md
|-- notebooks/               # Future Kaggle submission notebooks
|-- outputs/
|   |-- figures/             # Local visualizations; ignored
|   `-- runs/
|       |-- recordings/      # Full local trajectories; ignored
|       `-- random_smoke_ls20_seed0.json
`-- src/
    |-- inspect_public_games.py
    |-- render_recording.py
    |-- run_random_smoke.py
    `-- score_utils.py
```

### Script responsibilities

| Script | Purpose |
| --- | --- |
| `src/inspect_public_games.py` | Read public environment metadata and produce a game inventory. |
| `src/run_random_smoke.py` | Verify environment loading, action execution, recording, and scorecard generation. |
| `src/render_recording.py` | Render a selected frame from a JSONL recording into an HTML visualization. |
| `src/score_utils.py` | Provide a small local implementation of the currently documented competition-style score. |

## Local Setup on Windows

The verified local configuration uses:

- Windows and PowerShell;
- Python `3.12.13`;
- `arc-agi==0.9.8` from the competition package;
- `arcengine==0.9.3` from the competition package.

The current Kaggle archive was downloaded again and hash-checked on September 13, 2026. It is byte-for-byte identical to the local archive and still bundles `arc-agi==0.9.8` and `arcengine==0.9.3`. PyPI offers `arc-agi==0.9.9`, whose official changelog only adds the HTTP response body to remote-action error logs. This project intentionally remains on `0.9.8` to match the Kaggle package. Re-run the package audit before changing this pin.

`requirements-local.txt` also pins the direct runtime dependencies to the versions included in the verified competition archive. This prevents a clean installation from silently drifting to newer NumPy, Matplotlib, Pydantic, or HTTP-library versions.

Always run project commands through `.\.venv\Scripts\python.exe`. A bare `python` command may resolve to a global Python installation that this project has not verified.

### 1. Clone the private repository

```powershell
git clone https://github.com/hanxiangli666/arc-prize-2026-arc-agi-3.git
Set-Location arc-prize-2026-arc-agi-3
```

Repository access does not grant competition access. Each contributor must separately join the Kaggle competition and accept its rules.

### 2. Download the competition package

Install and authenticate the Kaggle CLI, then run:

```powershell
New-Item -ItemType Directory -Path data\raw -Force
kaggle competitions download -c arc-prize-2026-arc-agi-3 -p data\raw
Expand-Archive -LiteralPath data\raw\arc-prize-2026-arc-agi-3.zip -DestinationPath data\raw\extracted -Force
```

Do not commit Kaggle credentials, `.env` files, downloaded archives, or extracted competition data.

### 3. Create the Python environment

With `uv` and Python 3.12 installed:

```powershell
uv venv .venv --python 3.12
.\.venv\Scripts\python.exe -m ensurepip --upgrade
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

Install general dependencies and the competition-bundled toolkit wheels:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-local.txt
.\.venv\Scripts\python.exe -m pip install --force-reinstall --no-deps .\data\raw\extracted\arc_agi_3_wheels\arcengine-0.9.3-py3-none-any.whl .\data\raw\extracted\arc_agi_3_wheels\arc_agi-0.9.8-py3-none-any.whl
```

### 4. Verify imports

```powershell
.\.venv\Scripts\python.exe -c "from importlib.metadata import version; import arc_agi, arcengine; print('arc-agi', version('arc-agi'), arc_agi.__file__); print('arcengine', version('arcengine'), arcengine.__file__)"
```

Use distribution metadata for version checks. The official `arcengine==0.9.3` wheel currently retains an outdated internal `arcengine.__version__` value of `0.1.0`.

### 5. Verify the project scripts

```powershell
.\.venv\Scripts\python.exe -m py_compile src\score_utils.py src\inspect_public_games.py src\run_random_smoke.py src\render_recording.py
```

## Current Commands

### Build the public-game inventory

```powershell
.\.venv\Scripts\python.exe src\inspect_public_games.py
```

Expected high-level inventory for the current package:

- 25 public games;
- 183 public levels;
- 17,135 total human baseline actions across public levels.

### Run the deterministic random smoke baseline

```powershell
.\.venv\Scripts\python.exe src\run_random_smoke.py --game ls20 --steps 20 --seed 0 --out outputs\runs\random_smoke_ls20_seed0.json
```

This command tests connectivity and reproducibility. It is not intended to be a competitive policy.

### Render a recording frame

```powershell
.\.venv\Scripts\python.exe src\render_recording.py --recording <recording.jsonl> --frame-index 0 --out outputs\figures\frame0.html
```

## Experiment Protocol

Every experiment should be traceable to a hypothesis and a saved result.

### Required experiment record

```text
Experiment ID:
Date:
Code commit:
Research question:
Hypothesis:
Environment set:
Seeds:
Policy/configuration:
Action budget:
Runtime budget:
Metrics:
Result:
Failure cases:
Interpretation:
Next experiment:
Artifacts:
```

### Minimum metrics

- games attempted;
- levels completed;
- total and per-level actions;
- resets;
- invalid or failed actions;
- per-game and aggregate score;
- wall-clock runtime;
- peak memory when relevant;
- random seed;
- model name and decoding parameters when relevant;
- recording and scorecard paths.

### Evaluation discipline

- Separate local public-game results from Kaggle leaderboard results.
- Never report a public-game score as evidence of hidden-game generalization.
- Compare methods under the same games, seeds, budgets, and package versions.
- Preserve negative results and failure examples.
- Use ablations to identify which component caused an improvement.
- Repeat stochastic experiments.
- Record changes in environment, model, prompt, package, and hardware versions.
- Prefer held-out public games when testing generalization hypotheses.
- Avoid tuning repeatedly against Kaggle Public Leaderboard feedback.

## Collaboration Workflow

### Git workflow

1. Pull the latest `main` before starting work.
2. Create a focused branch such as `experiment/action-probing` or `docs/scoring-notes`.
3. Keep each commit limited to one logical change.
4. Include the experiment ID or issue number in the commit or pull request when relevant.
5. Open a pull request for review before merging substantial algorithm changes.
6. Require reproducibility commands and result artifacts in the pull request description.
7. Merge only after focused validation passes.

### Suggested division of research work

| Workstream | Typical outputs |
| --- | --- |
| Benchmark study | Rule summaries, source links, scoring checks, and open questions. |
| Environment analysis | Object annotations, action maps, transition hypotheses, and failure cases. |
| Agent engineering | Policies, planners, memory systems, action validation, and runtime controls. |
| Evaluation | Reproducible runs, ablations, metrics tables, and regression checks. |
| Kaggle packaging | Offline notebook, attached dependencies, runtime audit, and submission record. |

### Data and access discipline

- Keep secrets in ignored environment files.
- Keep downloaded competition data out of Git.
- Give private repository access only to authorized official team members.
- Do not privately share competition code or data across separate Kaggle teams.
- Review notebook visibility and licenses before any public release.

## Current Baseline

### Public data inventory

- Public environments: `25`.
- Public levels: `183`.
- Total public human baseline actions: `17,135`.

The detailed inventory is stored in [`docs/public_games_inventory.md`](docs/public_games_inventory.md).

### Random smoke result

Verified configuration:

- requested game: `ls20`;
- resolved environment: `ls20-9607627b`;
- seed: `0`;
- requested actions: `20`;
- initial frame shape: `[1, 64, 64]`;
- levels completed: `0 / 7`;
- total actions: `20`;
- score: `0.0`.

The tracked summary is stored in [`outputs/runs/random_smoke_ls20_seed0.json`](outputs/runs/random_smoke_ls20_seed0.json).

Interpretation: the environment, action loop, recording, and scoring pipeline work. Random action selection did not solve a level and provides no evidence of intelligent behavior.

## Known Risks and Open Questions

### Benchmark risks

- Public demonstrations are easier and out-of-distribution relative to private evaluation games.
- Game-specific heuristics can create misleading public success.
- Sparse feedback makes goal discovery difficult.
- Long trajectories create memory and context pressure.
- Inefficient exploration is heavily penalized by the squared action-efficiency score.
- Irreversible actions can destroy information or force resets.

### Engineering risks

- Local package versions can drift from Kaggle-bundled versions.
- A locally working agent may fail in an offline Kaggle notebook because of missing assets.
- Long model inference can exceed the 9-hour runtime limit.
- Raw frame histories can exceed model context or memory limits.
- Non-deterministic experiments can hide regressions.
- The current repository has no automated test suite beyond compilation and smoke checks.

### Research questions

- How can an agent distinguish controllable objects from environmental motion with minimal actions?
- Which compact state representation transfers best across unseen games?
- How should the agent value information when every exploratory action reduces efficiency?
- How can candidate goals be ranked before any level is completed?
- Which search strategy performs best under irreversible transitions and sparse feedback?
- How much memory is necessary, and what information can be safely compressed?
- Can a small model improve hypothesis generation without dominating runtime?
- Which improvements survive leave-one-game-out evaluation?
- Which scoring cap is implemented in the final Kaggle evaluator if the published sources remain inconsistent?

## Glossary

| Term | Meaning in this project |
| --- | --- |
| Action | A discrete command submitted to an environment. |
| Action budget | Maximum number of environment interactions allowed or planned. |
| Agent | The complete system that observes, reasons, remembers, plans, and acts. |
| Belief state | The agent's current uncertain model of hidden rules and state. |
| Environment | One interactive ARC-AGI-3 game. |
| Frame | A grid observation and associated metadata returned by the environment. |
| Generalization | Successful adaptation to environments not seen during development. |
| Goal acquisition | Inferring which future state represents success or progress. |
| Harness | The surrounding system that connects a model or policy to observations, memory, tools, and actions. |
| Level | One sequential stage within an environment. |
| Observation | Information available to the agent at a particular step. |
| Policy | The mechanism that selects the next action from the current history or state. |
| RHAE | Relative Human Action Efficiency, the benchmark scoring framework. |
| Scorecard | Structured record of actions, completed levels, and scores. |
| Trajectory | Ordered history of observations, actions, and outcomes. |
| Transition model | A model that predicts the next state after an action. |
| World model | A compact representation of objects, rules, dynamics, and likely outcomes. |

## Project Principles

1. Ground every conclusion in real frames, trajectories, scorecards, or leaderboard evidence.
2. Begin with interpretable and reproducible experiments.
3. Preserve failures because they constrain future hypotheses.
4. Separate environment connectivity from agent competence.
5. Separate public-game performance from hidden-game generalization.
6. Add complexity only after a smaller baseline exposes a specific limitation.
7. Treat Kaggle submissions as scarce experiments with recorded provenance.
8. Re-check official rules before decisions involving submission, publication, licensing, or prizes.
