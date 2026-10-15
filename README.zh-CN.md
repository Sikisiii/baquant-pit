# baquant-pit

[English](README.md) | **简体中文**

**研究过去的决策，只应使用当时已经可知的信息**

面向 Point-in-Time 金融研究的 Python 基础工具

**当前状态：PUBLIC / OPEN SOURCE / 0.1.0** — 早期 Alpha

## 为什么需要它

回测时误用未来信息，结果可能看起来很好；baquant-pit 提供时间与哈希工具，并用离线示例展示这种错误

## 一个简单例子

假设某家公司公布了以下**合成数据**：

| 信息何时可用 | 公布的利润 |
| --- | --- |
| 6 月 20 日 | 1 亿元 |
| 8 月 10 日 | 修订为 7000 万元 |

评估 6 月 30 日的决策时，今天的最新值是 7000 万元，但当时只能知道 1 亿元；用后来的修订替代，就是前视偏差 / 未来数据泄漏（look-ahead bias / future-data leakage）

这只是概念示例，不是本库提供的财务数据集

## Point-in-Time 是什么意思

Point-in-Time（PIT）问的是：**截至选定的历史时刻，哪些信息已经可用？** 按这个条件看到的数据，就是 as-of 视图

8 月公布的 6 月报表，在 6 月尚不可用；调用方须提供可用时间，本库无法仅凭数值推断它

## 为什么 AI 金融研究也需要关心

研究 Agent 可能把文档与数据库的最新值拼成看似合理的历史答案，却夹带当时无人知晓的信息；答案听起来正确，也需要检查可用时间

这是项目的应用动机；v0.1.0 不包含 Agent 运行时、LLM 集成、检索系统或 RAG 流水线

## baquant-pit 目前提供什么

- 让时间戳使用明确的 UTC 表达：带时区 datetime 的规范化与固定 UTC 文本格式
- 显式保存截止时间与日期范围：不可变的 `DateWindow` 包含起止日期两端，不筛选记录
- 为支持的输入生成可重复的内容标识：确定性的类型化字节与文本编码（canonicalization），以及 SHA-256、原始字节和文件内容哈希

这些是可复用的基础工具，不是生产级 PIT reader 或修订数据库

## 30 秒演示

完成[安装](#安装与开发)后，对比直接取全部记录的最新值，与只选择截止时间之前或恰好在该时刻可用的记录：

```sh
python examples/minimal_asof_demo.py
python examples/minimal_asof_demo.py --json
```

关键输出：

```text
as_of: 2032-04-05T10:30:00.000000Z
naive latest: obs-003
point-in-time visible: obs-001
future observations excluded: obs-002, obs-003
```

选择逻辑只在示例中，不属于库的 API；详见[合成时间线与歧义规则](docs/demos/minimal-asof-demo-v1.md)

## 最小 Python 示例

记录截止时间并标识输入，不查询数据：

```python
from datetime import UTC, date, datetime

from baquant_pit import DateWindow, canonical_sha256

window = DateWindow(
    date(2032, 4, 4), date(2032, 4, 6), datetime(2032, 4, 5, tzinfo=UTC)
)
payload = {"cutoff": window.cutoff, "label": "synthetic"}
print(canonical_sha256(payload))
```

`DateWindow` 本身不是 canonical 输入；哈希用于识别内容，不能证明数据真实、来源可信或历史上已经可用

## 本项目不提供什么

- 生产级 PIT 数据库、完整的历史修订版本引擎（vintage engine）或市场数据服务
- 回测框架、交易日历、组合引擎、交易系统或券商集成
- 完整金融研究或 AI Agent 平台，也不保证回测正确或具备生产可用性

这些工具不绑定市场，不代表支持任何交易所、资产类别或数据提供方；私有数据、策略和竞赛资产均不包含在内

## 技术保证与边界

- 运行时仅依赖标准库，要求 **Python >=3.12**；已验证 **Windows 与 Ubuntu/Linux 上的 Python 3.12**，更高版本尚未验证
- 截止时间必须显式提供，不默认使用当前时间，也不赋予日历或数据覆盖范围的权威语义
- Canonical 输入限于精确支持的类型，有资源上限与稳定安全的错误标识；不隐式转换，也不以 `str()` / `repr()` 回退
- 文件原始哈希会跟随指向普通文件的链接，只处理内容；不提供锁、不可变快照、路径安全或检查与使用之间的竞态（TOCTOU）防护
- 真实 API 测试使用冻结的合成期望值（golden vectors）与临时文件；[覆盖表](docs/implementation/golden-runtime-coverage-v1.json)与[一致性指南](docs/implementation/cross-platform-conformance-v1.md)记录跳过情况

## 文档导航

- **开始使用**：[演示时间线](docs/demos/minimal-asof-demo-v1.md)与[当前发布状态](docs/release/RELEASE_STATE.md)
- **了解实现**：[架构](docs/ARCHITECTURE.md)、[合同](contracts/minimal-primitives-v1.json)、[规范](docs/specs/compatibility-and-versioning-v1.md)与[实现细节](docs/implementation/minimal-primitives-v1.md)
- **了解来源**：[公开与私有内容边界](docs/PUBLIC_PRIVATE_BOUNDARY.md)及[来源与权威范围](docs/ORIGIN_AND_AUTHORITY.md)

部分链接文档保留公开前的表述，状态见当前发布状态文档，语义以冻结规范为准

## 安装与开发

使用 Python 3.12 或更高版本：

```sh
git clone https://github.com/Sikisiii/baquant-pit.git
cd baquant-pit
python -m venv .venv
```

POSIX shell 使用 `. .venv/bin/activate` 激活，Windows PowerShell 使用 `.venv\Scripts\Activate.ps1`，然后安装：

```sh
python -m pip install .
```

示例需要源码仓库或源码分发包，wheel 仅含运行时与元数据；开发时在源码根目录运行：

```sh
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest
```

## 状态与兼容性

`0.1.0` 仍处于早期 Alpha，公共 API 兼容性尚未建立（**NOT_ESTABLISHED**），不声明 BAquant 兼容性（**NOT_CLAIMED**）

运行时依据本项目的合同、规范与合成向量独立编写，没有查阅或复制私有 BAquant 实现源码

## 许可证

[Apache License 2.0](LICENSE)
