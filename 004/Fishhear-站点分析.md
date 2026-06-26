# Fishhear.com — 站点分析

> 分析日期：2026-06-27  
> 目标地址：https://fishhear.com  
> 作者：18 年经验的水族爱好者，个人项目  
> 技术栈：纯静态 HTML + 自研 vanilla JS + 自定义 CSS

---

## 一、站点定位

Fishhear 是一个**极简水族计算器 + 博客**。由一个 18 年经验的鱼友独立打造。

Slogan：*"Built by an aquarist, not a marketing team."*

核心卖点：
- **No accounts. No ads.**
- 玻璃厚度补偿（从外尺寸扣掉玻璃厚度得出真实水量）
- 90% 实际装水量（扣除底砂和装饰）
- 放养量 sanity check
- CSV/打印/复制 导出
- i18n 多语言 + 语音播报
- 仅 3 种缸型（矩形/圆柱/球形），不贪多

---

## 二、计算器

### 2.1 体积计算器（主页 `/`）

**公式**：
```
V_gross(L) = L×W×H × 0.001        (矩形)
           = π×(D/2)²×H × 0.001  (圆柱)
           = 4/3×π×(D/2)³ × 0.001 (球形)

V_net = V(L - 2t, W - 2t, H - t)  // 扣掉玻璃厚度
V_real = V_net × 0.90              // 90% 实际装水量

放养量 = V_real(US gal) × 1 inch  // 1寸鱼/加仑
```

**输入**：
- 长度/宽度/高度（cm / mm / in 切换）
- 玻璃厚度（mm，可选）

**输出**：
- 实际水量（L / UK gal / US gal）
- 毛容积（对比参考）
- 放养建议（适合多少英寸长度的小型群游鱼）

### 2.2 喂食计算器 (`/feeding-calculator`)

**功能**：28+ 种鱼类的喂食量和频率建议

包含 5 条喂食法则：
1. 只喂鱼在 2 分钟内能吃完的量
2. 每周停食 1 天让消化系统休息
3. 不同鱼种需要不同类型食物
4. 小鱼一天多次，大鱼一天一次
5. 观察鱼腹——吃饱后微鼓即可

---

## 三、技术架构

```
fishhear.com/
├── index.html              ← 首页（体积计算器）
├── feeding-calculator/     ← 喂食计算器
├── blog/
├── stocking-math/          ← 放养数学（文章）
├── cycling-without-fish/   ← 无鱼循环（文章）
├── choosing-first-aquarium/← 选购指南（文章）
├── about/
├── contact/
├── style.min.css           ← 65KB 自定义 CSS
├── main.min.js             ← 10KB 通用 JS
├── calculator.min.js       ← 12KB 体积计算器
├── feeding.min.js          ← 26KB 喂食计算器
└── i18n-voice.min.js       ← 9KB 多语言+语音
```

### 技术特点

| 项目 | 详情 |
|------|------|
| 框架 | **无** — 纯手工 vanilla JS |
| CSS | 自定义 65KB（无 Tailwind/Bootstrap） |
| 构建 | 手工 minify |
| i18n | 自研模块，支持多语言 |
| 语音 | Web Speech API 播报结果 |
| 导出 | CSV 下载 + 剪贴板复制 + 打印 |
| 后端 | **无** |
| 广告 | **无** |
| 分析 | Grow.me（`faves.grow.me`） |
| 动画 | CSS `fade-up` 滚动渐入 |

---

## 四、设计亮点

### 4.1 视觉设计

- **Hero 区**：巨大的鱼缸 SVG 插画（手绘风格）
- **渐入动画**：`.fade-up` class，滚动时元素从下方淡入
- **形状标签**：矩形/圆柱/球形的图标化切换
- **单位药丸**：cm / mm / in 三选一，视觉清晰
- **结果区**：大字号 + 单位后缀，一目了然
- **SVG tank fill**：结果区有一个小水箱图标，水位随结果变化

### 4.2 交互设计

- **Enter 键即算**：不用点按钮
- **即时反馈**：计算结果带微动画
- **重置按钮**：一键清空所有输入
- **玻璃厚度可选**：不影响基础计算

### 4.3 内容策略

- 计算器 + 教育文章互补
- 文章深入（放养数学、无鱼循环）
- 作者背书（18 年经验、4 个草缸、1 个海水微缸）

---

## 五、与其他站点对比

| | Fishhear | AquaCalcs | AquariumMath | Omni Calculator |
|---|---|---|---|---|
| 计算器数 | 2 | 32 | 13 | 300+ |
| 框架 | 无 | 无 | Next.js | Next.js |
| 广告 | 无 | AdSense | 站群互推 | 站内广告 |
| i18n | ✅ | ❌ | ❌ | ✅ |
| 语音播报 | ✅ | ❌ | ❌ | ❌ |
| 导出 | CSV+打印+复制 | ❌ | ❌ | ❌ |
| 设计感 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 代码可读 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ |
| 作者署名 | ✅ 实名 | ✅ | ❌ | ❌ |
| 玻璃厚度补偿 | ✅ 扣减 | ❌ | ⚠️ bug | ✅ |

---

## 六、calculator.min.js 核心架构

12KB 的纯 vanilla JS，结构清晰：

```javascript
state = {
  shape: 'rectangle'|'cylinder'|'sphere',
  unit: 'cm'|'mm'|'in',
  inputs: {},
  glassMm: 0,
  result: null
}

// 核心计算
calculate() → {
  grossL,        // 毛容积
  netL,          // 扣玻璃厚度后
  realFillL,     // ×0.90 实际水量
  ukGal, usGal,  // 加仑转换
  stockingInches // 1"/gal 估算
}

// 输出
renderResults()  // 更新 DOM
exportCSV()      // Blob 下载
copyResult()     // clipboard API
```

---

## 七、总结

Fishhear 是四个站中**设计最美、代码最干净**的一个：

- **极简但不简陋**：只做 2 个计算器，但每个做到极致
- **有温度的站**：作者署名、个人故事、18 年经验背书
- **技术克制**：无框架、无构建工具、无后端 — 但功能齐全
- **可访问性**：i18n 多语言 + 语音播报，考虑到了残障用户
- **导出功能**：CSV/打印/复制，实用性强

最适合作为"理想计算器站"的参考模板。
