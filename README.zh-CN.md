# baquant-pit

[English](README.md) | **简体中文**

面向 AI 金融研究的 Point-in-Time（PIT，时点可见性）与时间语义基础设施

**当前状态：PUBLIC / OPEN SOURCE / 0.1.0**

最小原语 v1 运行时已经实现，提供以下能力：

- 显式 aware datetime 的 UTC 规范化与固定 UTC 文本格式
- 带强制 cutoff、起止日期均包含的不可变日期窗口
- 带边界限制的类型化 canonical bytes/text 与 SHA-256
- 原始 bytes 的精确 SHA-256，以及常规文件内容的流式 SHA-256

运行时代码仅依赖 Python 标准库，要求 Python 3.12 或更高版本

当前验证覆盖 Windows 与 Ubuntu/Linux 的 Python 3.12，当前版本为 `0.1.0`（Alpha）

[当前发布状态](docs/release/RELEASE_STATE.md) 说明已实现范围、冻结的设计期规范及当前公开状态

公共 API 兼容性尚未建立（`NOT_ESTABLISHED`），也不声明 BAquant 兼容性（`NOT_CLAIMED`）

运行时依据 baquant-pit 的合同、规范与 synthetic golden vectors 独立编写，没有查阅或复制私有 BAquant 实现源码

## 安装并验证源码

在仓库根目录或完整解压的 source distribution 中，创建并激活 Python 3.12 虚拟环境，然后安装开发工具：

```sh
python -m venv .venv
# 使用当前平台的标准方式激活虚拟环境
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest
```

仅使用库时，`python -m pip install .` 可执行普通安装，无需 editable 模式

Wheel 包含运行时库和元数据，下文的示例与验证命令需要完整的源码仓库或 source distribution

## 最小原语

```python
from datetime import UTC, date, datetime

from baquant_pit import DateWindow, canonical_bytes, canonical_sha256

window = DateWindow(
    date(2032, 4, 4), date(2032, 4, 6), datetime(2032, 4, 5, tzinfo=UTC)
)
payload = {"cutoff": window.cutoff, "label": "synthetic"}
encoded = canonical_bytes(payload)
digest = canonical_sha256(payload)
```

`DateWindow` 保存起止日期均包含的日期范围，以及已经规范化为 UTC 的 cutoff；它本身不是 canonical input

这些字段不赋予日历、交易所交易时段或数据覆盖范围的权威语义

Canonical 输入只接受规范明确支持的 Python 精确类型，不进行隐式类型转换，也不会使用 `str()` / `repr()` 回退

`BaquantPITError` 暴露稳定的 `.error_id` 与固定安全文本，temporal、canonical 和 raw integrity 分别有轻量子异常类

## 最小 as-of 演示

假设某条 observation 明天发生更新，今天做出的历史决策就不能看到明天才出现的信息

按照上文从完整源码安装后，运行：

```sh
python examples/minimal_asof_demo.py
python examples/minimal_asof_demo.py --json
```

使用显式 synthetic cutoff 时，naive latest 会选择 `obs-003`，而 as-of 视图只能看到 `obs-001`，并排除未来的 `obs-002` / `obs-003`

详细说明见 [synthetic 时间线、inclusive cutoff 与 demo 边界](docs/demos/minimal-asof-demo-v1.md)

选择规则只存在于示例中，不会新增 package-level reader API

## 范围与一致性验证

baquant-pit 是 market-neutral 的基础设施，其原语不会授权或暗示对任何特定交易所、证券市场、资产类别或 Provider 的支持

市场特定规则由下游 consumer 实现，私有市场数据、专有策略和竞赛资产均不包含在本项目中

当前没有 production PIT reader、vintage engine、PIT grade、TrustSnapshot、applicability classification、database、provider adapter、manifest registry、safe-root policy、atomic publication、brokerage 或 trading 功能

文件哈希会跟随指向普通文件的链接，并且只对内容做摘要；它不提供锁、不可变快照、TOCTOU 防护或真实性保证

当前早期 Alpha 版本不代表 production readiness、scientific acceptance 或 public API stability

测试使用真实 API 验证冻结的 synthetic golden 期望，所有 golden vector 均在 [runtime coverage table](docs/implementation/golden-runtime-coverage-v1.json) 中明确记账

概念性的 leap second 和 Python dict 构造前的重复 key 不会被伪造成可执行输入

原生 FIFO 与 symlink 测试只在宿主支持时执行，权限错误与读取失败通过受控方式验证真实文件 API；测试仅使用 synthetic 值和临时文件

同一套冻结的 v1 测试在 Windows 与 Ubuntu/Linux 的 Python 3.12 环境运行，详见 [一致性验证范围与宿主边界](docs/implementation/cross-platform-conformance-v1.md)

核心 temporal、canonical 和 hash 语义必须在两个平台通过，原生文件系统能力导致的跳过会明确记账

从 [发布状态](docs/release/RELEASE_STATE.md) 开始，再查看 [架构](docs/ARCHITECTURE.md)、[最小合同](contracts/minimal-primitives-v1.json)、[规范](docs/specs/compatibility-and-versioning-v1.md)、[实现说明](docs/implementation/minimal-primitives-v1.md)、[内容边界](docs/PUBLIC_PRIVATE_BOUNDARY.md) 与 [来源及权威范围](docs/ORIGIN_AND_AUTHORITY.md)

本项目采用 [Apache License 2.0](LICENSE)，`0.1.0` 是首个公开开源版本，Owner 已接受历史提交身份公开并保留原有 Git 历史

项目仍处于早期 Alpha 阶段，不代表 public API stability、production readiness 或 BAquant compatibility
