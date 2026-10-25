# Brief to UI

把一句想法整理成完整的页面生成提示词，确认后出预览，再经过视觉确认与局部迭代，形成清晰、一致、可验证的中文业务后台界面。

An opinionated, configurable skill for turning a rough idea into a reviewable page-generation prompt, then a Chinese admin UI preview, with explicit approval before implementation.

作者：Deityki。许可证：[MIT](LICENSE)。当前版本：[0.2.0](VERSION)。

## 为什么做这个 skill

你可以只说“我想做一个后台，方便主管处理异常”。Brief to UI 会主动整理需求并研究参考，先生成一份可复制、可修改的完整页面生成提示词。你只需判断是否符合想法，确认或补充后才生成示例图；修改业务实现另需明确批准。

它优先服务中文业务后台、管理系统与内部工具。它重视成熟用语、清晰分组、适量容器和稳定的局部迭代；不会把更少卡片、更少颜色或更大留白自动当成更好的设计。

## 看一个例子

![后台首页 A 版，用户在本次比较中更偏好的方向](examples/admin-home/a-preferred.png)

这是一张使用模拟数据生成的静态示例图。一次比较中，用户更喜欢保留适量分区的 A 版，而不是移除所有外围卡片的 A2。完整案例、通用版对照和提示词记录见 [后台首页案例](examples/admin-home/README.md)。图像没有对应的已验证业务实现，也不是与其他开源 skill 的效果排名。

## 它如何工作

1. 整理需求：从简单描述中提炼人群、场景、痛点、1–3 项主任务、约束与完成标准。
2. 有针对性地研究：通常选 3–5 个相关参考，说明学习点与适用边界；已有研究足够时复用。
3. 确认提示词：助手补齐页面结构、内容与状态、视觉、交互和交付约束，标明关键假设，等你确认或补充。
4. 提供预览：提示词确认后生成示例图，重要动效补充可播放演示或交互原型。
5. 明确批准实现：确认提示词、选定图片与批准修改代码分别理解；已有批准在范围内持续有效。
6. 局部迭代：保持已认可的提示词与视觉基线，只改变有理由调整的部分。
7. 如实验收：分别说明提示词、预览、代码、验证、部署和发布状态。

不需要自己写专业提示词。完整输入与预期输出见 [一句想法到提示词的示例](examples/idea-to-prompt/README.md)，规则见 [页面生成提示词](skills/brief-to-ui/references/page-prompt.md)。

关键原则：任务与数据正确、分组与操作清晰，优先于追求装饰极简。详情见 [后台判断规则](skills/brief-to-ui/references/admin-patterns.md) 和 [协作流程](skills/brief-to-ui/references/collaboration.md)。

## 安装

核心 skill 是 `skills/brief-to-ui/` 文件夹，无需运行时或 API 密钥即可阅读规则。生成图片、访问网页和修改代码由所用 AI 工具提供，本仓库不捆绑这些能力。

Codex 本地安装示例：在本仓库根目录执行 PowerShell。若目标已存在，先比较版本，下面的命令会停止而不是覆盖。

```powershell
$skillSource = Join-Path (Get-Location) 'skills\brief-to-ui'
$skillTarget = Join-Path $env:USERPROFILE '.codex\skills\brief-to-ui'
if (Test-Path -LiteralPath $skillTarget) {
    throw '目标 skill 已存在，请先比较版本并备份'
}
New-Item -ItemType Directory -Path (Split-Path -Parent $skillTarget) -Force | Out-Null
Copy-Item -LiteralPath $skillSource -Destination $skillTarget -Recurse
```

让所用工具重新发现 skill，然后使用 `$brief-to-ui` 调用。其他支持 Agent Skills 的工具按其文档放置该文件夹；本版本尚未逐一验证所有工具。若已有相同用途的个人 skill，可选择其一，避免多套默认规则同时介入；安装不会删除任何现有 skill。

## 只需要这样开始

```text
使用 $brief-to-ui
我想做一个给运营主管使用的后台，主要处理项目异常和待审批事项
请先帮我整理需求、找参考，输出完整页面生成提示词
等我确认或补充后，再生成示例图
先不要修改代码
```

局部迭代可以这样说：

```text
选择 A 作为基线
请只改善表格行距和操作列对齐，保留现有导航、配色和分区
先给我看预览，确认后再修改实现
```

## 可配置的默认审美

公开版保留 Deityki 默认配置：Radix Colors、克制动效、成熟中文文案；新 React Web 项目默认 shadcn/ui Nova 与 Lucide，其他库按需引入。普通细边框、字号数量与动效参数属于默认偏好，不是行业统一要求。

可以直接描述自己的偏好，也可复制 [UI_PROFILE.example.md](UI_PROFILE.example.md) 为项目的 `UI_PROFILE.md`。已有技术栈与设计系统优先，不因采用本 skill 迁移框架或安装整套依赖。详细优先级见 [配置说明](skills/brief-to-ui/references/profiles.md)。

## 验证与局限

- [发布结构检查](scripts/validate_release.py) 使用 Python 3 标准库，检查包结构、本地引用、来源编号、示例尺寸与明显的本机路径泄漏；它不证明 UI 可用性或设计质量。
- [评测场景](evals/README.md) 覆盖模糊想法转提示词、修改与确认边界、既有框架、卡片取舍、必要文案与局部实现。场景已定义，尚无跨模型独立评测结果。
- 静态示例图不能证明精确色值、字号、0.5px 边框、键盘操作、性能、业务数据或动效已落实。

在仓库根目录运行：

```text
python scripts/validate_release.py
```

## 来源与贡献

规则是 Deityki 偏好与实践的整理，参考页面和相关开源工作列于 [来源说明](skills/brief-to-ui/references/sources.md)。本项目没有复制并分发其他 skill 的实现或组件源码。

欢迎通过具体任务、预览和用户反馈提出改进，贡献方式见 [CONTRIBUTING.md](CONTRIBUTING.md)。不要用更多禁止项替代对实际问题的解释。
