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
- 不提交 Kaggle；collaborator 邀请由仓库所有者稍后完成。

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

- 父仓库中的旧 ARC 目录将在独立仓库验证和用户确认后精确移除。
- GitHub collaborator 邀请仍需由仓库所有者完成。

## 2026-09-13 父仓库清理与项目文档扩充

目标：完成独立仓库迁移的收尾工作，从共享 Kaggle 父仓库移除旧副本，并为后续协作建立详细、可复核的英文项目说明。

假设：

- `D:\02_Projects\arc-prize-2026-arc-agi-3` 是唯一后续开发目录。
- 父仓库只删除 `arc-prize-2026-arc-agi-3` 子目录，其他未提交改动必须保持原状。
- 本轮只处理仓库迁移和文档，不修改 agent 算法，不提交 Kaggle。

已完成：

- 再次核对新旧 Kaggle ZIP 的 SHA-256，均为 `C72400A32DB5E48DA9014BAF893B48016B300E9A6A77BD5D505DE2B1EC61D645`。
- 确认独立目录中的 `.venv`、原始数据包和可视化产物存在。
- 从父仓库精确删除旧 ARC 目录的 11 个受控文件，并以提交 `6da48fb` 推送到父仓库 `main`。
- 删除父仓库中被 Git 忽略的旧数据、环境和输出副本。
- 将根目录 README 扩充为英文项目指南，覆盖任务定义、交互接口、数据和评估、奖金、规则、知识路线、agent 架构、研究阶段、环境搭建、实验协议和协作流程。
- 用全局 Kaggle CLI 复核报名状态、最终截止时间、奖池和提交历史。

结果：

- 父仓库旧路径已不存在，独立仓库路径仍存在且数据和 Python 环境完整。
- 父仓库清理提交只包含旧 ARC 子目录的删除，其他工作区改动未进入提交。
- Kaggle 状态为 `userHasEntered=True`，最终截止为 `2026-11-02 23:59:00 UTC`，奖池显示 `850,000 Usd`，当前无提交。
- README 共 969 行、约 5,695 个英文单词，非 ASCII 字符为 0，内部文件链接均存在，Markdown diff 检查通过。

失败/风险：

- Kaggle 数据页和 ARC Prize 通用方法页对单关得分上限的表述存在差异，README 已记录，最终提交前必须重新核实。
- Kaggle 奖金、规则、参与人数和时间线可能更新，README 的状态快照不能替代提交前的实时检查。
- 本轮没有改变 agent 能力；random smoke 的 0 分仍只证明环境链路可运行。
- GitHub collaborator 邀请和 Kaggle 官方组队仍需由仓库所有者完成。

下一步：

- 为 `ls20` 实现 deterministic action probing，并记录每次动作带来的 grid diff、可逆性和状态变化。
- 以 public games 为依据建立 object-centric 表示和动作语义假设表。
- 在本地完成最小 Kaggle Notebook 草稿与离线检查；正式提交前再次取得明确确认。

## 2026-09-13 双语 README、GitHub About 与依赖审计

目标：为英文项目指南增加内容完整、表达自然的简体中文版本，完善 GitHub 仓库元数据，并核实本地依赖是否需要升级。

假设：

- 英文 README 继续作为 GitHub 默认入口，中文版单独存放在 `README.zh-CN.md`，两份文档顶部互相链接。
- 依赖版本应优先匹配 Kaggle 当前官方比赛包，不能只因 PyPI 出现更高版本就升级。
- 本轮不修改 agent 算法，不提交 Kaggle。

已完成：

- 新增完整简体中文 README，保留英文版的 19 个主题、评分公式、奖金表、时间线、规则、知识路线、架构、实验规范和命令。
- 在两份 README 顶部加入 English / 简体中文切换入口。
- 更新 GitHub About：增加项目简介、Kaggle 比赛主页和 8 个研究主题标签。
- 重新下载 Kaggle 官方比赛压缩包，并与本地包比较大小和 SHA-256。
- 核查 PyPI 与官方 changelog：`arc-agi==0.9.9` 只增加远程动作失败时的 HTTP 响应正文日志；Kaggle 包仍内置 `0.9.8`。
- 将 `requirements-local.txt` 的直接运行依赖固定到 Kaggle 官方包内版本，并按该组合重新对齐本地 `.venv`。

结果：

