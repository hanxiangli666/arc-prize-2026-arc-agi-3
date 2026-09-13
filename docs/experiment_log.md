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

## 2026-08-21 D 盘迁移恢复

目标：确认迁移后的 D 盘目录是当前真实工作区，恢复被 Git 忽略的本地运行证据，并复跑最小验证闭环。

假设：

- 以 `D:\02_Projects\08_Kaggle\arc-prize-2026-arc-agi-3` 为唯一真实项目目录。
- E 盘旧路径只作为历史记录，不再作为运行路径。
- 不提交 Kaggle，不提交或推送 Git。

已完成：

- 核实 D 盘目录保留了 README、requirements、docs、src 和旧 `outputs/runs/random_smoke_ls20_seed0.json`。
- 核实迁移缺失项：`data/raw`、`data/working`、`.venv`、`notebooks`、`outputs/figures`。
- 用全局 Kaggle CLI 复核比赛状态：报名为 True，当前无提交，截止仍为 2026-11-02 23:59:00。
- 重新下载 `arc-prize-2026-arc-agi-3.zip` 到 D 盘项目 `data/raw`，并解压到 `data/raw/extracted`。
- 用 Python 3.12.13 重建 `.venv`，安装 `arc_agi==0.9.8` 和 `arcengine==0.9.3`。
- 重新生成 `data/working/public_games_summary.csv` 和 `docs/public_games_inventory.md`。
- 复跑 `ls20` seed 0、20 步 random smoke baseline。
- 重新生成 `outputs/figures/ls20_seed0_frame0.html`。

结果：

- public games = 25。
- total public levels = 183。
- total human baseline actions = 17135。
- `ls20-9607627b` random smoke：score = 0.0，levels_completed = 0 / 7，total_actions = 20。
- 本次 scorecard id：`62adb96e-ec35-4660-942e-d4972c1c0cb8`。

失败/风险：

- 父仓库有其他项目的未提交变更，本轮没有触碰。
- D 盘迁移后的 official raw data 和 `.venv` 已恢复，但这些仍被 Git 忽略，未来换机或迁移需要重新生成。
- random smoke 仍然只是连通性 baseline，下一步需要做 deterministic probing。

下一步：

- 为 `ls20` 写动作探针，记录每个 action 对 grid、位置、level 状态的影响。
- 用可视化辅助识别 `keyboard` 类 game 的角色、目标、障碍和奖励色块。
- 准备最小 Kaggle Notebook 草稿；正式提交前需要你明确确认。

## 2026-09-13 独立私有仓库迁移

目标：将 ARC-AGI-3 从共享 Kaggle 父仓库拆出，保留相关提交历史，并建立独立私有 GitHub 远端和本地工作目录。

假设：

- 新本地目录为 `D:\02_Projects\arc-prize-2026-arc-agi-3`。
- 新远端为私有仓库 `hanxiangli666/arc-prize-2026-arc-agi-3`。
- 保留父仓库旧目录作为迁移回滚副本，完成验证前不删除。
- 不提交 Kaggle；女朋友的 collaborator 邀请由仓库所有者稍后完成。

已完成：

- 核实新 GitHub 仓库为空且可见性为 Private。
- 从父仓库过滤出只涉及 ARC 子目录的 3 个提交。
- 将独立历史推送到新仓库 `main`，并克隆到新本地目录。
- 复制被 Git 忽略的本地数据、recordings 和可视化产物。
- 补齐独立仓库对 `data/working/` 和 `outputs/figures/` 的忽略规则。
- 用 Python 3.12.13 重建 `.venv`，确认 `arc_agi==0.9.8` 和 `arcengine==0.9.3` 可导入。
- 通过四个项目脚本的语法检查，并在新目录复跑 `ls20` seed 0、20 步 random smoke。

结果：

- 新目录 smoke baseline 仍为 score = 0.0、levels_completed = 0 / 7、total_actions = 20。
- 动作序列与原 seed 0 基线一致，说明迁移前后运行行为可复现。
- 本次迁移验证 scorecard id 为 `4dc00265-5dc4-4952-b545-56cffcd7a263`，记录位于已忽略的 `outputs/runs/recordings/`。

风险与下一步：

- 父仓库仍保留旧 ARC 目录；新仓库验证通过后，再经确认执行精确移除。
- 女朋友尚未加入 GitHub 私有仓库，需要仓库所有者稍后发送 collaborator 邀请。
