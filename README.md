# 水族逆向分析

水族计算器逆向工程，分析三个主流水族计算器网站的算法与架构，并复刻修正版。

## 项目结构

```
├── 001-omni水族箱玻璃厚度/     ← Omni Calculator 逆向
├── 002-aquariummath玻璃厚度/   ← AquariumMath 分析与修正
└── 003-aquacalcs中文镜像/      ← AquaCalcs 全站汉化
```

## 001 — Omni Calculator 逆向

**目标**：https://www.omnicalculator.com/other/aquarium-glass-thickness

- 从 `__NEXT_DATA__` 中提取完整公式定义
- 20 个方程式、27 个变量、34 条公式变体
- 通过 GraphQL 接口验证数据来源
- 制作带逐步推导的复刻版计算器

**核心公式**：`t = (√10/1000) × √(β × H³ / σ_allow)`

## 002 — AquariumMath 分析与修正

**目标**：https://aquariummath.com/calculators/glass-thickness

- 分析站点全部 13 个计算器和 35 种鱼类数据库
- **发现并修正原站公式错误**：原站将长度 L² 错误地乘入公式
- 制作修正版计算器，使用正确的平板弯曲理论

**Bug 示例**：48" 缸原站算出 777mm → 修正后约 6mm

## 003 — AquaCalcs 中文镜像

**目标**：https://aquacalcs.com

- 完整下载并汉化全部 15 个页面
- 修复链接为本地相对路径
- 缺失页面指向原站
- 保留完整功能（计算引擎 + Chart.js 图表）

## 三站对比

| | Omni Calculator | AquariumMath | AquaCalcs |
|---|---|---|---|
| 计算器数 | 300+ | 13 | 10 |
| 后端 | GraphQL + 数据库 | 纯前端 | 纯静态 |
| 公式正确性 | ✅ | ⚠️ 有 bug | ✅ |
| 透明度 | 低（混淆） | 中（压缩） | 高（源码可见） |

## 使用方式

每个子目录下双击 HTML 文件即可在浏览器中打开使用。
