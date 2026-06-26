# AquariumMath.com — 站点全貌分析

> 分析日期：2026-06-26  
> 目标地址：https://aquariummath.com  
> 技术栈：Next.js App Router (turbopack) + React Server Components + Tailwind CSS

---

## 一、站点定位

AquariumMath 是一个**水族箱爱好者计算器工具站**，覆盖从开缸规划到日常维护的全流程计算需求。

Slogan：*"Free aquarium calculators and guides. Everything you need for a healthy tank."*

属于一个**跨领域计算器站群**的一部分（见第十二节）。

---

## 二、全部 13 个计算器

| # | Slug | 名称 | 功能 |
|---|------|------|------|
| 1 | `aquarium-volume` | 水族箱体积 | 5种形状（矩形/鼓形/圆柱/六角/角缸），公制/英制 |
| 2 | `stocking` | 鱼只密度 | 计算合理饲养量，推荐兼容鱼种 |
| 3 | `substrate` | 底砂用量 | 底砂/沙/泥的用量估算 |
| 4 | `heater` | 加热棒功率 | 根据温差推荐加热棒瓦数 |
| 5 | `filter` | 过滤器流量 | 计算所需 GPH 和推荐过滤类型 |
| 6 | `glass-thickness` | 玻璃厚度 | DIY 鱼缸的玻璃/亚克力安全厚度 |
| 7 | `salinity` | 盐度 | 海水缸/汽水缸的盐量计算 |
| 8 | `lighting` | 灯光强度 | 不同缸型的灯光推荐 |
| 9 | `co2` | CO₂ 浓度 | 从 pH 和 KH 计算溶解 CO₂ |
| 10 | `dosing` | 药剂用量 | 肥料和药物的精确剂量 |
| 11 | `weight` | 缸体总重 | 水+玻璃+底砂的总重量 |
| 12 | `cost` | 开缸成本 | 完整设备成本估算 |

---

## 三、鱼类数据库（35 种）

所有数据硬编码在前端 JS bundle 中，无需后端查询。

字段结构：
```javascript
{
  name,              // 中文俗名
  scientificName,    // 学名
  minTankSize,       // 最小缸体 (US gal)
  maxSize,           // 最大体长 (inch)
  temperament,       // 性情: peaceful / semi-aggressive
  temperatureRange,  // 温度范围 [low°F, high°F]
  phRange,           // pH 范围 [low, high]
  bioload,           // 生物负荷: low / medium
  schooling,         // 是否群游
  minSchoolSize,     // 最少群游数量
  diet,              // 食性: carnivore / omnivore / herbivore
  careLevel,         // 饲养难度: easy / moderate
}
```

### 按类型统计

| 类型 | 数量 | 代表物种 |
|------|------|---------|
| 灯科鱼 (Tetra) | 4 | 霓虹灯、宝莲灯、红鼻剪刀、琥珀灯 |
| 胎鳉 (Livebearer) | 4 | 孔雀、月光、玛丽、剑尾、安德拉斯 |
| 鲤科 (Cyprinid) | 4 | 樱桃灯、斑马、白云山、银河斑马 |
| 攀鲈 (Gourami) | 4 | 矮珍珠、珍珠、蓝曼龙、蜂蜜 |
| 鲶科 (Catfish) | 4 | 鼠鱼、小精灵、小精灵鼠、枝桠 |
| 异型 (Pleco) | 2 | 红眼胡子、小丑胡子 |
| 丽鱼 (Cichlid) | 3 | 神仙、蓝宝石、阿卡西 |
| 鳅科 (Loach) | 2 | 蛇仔、间吸鳅 |
| 河豚 (Puffer) | 1 | 侏儒河豚 |
| 虾类 | 2 | 樱花虾、大和沼虾 |
| 螺类 | 2 | 神秘螺、斑马螺 |
| 斗鱼 | 1 | 泰国斗鱼 |

### 按饲养难度

