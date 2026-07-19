from __future__ import annotations

import argparse
import json
import os
import random
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_DIR = ROOT / "data" / "raw" / "extracted" / "environment_files"
DEFAULT_RECORDINGS_DIR = ROOT / "outputs" / "runs" / "recordings"
DEFAULT_OUT = ROOT / "outputs" / "runs" / "random_smoke_summary.json"


def frame_shape(frame: Any) -> list[int]:
    if not frame:
        return [0, 0, 0]
    layers = len(frame)
    rows = len(frame[0]) if layers else 0
    cols = len(frame[0][0]) if rows else 0
    return [layers, rows, cols]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--game", default="ls20")
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--env-dir", type=Path, default=DEFAULT_ENV_DIR)
    parser.add_argument("--recordings-dir", type=Path, default=DEFAULT_RECORDINGS_DIR)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    os.environ["OPERATION_MODE"] = "offline"
    os.environ["ENVIRONMENTS_DIR"] = str(args.env_dir.resolve())
    os.environ["RECORDINGS_DIR"] = str(args.recordings_dir.resolve())

    from arc_agi import Arcade, OperationMode
    from arcengine import GameAction, GameState

    rng = random.Random(args.seed)
    arcade = Arcade(
        operation_mode=OperationMode.OFFLINE,
        environments_dir=str(args.env_dir.resolve()),
        recordings_dir=str(args.recordings_dir.resolve()),
    )
    card_id = arcade.open_scorecard(tags=["local-smoke", "random"])
    wrapper = arcade.make(
        args.game,
        scorecard_id=card_id,
        seed=args.seed,
        save_recording=True,
    )
    if wrapper is None:
        raise SystemExit(f"Could not create wrapper for {args.game}")

    actions_taken: list[dict[str, Any]] = []
    for step in range(args.steps):
        latest = wrapper.observation_space
        if latest.state == GameState.WIN:
            break

        available = [
            GameAction.from_id(action) if isinstance(action, int) else action
            for action in latest.available_actions
        ]
        if latest.state in (GameState.NOT_PLAYED, GameState.GAME_OVER):
            action = GameAction.RESET
        else:
            playable = [action for action in available if action != GameAction.RESET]
            action = rng.choice(playable or [GameAction.RESET])

        data = {"x": 0, "y": 0} if action.is_complex() else {}
        frame = wrapper.step(
            action,
            data=data,
            reasoning={"policy": "local_random_smoke", "step": step},
        )
        if frame is None:
            actions_taken.append({"step": step, "action": action.name, "failed": True})
            break
        actions_taken.append(
            {
                "step": step,
                "action": action.name,
                "state": frame.state.name,
                "levels_completed": frame.levels_completed,
            }
        )

    scorecard = arcade.close_scorecard(card_id)
    summary = {
        "game_requested": args.game,
        "game_id": wrapper.environment_info.game_id,
        "seed": args.seed,
        "steps_requested": args.steps,
        "initial_shape": frame_shape(wrapper.observation_space.frame),
        "actions_taken": actions_taken,
        "scorecard": scorecard.model_dump() if scorecard else None,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
