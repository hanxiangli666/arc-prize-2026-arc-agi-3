# ARC Prize 2026 ARC-AGI-3

本目录是 `arc-prize-2026-arc-agi-3` 的长期工作区。当前原则是先理解环境、数据格式和评价方式，再做可解释的小实验；不先训练大模型，不把不可复现的猜测写成结论。

## 当前状态

- Kaggle CLI 已核实账号已报名：`userHasEntered=True`。
- 原始比赛包已下载到 `data/raw/arc-prize-2026-arc-agi-3.zip`，并解压到 `data/raw/extracted/`。
- 本地 Python 3.12 虚拟环境在 `.venv/`，已能 import `arc_agi==0.9.8` 和 `arcengine==0.9.3`。
- 已跑通一个 offline public game smoke baseline：`ls20`，随机 20 步，0 分。

## 目录

- `data/raw/`: Kaggle 原始下载和解压内容。
- `data/working/`: 从原始数据派生出的轻量索引。
- `docs/`: 比赛核实、实验日志、数据清点。
- `src/`: 本地 evaluation、baseline、可视化脚本。
- `outputs/runs/`: 本地运行结果和 recordings。
- `outputs/figures/`: 可视化输出。
- `notebooks/`: 以后放 Kaggle submission notebook。

## 常用命令

```powershell
.\.venv\Scripts\python.exe src\inspect_public_games.py
.\.venv\Scripts\python.exe src\run_random_smoke.py --game ls20 --steps 20 --seed 0
.\.venv\Scripts\python.exe src\render_recording.py --recording <recording.jsonl> --frame-index 0
```

## 提交流程边界

Kaggle 页面显示本赛是 Notebook-only code competition，每天最多 1 次提交。当前只做了本地最小 smoke run，没有消耗每日提交名额。真正提交前需要确认 notebook 内容、运行时长、Internet disabled 和依赖来源。