| 难度 | 数量 |
|------|------|
| Easy（简单） | 18 |
| Moderate（中等） | 17 |
| Advanced（困难） | 0 |

### 按性情

| 性情 | 数量 |
|------|------|
| Peaceful（温和） | 30 |
| Semi-aggressive（半攻击） | 5 |

---

## 四、药剂/添加物数据库（8 种）

同样硬编码在 JS 中：

| 产品 | 分类 | 用量 | 说明 |
|------|------|------|------|
| Seachem Prime | 水质调节 | 0.02 mL/gal | 换水时除氯/解氨 |
| Seachem Flourish | 液肥 | 0.02 mL/gal | 草缸每周 1-2 次 |
| Seachem Excel | 碳源 | 0.04 mL/gal | 每日液态碳 |
| API Stress Coat | 水质调节 | 0.04 mL/gal | 换水/新鱼入缸 |
| Ich-X | 药物 | 0.04 mL/gal | 白点病每日给药 |
| API General Cure | 药物 | 1包/10gal | 每48h一次共2次 |
| Fritz Maracyn | 药物 | 1包/10gal | 每日给药共5天 |
| Seachem Stability | 硝化菌 | 0.02 mL/gal | 开缸或换水后7天 |

---

## 五、指南内容

| 页面 | 内容 |
|------|------|
| `/guides/beginners-guide` | 新手入门指南 |
| `/guides/nitrogen-cycle` | 氮循环 (NH₃→NO₂→NO₃) |
| `/betta` | 斗鱼完整饲养指南 |

---

## 六、玻璃厚度计算公式（⭐ 核心发现）

### 6.1 源代码

从 chunk1.js (`312f380bb05b693b.js`) 中提取的函数 `p`（即 `calcGlassThickness`）：

```javascript
function calcGlassThickness(length_in, height_in, material) {
  let h_mm = 25.4 * height_in;  // 高度 → mm
  let l_mm = 25.4 * length_in;  // 长度 → mm
  let sf = material === "glass" ? 3.8 : 2.5;
  let strength = material === "glass" ? 19.2 : 7.0;  // MPa

  return Math.max(
    Math.ceil(
      Math.sqrt(
        0.00981 * h_mm * h_mm * sf * l_mm * l_mm
        / (1000 * strength)
      )
    ),
    6  // 最小 6mm
  );
}
```

### 6.2 数学形式

```
t = max( ceil( √( 0.00981 × H² × SF × L² / (1000 × σ) ) ), 6 )

其中：
  H = 高度 (mm)
  L = 长度 (mm)
  SF = 安全系数 (玻璃 3.8, 亚克力 2.5)
  σ  = 材料强度 (玻璃 19.2 MPa, 亚克力 7.0 MPa)
  输出 = mm (最小 6mm)
```

### 6.3 ⚠️ 公式存在严重 Bug

这个公式**把长度 L 也作为厚度的决定因素**，但静水压力只取决于水深（高度 H），与水平方向尺寸无关。长度 L 只影响**是否需要加横梁**（bracing），不影响玻璃厚度。

**验证**：48"×12"×18"（L=48", H=18"）→ 计算得 777mm → 完全不合理，应该约 6-10mm。

**正确做法**（对比 Omni Calculator）：
- 侧板厚度仅取决于 H（高度）、LHratio（长高比）、许用弯曲应力
- 长度 L 不影响厚度，只影响是否加中心横梁（L > 36"）

### 6.4 公式对比

| | AquariumMath | Omni Calculator |
|---|---|---|
| 厚度公式 | 含 L² 和 H² | 仅 H³（含 β 系数） |
| 长高比 | 未使用 | LHratio 决定 β 系数 |
| 分段多项式 | 无 | 侧板 4 次、底板 3 次 |
| 挠度计算 | 无 | 有 |
| α/β 系数 | 无 | 有（弹性力学 Navier 解拟合） |
| 结果正确性 | ❌ 有误 | ✅ 正确 |

---

## 七、玻璃重量公式

