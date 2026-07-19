from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_DIR = ROOT / "data" / "raw" / "extracted" / "environment_files"
DEFAULT_CSV = ROOT / "data" / "working" / "public_games_summary.csv"
DEFAULT_MD = ROOT / "docs" / "public_games_inventory.md"


def load_rows(env_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for metadata_path in sorted(env_dir.rglob("metadata.json")):
        data = json.loads(metadata_path.read_text(encoding="utf-8"))
        baseline = data.get("baseline_actions") or []
        rows.append(
            {
                "game_id": data.get("game_id", ""),
                "title": data.get("title", ""),
                "default_fps": data.get("default_fps", ""),
                "tags": ",".join(data.get("tags") or []),
                "levels": len(baseline),
                "baseline_total_actions": sum(baseline),
                "baseline_min_actions": min(baseline) if baseline else "",
                "baseline_max_actions": max(baseline) if baseline else "",
                "baseline_mean_actions": round(statistics.mean(baseline), 2)
                if baseline
                else "",
                "local_dir": data.get("local_dir", ""),
                "metadata_path": str(metadata_path.relative_to(ROOT)),
            }
        )
    return rows


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "game_id",
        "title",
        "default_fps",
        "tags",
        "levels",
        "baseline_total_actions",
        "baseline_min_actions",
        "baseline_max_actions",
        "baseline_mean_actions",
        "local_dir",
        "metadata_path",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    total_levels = sum(int(row["levels"]) for row in rows)
    total_baseline = sum(int(row["baseline_total_actions"]) for row in rows)
    lines = [
        "# Public Games Inventory",
        "",
        f"- public games: {len(rows)}",
        f"- total levels: {total_levels}",
        f"- total human baseline actions: {total_baseline}",
        "",
        "| game_id | levels | baseline_total | fps | tags |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| {game_id} | {levels} | {baseline_total_actions} | {default_fps} | {tags} |".format(
                **row
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-dir", type=Path, default=DEFAULT_ENV_DIR)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--md", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    rows = load_rows(args.env_dir)
    if not rows:
        raise SystemExit(f"No metadata.json files found under {args.env_dir}")
    write_csv(rows, args.csv)
    write_markdown(rows, args.md)
    print(f"wrote {len(rows)} games to {args.csv}")
    print(f"wrote inventory markdown to {args.md}")


if __name__ == "__main__":
    main()
