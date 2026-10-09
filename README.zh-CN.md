# baquant-pit

[English](README.md) | **简体中文**

面向 AI 金融研究的 Point-in-Time（PIT，时点可见性）与时间语义基础设施。

**当前状态：PRIVATE IMPLEMENTATION CANDIDATE / PRE-RELEASE（私有实现候选 / 预发布）。**

最小原语运行时已经实现 private v1 语义，包括：显式 aware datetime 的 UTC 规范化与固定 UTC 文本格式、带强制 cutoff、起止日期均包含的不可变日期窗口、带边界限制的类型化 canonical bytes/text 与 SHA-256、原始 bytes 的精确 SHA-256，以及常规文件内容的流式 SHA-256。运行时代码仅依赖 Python 标准库。要求 Python 3.12 或更高版本；当前版本仍为 `0.0.0.dev0`。

该实现依据已经合并到 baquant-pit 的合同、规范文档与 synthetic golden vectors 独立编写，没有查阅或复制私有 BAquant 的实现源码。当前不声明 BAquant 兼容性（`NOT_CLAIMED`），公共 API 兼容性也尚未建立（`NOT_ESTABLISHED`）。

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

`DateWindow` 保存起止日期均包含的日期范围，以及已经规范化为 UTC 的 cutoff。它本身不是 canonical input。这些字段不赋予日历、交易所交易时段或数据覆盖范围的权威语义。Canonical 输入只接受规范明确支持的 Python 精确类型，不进行隐式类型转换，也不会使用 `str()` / `repr()` 回退。`BaquantPITError` 暴露稳定的 `.error_id` 与固定安全文本；temporal、canonical 和 raw integrity 分别有轻量子异常类。

## 最小 as-of 演示

假设某条 observation 明天发生了更新，那么今天做出的历史决策不能看到明天才出现的信息。这个完全 synthetic 的演示使用显式 cutoff：naive latest 会选择 `obs-003`，而正确的 as-of 视图只能看到 `obs-001`，并排除未来的 `obs-002` / `obs-003`。

```sh
python examples/minimal_asof_demo.py
python examples/minimal_asof_demo.py --json
```

详细说明见 [synthetic 时间线、inclusive cutoff 与 demo 边界](docs/demos/minimal-asof-demo-v1.md)。选择规则只存在于示例中，不会新增 package-level reader API。

在虚拟环境中运行本地验证：

```sh
python -m venv .venv
# 使用当前平台的标准方式激活虚拟环境。
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest
```

测试明确区分“声明式资产的一致性检查”和“真实运行时 API 对冻结 golden 期望的执行验证”。所有 golden vector 都在 [runtime coverage table](docs/implementation/golden-runtime-coverage-v1.json) 中有明确记账。概念性的 leap second 和 Python dict 构造前的重复 key 不会被伪造成可执行输入。原生 FIFO 与 symlink 测试只在宿主平台支持时执行；权限错误与读取失败通过受控方式验证真实文件 API 的错误映射。测试数据仅使用 synthetic 值和临时文件。当前实现状态见 [implementation status](docs/implementation/minimal-primitives-v1.md)。

[minimal contract](contracts/minimal-primitives-v1.json) 会在 runtime conformance 通过后记录实现已经存在。冻结的 [specifications](docs/specs/compatibility-and-versioning-v1.md) 与 golden assets 保留其设计阶段的状态文字和输入描述，其语义与期望输出没有因为运行时实现而改变。早期设计范围中“runtime 尚未实现”的说明属于当时的 specification task；当前实际状态以实现标志和 implementation 文档为准。

当前仓库**没有** production PIT reader、vintage engine、PIT grade、TrustSnapshot、applicability classification、database、provider adapter、manifest registry、safe-root policy、atomic publication、brokerage 或 trading 功能。文件哈希会跟随指向普通文件的链接，并且只对内容做摘要；它不提供锁、不可变快照、TOCTOU 防护或真实性保证。当前实现候选也不代表 production readiness、scientific acceptance 或 public API stability。

baquant-pit 是 **market-neutral** 的基础设施。它的原语不会授权或暗示对任何特定交易所、证券市场、资产类别或 Provider 的支持。市场特定规则应该由下游 consumer 实现，而不是写入这个核心库。私有市场数据、专有策略和竞赛资产都不包含在本项目中。历史来源范围记录在 [origin and authority](docs/ORIGIN_AND_AUTHORITY.md)。

同一套冻结的 v1 测试会在 Windows 与 Ubuntu/Linux 的 Python 3.12 环境上运行。跨平台覆盖与宿主边界见 [portability coverage and host boundaries](docs/implementation/cross-platform-conformance-v1.md)。原生 symlink 与 FIFO 的创建能力取决于宿主环境，但 canonical、temporal 和 hash 核心语义必须在两个平台上都通过。

更多文档：

- [extraction plan](docs/BAQUANT-PIT-PUBLIC-EXTRACTION-PLAN-V1.md)
- [public/private boundary](docs/PUBLIC_PRIVATE_BOUNDARY.md)
- [architecture](docs/ARCHITECTURE.md)
- [origin and authority](docs/ORIGIN_AND_AUTHORITY.md)
- [future release checklist](docs/PUBLIC_RELEASE_AUDIT_CHECKLIST.md)

当前**没有授予任何再分发或开源许可**。仓库仍保持 PRIVATE，license 状态未改变，也没有授权 release 或 package publication。任何合并以及未来的公开发布，都需要单独的 Owner 授权。
