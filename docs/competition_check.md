# Competition Check

核实日期：2026-06-27
核实方式：全局 `kaggle` CLI，入口为 `C:\Users\LIHAN\.codex\bin\kaggle.cmd`。

## Kaggle 状态

- CLI 版本：`Kaggle CLI 2.2.2`。
- 比赛：`https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3`。
- 类别：Featured。
- 奖金：850,000 USD。
- 队伍数：1458。
- 报名状态：`userHasEntered=True`。
- 当前账号提交记录：无提交。
- 截止：2026-11-02 23:59 UTC。

## 2026-08-21 复核

- 当前真实项目目录：`D:\02_Projects\08_Kaggle\arc-prize-2026-arc-agi-3`。
- CLI 版本仍为 `Kaggle CLI 2.2.2`。
- `kaggle competitions list --search arc-prize-2026-arc-agi-3` 返回 `userHasEntered=True`。
- 当前队伍数为 2458，属于会变化的实时状态。
- 截止时间仍为 2026-11-02 23:59:00。
- `kaggle competitions submissions -c arc-prize-2026-arc-agi-3` 返回无提交。
- Code Requirements 仍显示 Notebook-only、CPU/GPU Notebook 均不超过 9 小时、Internet disabled、允许公开外部数据和预训练模型、submission file 自动生成。

## Timeline

- 2026-03-25：Start Date。
- 2026-06-30：Milestone 1，可选。
- 2026-09-30：Milestone 2，可选。
- 2026-10-26：Entry Deadline / Team Merger Deadline。
- 2026-11-02：Final Submission Deadline。
- 2026-12-04：Winners announcement。

## 数据

Kaggle 文件列表显示三类核心内容：

- `ARC-AGI-3-Agents/`: 官方 agent 框架本地副本。
- `arc_agi_3_wheels/`: `arc_agi`、`arcengine` 和 Kaggle/Linux 运行依赖 wheels。
- `environment_files/`: 25 个 public games，每个 game 有 `metadata.json` 和 Python 环境实现。

任务是交互式环境，不是静态 CSV 预测。每个 frame 是 JSON 状态，其中 grid 最大 64 x 64，cell 取值 0-15。agent 通过 `RESET`、`ACTION1` 到 `ACTION7` 交互；`ACTION6` 是带 `(x, y)` 坐标的复杂动作。

## 评价方式

Kaggle Evaluation 页和 Data 页给出的核心规则：

- 单个 game 分数范围 0 到 100%。
- 每个 level 看是否完成，以及完成动作数相对 human baseline 的效率。
- per-level raw score = `min(human_actions / agent_actions, 1.0)`，再平方。
- per-game score 是按 level index 加权的 level score 平均。
- total score 是所有 games 的平均。
- leaderboard 使用 private set 的 110 个 hidden games，其中一半 public leaderboard，一半 private leaderboard。

## 提交限制

- Notebook-only code competition。
- CPU Notebook <= 9 小时。
- GPU Notebook <= 9 小时。
- Internet access disabled。
- 允许 freely and publicly available external data，包括 pretrained models。
- submission file 自动生成，只要 agent 对任意 game 有动作。
- 规则页显示每天最多 1 次提交。
- 最多选择 2 个 final submissions。
- 最大 team size 为 8。
- 获奖相关方案需要开源；规则页提到 winning submission/source code 许可为 CC-BY 4.0，并要求满足 Open Source AI definition 相关条件。

## 当前冲突/注意

- 官方 `ARC-AGI-3-Agents/README.md` 写 Contest Submission 使用 Google Form，但 Kaggle Code Requirements 页面写 Notebook-only。当前以后者为正式 Kaggle 提交约束。
- 官方 `ARC-AGI-3-Agents/tests` 与源码有版本漂移迹象：测试引用 `agents.structs`，而当前源码从 `arcengine` 导入结构体。当前不把官方测试作为本地验收标准。
- 本地官方 `main.py` 会 import 多个 LLM agent 模板，轻量验证时先直接用 `arc_agi.Arcade`，避免引入不必要重依赖。
