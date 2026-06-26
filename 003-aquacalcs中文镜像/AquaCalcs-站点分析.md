# AquaCalcs.com — 站点全貌分析

> 分析日期：2026-06-26  
> 目标地址：https://aquacalcs.com  
> 作者：Angelo Smith  
> 技术栈：纯静态 HTML + 自研轻量计算器引擎 + Chart.js

---

## 一、站点定位

AquaCalcs 是一个**纯静态水族计算器站**。No signup, no backend, no framework — 只有 HTML + CSS + 一个 12KB 的自研 JS 引擎。

Slogan：*"Free aquarium & fish keeping calculators. No signup, no guesswork."*

---

## 二、全部 10 个计算器

按 4 个分类组织：

### 缸体设置 (Tank Setup)
| # | URL | 名称 | 功能 |
|---|-----|------|------|
| 1 | `/tank-volume-calculator/` | 水族箱体积 | 计算缸体容积（加仑/升） |
| 2 | `/substrate-calculator/` | 底砂用量 | 底砂/沙/泥所需袋数 |
| 3 | `/aquarium-stand-weight/` | 缸体承重 | 满水+玻璃+底砂的总重量 |

### 水质化学 (Water Chemistry)
| # | URL | 名称 | 功能 |
|---|-----|------|------|
| 4 | `/co2-dosing-calculator/` | CO₂ 浓度 | pH+KH → 溶解 CO₂ (ppm) |
| 5 | `/ammonia-calculator/` | 氨毒性 | 温度+pH → NH₃ 游离氨比例 |
| 6 | `/water-change-calculator/` | 换水量 | 计算换水后的水质参数变化 |

### 鱼类放养 (Fish & Stocking)
| # | URL | 名称 | 功能 |
|---|-----|------|------|
| 7 | `/stocking-level-calculator/` | 放养密度 | 基于缸容和过滤的合理鱼量 |
| 8 | `/fish-feeding-calculator/` | 喂食量 | 根据鱼种和数量计算日粮 |

### 设备维护 (Equipment & Maintenance)
| # | URL | 名称 | 功能 |
|---|-----|------|------|
| 9 | `/aquarium-heater-calculator/` | 加热棒功率 | 温差→瓦数→推荐规格 |
| 10 | `/filter-flow-calculator/` | 过滤器流量 | GPH 需求和过滤类型 |

---

## 三、计算公式（摘录）

每个计算器的公式直接写在页面 HTML 的 `<script>` 标签中，完全透明：

### CO₂ 浓度
```javascript
co2 = 3 * kh * Math.pow(10, 7 - ph)
// 标准水族 CO₂ 公式（基于碳酸平衡）
```

### 加热棒功率
```javascript
diff = targetTemp - roomTemp
wattsPerGal = diff > 15 ? 5 : diff > 10 ? 4.5 : diff > 5 ? 4 : diff > 0 ? 3 : 2
watts = gallons * wattsPerGal
// 取最近的规格：25/50/75/100/150/200/250/300W
```

### 氨毒性
```javascript
// NH₃ 游离氨比例取决于温度和 pH
// 温度越高、pH 越高 → NH₃ 占比越大 → 毒性越强
```

---

## 四、技术架构

```
aquacalcs.com/
├── index.html              ← 首页 + 计算器导航
├── style.css               ← 全局样式 (12KB)
├── calculator.js           ← 共享计算器引擎 (12KB)
├── tank-volume-calculator/
│   └── index.html          ← 各自独立页面，内嵌公式
├── co2-dosing-calculator/
│   └── index.html
├── ...（10个计算器各一个目录）
└── category/
    ├── tank-setup/
    ├── water-chemistry/
    ├── fish-stocking/
    └── equipment-maintenance/
```

### 技术特点

| 层面 | 技术 |
|------|------|
| 框架 | **无框架** — 纯静态 HTML |
| 计算引擎 | **自研** `calculator.js`（12KB，可读源码） |
| 图表 | Chart.js (CDN) |
| 路由 | 静态目录（每个计算器一个文件夹） |
| 状态管理 | URL hash（`#ph=6.8&kh=4`） |
| 后端 | **无** |
| 数据库 | **无** |
| 构建工具 | **无**（手写 HTML） |
| 广告 | Google AdSense |
| Schema | JSON-LD (WebApplication + FAQPage + BreadcrumbList) |

---

## 五、calculator.js 引擎剖析

