"""
批量翻译 AquaCalcs 全部页面为中文
"""
import os, re, glob

SITE = r'E:/SHEN/逆向/003/site'

# ============================================================
# 全局替换表（所有页面通用）
# ============================================================
GLOBAL_REPLACE = [
    # ---- Header / Nav ----
    ('Tank Setup', '缸体设置'),
    ('Water Chemistry', '水质化学'),
    ('Fish &amp; Stocking', '鱼类放养'),
    ('Fish & Stocking', '鱼类放养'),
    ('Equipment &amp; Maintenance', '设备维护'),
    ('Equipment & Maintenance', '设备维护'),

    # ---- Breadcrumb ----
    ('<span aria-current="page">Home</span>', '<span aria-current="page">首页</span>'),
    ('Home</a>', '首页</a>'),
    ('Home</span>', '首页</span>'),
    ('aria-label="Home"', 'aria-label="首页"'),
    ('aria-label="Breadcrumb"', 'aria-label="面包屑导航"'),
    ('aria-label="Main navigation"', 'aria-label="主导航"'),

    # ---- Footer ----
    ('<h4>Calculators</h4>', '<h4>计算器</h4>'),
    ('<h4>More Tools</h4>', '<h4>更多工具</h4>'),
    ('<h4>AquaCalcs</h4>', '<h4>关于本站</h4>'),
    ('<a href="/about/">About</a>', '<a href="/about/">关于我们</a>'),
    ('<a href="/privacy/">Privacy Policy</a>', '<a href="/privacy/">隐私政策</a>'),
    ('<a href="/terms/">Terms of Use</a>', '<a href="/terms/">使用条款</a>'),
    ('Aquarium calculations including', '水族箱计算结果（包括'),
    ('are approximate guidelines', '均为近似参考值'),
    ('Actual requirements vary by species, water source, and tank conditions', '实际需求因鱼种、水源和缸体条件而异'),
    ('Always research species-specific needs and test water parameters regularly', '请务必研究具体鱼种需求并定期测试水质参数'),

    # ---- Cookie ----
    ('We use cookies to improve your experience and serve relevant ads. By continuing to use this site, you consent to our use of cookies. See our',
     '本站使用 Cookie 改善体验。继续使用即表示同意。详见'),
    ('Accept', '接受'),

    # ---- Common sections ----
    ('<h2>Results</h2>', '<h2>计算结果</h2>'),
    ('<h2>Visualization</h2>', '<h2>可视化图表</h2>'),
    ('<h2>How It Works</h2>', '<h2>使用说明</h2>'),
    ('<h3>The Formula</h3>', '<h3>计算公式</h3>'),
    ('<h3>Worked Example</h3>', '<h3>计算示例</h3>'),
    ('<h3>Methodology</h3>', '<h3>方法论</h3>'),
    ('<h3>When to Use This Calculator</h3>', '<h3>适用场景</h3>'),
    ('<h3>Common Mistakes to Avoid</h3>', '<h3>常见错误</h3>'),
    ('<h3>Practical Tips</h3>', '<h3>实用建议</h3>'),
    ('<h3>Frequently Asked Questions</h3>', '<h3>常见问题</h3>'),
    ('<h3>Sources</h3>', '<h3>参考来源</h3>'),
    ('<h2>More Water Chemistry Calculators</h2>', '<h2>更多水质化学计算器</h2>'),
    ('<h2>More Tank Setup Calculators</h2>', '<h2>更多缸体设置计算器</h2>'),
    ('<h2>More Fish &amp; Stocking Calculators</h2>', '<h2>更多鱼类放养计算器</h2>'),
    ('<h2>More Fish Stocking Calculators</h2>', '<h2>更多鱼类放养计算器</h2>'),
    ('<h2>More Equipment &amp; Maintenance Calculators</h2>', '<h2>更多设备维护计算器</h2>'),
    ('<h2>More Equipment Maintenance Calculators</h2>', '<h2>更多设备维护计算器</h2>'),
    ('Last updated:', '最后更新：'),
    ('Reviewed by Angelo Smith', '审阅：Angelo Smith'),

    # ---- Sidebar ----
    ('<h3>Related Calculators</h3>', '<h3>相关计算器</h3>'),

    # ---- Common buttons & UI ----
    ('<button type="submit" id="btn-calculate" class="btn-calculate">Calculate</button>',
     '<button type="submit" id="btn-calculate" class="btn-calculate">计算</button>'),
    ('role="banner"', 'role="banner"'),
    ('role="contentinfo"', 'role="contentinfo"'),
    ('aria-label="Calculator inputs"', 'aria-label="计算器输入"'),
    ('aria-label="Calculator chart"', 'aria-label="计算器图表"'),
    ('aria-label="Sidebar"', 'aria-label="侧边栏"'),
    ('aria-label="Advertisement"', 'aria-label="广告"'),
    ('aria-live="polite"', 'aria-live="polite"'),
    ('aria-hidden="true"', 'aria-hidden="true"'),

    # ---- lang attribute ----
    ('<html lang="en">', '<html lang="zh-CN">'),
    ('og:locale" content="en_US"', 'og:locale" content="zh_CN"'),

    # ---- Free Calculator labels ----
    ('| Free Calculator | AquaCalcs', '| 免费计算器 | AquaCalcs'),
    ('| Free Calculator', '| 免费计算器'),

    # ---- Common form labels ----
    ('Tank Volume (gallons)', '鱼缸容积（加仑）'),
    ('Tank Volume (liters)', '鱼缸容积（升）'),

    # ---- Calculator description pattern (Common) ----
    ('The calculator provides estimates based on standard formulas.',
     '本计算器基于标准公式提供估算值。'),

    # ---- FAQ translations ----
    ('How often should I recalculate these values?',
     '我应该多久重新计算一次？'),
    ('You should recalculate whenever you make changes',
     '当您对鱼缸进行任何更改时都应重新计算'),
    ('Can I use this calculator for both freshwater and saltwater aquariums?',
     '此计算器适用于淡水和海水鱼缸吗？'),
    ('This calculator is designed to work with both freshwater and saltwater setups',
     '此计算器适用于淡水和海水两种配置'),
    ('What should I do if my actual results differ significantly from the calculated values?',
     '如果实际结果与计算值差异很大怎么办？'),
    ('A significant discrepancy usually indicates',
     '显著差异通常表明'),
    ('Do I need to account for live plants when using this calculator?',
     '使用此计算器时需要考虑活体植物吗？'),
    ('Yes, live aquatic plants can significantly affect',
     '是的，活体水生植物会显著影响'),
    ('How does water temperature affect the calculator results?',
     '水温如何影响计算结果？'),
    ('Water temperature directly impacts',
     '水温直接影响'),
    ('Can beginners rely on this calculator or should they consult an expert?',
     '新手可以依赖此计算器还是应该咨询专家？'),
    ('This calculator is specifically designed to be useful for beginners',
     '此计算器专为新手设计，同时对有经验的鱼友也提供准确结果'),
    ('PH Level', 'pH 值'),
    ('KH Level', 'KH 值'),
    ('Ammonia Level', '氨浓度'),
    ('Temperature', '温度'),

    # ---- Sources ----
    ('American Fisheries Society', '美国渔业学会'),
    ('Guidelines for Aquaculture and Aquarium Management', '水产养殖与水族箱管理指南'),
    ('Pet Industry Joint Advisory Council', '宠物行业联合咨询委员会'),
    ('Aquatic Species Care Standards', '水生生物护理标准'),
    ('World Aquatic Veterinary Medical Association', '世界水生兽医协会'),
    ('Best Practice Guidelines', '最佳实践指南'),

    # ---- Common edu section title tags ----
    ('is a comprehensive tool designed to help enthusiasts and professionals quickly determine accurate values based on multiple input variables.',
     '是一款综合工具，旨在帮助爱好者和专业人士基于多个输入变量快速获取准确数值。'),
    ('This calculator takes into account the key factors that affect the final result, providing both standard and optimized recommendations.',
     '此计算器考虑了影响最终结果的关键因素，同时提供标准和优化建议。'),
    ('Understanding these calculations is essential for making informed decisions',
     '理解这些计算对于做出明智决策至关重要'),
    ('whether you are a beginner or an experienced practitioner',
     '无论您是初学者还是有经验的从业者'),
    ('The underlying formulas have been derived from industry standards and peer-reviewed research, ensuring reliable results.',
     '底层公式源自行业标准和同行评审研究，确保结果可靠。'),
    ('Many users find that manually performing these calculations is time-consuming and error-prone, making an automated calculator particularly valuable.',
     '许多用户发现手动执行这些计算既耗时又容易出错，因此自动化计算器特别有价值。'),
    ('Factors such as environmental conditions, equipment specifications, and personal preferences all influence the optimal values.',
     '环境条件、设备规格和个人偏好等因素都会影响最佳值。'),
    ('Whether you are a beginner setting up your first tank or an experienced hobbyist expanding a multi-tank system, this calculator provides the data-driven guidance needed to avoid costly mistakes and maintain a thriving aquatic environment.',
     '无论您是第一次设置鱼缸的新手，还是扩展多缸系统的资深爱好者，此计算器都能提供数据驱动的指导，帮助避免代价高昂的错误并维持健康的水生环境。'),
]

