# Experiment Log

## 2026-06-27 Bootstrap

目标：核实比赛真实状态，下载数据，建立本地最小 evaluation/可视化/baseline 框架。

假设：

- 先用 public games 建立工具链；hidden games 不可见，不能从 public score 直接推断最终成绩。
- 评价核心是 completion + efficiency；任何实验都要记录动作数、完成 level 数和 scorecard。
- 每天只有 1 次 Kaggle 提交，真正提交前需要确认 notebook 内容，避免浪费名额。

已完成：

- 用全局 Kaggle CLI 确认报名状态为 `userHasEntered=True`。
- 下载并解压 `arc-prize-2026-arc-agi-3.zip`。
- 建立 `.venv`，修复中途不完整的 `numpy` 安装，确认 `arc_agi` 和 `arcengine` 可 import。
- 用 offline public environment 跑通 `ls20` 随机 20 步 smoke baseline。

结果：

- `ls20-9607627b`，随机 20 步。
- score = 0.0。
- levels_completed = 0 / 7。
- total_actions = 20。
- recording 写入 `outputs/runs/recordings/5324ce23-facd-49f7-b7ea-a263e7de268e/`。

失败/风险：

- 第一次 `uv pip install` 超时，留下半安装状态；后续用 `ensurepip` 和 pip 重装 `numpy` 修复。
- 第一次 environment smoke run 误以为 `available_actions` 是 `GameAction` 枚举，实际返回 action id 整数；已在 baseline 脚本中做转换。
- 随机策略没有完成任何 level，不能作为有效策略，只能作为环境连通性 baseline。
- 尚未消耗 Kaggle 每日提交名额，也尚未创建/提交 Kaggle Notebook。

下一步：

- 用数据清点脚本生成 25 个 public games 的 baseline/action/tag 概览。
- 对 `ls20` 做人工观测：渲染初始 frame 和几步随机 recording，猜测 action mapping。
- 写一个 deterministic probing policy：逐个动作试探状态变化，而不是随机游走。
- 准备最小 Kaggle Notebook，但正式 submit 前先确认是否要用掉当天 1 次提交。