```javascript
// 从 JS 源码提取
function calcGlassWeight(length, height, thickness_inch, material) {
  let density = material === "glass" ? 0.091 : 0.043;  // lb/in³
  return length * height * thickness_inch * density;     // 单块面板重量 (lb)
}
// 5 块面板分别计算后求和
```

---

## 八、横梁建议逻辑

```javascript
let needsCenterBrace = length > 36;   // 长度 > 36" 需要中心横梁
let needsEuroBracing = length > 48;   // 长度 > 48" 建议欧式包边
```

---

## 九、技术架构

| 层面 | 技术 |
|------|------|
| 框架 | Next.js (App Router) |
| 打包 | Turbopack |
| 渲染 | React Server Components (RSC) |
| CSS | Tailwind CSS |
| 字体 | Google Fonts (Inter) |
| SSR 协议 | `self.__next_f.push()` RSC 流式传输 |
| 数据方式 | **全部数据硬编码在前端 JS**，无后端 API |
| 分析 | Google Analytics (G-GCF9QXKB3C) |
| CDN | Vercel (`_next/static/chunks/`) |

**关键差异**：与 Omni Calculator 不同，AquariumMath **没有 GraphQL、没有数据库、没有后端 API**。所有计算器公式、鱼类数据、药剂数据全部打包在前端 JavaScript bundle 中。

---

## 十、主页体积计算器（特色功能）

支持 5 种缸型：

| 形状 | 体积公式 |
|------|---------|
| 矩形 (Rectangle) | L × W × H × 0.004329 (US gal) |
| 鼓形 (Bowfront) | L × W × H × 0.004329 × 1.1 |
| 圆柱 (Cylinder) | π × (D/2)² × H × 0.004329 |
| 六角 (Hexagon) | (3√3/2) × S² × H × 0.004329 |
| 角缸 (Corner) | 三角形面积 × H × 0.004329 |

同时显示**毛容量**和**可用容量**（扣除底砂和装饰，≈90%）。

---

## 十一、内容质量评估

| 维度 | 评价 |
|------|------|
| 计算器覆盖度 | ⭐⭐⭐⭐⭐ 完整（从开缸到维护全流程） |
| 公式正确性 | ⭐⭐ 玻璃厚度公式有严重 bug |
| 鱼类数据库 | ⭐⭐⭐ 35种偏少，但参数详细 |
| UI/UX | ⭐⭐⭐⭐ 简洁现代，响应式好 |
| 技术架构 | ⭐⭐⭐ 纯前端硬编码，无扩展性 |
| SEO | ⭐⭐⭐⭐ Schema.org 结构化数据完整 |

---

## 十二、关联站群

AquariumMath 属于一个**计算器工具站群**，共享技术模板：

| 站点 | 领域 |
|------|------|
| utilfox.dev | 通用工具 |
| hvaccalc.dev | 暖通空调 |
| roofmath.dev | 屋顶计算 |
| loancrunch.dev | 贷款计算 |
| freelancetax.dev | 自由职业税务 |
| mortgagefox.dev | 房贷计算 |
| impuestosfreelance.com | 西班牙语税务 |
| calcucamper.com | 房车计算 |
| tiremath.com | 轮胎计算 |
| poolsizer.com | 泳池尺寸 |
| solarpanelmath.com | 太阳能板 |
| framingcalc.com | 框架计算 |
| ... 等 17+ 站点 | |

这表明网站是一个**模板化批量建站策略**——同一套 Next.js 代码库，通过配置不同领域的计算器数据库，快速生成行业垂直站。

---

## 十三、总结

AquariumMath 是一个**轻量级纯前端水族计算器站**，优势在于：
- 覆盖全、UX 好、对新手友好
- 零后端成本（全部硬编码）

主要缺陷：
- 玻璃厚度公式存在**严重数学错误**（不应含长度因子）
- 鱼类数据库仅 35 种，且无搜索/筛选功能
- 作为纯前端站，数据更新需要重新部署
