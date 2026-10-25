# 来源与归纳边界

公开版只保留规则归纳和原始链接，未复制第三方 skill 全文、组件源码、付费资料或原始抓取目录。引用来源不代表作者认可本项目。Deityki 的个人参数属于可替换配置，不宣称为行业统一规范。

## 设计依据

下列来源在本项目形成过程中于 2026-10-11 或 2026-10-25 阅读或核对。链接可能变化，实施具体 API 时重新检查当前官方文档。已读正文不等于已运行组件或完成整站审计。

| 编号 | 来源 | 采用内容与边界 |
| --- | --- | --- |
| S01 | [UI Playbook · Button](https://uiplaybook.dev/play/button) | 动作语义、状态、焦点和加载尺寸；尺寸要求以现行标准复核 |
| S02 | [UI Playbook · Textfield](https://uiplaybook.dev/play/textfield) | 标签、帮助、错误、验证时机与只读状态；字段类型依平台与语义选择 |
| S03 | [UI Playbook · Tooltip](https://uiplaybook.dev/play/tooltip) | 非交互补充、焦点与关闭；没有采纳将 HTML title 视为通用无障碍替代的建议 |
| S04 | [Radix · Accessibility](https://www.radix-ui.com/primitives/docs/overview/accessibility) | 原语处理部分键盘、焦点与语义，调用方仍负责标签；不是整页认证 |
| S05 | [Practical Typography · Typography in ten minutes](https://practicaltypography.com/typography-in-ten-minutes.html) | 正文优先及文字尺度关系；英文行宽和作者字体偏好不通用 |
| S06 | [Utopia](https://utopia.fyi/) | 文字与间距的端点协调和连续尺度；没有宣称读完全部计算器或实现文档 |
| S07 | [Color.review](https://color.review/) | 前景与背景对比；其标准版本表述使用 W3C 当前说明校正 |
| S08 | [Inclusive Components · Cards](https://inclusive-components.design/cards/) | 标题、主链接、整卡点击与内容结构；旧代码需复核 |
| S09 | [Inclusive Components · Data Tables](https://inclusive-components.design/data-tables/) | 保留行列语义与比较关系，适配小屏；旧浏览器与 ARIA 方案不直接复制 |
| S10 | [Laws of UX](https://lawsofux.com/) | 首页中的分组、熟悉性与注意力等启发式；未阅读所有专题，不作为定量保证 |
| S11 | [W3C · Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) | WCAG 2.2 AA 目标尺寸、间距与例外；补充核对来源，不是目录原始条目 |
| S12 | [W3C · Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) | 文字对比及适用条件；补充核对来源，不是目录原始条目 |
| S13 | [UI Playbook · Motion](https://uiplaybook.dev/play/motion) | 目的、空间关系、反馈、复杂度与减少动态效果；时长仅作起点 |
| S14 | [Radix Colors 色阶用途](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale) | 12 阶语义、组件状态与实色背景前景例外；实际组合仍需对比检查 |
| S15 | [shadcn/ui Theming](https://ui.shadcn.com/docs/theming) | Nova 配置示例、语义 CSS 变量及浅深模式映射；未安装或运行项目 |
| S16 | [Motion React Transitions](https://motion.dev/docs/react-transitions) | tween、easeOut、以秒为单位的 duration；250ms 来自用户偏好，非库的通用默认 |
| S17 | [Lucide Guide](https://lucide.dev/guide/) | 开源图标、尺寸、线宽与无障碍文档入口；实施时另核对所用包与许可 |
| S18 | [react-resizable-panels 官方仓库](https://github.com/bvaughn/react-resizable-panels) | 可调整面板职责及 README；未对其全部 API 与交互逐项验证 |
| S19 | [dnd-kit 官方概览](https://dndkit.com/) | 拖拽、排序及多框架入口；实施时核对当前包与 API，不混用不同代示例 |
| S20 | [Zustand 官方仓库](https://github.com/pmndrs/zustand) | 共享状态 store、选择器与组件订阅示例；未实测应用，旧 getting-started/introduction 文档路径本次返回 404，改用官方仓库核对 |

## 工作流程启发

- [Lovart 首个项目流程](https://www.lovart.ai/docs/getting-started/design-your-first-project)
- [Lovart 参考素材与品牌配置](https://www.lovart.ai/docs/how-to-prompt/adding-references)
- [Lovart 局部编辑](https://www.lovart.ai/docs/edit-your-design/advanced-ai-editing)

以上用于归纳“用途与参考 → 首版 → 方向确认 → 局部迭代 → 交付”，不涉及其私有实现，也不证明生成质量。上述页面于本项目形成过程中阅读，未在每次发布时重测全部功能。

## 相关开源工作

- [Anthropic frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design)：相关视觉判断与文案原则的比较对象。
- [Vercel web-design-guidelines](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines)：相关 UI 规范检查的比较对象。
- [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)：相关设计知识检索的比较对象。
- [Impeccable](https://github.com/pbakaus/impeccable)：相关产品背景、规划与细化流程的比较对象。
- [Designeer](https://www.designeer.xyz/)：早期设计参考发现入口。

这些工作用于定位比较，不作为本项目生成效果更优的证据。它们各自的许可继续适用；本项目没有随包分发其实现。公开版不使用“发现或自动检查过的链接数量”宣传为“学完的设计资料数量”。
