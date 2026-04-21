## 固定区

- 角色: AgentFlow 主控 Agent，负责任务分解、调度、验证和经验沉淀
- 核心原则: 搜索先行、证据驱动、保守过滤、不扩范围、安全优先
- 工作风格: 简洁直接，先查后做，严格按协议执行

## 动态区

### 2026-04-13 | module:tools | type:pattern | abstraction:universal

markitdown 安装：`pip install 'markitdown[all]'`
需用户确认（pip 包名在白名单外，但 pip 工具本身在白名单内）
安装后验证：`python -c "from markitdown import MarkItDown; print('ok')"`
关键：convert_stream() 需二进制流，不支持文本流；输出面向 LLM 非人类阅读
confidence: 0.8

### 2026-04-13 | module:requirements | type:pitfall | abstraction:universal

需求分析时应按业务关键词精准搜索代码位置，而非全盘扫描泛化关键词
原因：泛化关键词匹配到多个不相关功能，导致分析范围扩大且不精准
做法：先从需求文档提取业务领域关键词 → 按关键词精确搜索代码 → 定位修改范围
confidence: 0.9

### 2026-04-13 | module:llm-coding | type:pattern | abstraction:universal

Karpathy LLM编程四原则已整合到 Wiki → [[karpathy-principles|concepts/karpathy-principles]]
confidence: 0.9

### 2026-04-13 | module:workflow | type:pitfall | abstraction:universal

EXECUTE阶段不查就执行陷阱已整合到 Wiki → [[execute-without-search|pitfalls/workflow/execute-without-search]]
confidence: 0.95
validations: 2

### 2026-04-13 | module:workflow | type:pitfall | abstraction:universal

REFLECT阶段容易遗漏：执行任务时使用的新模板/新规范，必须沉淀到Wiki
遗漏了将使用的模板写入Wiki，用户指出后才补上
教训：REFLECT时除了提取经验和创建Skill，还要检查"本次任务中使用了哪些新模板/新规范"
如果是从WebSearch获取的规范，更应该沉淀——否则下次还要再搜一遍
confidence: 0.9

### 2026-04-15 | module:maimai | type:pitfall | abstraction:project

maimai 圈子双架构陷阱：
- 同事圈(company_circle)在 rn/page/gossip/pages/company_circle/，数据来自 circleTop.core_area_data_list
- 组合圈/实习圈(company-circle)在 rn/page/content/pages/company-circle/，数据来自 API 的 combo_circle_top_info
- 修改实习圈功能时，必须从 CombinationListStore 的 API 响应处理函数追踪数据来源，不能用同事圈的数据字段
- 踩坑：首次实现错误地用了同事圈的 core_area_data_list，用户纠正后才改为 combo_circle_top_info
confidence: 0.95
validations: 1

### 2026-04-15 | module:react | type:pitfall | abstraction:universal

React 子组件事件处理：永远通过 callback props 从父组件传递事件处理器，禁止在子组件中复制导航/路由逻辑
原因：在 CombinationListHeader 中复制了 handleEntranceClick（含 MMTrack + MMNative.openSchema），用户指出应统一写在父组件 VajraPositionV3 通过 props 传回调
做法：子组件只负责渲染和触发回调（onEntranceClick?.(item)），父组件负责业务逻辑（埋点+导航）
confidence: 0.95
validations: 1

### 2026-04-13 | module:enforcement | type:pattern | abstraction:universal

规则执行保障三层架构：短规则 + 详细技能 + 守卫技能
1. Layer 1: ~/.claude/rules/ — 铁律，每次对话自动加载，极简措辞
2. Layer 2: ~/.agent-flow/skills/pre-flight-check/ — 完整5步Procedure，指导"怎么做"
3. Layer 3: ~/.agent-flow/skills/subtask-guard/ — 子任务执行守卫，4步搜索防止跳过
核心原则："文档定义 ≠ 规则执行"，需要结构化强制机制
confidence: 0.9

### 2026-04-13 | module:requirement | type:pitfall | abstraction:universal

需求解析到代码修改缺少交互确认环节：
1. Agent 读完需求后直接假设理解了需求，没有逐项向用户确认
2. 正确流程：需求拆解为变更点(CP1,CP2,...) → 逐项确认理解 → 逐项确认代码映射
3. 两个确认点都不能跳过：(a)确认"做什么" (b)确认"改哪里"
4. 绝不能批量确认，必须逐项确认
confidence: 0.95

### 2026-04-13 | module:requirement | type:pitfall | abstraction:universal

需求分析时未精准定位代码，导致全项目扫描效率极差：
1. 需求文档提到的业务实体词，必须用这些词精准搜索代码
2. 直接做全项目扫描而不是分层递进搜索 = 效率极差
3. 正确做法：L1精确→L2模糊→L3路由→L4全局(最后手段)
4. 必须生成代码影响地图，明确标记需修改/可能影响/无关的代码
confidence: 0.9

### 2026-04-13 | module:workflow | type:pattern | abstraction:universal

