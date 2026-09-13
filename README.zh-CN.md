# ARC Prize 2026：ARC-AGI-3

**语言：** [English](README.md) | [简体中文](README.zh-CN.md)

本仓库是 Kaggle **ARC Prize 2026 - ARC-AGI-3** 竞赛的可复现研究工作区。项目研究的核心问题是：一个 AI Agent 进入从未见过的交互环境后，怎样自行发现控制方式和目标，建立简洁有效的环境模型，并用尽可能少的动作完成难度逐步上升的关卡。

本项目坚持以证据推进研究：先读懂基准和评估协议，再搭建可靠的本地工具，建立简单基线，系统分析失败案例；只有受控实验能够说明复杂方法确有价值时，才引入更复杂的模型或训练方案。

<a id="zh-official-links"></a>

## 官方链接

| 资源 | 链接 |
| --- | --- |
| Kaggle 比赛主页 | [ARC Prize 2026 - ARC-AGI-3](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3) |
| Kaggle 比赛规则 | [Competition Rules](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/rules) |
| Kaggle 比赛数据 | [Competition Data](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/data) |
| Kaggle Notebooks | [Competition Code](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/code) |
| Kaggle 排行榜 | [Competition Leaderboard](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/leaderboard) |
| ARC Prize 竞赛页面 | [ARC-AGI-3 Competition](https://arcprize.org/competitions/2026/arc-agi-3) |
| ARC-AGI-3 基准介绍 | [Benchmark Overview](https://arcprize.org/arc-agi/3) |
| 官方文档与 SDK | [ARC-AGI-3 Documentation](https://docs.arcprize.org/) |
| 评分方法 | [Relative Human Action Efficiency](https://docs.arcprize.org/methodology) |
| 技术报告 | [ARC-AGI-3 Technical Report](https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf) |
| 官方工具包 | [arcprize/ARC-AGI](https://github.com/arcprize/ARC-AGI) |
| 官方 Agent 框架 | [arcprize/ARC-AGI-3-Agents](https://github.com/arcprize/ARC-AGI-3-Agents) |
| 官方 Kaggle Starter | [arcprize/ARC-AGI-3-Kaggle-Starter](https://github.com/arcprize/ARC-AGI-3-Kaggle-Starter) |

<a id="zh-status"></a>

## 当前状态快照

以下状态核实于 **2026 年 9 月 13 日**：

- 本工作区关联的 Kaggle 账号已经接受比赛规则，CLI 返回 <code>userHasEntered=True</code>。
- 最终提交截止时间为 **2026 年 11 月 2 日 23:59 UTC**。
- 报名和队伍合并截止时间为 **2026 年 10 月 26 日 23:59 UTC**。
- Kaggle 当前显示 ARC-AGI-3 赛道总奖池为 **850,000 美元**。
- 比赛仅接受 Kaggle Notebook 提交，每支队伍每天最多提交一次。
- 本项目目前没有向 Kaggle 提交过作品。
- 本地 public game 工具、数据清点、轨迹记录、可视化和随机 smoke baseline 已经跑通。
- 2026 年 9 月 13 日重新下载的官方比赛压缩包与本地压缩包逐字节一致。

参赛人数、排行榜、规则和截止日期都有可能调整。每次正式提交或判断奖金资格前，必须重新查看 Kaggle 官方页面。

<a id="zh-contents"></a>

## 目录

1. [比赛概述](#zh-overview)
2. [ARC-AGI-3 测量什么能力](#zh-capabilities)
3. [环境如何运行](#zh-environment)
4. [数据与评估集划分](#zh-data)
5. [评分方式](#zh-scoring)
6. [奖金结构](#zh-prizes)
7. [比赛时间线](#zh-timeline)
8. [提交与组队规则](#zh-rules)
9. [需要掌握的知识](#zh-knowledge)
10. [参考 Agent 架构](#zh-architecture)
11. [研究路线](#zh-strategy)
12. [仓库结构](#zh-repository)
13. [Windows 本地环境搭建](#zh-setup)
14. [当前常用命令](#zh-commands)
15. [实验规范](#zh-experiments)
16. [协作流程](#zh-collaboration)
17. [当前基线](#zh-baseline)
18. [已知风险与开放问题](#zh-risks)
19. [术语表](#zh-glossary)

<a id="zh-overview"></a>

## 比赛概述

ARC-AGI-3 是 ARC-AGI 系列中的第一个交互式基准。早期 ARC-AGI 基准主要给出静态的输入网格与输出网格，要求系统推断二者之间的变换规律。ARC-AGI-3 把测试者放进一个陌生的回合制环境，要求测试者通过实际交互学习规则。

比赛不会提供自然语言说明、按键解释或明确目标。Agent 需要自行发现：

- 画面中哪些结构真正重要；
- 当前允许执行哪些动作；
- 每个动作会产生什么效果；
- 哪些状态变化代表进展；
- 什么情况属于失败或成功；
- 早期关卡学到的知识怎样迁移到后续关卡；
- 怎样高效到达推断出的目标状态。

基准的设计目标是让人类在第一次接触时能够通过试验学会，同时让当前 AI 系统仍然感到困难。受控测试中，每个被正式接纳的环境都至少被两名彼此独立的人类参与者完整通关。因此，这项基准关注人类与机器在学习新技能效率上的差距，而非单纯判断某个谜题理论上能否被解决。

### 为什么这是一个机器学习问题

系统需要把观察历史和动作历史转化为有价值的下一步动作：

~~~text
观察历史 + 动作历史 + 已推断规则 -> 下一步动作
~~~

这项任务把多个通常分开研究的方向放进同一个闭环：

- 结构化网格的视觉表示；
- 序列决策；
- 主动探索；
- 系统辨识；
- 记忆与状态抽象；
- 目标推断；
- 规划与搜索；
- 在线适应；
- 对未知任务的泛化。

Agent 可以使用人工规则、经典搜索、概率推断、学习模型、语言模型、视觉语言模型，也可以采用混合系统。大规模模型训练并非必需。可靠的研究流程应从能够检验明确假设的最简单方法开始。

<a id="zh-capabilities"></a>

## ARC-AGI-3 测量什么能力

官方比赛说明重点关注四类能力。

### 1. 探索

Agent 必须主动获取信息。一个动作可以服务于实验，而不必立即服务于通关。例如，从相同的 reset 状态出发，把每个可用动作分别执行一次，可以帮助识别控制语义、移动规则、不可逆变化或危险状态。

相关概念包括：

- 探索与利用；
- 信息增益；
- 可逆动作与不可逆动作；
- 受控干预；
- 面向不确定性的动作选择。

### 2. 建模

Agent 需要把原始画面转化为能够预测未来状态的模型。模型可以是符号式、以对象为中心、神经网络式，也可以是混合形式。

一个有用的模型应能回答：

- 哪些单元格属于同一个对象？
- 哪些对象可以被控制？
- 哪些特征会跨帧持续存在？
- 执行动作后，画面具体改变了什么？
- 环境是否是确定性的？
- 哪些变量表示生命、物品、进度或关卡状态？

### 3. 目标习得

环境不会直接告诉 Agent 应该优化什么。Agent 需要从反馈、视觉结构、关卡切换和重复交互中推断值得追求的状态。

可用于目标推断的信号包括：

- 进入下一关；
- 某个对象消失或被收集；
- 计数器或状态区域发生变化；
- 出现 <code>WIN</code> 或 <code>GAME_OVER</code> 等终止状态；
- 多个关卡反复出现一致的结构规律。

### 4. 规划与执行

推断出目标和转移规则后，Agent 需要选择高效的动作序列。新的观察一旦与当前模型矛盾，Agent 还必须及时修改计划。

评分同时奖励完成度和动作效率，因此规划质量会直接影响最终得分。

<a id="zh-environment"></a>

## 环境如何运行

### 核心交互循环

~~~text
重置环境
    |
    v
接收画面和可用动作
    |
    v
解析对象、变化和状态
    |
    v
更新信念、记忆和候选目标
    |
    v
选择并校验一个动作
    |
    v
执行动作并接收下一帧
    |
    +---- 重复，直到 WIN、GAME_OVER 或预算耗尽
~~~

### 画面 Frame

Agent 接收与 JSON 兼容的 frame 对象，其中包含当前网格和元数据。

- 最大网格尺寸：<code>64 x 64</code>。
- 单元格取值：从 <code>0</code> 到 <code>15</code> 的整数。
- 坐标原点：左上角为 <code>(0, 0)</code>。
- 一个环境可以包含多个难度逐步增加的关卡。
- 常见的进行中和终止状态包括 <code>NOT_FINISHED</code>、<code>WIN</code> 和 <code>GAME_OVER</code>。

这些整数可以理解为颜色或符号状态，其含义由具体环境决定。同一种颜色在一个环境中可能表示墙，在另一个环境中可能表示可移动对象。

### 动作 Action

每个环境会开放下列动作接口中的一个子集：

| 动作 | 通用接口含义 |
| --- | --- |
| <code>RESET</code> | 启动或重新启动一个环境。 |
| <code>ACTION1</code> 至 <code>ACTION5</code> | 简单动作，可能代表移动、交互、旋转或其他环境专属操作。 |
| <code>ACTION6</code> | 接收 <code>(x, y)</code> 坐标的复杂动作，常用于类似点击的交互。 |
| <code>ACTION7</code> | 某些环境需要的额外简单动作。 |

动作名称不会透露语义。不能假设不同游戏中的 <code>ACTION1</code> 含义相同，Agent 必须根据动作前后的状态变化自行推断。

### 关卡 Level

每个游戏由连续关卡组成。后续关卡通常更难，在单个游戏的评分中权重也更高。早期关卡可以揭示能够复用的机制，但 Agent 需要避免只记住某一关的具体布局。

### 什么会被计为一个动作

提交给环境的一次离散交互会被计为动作。不会改变环境的内部计算、推理、解析、搜索、工具调用和重试不计入环境动作数，但仍会占用 Notebook 运行时间和计算资源。

<a id="zh-data"></a>

## 数据与评估集划分

比赛压缩包包含三个主要部分：

| 组成部分 | 用途 |
| --- | --- |
| <code>ARC-AGI-3-Agents/</code> | 官方 Agent 框架和模板的本地副本。 |
| <code>arc_agi_3_wheels/</code> | 比赛环境使用的 Python wheel 包。 |
| <code>environment_files/</code> | 25 个公开环境的 Python 实现和元数据。 |

基准划分如下：

| 划分 | 环境数量 | 可见性 | 用途 |
| --- | ---: | --- | --- |
| 公开演示集 | 25 | 公开 | 学习接口、搭建工具并展示方法。 |
| 半私有评估集 | 55 | 隐藏 | 用于 Kaggle Public Leaderboard 部分。 |
| 完全私有评估集 | 55 | 隐藏 | 用于 Private Leaderboard 最终排名。 |
| 隐藏竞赛集总计 | 110 | 隐藏 | 衡量方法能否泛化到公开演示之外。 |

公开环境有意设计得更容易，也不能完整代表私有环境中可能出现的机制。公开环境上的成功适合用于调试和受控研究，却不能可靠估计隐藏环境上的表现。

这种分布差异是基准的核心。一个系统可以通过大量游戏专属解法在公开环境上获得亮眼结果，同时几乎没有学到能迁移到未知环境的方法。

<a id="zh-scoring"></a>

## 评分方式

ARC-AGI-3 同时评估 **完成度** 与 **效率**。指标名称为 **Relative Human Action Efficiency**，简称 RHAE，可译为相对人类动作效率。

### 人类基线

人类基线来自受控条件下第一次接触游戏的参与者。对每一关，把已通关的人类轨迹按动作数排序，选择熟练参与者中的上中位数轨迹作为基线。这样可以降低偶然幸运或异常低效操作对基线的影响。

设：

- <code>H_l</code> 表示人类完成第 <code>l</code> 关所需的基线动作数；
- <code>A_l</code> 表示 Agent 完成第 <code>l</code> 关所用的动作数；
- <code>S_l</code> 表示第 <code>l</code> 关的得分。

### 单关得分

Kaggle 比赛数据页当前给出的计算方式是：

~~~text
efficiency_l = min(H_l / A_l, 1.0)
S_l = efficiency_l^2
~~~

未完成的关卡得分为零。

示例：

| 人类动作数 | Agent 动作数 | 效率比 | 单关得分 |
| ---: | ---: | ---: | ---: |
| 10 | 10 | 1.00 | 100% |
| 10 | 20 | 0.50 | 25% |
| 10 | 40 | 0.25 | 6.25% |
| 10 | 100 | 0.10 | 1% |

平方会明显惩罚低效探索。Agent 使用人类两倍的动作数时，该关得分为 25%，不会保留为 50%。

### 单个游戏得分

每一关按从 1 开始的关卡编号加权：

~~~text
weight_l = l
game_score = sum(weight_l * S_l) / sum(weight_l)
~~~

未完成关卡贡献零分。后续关卡权重更高，因此只完成教学性质的前几关无法获得很高的单局得分。

### 总分

最终基准分数是评估集中各个游戏得分的算术平均值。比赛以 0% 至 100% 的形式显示分数。

### 需要持续核实的评分口径差异

ARC-AGI-3 通用方法文档目前提到：当 Agent 比人类基线更快时，单关得分上限最高可到 <code>1.15</code>。Kaggle 数据页则写明先把效率比截断到 <code>1.0</code>，再做平方。本仓库在本地竞赛核验中暂以实时 Kaggle 比赛定义为操作口径。最终提交前必须重新核实；如果 Kaggle 更新或澄清实现，本地评分工具也应同步修改。

<a id="zh-prizes"></a>

## 奖金结构

Kaggle 当前列出的 ARC-AGI-3 总奖金为 **850,000 美元**。

### 进展奖：150,000 美元

#### 最终排行榜奖金：75,000 美元

| 最终名次 | 奖金 |
| ---: | ---: |
| 第 1 名 | 40,000 美元 |
| 第 2 名 | 15,000 美元 |
| 第 3 名 | 10,000 美元 |
| 第 4 名 | 5,000 美元 |
| 第 5 名 | 5,000 美元 |

#### 里程碑奖金：75,000 美元

两个里程碑各分配 37,500 美元：

| 里程碑名次 | 里程碑 1 | 里程碑 2 |
| ---: | ---: | ---: |
| 第 1 名 | 25,000 美元 | 25,000 美元 |
| 第 2 名 | 7,500 美元 | 7,500 美元 |
| 第 3 名 | 5,000 美元 | 5,000 美元 |

- 里程碑 1 截止时间：2026 年 6 月 30 日 23:59 UTC。
- 里程碑 2 截止时间：2026 年 9 月 30 日 23:59 UTC。
- 参与里程碑评奖的 Notebook 必须在对应截止时间前以符合要求的开源许可证公开。

ARC Prize 网站的部分版本曾显示不同的里程碑第二、第三名分配方式，但里程碑奖金总额相同。本项目把 Kaggle 实时 Prizes 页面视为实际操作依据，准备里程碑提交前仍需再次核实。

### 额外大奖：700,000 美元

如果有队伍在比赛排行榜上达到 100% 得分，则解锁 700,000 美元额外奖池。Kaggle 当前列出的合格队伍奖金分配为：

| 名次 | 额外奖金 |
| ---: | ---: |
| 第 1 名 | 350,000 美元 |
| 第 2 名 | 175,000 美元 |
| 第 3 名 | 70,000 美元 |
| 第 4 名 | 70,000 美元 |
| 第 5 名 | 35,000 美元 |

获奖资格还受到正式规则、身份和司法管辖区核验、可复现性审查、许可证义务与主办方确认的约束。获奖者自行承担相应税务责任。

<a id="zh-timeline"></a>

## 比赛时间线

Kaggle 当前说明下列截止时间均为对应日期的 <code>23:59 UTC</code>。

| 日期 | 事件 | 截至 2026-09-13 的状态 |
| --- | --- | --- |
| 2026 年 3 月 25 日 | 比赛开始 | 已完成 |
| 2026 年 6 月 30 日 | 可选里程碑 1 截止 | 已完成 |
| 2026 年 9 月 30 日 | 可选里程碑 2 截止 | 即将到来 |
| 2026 年 10 月 26 日 | 报名截止 | 即将到来 |
| 2026 年 10 月 26 日 | 队伍合并截止 | 即将到来 |
| 2026 年 11 月 2 日 | 最终提交截止 | 即将到来 |
| 2026 年 12 月 4 日 | 获奖者公布 | 计划中 |

主办方保留更新时间线的权利。做任何截止时间相关决定前，应再次查看 Kaggle。

<a id="zh-rules"></a>

## 提交与组队规则

本节归纳从 Kaggle 比赛页面核实的实际操作规则，完整规则始终具有最高效力。

### Notebook 提交要求

- 提交必须通过 Kaggle Notebook 生成。
- CPU Notebook 运行时间不得超过 9 小时。
- GPU Notebook 运行时间不得超过 9 小时。
- 评估期间必须关闭互联网访问。
- 可以使用自由且公开可得的外部数据。
- 可以使用公开可得的预训练模型，但必须满足许可证和可获取性要求。
- 只要 Agent 对任一游戏执行动作，比赛提交产物就会自动生成。
- 每支队伍每天最多提交一次。
- 每支队伍最多选择两份最终提交参与评审。

### 队伍要求

- 队伍人数上限为 8 人。
- 每位成员必须使用独立的 Kaggle 账号。
- 每位成员在加入队伍前必须接受比赛规则。
- 每位参赛者在本比赛中只能加入或创建一支队伍。
- 被邀请者在 Kaggle 正式接受邀请后，队伍关系才生效。
- 队伍合并必须在 2026 年 10 月 26 日 23:59 UTC 前完成。
- 如果合并后的历史提交次数超过规则允许的队伍提交上限，合并申请可能被拒绝。
- 禁止向 Kaggle 官方队伍之外的人员私下共享比赛代码或比赛数据。

因此，私有仓库的 collaborator 权限应只授予已经接受 Kaggle 规则并正式加入同一 Kaggle 队伍的成员。

### 队伍奖金分配

Kaggle 通用规则规定，团队奖金默认由所有符合资格的成员平均分配。全体成员也可以一致同意采用其他分配方案，并在付款前通知 Kaggle。

### 开源和许可证义务

- 开发阶段可以保持仓库私有。
- 符合里程碑奖金资格的 Notebook 必须在对应截止时间前公开。
- 获奖提交及源代码需要满足比赛的开源要求。
- 比赛列出的获奖者许可证类型为 <code>CC-BY 4.0</code>。
- 比赛数据列在 <code>Apache 2.0</code> 的访问和使用条款下。
- 获奖者可能需要提供训练代码、推理代码、环境说明、模型信息和足以复现结果的文档。
- 公开发布前必须审查模型、权重、数据和第三方软件的许可证。

本仓库目前尚未声明覆盖整个项目的许可证。任何公开发布、里程碑提交或可能获奖的发布之前，都必须完成合规许可证选择和第三方依赖审计。

<a id="zh-knowledge"></a>

## 需要掌握的知识

这个项目适合循序渐进地学习。新加入的贡献者不需要先掌握所有主题才能开始。

### 第 1 层：编程与数据基础

| 主题 | 为什么重要 | 入门练习 |
| --- | --- | --- |
| Python 函数、类和模块 | 工具包、引擎、环境和 Agent 都使用 Python 实现。 | 阅读 <code>src/run_random_smoke.py</code>，找出初始化、循环和输出三个阶段。 |
| 列表、字典和 dataclass | frame、元数据、动作和 scorecard 都是结构化对象。 | 打印一个 frame，并标注每个字段的含义。 |
| NumPy 数组 | 网格和帧差异天然适合表示为数组。 | 计算两个 frame 之间有多少单元格发生变化。 |
| JSON 与 JSONL | scorecard 和 recording 使用结构化序列化数据。 | 加载一份 recording，检查其中一个 step。 |
| CSV | 公开游戏清单和实验摘要适合整理为表格。 | 按关卡数量或人类基线动作数排序游戏。 |
| Git 与 GitHub | 可复现协作需要版本化代码和可审查改动。 | 创建分支并完成一次只改文档的提交。 |
| 虚拟环境 | 隔离依赖可以避免不同项目之间发生包冲突。 | 根据文档中的版本重新创建 <code>.venv</code>。 |

### 第 2 层：机器学习核心概念

| 主题 | 在 ARC-AGI-3 中的含义 |
| --- | --- |
| 状态 State | 预测环境未来行为所需的信息，可能比可见 frame 更多或更少。 |
| 观察 Observation | Agent 当前可以获得的 frame 和元数据。 |
| 动作 Action | 从当前可用动作集合中选出的一次环境交互。 |
| 策略 Policy | 根据交互历史选择下一步动作的规则或模型。 |
| 轨迹 Trajectory | 按时间排列的观察、动作和结果状态序列。 |
| 奖励或反馈 | 关卡完成、终止状态或 scorecard 变化等进展信号；该任务反馈较稀疏。 |
| 探索 Exploration | 用于学习控制方式、动态规律、危险和目标的动作。 |
| 利用 Exploitation | 用于执行当前最佳计划的动作。 |
| 泛化 Generalization | 把学习过程应用到机制陌生的隐藏环境。 |
| 过拟合 Overfitting | 行为在公开游戏上成功，却在隐藏游戏上失效。 |

ARC-AGI-3 具有类似强化学习的交互循环，但不强制进行强化学习训练。确定性搜索策略或符号模型同样是有效的 Agent。

### 第 3 层：感知与表示

相关技术包括：

- 连通分量分析；
- 颜色与形状统计；
- 对象分割；
- 包围盒与质心；
- 帧差分；
- 运动与可控性检测；
- 持续对象跟踪；
- 坐标变换；
- 以对象为中心的状态表示；
- 场景图与关系表示。

基准使用符号化网格，因此少量结构化视觉处理往往比大型通用图像编码器提供更容易解释的信息。

### 第 4 层：搜索与规划

相关算法包括：

- 广度优先搜索；
- 深度优先搜索；
- 迭代加深；
- 一致代价搜索；
- A* 搜索；
- Beam Search；
- 蒙特卡洛树搜索；
- 模型预测控制；
- 新颖性搜索；
- 状态哈希与重复状态检测；
- 可逆动作分析。

搜索需要状态表示、转移模型、候选目标和预算。盲目搜索会浪费动作和 Notebook 运行时间，已经学到或推断出的结构应当用来缩小搜索空间。

### 第 5 层：规则归纳与世界模型

Agent 需要从少量交互中归纳出简洁解释。相关思想包括：

- 系统辨识；
- 因果干预；
- 假设生成与排除；
- 有限状态机；
- 程序合成；
- 贝叶斯信念更新；
- 潜状态模型；
- 状态转移预测；
- 测试时适应；
- 分层技能与可复用 option。

### 第 6 层：记忆与上下文管理

对于基于模型的 Agent，长期保存每一张原始 <code>64 x 64</code> frame 成本很高。一个实用的记忆系统可以存储：

- 动作与效果的摘要；
- 已发现对象及其属性；
- 候选目标及置信度；
- 失败状态和禁止进入的转移；
- 压缩后的帧差异；
- 关卡专属事实；
- 跨关卡规则；
- 尚未解决的问题。

记忆系统应保留与决策有关的证据，同时丢弃重复像素和冗余观察。

### 第 7 层：可选的学习模型方法

后续实验可以评估：

- 使用视觉语言模型解释 frame；
- 使用语言模型生成假设和计划；
- 小型学习式转移模型；
- 基于规则允许的人类轨迹进行模仿学习；
- 测试时微调；
- 集成系统或候选方案排序；
- 在评估期间生成任务专属分析工具的代码 Agent。

Kaggle Notebook 中使用的任何模型都必须满足离线运行时间、内存、许可证和可复现性约束。单纯扩大模型规模本身不构成一个实验假设。

<a id="zh-architecture"></a>

## 参考 Agent 架构

一个模块化 Agent 可以按以下方式组织：

~~~text
ARC 环境
   |
   v
Frame 解析器与对象提取器
   |
   v
帧变化与可控性分析器
   |
   v
信念状态与压缩记忆
   |
   +--------------------+
   |                    |
   v                    v
目标推断             转移模型
   |                    |
   +---------+----------+
             |
             v
        规划器或搜索策略
             |
             v
        合法动作校验器
             |
             v
          选定动作
             |
             v
       记录器与本地评估器
~~~

### 各模块职责

| 模块 | 职责 | 应记录的证据 |
| --- | --- | --- |
| Frame 解析器 | 把网格转换为对象、区域和特征。 | 解析出的对象和 mask。 |
| 变化分析器 | 比较动作前后的 frame，并尝试把变化归因到动作。 | 变化单元格、包围盒和候选原因。 |
| 信念状态 | 跟踪不确定规则和持续变量。 | 假设、置信度及支持该假设的转移。 |
| 目标推断 | 对候选成功条件排序。 | 目标候选和进展信号。 |
| 转移模型 | 预测各动作可能产生的下一状态。 | 预测转移与真实观察的对比。 |
| 规划器 | 选择能获取信息或接近目标的动作序列。 | 候选计划、代价和选择理由。 |
| 动作校验器 | 把动作限制在当前合法集合与有效参数内。 | 被拒绝的非法候选动作。 |
| 记录器 | 保存完整轨迹和摘要。 | JSONL recording 和 scorecard。 |
| 评估器 | 计算可比较的实验指标。 | 完成度、动作效率、运行时间和失败计数。 |

第一个实现不需要一次性完成所有模块。这套架构用于帮助隔离假设与失败原因，不要求项目立即建设庞大框架。

<a id="zh-strategy"></a>

## 研究路线

### 阶段 0：基础设施与可复现性

当前状态：已可运行。

交付物：

- 本地 Python 3.12 环境；
- 官方公开环境；
- 游戏清单；
- scorecard 提取；
- 轨迹记录；
- frame 可视化；
- 确定性随机基线。

退出条件：从干净环境启动时，同一个 seed 能产生相同动作序列和等价的 scorecard 行为。

### 阶段 1：确定性动作探测

目标：在不训练模型的前提下，发现动作语义和即时状态转移结构。

实验：

- 每次回到相同初始状态；
- 分别独立执行每个可用动作；
- 比较变化单元格与元数据；
- 测试重复执行同一动作；
- 测试可能互为逆操作的动作组合；
- 识别 no-op、移动、点击、危险和不可逆行为；
- 记录假设与反例。

退出条件：至少为一个公开游戏生成机器可读的动作效果报告。

### 阶段 2：以对象为中心的状态表示

目标：用简洁实体及其关系替代直接针对原始 frame 的推理。

实验：

- 按颜色提取连通分量；
- 跟踪对象在多帧之间是否持续存在；
- 识别可控对象；
- 区分静态区域与动态区域；
- 检测计数器、边框和状态面板。

退出条件：状态表示能够用少于原始网格的变量解释已观察到的画面变化。

### 阶段 3：转移与目标推断

目标：建立可以被实验验证的环境动态模型和进展条件。

实验：

- 确定性转移表；
- 有限状态机归纳；
- 候选目标排序；
- 观察到反例后更新置信度；
- 分离关卡专属规则与跨关卡规则。

退出条件：能够预测公开游戏中留出的状态转移，并识别至少一个经过验证的进展条件。

### 阶段 4：基于搜索的策略

目标：利用推断出的模型进行高效规划。

实验：

- 在压缩状态空间中运行广度优先搜索或 A*；
- 剪枝重复状态；
- 加入动作代价惩罚；
- 对新颖状态给予探索奖励；
- 每次观察后进行短视野重规划。

退出条件：可复现地完成至少一个公开关卡，并在动作数上优于无信息基线。

### 阶段 5：泛化实验

目标：判断哪些组件能够跨游戏迁移。

实验：

- Leave-one-game-out 评估；
- 测试保留公开游戏之前冻结策略；
- 比较游戏专属特征和通用特征；
- 对记忆、感知、规划和提示词进行消融；
- 跟踪不同 seed 和环境之间的方差。

退出条件：在检查后不添加游戏专属规则的前提下，对保留公开游戏取得可复现改进。

### 阶段 6：可选的模型辅助 Agent

目标：检验本地离线模型能否在结构化基线上带来可测量的增益。

采用模型前的要求：

- 明确定义模型承担的职责；
- 已有一个规模更小的非模型基线；
- 固定提示词和解码参数；
- 校验合法动作；
- 测量运行时间和内存；
- 提供消融证据；
- 模型和权重许可证兼容；
- 能够在 Kaggle Notebook 环境运行。

### 阶段 7：Kaggle 提交流程

目标：生成不依赖隐藏网络访问的有效离线 Notebook 提交。

检查清单：

- 附加所有必要的包、模型和资源；
- 关闭互联网；
- 从干净 Kaggle 会话完整运行 Notebook；
- 保持在 9 小时限制内；
- 确认 Agent 至少对一个游戏执行了动作；
- 检查生成的输出与日志；
- 记录 Notebook 版本、代码提交、依赖、运行时间和排行榜结果；
- 消耗当天提交机会前取得明确授权。

<a id="zh-repository"></a>

## 仓库结构

~~~text
arc-prize-2026-arc-agi-3/
|-- README.md
|-- README.zh-CN.md
|-- requirements-local.txt
|-- data/
|   |-- raw/                 # Kaggle 压缩包和解压后的官方文件；Git 忽略
|   +-- working/             # 本地派生索引；Git 忽略
|-- docs/
|   |-- competition_check.md
|   |-- experiment_log.md
|   +-- public_games_inventory.md
|-- notebooks/               # 后续 Kaggle 提交 Notebook
|-- outputs/
|   |-- figures/             # 本地可视化；Git 忽略
|   +-- runs/
|       |-- recordings/      # 完整本地轨迹；Git 忽略
|       +-- random_smoke_ls20_seed0.json
+-- src/
    |-- inspect_public_games.py
    |-- render_recording.py
    |-- run_random_smoke.py
    +-- score_utils.py
~~~

### 脚本职责

| 脚本 | 用途 |
| --- | --- |
| <code>src/inspect_public_games.py</code> | 读取公开环境元数据并生成游戏清单。 |
| <code>src/run_random_smoke.py</code> | 验证环境加载、动作执行、轨迹记录和 scorecard 生成。 |
| <code>src/render_recording.py</code> | 从 JSONL recording 中选取一帧并输出 HTML 可视化。 |
| <code>src/score_utils.py</code> | 提供一个小型本地实现，用于计算当前文档口径下的比赛式得分。 |

<a id="zh-setup"></a>

## Windows 本地环境搭建

已经验证的本地配置为：

- Windows 与 PowerShell；
- Python <code>3.12.13</code>；
- 来自比赛压缩包的 <code>arc-agi==0.9.8</code>；
- 来自比赛压缩包的 <code>arcengine==0.9.3</code>。

2026 年 9 月 13 日重新下载并计算哈希的 Kaggle 压缩包与本地压缩包逐字节一致，仍然内置 <code>arc-agi==0.9.8</code> 和 <code>arcengine==0.9.3</code>。PyPI 已提供 <code>arc-agi==0.9.9</code>，其官方变更记录只增加了远程动作失败时输出 HTTP 响应正文的诊断信息。本项目有意保留 <code>0.9.8</code>，以匹配 Kaggle 比赛包；改变固定版本前应重新审计官方包。

<code>requirements-local.txt</code> 也把直接运行依赖固定到已核实比赛包中的版本，防止全新安装时静默漂移到不同的 NumPy、Matplotlib、Pydantic 或 HTTP 库版本。

### 1. 克隆私有仓库

~~~powershell
git clone https://github.com/hanxiangli666/arc-prize-2026-arc-agi-3.git
Set-Location arc-prize-2026-arc-agi-3
~~~

获得仓库访问权限不等于获得比赛访问权限。每位贡献者都必须单独加入 Kaggle 比赛并接受比赛规则。

### 2. 下载比赛包

安装并登录 Kaggle CLI 后运行：

~~~powershell
New-Item -ItemType Directory -Path data\raw -Force
kaggle competitions download -c arc-prize-2026-arc-agi-3 -p data\raw
Expand-Archive -LiteralPath data\raw\arc-prize-2026-arc-agi-3.zip -DestinationPath data\raw\extracted -Force
~~~

不要提交 Kaggle 凭据、<code>.env</code> 文件、下载的压缩包或解压后的比赛数据。

### 3. 创建 Python 环境

安装 uv 和 Python 3.12 后运行：

~~~powershell
uv venv .venv --python 3.12
.\.venv\Scripts\python.exe -m ensurepip --upgrade
.\.venv\Scripts\python.exe -m pip install --upgrade pip
~~~

安装已固定的一般依赖和比赛包内的官方 toolkit wheels：

~~~powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-local.txt
.\.venv\Scripts\python.exe -m pip install --force-reinstall --no-deps .\data\raw\extracted\arc_agi_3_wheels\arcengine-0.9.3-py3-none-any.whl .\data\raw\extracted\arc_agi_3_wheels\arc_agi-0.9.8-py3-none-any.whl
~~~

### 4. 验证导入

~~~powershell
.\.venv\Scripts\python.exe -c "import arc_agi, arcengine; print(arc_agi.__file__); print(arcengine.__file__)"
~~~

### 5. 验证项目脚本

~~~powershell
.\.venv\Scripts\python.exe -m py_compile src\score_utils.py src\inspect_public_games.py src\run_random_smoke.py src\render_recording.py
~~~

<a id="zh-commands"></a>

## 当前常用命令

### 生成公开游戏清单

~~~powershell
.\.venv\Scripts\python.exe src\inspect_public_games.py
~~~

当前比赛包预期得到的总体清单：

- 25 个公开游戏；
- 183 个公开关卡；
- 所有公开关卡的人类基线动作总数为 17,135。

### 运行确定性随机 smoke baseline

~~~powershell
.\.venv\Scripts\python.exe src\run_random_smoke.py --game ls20 --steps 20 --seed 0 --out outputs\runs\random_smoke_ls20_seed0.json
~~~

该命令用于验证连通性和可复现性，不是具有竞争力的策略。

### 渲染 recording 中的一帧

~~~powershell
.\.venv\Scripts\python.exe src\render_recording.py --recording <recording.jsonl> --frame-index 0 --out outputs\figures\frame0.html
~~~

<a id="zh-experiments"></a>

## 实验规范

每个实验都必须能追溯到一个明确假设和一份保存的结果。

### 必填实验记录

~~~text
实验 ID：
日期：
代码提交：
研究问题：
假设：
环境集合：
随机种子：
策略或配置：
动作预算：
运行时间预算：
指标：
结果：
失败案例：
解释：
下一项实验：
产物：
~~~

### 最低指标要求

- 尝试的游戏数量；
- 完成的关卡数量；
- 总动作数和每关动作数；
- reset 次数；
- 非法或失败动作数；
- 单个游戏得分和总体得分；
- 墙钟运行时间；
- 需要时记录峰值内存；
- 随机种子；
- 使用模型时记录模型名称和解码参数；
- recording 与 scorecard 路径。

### 评估纪律

- 把本地公开游戏结果与 Kaggle 排行榜结果分开记录。
- 不能把公开游戏得分当作隐藏游戏泛化能力的证据。
- 比较方法时应使用相同的游戏、seed、预算和包版本。
- 保留负面结果和失败样例。
- 用消融实验判断究竟哪个组件带来了改进。
- 随机实验需要重复运行。
- 记录环境、模型、提示词、软件包和硬件版本的变化。
- 检验泛化假设时优先使用保留的公开游戏。
- 避免反复根据 Kaggle Public Leaderboard 反馈调参。

<a id="zh-collaboration"></a>

## 协作流程

### Git 工作流

1. 开始工作前拉取最新 <code>main</code>。
2. 创建目标单一的分支，例如 <code>experiment/action-probing</code> 或 <code>docs/scoring-notes</code>。
3. 每个 commit 只包含一个逻辑改动。
4. 相关时，在 commit 或 pull request 中写明实验 ID 或 issue 编号。
5. 重要算法改动合并前先发起 pull request 审查。
6. Pull request 描述需要包含复现命令和结果产物。
7. 仅在针对性验证通过后合并。

### 建议的研究分工

| 工作方向 | 典型产物 |
| --- | --- |
| 基准研究 | 规则摘要、来源链接、评分核验和开放问题。 |
| 环境分析 | 对象标注、动作映射、转移假设和失败案例。 |
| Agent 工程 | 策略、规划器、记忆系统、动作校验和运行时间控制。 |
| 评估 | 可复现运行、消融实验、指标表和回归检查。 |
| Kaggle 打包 | 离线 Notebook、附加依赖、运行时间审计和提交记录。 |

### 数据与访问纪律

- 密钥只保存在被 Git 忽略的环境文件中。
- 下载的比赛数据不得提交到 Git。
- 私有仓库权限只授予经过授权的官方队伍成员。
- 不得在不同 Kaggle 队伍之间私下共享比赛代码或数据。
- 任何公开发布前都要检查 Notebook 可见性和许可证。

<a id="zh-baseline"></a>

## 当前基线

### 公开数据清单

- 公开环境：<code>25</code>。
- 公开关卡：<code>183</code>。
- 公开关卡人类基线动作总数：<code>17,135</code>。

详细清单保存在 [<code>docs/public_games_inventory.md</code>](docs/public_games_inventory.md)。

### 随机 smoke 结果

已验证配置：

- 请求的游戏：<code>ls20</code>；
- 实际解析到的环境：<code>ls20-9607627b</code>；
- seed：<code>0</code>；
- 请求动作数：<code>20</code>；
- 初始 frame 尺寸：<code>[1, 64, 64]</code>；
- 完成关卡：<code>0 / 7</code>；
- 总动作数：<code>20</code>；
- 得分：<code>0.0</code>。

受 Git 管理的摘要保存在 [<code>outputs/runs/random_smoke_ls20_seed0.json</code>](outputs/runs/random_smoke_ls20_seed0.json)。

解释：环境加载、动作循环、轨迹记录和评分链路能够运行。随机选择动作没有完成任何关卡，也不能证明系统具备智能行为。

<a id="zh-risks"></a>

## 已知风险与开放问题

### 基准风险

- 公开演示环境比私有评估游戏更容易，而且存在分布差异。
- 游戏专属启发式方法可能制造具有误导性的公开成绩。
- 稀疏反馈使目标发现变得困难。
- 长轨迹会造成记忆和上下文压力。
- 动作效率分数采用平方，低效探索会受到明显惩罚。
- 不可逆动作可能破坏信息或迫使 Agent reset。

### 工程风险

- 本地软件包版本可能与 Kaggle 内置版本发生漂移。
- 本地可运行的 Agent 可能因为缺少资源而在离线 Kaggle Notebook 中失败。
- 模型推理过慢可能超过 9 小时限制。
- 原始 frame 历史可能超出模型上下文或内存上限。
- 非确定性实验可能掩盖回归。
- 当前仓库还没有完整自动化测试套件，现阶段只有编译检查和 smoke 检查。

### 研究问题

- 怎样用最少动作区分可控对象与环境自身运动？
- 哪种紧凑状态表示最容易迁移到未知游戏？
- 每次探索都会降低动作效率时，Agent 应怎样衡量信息价值？
- 尚未完成任何关卡之前，怎样对候选目标排序？
- 面对不可逆转移和稀疏反馈，哪种搜索策略表现最好？
- 需要保留多少记忆，哪些信息可以安全压缩？
- 小型模型能否改进假设生成，同时不过度占用运行时间？
- 哪些改进能够通过 leave-one-game-out 评估？
- 如果公开文档的表述仍不一致，最终 Kaggle 评估器实际采用哪个单关得分上限？

<a id="zh-glossary"></a>

## 术语表

| 术语 | 在本项目中的含义 |
| --- | --- |
| Action 动作 | 提交给环境的一条离散命令。 |
| Action budget 动作预算 | 允许或计划执行的最大环境交互次数。 |
| Agent 智能体 | 负责观察、推理、记忆、规划和行动的完整系统。 |
| Belief state 信念状态 | Agent 对隐藏规则和环境状态形成的、带有不确定性的当前模型。 |
| Environment 环境 | 一个 ARC-AGI-3 交互游戏。 |
| Frame 帧 | 环境返回的一次网格观察及相关元数据。 |
| Generalization 泛化 | 成功适应开发阶段从未见过的环境。 |
| Goal acquisition 目标习得 | 推断哪种未来状态代表成功或进展。 |
| Harness 运行框架 | 把模型或策略与观察、记忆、工具和动作连接起来的外围系统。 |
| Level 关卡 | 一个环境中的连续阶段。 |
| Observation 观察 | Agent 在某一步可以获得的信息。 |
| Policy 策略 | 根据当前历史或状态选择下一动作的机制。 |
| RHAE | Relative Human Action Efficiency，相对人类动作效率评分框架。 |
| Scorecard 计分卡 | 记录动作、完成关卡和分数的结构化数据。 |
| Trajectory 轨迹 | 按顺序排列的观察、动作和结果。 |
| Transition model 转移模型 | 预测执行动作后下一状态的模型。 |
| World model 世界模型 | 对对象、规则、动态规律和可能结果的紧凑表示。 |

## 项目原则

1. 每项结论都要有真实 frame、trajectory、scorecard 或排行榜证据。
2. 从可解释、可复现的实验开始。
3. 保留失败结果，因为失败会约束后续假设。
4. 区分环境链路可用与 Agent 具备能力。
5. 区分公开游戏表现与隐藏游戏泛化能力。
6. 只有较小基线暴露了明确限制后，才增加复杂度。
7. 把 Kaggle 提交视为稀缺实验，并记录完整来源。
8. 涉及提交、公开发布、许可证或奖金的决定前，重新核实官方规则。
