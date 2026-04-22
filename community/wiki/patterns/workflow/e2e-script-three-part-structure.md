# Pattern: 联调脚本三段式结构

> 端到端联调脚本每个场景必须包含完整的三段式结构，缺一不可。
> 来源：Maiya V1.5 步骤18联调脚本实践，Verifier发现场景9/10结构不完整。

## 问题

联调脚本中后期的场景（如模板选择、迭代修改）容易退化成只有验证要点的形式，缺少输入参数模板和预期输出。导致：
- 联调时无法直接使用，需要回头补充
- 不同场景的完整度不一致，联调效率低
- 新参与的同学无法自行执行

## 三段式结构定义

### 1. 输入参数模板

```typescript
// API请求参数模板
POST /api/agent/generate_page
{
  "pageId": "page_test_001",
  "prompt": "具体提示词",
  "mode": "page",
  "expectedBaseVersion": 0
}
```

**要求**：
- 包含完整的API路径和HTTP方法
- Body中每个字段都有示例值
- 标注哪些字段是必填/可选
- 多步骤场景为每一步都提供输入模板

### 2. 预期输出

```typescript
// 预期响应结构
{
  "pageId": "page_test_001",
  "mode": "page",
  "stage": "awaiting_plan_confirm",
  "planVersion": 1,
  "structureDraftId": "sd_xxx",
  "traceId": "trace_xxx"
}
```

**要求**：
- 包含关键返回字段的预期值
- 标注哪些字段必须有值（非null）
- 多步骤场景为每一步都提供预期输出
- 错误场景提供预期错误码和错误信息

### 3. 验证要点

```markdown
验证要点：
1. 模糊需求不直接生成成品页，先进入澄清流程
2. 返回的 clarificationQuestions 非空
3. V1 核心字段（pageDraft, draftId, resultVersion）都存在
4. 未确认规划前不会进入骨架生成
```

**要求**：
- 编号列表，每条一个验证点
- 验证点必须可操作（可检查的断言）
- 不允许模糊表述（如"功能正常"→ 应写"返回stage=awaiting_plan_confirm"）

## 反模式

### 反模式1：只有验证要点

```typescript
/**
 * 场景9：模板选择链路
 * 验证要点：
 *   1. 模板面板展示可用模板列表
 *   2. 选择模板后系统生成子组件列表
 */
```

**问题**：缺少输入/输出，联调人员不知道怎么触发这个场景，也不知道期望看到什么。

### 反模式2：输入输出不完整

```typescript
/**
 * 场景10：迭代链路
 * 输入：已有页面ID
 * 输出：迭代修改成功
 */
```

**问题**：没有具体的请求参数结构，也没有关键返回字段，等于没有输入输出。

## 与5维检查的关系

- 5维检查的"自动化映射"维度要求测试文件名+用例名，对联调脚本是 `integration_test` 类型
- 联调脚本的三段式结构使得验收矩阵中的 `integration_test` 验证方法可直接引用场景编号
- 场景完整度检查是5维检查"覆盖度"维度的补充

## 模板

```typescript
/**
 * 场景N：{场景名称}
 *
 * 场景描述：
 *   {一句话描述场景目标}
 *
 * 输入参数模板：
 *   Step 1: POST /api/xxx
 *   { JSON body }
 *
 *   Step 2: (如有后续步骤)
 *
 * 预期输出：
 *   Step 1 → { JSON response }
 *   Step 2 → { JSON response }
 *
 * 验证要点：
 *   1. {可操作的验证断言}
 *   2. ...
 */
export const scenarioN_description = '{场景名称}';
```