- 中英文 README 分别有 83 个标题；中文版 1,019 行，代码块、HTML code 标签和内部链接检查通过。
- GitHub About 简介、主页和 topics 已从远端读回确认，仓库仍为 Private。
- 新下载包和本地包大小均为 `44,339,942` 字节，SHA-256 均为 `C72400A32DB5E48DA9014BAF893B48016B300E9A6A77BD5D505DE2B1EC61D645`。
- 最终直接依赖为 `arc-agi 0.9.8`、`arcengine 0.9.3`、`Flask 3.1.3`、`matplotlib 3.10.8`、`numpy 2.4.4`、`pillow 12.2.0`、`pydantic 2.13.2`、`python-dotenv 1.2.2`、`requests 2.33.1`。
- `pip check` 无依赖冲突，四个项目脚本通过 `py_compile`。
- 对齐依赖后复跑 `ls20` seed 0、20 步 smoke，结果仍为 score `0.0`、完成 `0 / 7` 关、总动作 `20`；scorecard id 为 `add2d523-9ed1-4598-ad28-f9217648b30f`。

失败/风险：

- PyPI 的 `arc-agi` 比 Kaggle 包高一个补丁版本。本轮有意不升级，以保持比赛环境一致；Kaggle 包更新后需要重新评估。
- 通用依赖即使版本相同，也可能因操作系统使用不同 wheel 构建；最终提交仍需在干净 Kaggle Notebook 中复核。
- README 中的比赛状态和奖金属于 2026-09-13 快照，不能替代提交前实时核验。

下一步：

- 在 GitHub 页面确认中英文切换和 About 展示效果。
- 开始 `ls20` deterministic action probing，实现机器可读的 action-effect 报告。

## 2026-09-13 中文 README 复核与 Windows 环境验收

目标：逐项检查中文版是否忠实于英文原文并减少翻译腔，同时在当前 Windows 电脑上重新验证项目环境。

假设：

- 技术文档需要保留公式、表格和实验阶段结构，但正文应使用自然、直接的中文。
- 软件包版本以 Python distribution metadata 和 Kaggle 官方比赛包为准，不能依赖模块内可能过期的 `__version__` 常量。
- 本轮不修改 agent 算法，不提交 Kaggle。

已完成：

- 对照英文 README 和 ARC-AGI-3 官方 scoring methodology，复核任务、动作、数据划分、评分、奖金、时间线和组队规则。
- 修正“服务于实验”“上中位数轨迹”“可获取性”“墙钟运行时间”等直译表达。
- 补入 upper median 的准确例子：4 人通关取第 3 名，5 人通关仍取第 3 名。
- 减少正文中不必要的 `Agent`、`frame`、`scorecard`、`recording` 和 `seed` 混用；首次定义、API 名称和命令参数继续保留英文。
- 改写开场、数据划分、研究阶段、基线解释和项目原则中的模板化句子。
- 核实操作系统、PowerShell、Python 安装、项目虚拟环境、数据目录、依赖、脚本和最小运行链路。

结果：

- 系统为 64 位 Windows 11，PowerShell 为 `7.6.5`。
- 全局默认 Python 为 `3.14.4`，项目 `.venv` 独立使用 Python `3.12.13`，解释器路径为 `D:\02_Projects\arc-prize-2026-arc-agi-3\.venv\Scripts\python.exe`。
- `.venv`、官方 ZIP、解压环境、官方 wheels、working 数据、runs 和 figures 均存在。
- 安装元数据为 `arc-agi==0.9.8` 和 `arcengine==0.9.3`；`pip check` 无依赖冲突。
- 四个项目脚本通过 `py_compile`。
- 数据清单仍为 25 个公开游戏、183 个关卡和 17,135 个人类基线动作。
- `ls20` seed 0、20 步 smoke 仍为 score `0.0`、完成 `0 / 7` 关，动作序列与受控基线完全一致。
- 中英文 README 都有 83 个标题，外部链接集合一致；中文代码块、HTML code 标签、目录锚点和 Markdown diff 检查通过。
- 针对常见 AI 写作词、否定式排比和已发现直译词的复查没有剩余命中。

失败/风险：

- 首次汇总 CSV 时误用了不存在的 `level_count` 和 `human_baseline_actions` 字段，导致两个合计为空；按真实字段 `levels` 和 `baseline_total_actions` 重算后得到 183 和 17,135。
- 官方 `arcengine==0.9.3` wheel 内部仍保留 `arcengine.__version__ = 0.1.0`；实际版本必须通过 `importlib.metadata.version('arcengine')` 查询。
- 直接运行全局 `python` 会进入 3.14 环境。项目命令必须显式调用 `.venv\Scripts\python.exe`。
- 本轮只证明 Windows 本地环境完整和可复现，尚未证明 Kaggle Notebook 运行环境或 agent 解题能力。

下一步：

- 在后续文档改动中同时维护中英文 README，避免事实和命令发生漂移。
- 开始 `ls20` 的确定性动作探测实验。