文档驱动思维链已整合到 Wiki → [[thinking-chain-guidelines|concepts/thinking-chain-guidelines]]
confidence: 0.85

### 2026-04-13 | module:tools | type:pattern | abstraction:universal

markitdown 安装：`pip install 'markitdown[all]'`
需用户确认（pip 包名在白名单外，但 pip 工具本身在白名单内）
安装后验证：`python -c "from markitdown import MarkItDown; print('ok')"`
关键：convert_stream() 需二进制流，不支持文本流；输出面向 LLM 非人类阅读
confidence: 0.8

### 2026-04-13 | module:requirements | type:pitfall | abstraction:universal

需求分析时应按业务关键词精准搜索代码位置，而非全盘扫描泛化关键词
原因：泛化关键词匹配到多个不相关功能，导致分析范围扩大且不精准
做法：先从需求文档提取业务领域关键词 → 按关键词精确搜索代码 → 定位修改范围
confidence: 0.9

### 2026-04-13 | module:llm-coding | type:pattern | abstraction:universal

Karpathy LLM编程四原则已整合到 Wiki → [[karpathy-principles|concepts/karpathy-principles]]
confidence: 0.9

### 2026-04-13 | module:workflow | type:pitfall | abstraction:universal

EXECUTE阶段不查就执行陷阱已整合到 Wiki → [[execute-without-search|pitfalls/workflow/execute-without-search]]
confidence: 0.95

### 2026-04-13 | module:workflow | type:pitfall | abstraction:universal

REFLECT阶段容易遗漏：执行任务时使用的新模板/新规范，必须沉淀到Wiki
遗漏了将使用的模板写入Wiki，用户指出后才补上
教训：REFLECT时除了提取经验和创建Skill，还要检查"本次任务中使用了哪些新模板/新规范"
如果是从WebSearch获取的规范，更应该沉淀——否则下次还要再搜一遍
confidence: 0.9

### 2026-04-15 | module:maimai | type:pitfall | abstraction:project

maimai 圈子双架构陷阱：
- 同事圈(company_circle)在 rn/page/gossip/pages/company_circle/，数据来自 circleTop.core_area_data_list
- 组合圈/实习圈(company-circle)在 rn/page/content/pages/company-circle/，数据来自 API 的 combo_circle_top_info
- 修改实习圈功能时，必须从 CombinationListStore 的 API 响应处理函数追踪数据来源，不能用同事圈的数据字段
- 踩坑：首次实现错误地用了同事圈的 core_area_data_list，用户纠正后才改为 combo_circle_top_info
confidence: 0.95

### 2026-04-15 | module:react | type:pitfall | abstraction:universal

React 子组件事件处理：永远通过 callback props 从父组件传递事件处理器，禁止在子组件中复制导航/路由逻辑
原因：在 CombinationListHeader 中复制了 handleEntranceClick（含 MMTrack + MMNative.openSchema），用户指出应统一写在父组件 VajraPositionV3 通过 props 传回调
做法：子组件只负责渲染和触发回调（onEntranceClick?.(item)），父组件负责业务逻辑（埋点+导航）
confidence: 0.95

### 2026-04-13 | module:enforcement | type:pattern | abstraction:universal

规则执行保障三层架构：短规则 + 详细技能 + 守卫技能
1. Layer 1: ~/.claude/rules/ — 铁律，每次对话自动加载，极简措辞
2. Layer 2: ~/.agent-flow/skills/pre-flight-check/ — 完整5步Procedure，指导"怎么做"
3. Layer 3: ~/.agent-flow/skills/subtask-guard/ — 子任务执行守卫，4步搜索防止跳过
核心原则："文档定义 ≠ 规则执行"，需要结构化强制机制
confidence: 0.9

### 2026-04-13 | module:requirement | type:pitfall | abstraction:universal

需求解析到代码修改缺少交互确认环节：
1. Agent 读完需求后直接假设理解了需求，没有逐项向用户确认
2. 正确流程：需求拆解为变更点(CP1,CP2,...) → 逐项确认理解 → 逐项确认代码映射
3. 两个确认点都不能跳过：(a)确认"做什么" (b)确认"改哪里"
4. 绝不能批量确认，必须逐项确认
confidence: 0.95

### 2026-04-13 | module:requirement | type:pitfall | abstraction:universal

需求分析时未精准定位代码，导致全项目扫描效率极差：
1. 需求文档提到的业务实体词，必须用这些词精准搜索代码
2. 直接做全项目扫描而不是分层递进搜索 = 效率极差
3. 正确做法：L1精确→L2模糊→L3路由→L4全局(最后手段)
4. 必须生成代码影响地图，明确标记需修改/可能影响/无关的代码
confidence: 0.9

### 2026-04-13 | module:workflow | type:pattern | abstraction:universal

文档驱动思维链已整合到 Wiki → [[thinking-chain-guidelines|concepts/thinking-chain-guidelines]]
confidence: 0.85
