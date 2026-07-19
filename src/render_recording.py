from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "outputs" / "figures" / "recording_frame.html"
PALETTE = {
    0: "#111827",
    1: "#f9fafb",
    2: "#ef4444",
    3: "#22c55e",
    4: "#3b82f6",
    5: "#f59e0b",
    6: "#8b5cf6",
    7: "#14b8a6",
    8: "#ec4899",
    9: "#facc15",
    10: "#6b7280",
    11: "#84cc16",
    12: "#06b6d4",
    13: "#fb7185",
    14: "#a855f7",
    15: "#e5e7eb",
}


def load_recording(path: Path) -> list[dict[str, Any]]:
    frames: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                frames.append(json.loads(line))
    return frames


def render_grid(grid: list[list[int]]) -> str:
    rows: list[str] = []
    for row in grid:
        cells = []
        for value in row:
            color = PALETTE.get(int(value), "#ffffff")
            cells.append(
                f'<span class="cell" title="{int(value)}" style="background:{color}"></span>'
            )
        rows.append('<div class="row">' + "".join(cells) + "</div>")
    return "\n".join(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--recording", type=Path, required=True)
    parser.add_argument("--frame-index", type=int, default=0)
    parser.add_argument("--layer", type=int, default=0)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    frames = load_recording(args.recording)
    if not frames:
        raise SystemExit(f"No frames found in {args.recording}")
    if args.frame_index < 0 or args.frame_index >= len(frames):
        raise SystemExit(f"frame-index must be between 0 and {len(frames) - 1}")

    payload = frames[args.frame_index]["data"]
    grid = payload["frame"][args.layer]
    action = payload.get("action_input") or {}
    title = f"{payload.get('game_id')} frame {args.frame_index}"
    meta = {
        "state": payload.get("state"),
        "levels_completed": payload.get("levels_completed"),
        "action": action.get("id"),
        "available_actions": payload.get("available_actions"),
        "recording": str(args.recording),
    }
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 24px; background: #f8fafc; color: #111827; }}
.meta {{ margin-bottom: 16px; font-size: 14px; line-height: 1.5; }}
.grid {{ display: inline-block; border: 1px solid #111827; background: #111827; }}
.row {{ display: flex; }}
.cell {{ width: 10px; height: 10px; display: block; }}
pre {{ background: #e5e7eb; padding: 12px; overflow: auto; }}
</style>
</head>
<body>
<h1>{html.escape(title)}</h1>
<pre>{html.escape(json.dumps(meta, indent=2))}</pre>
<div class="grid">
{render_grid(grid)}
</div>
</body>
</html>
"""
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(doc, encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