# ============================================================
# 页面特定翻译
# ============================================================
PAGE_TRANSLATIONS = {
    'index.html': [
        ('Free Aquarium &amp; Fish Keeping Calculators | AquaCalcs',
         '免费水族计算器 | 鱼缸计算工具 | AquaCalcs'),
        ('AquaCalcs.com provides free aquarium calculators including tank volume, stocking levels, water chemistry, equipment sizing, and maintenance planning tools. No signup, no guesswork.',
         'AquaCalcs 提供免费水族计算器，包括鱼缸容积、放养密度、水质化学、设备选型和维护规划工具。无需注册，无需猜测。'),
        ('<h1>\nCalculators\n</h1>', '<h1>计算器</h1>'),
        ('<h1>Calculators</h1>', '<h1>计算器</h1>'),
        ('Browse by Category', '按分类浏览'),
        ('Popular Calculators', '热门计算器'),
        ('Tank Volume Calculator', '鱼缸容积计算器'),
        ('Substrate Calculator', '底砂用量计算器'),
        ('Aquarium Heater Calculator', '加热棒功率计算器'),
        ('Filter Flow Rate Calculator', '过滤器流量计算器'),
        ('Aquarium Weight Calculator', '鱼缸重量计算器'),
        ('Water Change Calculator', '换水计算器'),
        ('CO2 Dosing Calculator', 'CO₂ 添加计算器'),
        ('Ammonia Toxicity Calculator', '氨毒性计算器'),
        ('Stocking Level Calculator', '放养密度计算器'),
        ('Fish Feeding Calculator', '喂食量计算器'),
        ('Fish &amp; Stocking', '鱼类放养'),
        ('Equipment &amp; Maintenance', '设备维护'),
        ('Free aquarium calculators for tank volume, stocking levels, water chemistry, and equipment sizing.',
         '免费水族计算器：鱼缸容积、放养密度、水质化学、设备选型。'),
    ],

    'co2-dosing-calculator': [
        ('CO2 Dosing Calculator | Free Calculator | AquaCalcs',
         'CO₂ 添加计算器 | 免费计算器 | AquaCalcs'),
        ('Calculate CO2 concentration from pH and KH, and determine target bubble rate.',
         '根据 pH 和 KH 计算 CO₂ 浓度，确定目标气泡速率。'),
        ('<h1>CO2 Dosing Calculator</h1>', '<h1>CO₂ 添加计算器</h1>'),
        ('<p class="calc-description">Calculate CO2 concentration from pH and KH, and determine target bubble rate.</p>',
         '<p class="calc-description">根据 pH 和 KH 计算水中 CO₂ 浓度，确定植物光合作用所需的 CO₂ 目标气泡速率。</p>'),
        ('Tank pH', '鱼缸 pH'),
        ('KH (dKH)', 'KH（dKH）'),
        ('CO2 Dosing Calculator', 'CO₂ 添加计算器'),
        ('Calculate CO2 concentration from pH and KH, and determine target bubble rate.',
         '根据 pH 和 KH 计算 CO₂ 浓度，确定目标气泡速率。'),
        ('Too Low', '过低'),
        ('increase CO2', '增加 CO₂'),
        ('Low', '偏低'),
        ('plants will benefit from more', '植物会受益于更多 CO₂'),
        ('Ideal Range for planted tanks', '草缸理想范围'),
        ('Too High', '过高'),
        ('risk to fish, reduce CO2', '对鱼有风险，减少 CO₂'),
        ("CO2 Concentration (ppm)", 'CO₂ 浓度（ppm）'),
        ('Status', '状态'),
        ('Target CO2 (ppm)', '目标 CO₂（ppm）'),
        ('Suggested Bubble Rate (bps)', '建议气泡速率（bps）'),
        ('Current CO2', '当前 CO₂'),
        ('Ideal CO2', '理想 CO₂'),
        ("CO2 (ppm)", 'CO₂（ppm）'),
    ],

    'aquarium-heater-calculator': [
        ('Aquarium Heater Calculator | Free Calculator | AquaCalcs',
         '加热棒功率计算器 | 免费计算器 | AquaCalcs'),
        ('<h1>Aquarium Heater Calculator</h1>', '<h1>加热棒功率计算器</h1>'),
        ('Aquarium Heater Calculator', '加热棒功率计算器'),
        ('Calculate the recommended heater wattage for your aquarium based on tank size and temperature difference.',
         '根据鱼缸大小和温差计算推荐的加热棒功率。'),
        ('<p class="calc-description">Calculate the recommended heater wattage for your aquarium based on tank size and temperature difference.</p>',
         '<p class="calc-description">根据鱼缸容积和目标温差，计算维持稳定水温所需的最小加热棒瓦数。</p>'),
        ('Room Temperature (°F)', '室温（°F）'),
        ('Target Temperature (°F)', '目标温度（°F）'),
        ('Room Temperature (°C)', '室温（°C）'),
        ('Target Temperature (°C)', '目标温度（°C）'),
        ('Tank Volume (gallons)', '鱼缸容积（加仑）'),
        ('Recommended Wattage (watts)', '推荐功率（瓦）'),
        ('Standard Heater Size', '标准加热棒规格'),
        ('Temperature Difference', '温差'),
        ('Current Diff', '当前温差'),
        ('Wattage', '功率'),
    ],

    'ammonia-calculator': [
        ('Ammonia Toxicity Calculator | Free Calculator | AquaCalcs',
         '氨毒性计算器 | 免费计算器 | AquaCalcs'),
        ('<h1>Ammonia Toxicity Calculator</h1>', '<h1>氨毒性计算器</h1>'),
        ('Ammonia Toxicity Calculator', '氨毒性计算器'),
        ('Calculate free ammonia (NH3) toxicity from total ammonia, pH, and temperature.',
         '根据总氨、pH 和温度计算游离氨（NH₃）毒性。'),
        ('<p class="calc-description">Calculate free ammonia (NH3) toxicity from total ammonia, pH, and temperature.</p>',
         '<p class="calc-description">根据总氨读数、pH 和温度计算真正有毒的游离氨（NH₃）浓度。总氨中只有 NH₃ 对鱼有毒性，NH₄⁺ 相对安全。</p>'),
        ('Total Ammonia (ppm)', '总氨（ppm）'),
        ('Temperature (°F)', '温度（°F）'),
        ('pH', 'pH'),
        ('Free Ammonia NH3 (ppm)', '游离氨 NH₃（ppm）'),
        ('Toxicity Level', '毒性等级'),
        ('Safe', '安全'),
        ('Caution', '注意'),
        ('Dangerous', '危险'),
        ('Free NH3', '游离 NH₃'),
        ('Safe Threshold', '安全阈值'),
    ],

    'water-change-calculator': [
        ('Water Change Calculator | Free Calculator | AquaCalcs',
         '换水计算器 | 免费计算器 | AquaCalcs'),
        ('<h1>Water Change Calculator</h1>', '<h1>换水计算器</h1>'),
        ('Water Change Calculator', '换水计算器'),
        ('Calculate water change amounts and resulting parameter changes.',
         '计算换水量及换水后的水质参数变化。'),
        ('<p class="calc-description">Calculate water change amounts and resulting parameter changes.</p>',
         '<p class="calc-description">计算换水后的水质参数变化，帮助规划最佳换水频率和换水量。</p>'),
        ('Current Nitrate (ppm)', '当前硝酸盐（ppm）'),
        ('Target Nitrate (ppm)', '目标硝酸盐（ppm）'),
        ('Water Change Volume (%)', '换水比例（%）'),
        ('Water Change (gallons)', '换水量（加仑）'),
        ('Resulting Nitrate', '换后硝酸盐'),
        ('Nitrate Reduction', '硝酸盐减少量'),
    ],

    'filter-flow-calculator': [
        ('Filter Flow Rate Calculator | Free Calculator | AquaCalcs',
         '过滤器流量计算器 | 免费计算器 | AquaCalcs'),
        ('<h1>Filter Flow Rate Calculator</h1>', '<h1>过滤器流量计算器</h1>'),
        ('Filter Flow Rate Calculator', '过滤器流量计算器'),
        ('Calculate required filter flow rate (GPH) and recommended filter type.',
         '计算所需的过滤器流量（GPH）和推荐过滤类型。'),
        ('<p class="calc-description">Calculate required filter flow rate (GPH) and recommended filter type.</p>',
         '<p class="calc-description">基于鱼缸容积和生物负荷计算所需的最小过滤流量，并推荐合适的过滤器类型。</p>'),
        ('Bioload Level', '生物负荷等级'),
        ('Low (light stocking)', '低（少量鱼）'),
        ('Medium (average stocking)', '中（正常密度）'),
        ('High (heavy stocking)', '高（高密度）'),
        ('Minimum Flow Rate (GPH)', '最小流量（GPH）'),
        ('Recommended Flow Rate (GPH)', '推荐流量（GPH）'),
        ('Recommended Turnover', '推荐循环倍率'),
        ('Recommended Filter Type', '推荐过滤类型'),
        ('Flow Rate', '流量'),
        ('Minimum', '最小值'),
        ('Recommended', '推荐值'),
    ],

    'tank-volume-calculator': [
        ('Tank Volume Calculator | Free Calculator | AquaCalcs',
         '鱼缸容积计算器 | 免费计算器 | AquaCalcs'),
        ('<h1>Tank Volume Calculator</h1>', '<h1>鱼缸容积计算器</h1>'),
        ('Tank Volume Calculator', '鱼缸容积计算器'),
        ('Calculate aquarium volume in gallons and liters for various tank shapes.',
         '计算各种形状鱼缸的容积（加仑/升）。'),
        ('<p class="calc-description">Calculate aquarium volume in gallons and liters for various tank shapes.</p>',
         '<p class="calc-description">支持 5 种缸型的容积计算：矩形、鼓形、圆柱、六角、角缸。切换形状和单位即可。</p>'),
        ('Tank Shape', '缸体形状'),
        ('Rectangle', '矩形'),
        ('Bowfront', '鼓形'),
        ('Cylinder', '圆柱'),
        ('Hexagon', '六角'),
        ('Corner', '角缸'),
        ('Length (inches)', '长度（英寸）'),
        ('Width (inches)', '宽度（英寸）'),
        ('Height (inches)', '高度（英寸）'),
        ('Diameter (inches)', '直径（英寸）'),
        ('Side Length (inches)', '边长（英寸）'),
        ('Unit System', '单位制'),
        ('Inches', '英寸'),
        ('Centimeters', '厘米'),
        ('Gross Volume', '毛容积'),
        ('Usable Volume (~90%)', '可用容积（约90%）'),
        ('gallons', '加仑'),
        ('liters', '升'),
    ],

    'substrate-calculator': [
        ('Substrate Calculator | Free Calculator | AquaCalcs',
         '底砂用量计算器 | 免费计算器 | AquaCalcs'),
        ('<h1>Substrate Calculator</h1>', '<h1>底砂用量计算器</h1>'),
        ('Substrate Calculator', '底砂用量计算器'),
        ('Calculate how much substrate (gravel or sand) you need for your aquarium.',
         '计算水族箱所需的底砂（砾石或沙子）用量。'),
        ('<p class="calc-description">Calculate how much substrate (gravel or sand) you need for your aquarium.</p>',
         '<p class="calc-description">根据缸体尺寸、底砂类型和期望厚度，计算所需底砂的磅数和袋数。</p>'),
        ('Substrate Type', '底砂类型'),
        ('Gravel', '砾石'),
        ('Sand', '沙子'),
        ('Soil', '水草泥'),
        ('Desired Depth (inches)', '期望厚度（英寸）'),
        ('Substrate Needed (lbs)', '所需底砂（磅）'),
        ('Bags Needed (standard 20lb)', '所需袋数（标准 20 磅/袋）'),
        ('Substrate Weight', '底砂重量'),
        ('Bags', '袋'),
    ],

    'aquarium-stand-weight': [
        ('Aquarium Weight Calculator | Free Calculator | AquaCalcs',
         '鱼缸重量计算器 | 免费计算器 | AquaCalcs'),
        ('<h1>Aquarium Weight Calculator</h1>', '<h1>鱼缸重量计算器</h1>'),
        ('Aquarium Weight Calculator', '鱼缸重量计算器'),
        ('Calculate the total weight of your filled aquarium including water, substrate, and equipment.',
         '计算满水鱼缸的总重量，包括水、底砂和设备。'),
        ('<p class="calc-description">Calculate the total weight of your filled aquarium including water, substrate, and equipment.</p>',
         '<p class="calc-description">计算满载鱼缸的总重量——水 + 玻璃 + 底砂 + 装饰——确保地面和架子能承受。</p>'),
        ('Glass Thickness (mm)', '玻璃厚度（mm）'),
        ('Substrate Weight (lbs)', '底砂重量（磅）'),
        ('Decoration Weight (lbs)', '装饰重量（磅）'),
        ('Water Weight (lbs)', '水重量（磅）'),
        ('Glass Weight (lbs)', '玻璃重量（磅）'),
        ('Total Weight (lbs)', '总重量（磅）'),
        ('Water', '水'),
        ('Glass', '玻璃'),
        ('Substrate', '底砂'),
        ('Decor', '装饰'),
    ],

    'stocking-level-calculator': [
        ('Stocking Level Calculator | Free Calculator | AquaCalcs',
         '放养密度计算器 | 免费计算器 | AquaCalcs'),
        ('<h1>Stocking Level Calculator</h1>', '<h1>放养密度计算器</h1>'),
        ('Stocking Level Calculator', '放养密度计算器'),
        ('Calculate safe fish stocking levels based on tank size and filtration.',
         '根据鱼缸大小和过滤能力计算安全的鱼类放养数量。'),
        ('<p class="calc-description">Calculate safe fish stocking levels based on tank size and filtration.</p>',
         '<p class="calc-description">基于经典"每加仑一英寸鱼"规则和改进算法，估算鱼缸可安全容纳的鱼只总长度和数量。</p>'),
        ('Filtration Type', '过滤类型'),
        ('Basic (sponge/HOB)', '基础（海绵/瀑布）'),
        ('Standard (canister)', '标准（滤桶）'),
        ('Advanced (sump)', '高级（底滤）'),
        ('Stocking Approach', '放养策略'),
        ('Conservative', '保守'),
        ('Moderate', '中等'),
        ('Maximum', '最大'),
        ('Max Fish Inches', '最大鱼只总长（英寸）'),
        ('Stocking Percentage', '放养比例'),
        ('Recommendation', '建议'),
    ],

    'fish-feeding-calculator': [
        ('Fish Feeding Calculator | Free Calculator | AquaCalcs',
         '喂食量计算器 | 免费计算器 | AquaCalcs'),
        ('<h1>Fish Feeding Calculator</h1>', '<h1>喂食量计算器</h1>'),
        ('Fish Feeding Calculator', '喂食量计算器'),
        ('Calculate daily feeding amounts based on fish type and quantity.',
         '根据鱼种和数量计算每日喂食量。'),
        ('<p class="calc-description">Calculate daily feeding amounts based on fish type and quantity.</p>',
         '<p class="calc-description">根据鱼的数量、体型和种类估算每日食物量，避免过量喂食导致水质恶化。</p>'),
        ('Number of Fish', '鱼的数量'),
        ('Fish Type', '鱼种类型'),
        ('Small Community', '小型群游鱼'),
        ('Medium Community', '中型鱼'),
        ('Large Cichlids', '大型慈鲷'),
        ('Goldfish/Koi', '金鱼/锦鲤'),
        ('Daily Food (grams)', '每日食量（克）'),
        ('Feeding Frequency', '喂食频率'),
        ('Times per Day', '次/天'),
    ],
}

