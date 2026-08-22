from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class GameScore:
    score_percent: float
    levels_completed: int
    total_levels: int
    level_scores: list[float]


def score_level(
    human_actions: int,
    agent_actions: int,
    completed: bool,
    cap: float = 100.0,
) -> float:
    if not completed or human_actions <= 0 or agent_actions <= 0:
        return 0.0
    return min((human_actions / agent_actions) ** 2 * 100.0, cap)


def score_game(
    baseline_actions: Iterable[int],
    agent_actions_by_level: Iterable[int],
    levels_completed: int,
) -> GameScore:
    baseline = list(baseline_actions)
    actions = list(agent_actions_by_level)
    if len(actions) < len(baseline):
        actions.extend([0] * (len(baseline) - len(actions)))

    level_scores: list[float] = []
    weighted_sum = 0.0
    weight_sum = 0
    for idx, human_actions in enumerate(baseline, start=1):
        completed = idx <= levels_completed
        level_score = score_level(human_actions, actions[idx - 1], completed)
        level_scores.append(level_score)
        weighted_sum += level_score * idx
        weight_sum += idx

    score_percent = weighted_sum / weight_sum if weight_sum else 0.0
    return GameScore(
        score_percent=score_percent,
        levels_completed=levels_completed,
        total_levels=len(baseline),
        level_scores=level_scores,
    )
