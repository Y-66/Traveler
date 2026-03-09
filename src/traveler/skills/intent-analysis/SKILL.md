---
name: intent-analysis
description: 旅行意图分析技能 - 从用户自然语言中提取旅行意图、目的地、时间、人数、预算等结构化信息，为后续工作流步骤提供标准化输入。
license: MIT
metadata:
  version: "1.0.0"
  author: traveler-team
  tags: ["travel", "intent", "nlp", "extraction"]
---

# 旅行意图分析技能

从用户自然语言输入中提取结构化旅行信息，为工作流提供标准化数据。

## 适用场景

- 用户以自然语言描述旅行需求
- 需要从模糊描述中提取关键旅行参数
- 为后续规划步骤准备结构化输入

## 提取字段

必须从用户输入中提取以下信息（缺失的标记为 null）：

| 字段                 | 说明         | 示例                           |
| -------------------- | ------------ | ------------------------------ |
| destination          | 目的地       | "东京"、"巴黎"                 |
| origin               | 出发地       | "北京"、"上海"                 |
| start_date           | 出发日期     | "2026-04-01"                   |
| end_date             | 返回日期     | "2026-04-05"                   |
| days                 | 天数         | 5                              |
| travelers            | 旅行人数     | 2                              |
| budget_level         | 预算级别     | "budget" / "medium" / "luxury" |
| budget_amount        | 具体预算金额 | 10000                          |
| interests            | 兴趣偏好     | ["美食", "文化", "自然风光"]   |
| special_requirements | 特殊需求     | "带小孩"、"无障碍"、"素食"     |

## 输出格式

严格输出 JSON 格式，不要包含任何其他内容：

```json
{
  "destination": "东京",
  "origin": "北京",
  "start_date": "2026-04-01",
  "end_date": "2026-04-05",
  "days": 5,
  "travelers": 2,
  "budget_level": "medium",
  "budget_amount": null,
  "interests": ["美食", "文化"],
  "special_requirements": null,
  "summary": "从北京出发到东京的5天2人中等预算旅行，偏好美食和文化体验"
}
```

## 推断规则

1. 如果用户只说天数没说日期，日期设为 null
2. 如果用户没提预算，budget_level 默认 "medium"
3. 如果没提出发地，origin 设为 null
4. 如果没提人数，travelers 默认 1
5. 根据上下文推断 interests，例如"亲子游"推断 ["亲子", "主题乐园"]