# ============================================================
# 执行翻译
# ============================================================
def translate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 全局替换
    for old, new in GLOBAL_REPLACE:
        content = content.replace(old, new)

    # 页面特定替换
    fname = os.path.basename(filepath)
    dirname = os.path.basename(os.path.dirname(filepath))
    key = fname if fname == 'index.html' and dirname == 'site' else dirname

    if key in PAGE_TRANSLATIONS:
        for old, new in PAGE_TRANSLATIONS[key]:
            content = content.replace(old, new)

    # 翻译一些常见短句
    extras = [
        ('<a href="../category/tank-setup/">Tank Setup</a>', '<a href="../category/tank-setup/">缸体设置</a>'),
        ('<a href="../category/water-chemistry/">Water Chemistry</a>', '<a href="../category/water-chemistry/">水质化学</a>'),
        ('<a href="../category/fish-stocking/">Fish &amp; Stocking</a>', '<a href="../category/fish-stocking/">鱼类放养</a>'),
        ('<a href="../category/fish-stocking/">Fish Stocking</a>', '<a href="../category/fish-stocking/">鱼类放养</a>'),
        ('<a href="../category/equipment-maintenance/">Equipment &amp; Maintenance</a>', '<a href="../category/equipment-maintenance/">设备维护</a>'),
        ('<a href="../category/equipment-maintenance/">Equipment Maintenance</a>', '<a href="../category/equipment-maintenance/">设备维护</a>'),
        ('Tank Setup</a>', '缸体设置</a>'),
        ('Water Chemistry</a>', '水质化学</a>'),
        ('Fish Stocking</a>', '鱼类放养</a>'),
        ('Equipment Maintenance</a>', '设备维护</a>'),
        ('CO2 Dosing Calculator</a>', 'CO₂ 添加计算器</a>'),
        ('Ammonia Toxicity Calculator</a>', '氨毒性计算器</a>'),
        ('Water Change Calculator</a>', '换水计算器</a>'),
        ('Substrate Calculator</a>', '底砂用量计算器</a>'),
        ('Filter Flow Rate Calculator</a>', '过滤器流量计算器</a>'),
        ('Aquarium Heater Calculator</a>', '加热棒功率计算器</a>'),
        ('Tank Volume Calculator</a>', '鱼缸容积计算器</a>'),
        ('Aquarium Weight Calculator</a>', '鱼缸重量计算器</a>'),
        ('Stocking Level Calculator</a>', '放养密度计算器</a>'),
        ('Fish Feeding Calculator</a>', '喂食量计算器</a>'),
        ('Fertilizer Dosing Calculator</a>', '液肥添加计算器</a>'),
        ('Aquarium Lighting Calculator</a>', '鱼缸灯光计算器</a>'),
        ('Alkalinity Buffer Calculator</a>', '碱度缓冲计算器</a>'),
        ('Aquarium Salt Calculator</a>', '鱼缸盐度计算器</a>'),
        ('Planted Tank CO2 Calculator</a>', '草缸 CO₂ 计算器</a>'),
        ('Water Conditioner Calculator</a>', '水质调节剂计算器</a>'),
        ('Fish &amp; Stocking</a>', '鱼类放养</a>'),
        ('Equipment &amp; Maintenance</a>', '设备维护</a>'),
        ('Tank Setup</a>', '缸体设置</a>'),
        ('Search calculators', '搜索计算器'),
        ('Calculate', '计算'),
    ]
    for old, new in extras:
        content = content.replace(old, new)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# 处理所有 HTML 文件
for root, dirs, files in os.walk(SITE):
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            rel = os.path.relpath(filepath, SITE)
            translate_file(filepath)
            print(f'✅ {rel}')

print('\n🎉 全部翻译完成！')