这是整个站点的核心。一个 **320 行、12KB** 的 IIFE 模块，提供了：

```javascript
window.initCalculator({
  calculate: function(inputs) { /* 公式 */ },
  validation: [{field:'ph', min:5, max:9, message:'...'}],
  canvasId: 'calc-chart'
});
```

### 引擎功能

| 模块 | 功能 |
|------|------|
| `readInputs(form)` | 自动读取 `<form>` 中所有 input/select |
| `validate(inputs, rules)` | required/min/max 校验 |
| `displayResults(results, container)` | 渲染结果行，自动格式化 |
| `renderChart(data, canvasId)` | Chart.js 图表渲染 |
| `saveToHash(inputs)` | 状态保存到 URL hash（可分享） |
| `loadFromHash(form)` | 页面加载时从 hash 恢复输入 |
| `debounce(fn, 500ms)` | 输入防抖自动重算 |

### 输出格式

```javascript
{
  results: [
    {label: 'CO2 (ppm)', value: 18.5, format: 'number', decimals: 1},
    {label: 'Status', value: 'Ideal Range', format: 'text'}
  ],
  chart: {
    type: 'bar',
    labels: ['Current', 'Target'],
    values: [18.5, 30]
  }
}
```

### 设计亮点

1. **极简 API**：每个计算器只需提供一个 `calculate(inputs)` 函数
2. **格式自动推断**：`currency`/`percentage`/`integer`/`number` 根据字段名自动判断
3. **URL 可分享**：所有输入保存在 hash 中，复制 URL 即可复现计算
4. **零依赖**（除了 Chart.js CDN）：无 npm/webpack/babel

---

## 六、三站对比

| | AquaCalcs | AquariumMath | Omni Calculator |
|---|---|---|---|
| **定位** | 轻量工具 | 实用工具站 | 专业计算平台 |
| **计算器数** | 10 | 13 | 300+ |
| **框架** | 无（纯静态） | Next.js | Next.js |
| **引擎** | 自研 12KB | 硬编码在各 chunk | 独立 engine 包 |
| **公式透明度** | ⭐⭐⭐⭐⭐ 完全可见 | ⭐⭐ 压缩在 chunk 中 | ⭐⭐⭐ SSR 注入 |
| **后端** | 无 | 无 | GraphQL + 数据库 |
| **图表** | Chart.js | 无 | 无 |
| **状态分享** | URL hash | 无 | 无 |
| **广告** | AdSense | 站群互推 | 站内广告 |
| **SEO** | JSON-LD 完整 | JSON-LD + RSC | 完善 |
| **代码量** | 极小（~50KB/页） | 中等（~200KB/页） | 大（~600KB/页） |
| **可维护性** | ⭐⭐⭐⭐⭐ 手写 HTML | ⭐⭐⭐ Next 工程化 | ⭐⭐ Monorepo |
| **公式正确性** | ✅（都是标准公式） | ⚠️ 玻璃厚度有 bug | ✅ |
| **适合学习** | ⭐⭐⭐⭐⭐ 最佳 | ⭐⭐⭐ | ⭐⭐ |

---

## 七、总结

### AquaCalcs 的核心竞争力

1. **极致的简单**：没有构建工具，没有框架，手写 HTML + 一个 12KB 引擎驱动全部 10 个计算器
2. **完全透明**：每个公式以可读 JS 直接写在页面源码中，任何人都能看懂
3. **URL 可分享**：输入参数保存在 hash 中，计算结果可以分享链接复现
4. **Chart.js 可视化**：结果附带柱状图，比纯文本更直观
5. **SEO 完善**：每个计算器有 WebApplication + FAQPage + BreadcrumbList 三套 Schema

### 与技术更"先进"的站点的对比

| 优势 | 劣势 |
|------|------|
| 无构建步骤，改完即上线 | 10 个计算器各自复制 HTML 模板 |
| 无 npm 依赖漏洞 | 无组件复用 |
| 页面极快（无 JS bundle 加载） | 无数据库，数据更新需改代码 |
| 对搜索引擎最友好（纯 HTML） | 无用户系统、无个性化 |
| 最适合学习和二次开发 | Chart.js CDN 是唯一外部依赖 |

### 最适合

- **学习计算器开发**：代码结构清晰、公式直接可见
- **快速搭建工具站**：复制一个计算器 HTML、改 formula 函数即可
- **SEO 导向的工具站**：纯 HTML + Schema 对搜索引擎最友好
