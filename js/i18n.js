/**
 * RootZe Lightweight Bilingual i18n Engine
 * Supports seamless client-side switching between English and Chinese
 */
(function(window) {
  'use strict';

  var translations = {
    en: {
      "brand.name": "Rootze",
      "brand.legal_name": "Xiangyang Ruzhi Import & Export Co., Ltd.",
      "brand.tagline": "Factory-Backed Industrial Equipment & Special Purpose Vehicles",

      "nav.home": "Home",
      "nav.products": "Products",
      "nav.about": "About Us",
      "nav.news": "News",
      "nav.contact": "Contact",
      "nav.quote": "Request Quote",

      // Legacy nav keys preserved for compatibility
      "nav.battery": "Battery & ESS",
      "nav.ev": "EV Vehicles",
      "nav.advantages": "Advantages",
      "nav.track": "Track Record",

      "hero.badge": "Factory-Backed Export Coalition • Xiangyang Heavy Industry",
      "hero.title": "Your Direct Factory-Backed Supplying Partner for Industrial Equipment & Vehicles in Central China",
      "hero.subtitle": "Connecting global buyers directly with equity-partnered manufacturers for factory-direct pricing, custom engineering, and reliable supply.",
      "hero.feature1": "Direct Factory Equity & Zero Markup",
      "hero.feature2": "OEM Technical & Engineering Access",
      "hero.feature3": "Xiangyang Industrial Heritage & Logistics",
      "hero.cta_products": "Explore What We Supply",
      "hero.cta_contact": "Request a Quote",
      "hero.cta_battery": "Explore What We Supply",

      "subheading.about": "Who We Are",
      "subheading.products": "What We Supply",
      "subheading.why": "Why Rootze",
      "subheading.workflow": "How We Work",
      "subheading.news": "News & Insights",
      "subheading.contact": "Connect With Us",

      // Legacy subheadings
      "subheading.battery": "What We Supply",
      "subheading.ev": "Special Purpose Vehicles",
      "subheading.adv": "Why Rootze",
      "subheading.track": "Global Presence",

      // About Us
      "about.title": "Authorized International Export Arm for Specialized Makers",
      "about.subtitle": "Based in Hubei Province—the core of Central China's heavy machinery and automotive components hub—Rootze bridges specialized makers directly with overseas buyers.",
      "about.body1": "Based in Hubei Province—the core of Central China’s heavy machinery and automotive components hub (anchored by Xiangyang's legendary manufacturing roots)—Rootze operates as the authorized international export division for a coalition of specialized local manufacturers.",
      "about.body2": "Backed by direct factory equity investments and exclusive overseas representation agreements, Rootze eliminates unnecessary intermediaries. We bring passionate, specialized local makers directly to the global stage. Overseas buyers gain the exact benefits of dealing directly with factory engineers, combined with streamlined international export management.",

      // Products (4 Core Categories)
      "products.title": "What We Supply: 4 Core Industrial Sectors",
      "products.subtitle": "Factory-engineered electrical systems, precision railway maintenance instruments, specialized utility vehicles, and turnkey manufacturing lines.",
      "products.cat1_title": "Industrial Electrical Systems (Soft Starters)",
      "products.cat1_desc": "High & low-voltage solid-state soft starters, variable frequency drives, and heavy-duty motor control distribution cabinets engineered for mining, water pumping, metallurgy, and heavy industrial applications.",
      "products.cat1_spec1": "Voltage: Low (380V-690V) & High (3kV-10kV)",
      "products.cat1_spec2": "Power Range: Up to 10,000 kW Heavy Duty",
      "products.cat1_spec3": "Protection: Full Motor & Bypass Protection, IP40-IP54",
      "products.cat2_title": "Railway Track Equipment & Maintenance Tools",
      "products.cat2_desc": "Precision in-house railway track testing and measurement instruments, paired with an extended range of railway line maintenance machinery, hydraulic power tools, and rail track components.",
      "products.cat2_spec1": "Precision: Track Gauge & Superelevation ±0.1mm",
      "products.cat2_spec2": "Range: Turnout & Cross-sectional Geometry System",
      "products.cat2_spec3": "Portability: Lightweight Aluminum Alloy & Digital Display",
      "products.cat3_title": "Special Purpose Vehicles (SPV & Trucks)",
      "products.cat3_desc": "Commercial and municipal utility vehicles including refrigerated trucks for cold-chain transport, tank trucks for fuel, water, and hazardous fluids, and municipal sweepers and engineering vehicles.",
      "products.cat3_spec1": "Applications: Cold-Chain, Tankers, Municipal, Engineering",
      "products.cat3_spec2": "Chassis: Dongfeng, Shacman, Sinotruk Chassis Options",
      "products.cat3_spec3": "Compliance: Complete Export Customs & Seaworthy Prep",
      "products.cat4_title": "Automotive Manufacturing Lines (Brake Pads)",
      "products.cat4_desc": "Turnkey brake pad production lines and friction material manufacturing equipment: raw material mixing, multi-cavity thermal hot pressing, precision double-surface grinding, and automated packaging.",
      "products.cat4_spec1": "Capacity: Turnkey Setup from 500k to 5M pcs/year",
      "products.cat4_spec2": "Tooling: Formula Support, Molds & Site Engineering",
      "products.cat4_spec3": "Automation: PLC Control, Dust Extraction & ISO Quality",
      "products.btn_spec": "View Specifications",
      "products.btn_inquire": "Inquire Price",

      // Legacy product keys preserved for compatibility
      "battery.title": "Core Power Battery & Energy Storage Solutions",
      "battery.subtitle": "Industrial-grade power battery cells, battery packs, and scalable energy storage cabinets engineered for extreme safety, high energy density, and extended cycle life.",
      "battery.cell_title": "Prismatic LFP & NMC Traction Cells",
      "battery.cell_desc": "Tier-1 Grade-A lithium iron phosphate and ternary lithium prismatic cells. Designed for EV conversion, commercial vehicles, and heavy-duty battery pack assembly.",
      "battery.cell_spec1": "Chemistry: LFP / NMC",
      "battery.cell_spec2": "Capacity: 100Ah - 314Ah",
      "battery.cell_spec3": "Cycle Life: 4000 - 6000 cycles",
      "battery.ess_ci_title": "Commercial & Industrial ESS",
      "battery.ess_ci_desc": "Modular 100kWh–2MWh outdoor air/liquid-cooled energy storage containers. Ideal for peak shaving, solar-plus-storage, and microgrid installations.",
      "battery.ess_ci_spec1": "Config: 100kWh - 2MWh Modular",
      "battery.ess_ci_spec2": "Cooling: Smart Liquid / Air Cooling",
      "battery.ess_ci_spec3": "Cert: CE / IEC62619 / UL9540A",
      "battery.ess_res_title": "Residential ESS Systems",
      "battery.ess_res_desc": "High-safety 5kWh–20kWh stackable and wall-mounted low/high voltage home battery systems compatible with leading solar hybrid inverters.",
      "battery.ess_res_spec1": "Capacity: 5.12kWh - 20.48kWh",
      "battery.ess_res_spec2": "Voltage: 51.2V / High Voltage",
      "battery.ess_res_spec3": "Compatibility: Growatt, Deye, Solis",
      "battery.btn_spec": "View Specifications",
      "battery.btn_inquire": "Inquire Price",

      "ev.title": "Special Purpose Vehicles & Channel Distribution",
      "ev.subtitle": "Providing bulk commercial vehicles, left/right hand drive configurations, and comprehensive export logistics.",
      "ev.passenger_title": "Commercial Delivery Vans & Utility Trucks",
      "ev.passenger_desc": "High-efficiency utility models with flexible chassis adaptation and competitive factory-direct export pricing.",
      "ev.commercial_title": "Special Purpose Municipal & Tank Trucks",
      "ev.commercial_desc": "Customized municipal sweepers, fuel/water tankers, and specialized service bodies.",
      "ev.fleet_title": "Tailored Fleet & Heavy Duty Logistics",
      "ev.fleet_desc": "Factory allocation and engineering adaptation guarantees for international operators.",

      // Why Rootze
      "why.title": "Why Global Buyers Choose Rootze",
      "why.subtitle": "Eliminating middlemen through direct factory equity, engineering access, and consolidated supply chain management.",
      "why.card1_title": "Direct Factory Equity & Exclusive Arm",
      "why.card1_desc": "As the equity-backed export division for our partner manufacturers, we offer true factory-direct pricing without extra distributor markups.",
      "why.card2_title": "Direct Engineering & Customization",
      "why.card2_desc": "Gain direct access to factory technical teams for tailored electrical adaptation, specialized vehicle bodying, and production line layout.",
      "why.card3_title": "Central China Industrial Heritage",
      "why.card3_desc": "Located in Xiangyang's renowned Dongfeng automotive and machinery corridor, we leverage mature supply chains for superior value output.",
      "why.card4_title": "Consolidated Supply & Quality Assurance",
      "why.card4_desc": "We manage 100% pre-shipment factory QC, multi-product container consolidation, seaworthy export packaging, and spare parts support.",

      // Legacy adv keys
      "adv.title": "Why Global Partners Choose Rootze",
      "adv.subtitle": "Eliminating middlemen through direct factory equity, engineering access, and consolidated supply chain management.",
      "adv.adv1_title": "Direct Factory Equity & Exclusive Arm",
      "adv.adv1_desc": "As the equity-backed export division for our partner manufacturers, we offer true factory-direct pricing without extra distributor markups.",
      "adv.adv2_title": "Direct Engineering & Customization",
      "adv.adv2_desc": "Gain direct access to factory technical teams for tailored electrical adaptation, specialized vehicle bodying, and production line layout.",
      "adv.adv3_title": "Central China Industrial Heritage",
      "adv.adv3_desc": "Located in Xiangyang's renowned Dongfeng automotive and machinery corridor, we leverage mature supply chains for superior value output.",
      "adv.adv4_title": "Consolidated Supply & Quality Assurance",
      "adv.adv4_desc": "We manage 100% pre-shipment factory QC, multi-product container consolidation, seaworthy export packaging, and spare parts support.",

      // How We Work
      "workflow.title": "How We Work",
      "workflow.subtitle": "Transparent, efficient, and factory-backed from initial technical consultation to global on-site delivery.",
      "workflow.step1_title": "1. Technical Consultation",
      "workflow.step1_desc": "Review technical requirements, site conditions, and custom specifications directly with engineering teams.",
      "workflow.step2_title": "2. Factory Proposal & Pricing",
      "workflow.step2_desc": "Receive transparent factory-direct pricing, line layout designs, and FOB/CIF commercial proposals.",
      "workflow.step3_title": "3. Production & Strict QC",
      "workflow.step3_desc": "Factory fabrication with progress milestone updates, witnessed pre-shipment inspections, and batch testing.",
      "workflow.step4_title": "4. Export Logistics & Support",
      "workflow.step4_desc": "Seaworthy packaging, customs clearance, shipping documentation, and global spare parts supply.",

      // Track Record (Legacy)
      "track.title": "Proven Distribution Track Record",
      "track.subtitle": "Delivering industrial solutions to partners worldwide.",
      "track.stat1_num": "50+",
      "track.stat1_label": "Global Export Destinations",
      "track.stat2_num": "2.5+",
      "track.stat2_label": "Industrial Equipment Units Distributed",
      "track.stat3_num": "100%",
      "track.stat3_label": "Factory Inspection Passed",
      "track.stat4_num": "24/7",
      "track.stat4_label": "Dedicated Multilingual Desk",

      // News Subpage
      "news.hero_title": "News & Industry Insights",
      "news.hero_subtitle": "Product updates, technical guides, and market developments from Central China's industrial manufacturing hub.",
      "news.filter_all": "All Insights",
      "news.filter_product": "Product Updates",
      "news.filter_industry": "Industry Insights",
      "news.filter_turnkey": "Turnkey Solutions",
      "news.art1_tag": "Product Update",
      "news.art1_date": "November 2, 2026",
      "news.art1_title": "Heavy-Duty Motor Starting Solutions: Selecting Solid-State Soft Starters for Harsh Industrial Environments",
      "news.art1_desc": "A comprehensive engineering guide on mitigating grid inrush currents, heat dissipation challenges, and choosing the right bypass protection for mining and pump stations.",
      "news.art2_tag": "Industry Insights",
      "news.art2_date": "October 28, 2026",
      "news.art2_title": "Precision Railway Maintenance: High-Accuracy Track Geometry Measurement Systems for Overseas Corridors",
      "news.art2_desc": "How in-house engineered track measurement tools enhance line inspection accuracy to ±0.1mm while slashing track maintenance downtime for international railway operators.",
      "news.art3_tag": "Turnkey Solutions",
      "news.art3_date": "October 20, 2026",
      "news.art3_title": "Turnkey Export: Establishing an Automated Automotive Brake Pad Production Line Abroad",
      "news.art3_desc": "From raw material mixing and high-tonnage thermal pressing to CNC arc grinding: how Rootze coordinates factory tooling, formula transfer, and site commissioning.",
      "news.btn_read": "Read Full Article",
      "news.btn_back": "Back to News",
      "news.cta_inquire": "Inquire About This Solution",
      "news.banner_title": "Need a Customized Industrial Supply Solution?",
      "news.banner_desc": "Connect directly with Rootze factory engineers and overseas trade specialists for immediate technical and pricing support.",
      "news.banner_btn": "Contact Our Sales Desk",

      // Contact Form
      "contact.title": "Request a Factory-Direct Quote",
      "contact.subtitle": "Connect with our international export division and factory engineers for wholesale tier pricing, spec sheets, and delivery timelines.",
      "contact.form_name": "Full Name",
      "contact.form_company": "Company Name",
      "contact.form_email": "Business Email / WhatsApp",
      "contact.form_category": "Interested Category",
      "contact.cat_opt1": "Industrial Electrical Systems (Soft Starters)",
      "contact.cat_opt2": "Railway Track Equipment & Maintenance Tools",
      "contact.cat_opt3": "Special Purpose Vehicles (SPV & Trucks)",
      "contact.cat_opt4": "Automotive Manufacturing Lines (Brake Pads)",
      "contact.cat_opt5": "Other Custom Industrial Solutions",
      "contact.form_quantity": "Estimated Quantity / Delivery Country",
      "contact.form_message": "Tell us about your project requirements...",
      "contact.send": "Submit B2B Inquiry",
      "contact.btn_sending": "Sending Inquiry...",
      "contact.sent_direct_title": "Inquiry Delivered to Our Inbox!",
      "contact.sent_direct_desc": "Thank you! Your quotation request has been sent directly to our export desk. We will get back to you within 24 hours.",
      "contact.whatsapp_cta": "Chat with Us on WhatsApp",
      "contact.whatsapp_sub": "Direct line for instant factory quotes and engineering consultation",
      "contact.whatsapp_btn": "Start Instant Chat",
      "contact.ph_name": "John Doe",
      "contact.ph_company": "Global Industrial Corp",
      "contact.ph_email": "sales@rootzeglobal.com / +86 151 6820 3740",
      "contact.ph_quantity": "e.g. 5 units 10kV soft starters or 1 brake pad line",
      "contact.ph_message": "Please describe target models, delivery dates, or custom technical specs...",
      "contact.modal_btn_mail": "Open Email Client",
      "contact.modal_btn_wa": "Send via WhatsApp",
      "contact.modal_btn_copy": "Copy Inquiry Text",
      "contact.modal_copied": "Copied to clipboard!",
      "contact.direct_info_title": "Contact Information",
      "contact.email_label": "Official Business Email",
      "contact.email_val": "sales@rootzeglobal.com",
      "contact.office_label": "Global Operations Hub",
      "contact.office_val": "Dongfeng Automotive & Heavy Machinery Corridor, Xiangyang, Hubei, China",
      "contact.success_title": "Inquiry Prepared Successfully!",
      "contact.success_desc": "Your inquiry details have been formatted. Click below to launch your email client or chat directly on WhatsApp.",

      "modal.spec_title": "Product Technical Specifications",
      "modal.close": "Close",
      "modal.btn_inquire": "Inquire About This Model",

      "footer.about_title": "About Rootze",
      "footer.about_text": "Rootze operates as the authorized international export arm for an equity-partnered coalition of specialized industrial equipment, railway tools, special purpose vehicles, and automotive manufacturing lines in Xiangyang, Hubei, China.",
      "footer.quick_links": "Quick Links",
      "footer.products_title": "Product Categories",
      "footer.copyright": "© 2026 襄阳如志进出口有限公司 Xiangyang Ruzhi Import & Export Co., Ltd. All rights reserved."
    },
    zh: {
      "brand.name": "Rootze",
      "brand.legal_name": "襄阳如志进出口有限公司",
      "brand.tagline": "工业装备与特种车辆出海平台",

      "nav.home": "首页",
      "nav.products": "核心产品",
      "nav.about": "关于我们",
      "nav.news": "新闻动态",
      "nav.contact": "商业合作",
      "nav.quote": "立即询价",

      // Legacy nav keys
      "nav.battery": "核心产品",
      "nav.ev": "专用车辆",
      "nav.advantages": "核心优势",
      "nav.track": "实力指标",

      "hero.badge": "工厂股权直连 • 湖北襄阳重工制造集群",
      "hero.title": "依托中国中部制造重镇，工厂股权直连的工业装备与特种车辆出海合作伙伴",
      "hero.subtitle": "直连中国中部（襄阳）参股制造企业，提供原厂直供价格、专属工程定制支持与长效供应保障。",
      "hero.feature1": "工厂股权直联 无中间商溢价",
      "hero.feature2": "原厂总工程师团队直接技术支持",
      "hero.feature3": "襄阳成熟汽车与重工走廊底蕴",
      "hero.cta_products": "浏览核心供应板块",
      "hero.cta_contact": "获取工厂报价",
      "hero.cta_battery": "浏览核心供应板块",

      "subheading.about": "企业实力与背景",
      "subheading.products": "四大核心业务板块",
      "subheading.why": "为什么选择如志",
      "subheading.workflow": "四步出海流程",
      "subheading.news": "行业观察与产品动态",
      "subheading.contact": "商务洽谈与询价",

      // Legacy subheadings
      "subheading.battery": "四大核心业务板块",
      "subheading.ev": "特种车辆与商用车",
      "subheading.adv": "为什么选择如志",
      "subheading.track": "全球出海足迹",

      // About Us
      "about.title": "襄阳专精特新制造集群授权国际出口部门",
      "about.subtitle": "立足中国重型机械与汽车零部件核心枢纽（湖北襄阳），以工厂股权与独家代理为纽带，让中国智造直达全球。",
      "about.body1": "如志进出口（Rootze）根植于湖北省——中国中部重型机械与汽车零部件产业核心走廊（依托襄阳深厚的东风汽车与军工重工底蕴）。我们作为本地多家专精特新制造企业的授权国际出口代表处与外贸综合运作平台。",
      "about.body2": "通过直接参与工厂股权投资以及签署海外独家代理协议，Rootze 彻底打破冗余的中间分销壁垒。海外采购商既能享受直面原厂工程师团队的定制技术支持与真正出厂裸价，又能获得规范高效的国际商检、报关海运与外贸供应链保障。",

      // Products (4 Core Categories)
      "products.title": "四大核心工业制造与专用车板块",
      "products.subtitle": "原厂直供工业电控柜、高精度铁路工务检测养护装备、特种商用改装车辆及汽车刹车片整套产线装备。",
      "products.cat1_title": "工业电气系统（高低压软起动柜）",
      "products.cat1_desc": "高低压固态软起动器、变频控制柜及大功率电机配电电控系统，专为矿山开采、泵站供水、冶金化工等重工严苛工况设计。",
      "products.cat1_spec1": "适用电压：低压 380V-690V / 高压 3kV-10kV",
      "products.cat1_spec2": "功率范围：最高支持 10,000 kW 重载起动",
      "products.cat1_spec3": "防护等级：具备全电机旁路智能保护，IP40-IP54",
      "products.cat2_title": "铁路工务养护设备与检测仪器",
      "products.cat2_desc": "拥有自主核心技术的高精度铁路轨道几何状态检测仪，辅以全系列铁路线路养护机械、内燃/液压工务动力工具及轨道道岔零配件。",
      "products.cat2_spec1": "测量精度：轨距/水平误差 ±0.1mm 级",
      "products.cat2_spec2": "应用范围：道岔全断面测量仪与轨向检测",
      "products.cat2_spec3": "轻量便携：高强度铝合金机身，数字实时显示",
      "products.cat3_title": "特种专用汽车与商用运输车辆",
      "products.cat3_desc": "涵盖冷链物流冷藏车、洒水/供水车、燃油与危化品专用罐车、道路清扫清洗车、随车起重车及市政应急保障专用车辆。",
      "products.cat3_spec1": "车型覆盖：冷藏冷链、流体罐车、市政环卫、工程车",
      "products.cat3_spec2": "底盘匹配：东风、陕汽、重汽等成熟出海底盘",
      "products.cat3_spec3": "合规出口：完备出海公告、左右舵可选与滚装防护",
      "products.cat4_title": "汽车零部件整线装备（刹车片产线）",
      "products.cat4_desc": "交钥匙汽车刹车片与摩擦材料全套生产线设备：涵盖原材料自动配料混料机、多工位热压成型机、高精外弧双端磨床及全自动装配包装线。",
      "products.cat4_spec1": "产能定制：年产 50 万套至 500 万套整线定制",
      "products.cat4_spec2": "全套赋能：提供摩擦配方工艺、定制模具与厂房规划",
      "products.cat4_spec3": "自动化：全线 PLC 闭环控制、除尘环保与 ISO 达标",
      "products.btn_spec": "查看技术参数",
      "products.btn_inquire": "获取工厂报价",

      // Legacy product keys
      "battery.title": "核心动力电池与储能系统方案",
      "battery.subtitle": "工业级动力电芯、定制电池 PACK 与模块化储能系统，具备高安全性、高能量密度与超长循环寿命。",
      "battery.cell_title": "动力方形 LFP 与三元锂电芯",
      "battery.cell_desc": "一线大厂 A 规磷酸铁锂与三元锂方形单体电芯，专为电动乘用车、商用改装及重型电池包 PACK 研发定制。",
      "battery.cell_spec1": "材料体系：LFP 磷酸铁锂 / 三元锂",
      "battery.cell_spec2": "容量区间：100Ah - 314Ah 单体",
      "battery.cell_spec3": "循环寿命：4000 - 6000 次深循环",
      "battery.ess_ci_title": "工商业储能系统（C&I ESS）",
      "battery.ess_ci_desc": "100kWh 至 2MWh 模块化户外液冷/风冷储能柜，支持峰谷套利、微电网配储及光储一体化工程。",
      "battery.ess_ci_spec1": "容量配置：100kWh - 2MWh 模块化",
      "battery.ess_ci_spec2": "温控方案：智能液冷 / 强制风冷",
      "battery.ess_ci_spec3": "认证标准：CE / IEC62619 / UL9540A",
      "battery.ess_res_title": "户用储能系统（Residential ESS）",
      "battery.ess_res_desc": "5kWh 至 20kWh 壁挂式及堆叠式低压/高压家庭储能系统，广泛兼容全球主流光伏逆变器品牌。",
      "battery.ess_res_spec1": "电池容量：5.12kWh - 20.48kWh",
      "battery.ess_res_spec2": "电压等级：51.2V / 高压串联",
      "battery.ess_res_spec3": "适配逆变器：古瑞瓦特、德业、锦浪等",
      "battery.btn_spec": "查看规格书",
      "battery.btn_inquire": "获取报价",

      "ev.title": "新能源汽车整车渠道分销",
      "ev.subtitle": "面向海外车商与车队运营商，提供主流纯电车型配额直供、左右舵适配、报关出口及滚装海运全流程支持。",
      "ev.passenger_title": "纯电乘用轿车与家用 SUV",
      "ev.passenger_desc": "涵盖 400km–650km CLTC 续航的主流高性价比纯电车型，支持高压快充与批量外贸批发折扣。",
      "ev.commercial_title": "城市商用物流车与轻卡",
      "ev.commercial_desc": "专为海外城市配送与车队运营打造的高载重纯电面包车和轻量化货车，显著削减全生命周期运营成本。",
      "ev.fleet_title": "车队集采与特种纯电定制",
      "ev.fleet_desc": "针对出租车网络、公共出行与企业车队，提供批量工厂配额保障与定制化零配件海外保障方案。",

      // Why Rootze
      "why.title": "全球采购商为何选择如志",
      "why.subtitle": "以工厂股权与技术直联为基石，彻底剔除中间差价，提供全流程高可靠出海支持。",
      "why.card1_title": "工厂股权投资与独家出口代表",
      "why.card1_desc": "作为合伙制造工厂的直属股权出海部门，提供真正原厂裸价，彻底杜绝多层贸易商层层加价。",
      "why.card2_title": "原厂总工直联与专属技术定制",
      "why.card2_desc": "直面原厂工程师技术团队，支持软起动器参数调校、特种车上装非标定制与整厂工艺规划。",
      "why.card3_title": "中国中部产业集群与成本优势",
      "why.card3_desc": "根植湖北襄阳国家级汽车与装备制造走廊，依托成熟产业集群与供应链协同，兼具精湛工艺与极致性价比。",
      "why.card4_title": "集约集运出海与 100% 严格质检",
      "why.card4_desc": "实行出厂前 100% 全流程质检验收，支持多品类集装箱拼装配货、远洋防潮包装与长期备品备件保障。",

      // Legacy adv keys
      "adv.title": "选择 RootZe 的核心优势",
      "adv.subtitle": "以工厂股权与技术直联为基石，彻底剔除中间差价，提供全流程高可靠出海支持。",
      "adv.adv1_title": "工厂股权投资与独家出口代表",
      "adv.adv1_desc": "作为合伙制造工厂的直属股权出海部门，提供真正原厂裸价，彻底杜绝多层贸易商层层加价。",
      "adv.adv2_title": "原厂总工直联与专属技术定制",
      "adv.adv2_desc": "直面原厂工程师技术团队，支持软起动器参数调校、特种车上装非标定制与整厂工艺规划。",
      "adv.adv3_title": "中国中部产业集群与成本优势",
      "adv.adv3_desc": "根植湖北襄阳国家级汽车与装备制造走廊，依托成熟产业集群与供应链协同，兼具精湛工艺与极致性价比。",
      "adv.adv4_title": "集约集运出海与 100% 严格质检",
      "adv.adv4_desc": "实行出厂前 100% 全流程质检验收，支持多品类集装箱拼装配货、远洋防潮包装与长期备品备件保障。",

      // How We Work
      "workflow.title": "四步出海合作流程",
      "workflow.subtitle": "从最初的技术对接，到工厂直供方案交付，全程透明高效。",
      "workflow.step1_title": "1. 需求与技术咨询",
      "workflow.step1_desc": "与原厂工程师一对一对接工况参数、图纸要求及定制化技术指标。",
      "workflow.step2_title": "2. 工厂直供方案与报价",
      "workflow.step2_desc": "出具无溢价原厂出水价、整线设备布局图及详尽的国际贸易商务清单。",
      "workflow.step3_title": "3. 定制排产与严格质检",
      "workflow.step3_desc": "工厂透明化排产制造，支持第三方与远程视频验厂质检，提供完整出厂报告。",
      "workflow.step4_title": "4. 报关海运与长期售后",
      "workflow.step4_desc": "专业远洋适航包装、报关通关物流直达，提供长期原厂备件与海外技术指导。",

      // Track Record (Legacy)
      "track.title": "全球分销交付实力看板",
      "track.subtitle": "为全球合作伙伴持续提供高可靠的工业装备支持。",
      "track.stat1_num": "50+",
      "track.stat1_label": "出海覆盖国家与地区",
      "track.stat2_num": "2.5+",
      "track.stat2_label": "万台/套 累计交付工业装备",
      "track.stat3_num": "100%",
      "track.stat3_label": "出厂原装质检合格率",
      "track.stat4_num": "24/7",
      "track.stat4_label": "专属多语言外贸顾问支持",

      // News Subpage
      "news.hero_title": "新闻动态与行业观察",
      "news.hero_subtitle": "深度解读工业电控、特种车上装、铁路工务装备及零部件产线出海动态与技术指南。",
      "news.filter_all": "全部动态",
      "news.filter_product": "产品更新",
      "news.filter_industry": "行业深度",
      "news.filter_turnkey": "交钥匙产线",
      "news.art1_tag": "产品更新",
      "news.art1_date": "2026年11月2日",
      "news.art1_title": "矿山与重工业电机平稳启动：高低压固态软起动器在海外工况中的选型要点",
      "news.art1_desc": "深入解析高压大功率电机直接启动的电网冲击与机械磨损痛点，探讨在严苛矿区与水利工程中配置固态软起动柜的防护标准与选型逻辑。",
      "news.art2_tag": "行业深度",
      "news.art2_date": "2026年10月28日",
      "news.art2_title": "铁路轨道毫米级巡检与养护：高精度轨距轨向综合检测仪在海外线路中的应用",
      "news.art2_desc": "针对跨国干线与城市轻轨提速带来的维保高标准，解析具有自主知识产权的高精轨道几何状态检测仪如何实现现场快速测量与数字化建档。",
      "news.art3_tag": "交钥匙产线",
      "news.art3_date": "2026年10月20日",
      "news.art3_title": "交钥匙工程：如何在海外快速搭建一条年产数百万套的汽车刹车片全自动生产线",
      "news.art3_desc": "依托襄阳汽车零部件全产业链积淀，从配料混配、热压成型到双端精密研磨与包装，全面解析整线设备出口、配方指导与现场交付实施方案。",
      "news.btn_read": "阅读全文",
      "news.btn_back": "返回新闻列表",
      "news.cta_inquire": "咨询该方案详情",
      "news.banner_title": "需要原厂直供的设备与车辆定制方案？",
      "news.banner_desc": "直面原厂工程师团队，获取详尽的技术规格书与一手工厂出口报价。",
      "news.banner_btn": "联系外贸业务部",

      // Contact Form
      "contact.title": "获取原厂出口报价与商务洽谈",
      "contact.subtitle": "直接联系如志外贸代表处与原厂工程师团队，获取专属技术方案、一手出厂报价及出海船期计划。",
      "contact.form_name": "您的姓名",
      "contact.form_company": "企业名称",
      "contact.form_email": "业务邮箱 / WhatsApp",
      "contact.form_category": "意向采购品类",
      "contact.cat_opt1": "工业电气系统（软起动柜/电控柜）",
      "contact.cat_opt2": "铁路工务养护设备与检测仪器",
      "contact.cat_opt3": "特种专用车辆与商用改装车",
      "contact.cat_opt4": "汽车零部件整线装备（刹车片产线）",
      "contact.cat_opt5": "其他综合工业设备定制需求",
      "contact.form_quantity": "预估采购量 / 目标交付国",
      "contact.form_message": "请简述您的项目背景或规格要求...",
      "contact.send": "提交 B2B 询价",
      "contact.btn_sending": "正在发送中...",
      "contact.sent_direct_title": "询盘已成功送达负责人邮箱！",
      "contact.sent_direct_desc": "感谢您的询盘！您的采购需求已直接送达我司外贸出口部负责人邮箱，我们将在 24 小时内为您提供正式报价与交期答复。",
      "contact.whatsapp_cta": "WhatsApp 一键直连对话",
      "contact.whatsapp_sub": "一手原厂出口报价与技术方案即时沟通专线",
      "contact.whatsapp_btn": "发起 WhatsApp 对话",
      "contact.ph_name": "例如：张经理",
      "contact.ph_company": "例如：海外重工机械设备有限公司",
      "contact.ph_email": "sales@rootzeglobal.com / +86 151 6820 3740",
      "contact.ph_quantity": "例如：5 台 10kV 高压软起动柜，或一条年产 100 万套刹车片产线出口中东",
      "contact.ph_message": "请简要描述您的采购型号、交付周期或特殊定制规格...",
      "contact.modal_btn_mail": "调起邮件客户端发送",
      "contact.modal_btn_wa": "通过 WhatsApp 发送",
      "contact.modal_btn_copy": "复制询盘文本",
      "contact.modal_copied": "已成功复制到剪贴板！",
      "contact.direct_info_title": "直接联络方式",
      "contact.email_label": "官方商务邮箱",
      "contact.email_val": "sales@rootzeglobal.com",
      "contact.office_label": "全球运营与外贸枢纽",
      "contact.office_val": "中国湖北省襄阳市东风汽车与高新重工产业带",
      "contact.success_title": "询盘草稿已准备就绪！",
      "contact.success_desc": "您的询价内容已格式化完毕。点击下方按钮即可唤醒邮件客户端发送，或通过 WhatsApp 直接对话。",

      "modal.spec_title": "产品技术规格参数详情",
      "modal.close": "关闭",
      "modal.btn_inquire": "针对该产品立即询价",

      "footer.about_title": "关于如志",
      "footer.about_text": "襄阳如志进出口有限公司（Rootze Global）依托湖北襄阳汽车与重工装备制造基地，作为多家专精特新制造厂的授权国际出口部门，为全球采购商直供高可靠工业装备与特种车辆。",
      "footer.quick_links": "快捷导航",
      "footer.products_title": "产品板块",
      "footer.copyright": "© 2026 襄阳如志进出口有限公司 版权所有。"
    }
  };

  var currentLang = 'en';

  function getLanguage() {
    return currentLang;
  }

  function t(key) {
    if (!translations[currentLang]) {
      return translations.en[key] || key;
    }
    return translations[currentLang][key] || translations.en[key] || key;
  }

  function setLanguage(lang) {
    if (!translations[lang]) {
      lang = 'en';
    }
    currentLang = lang;
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        window.localStorage.setItem('rootze_lang', lang);
      }
    } catch (e) {
      // localStorage may fail in private mode
    }

    if (typeof document !== 'undefined') {
      if (document.documentElement) {
        document.documentElement.setAttribute('lang', lang);
      }
      if (document.querySelectorAll) {
        // Update text nodes
        var elements = document.querySelectorAll('[data-i18n]');
        for (var i = 0; i < elements.length; i++) {
          var el = elements[i];
          var key = el.getAttribute('data-i18n');
          var val = t(key);
          if (val) {
            el.innerHTML = val;
          }
        }

        // Update placeholders
        var placeholders = document.querySelectorAll('[data-i18n-placeholder]');
        for (var j = 0; j < placeholders.length; j++) {
          var pel = placeholders[j];
          var pkey = pel.getAttribute('data-i18n-placeholder');
          var pval = t(pkey);
          if (pval) {
            pel.setAttribute('placeholder', pval);
          }
        }

        // Update switcher active buttons
        var btns = document.querySelectorAll('.lang-btn');
        for (var k = 0; k < btns.length; k++) {
          var btn = btns[k];
          if (btn.getAttribute('data-lang') === lang) {
            btn.classList.add('active');
          } else {
            btn.classList.remove('active');
          }
        }
      }
    }
  }

  function init() {
    var saved = null;
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        saved = window.localStorage.getItem('rootze_lang');
      }
    } catch (e) {}

    if (saved && (saved === 'en' || saved === 'zh')) {
      setLanguage(saved);
    } else {
      setLanguage('en');
    }
  }

  var RootZeI18n = {
    init: init,
    setLanguage: setLanguage,
    getLanguage: getLanguage,
    t: t,
    translations: translations
  };

  if (typeof window !== 'undefined') {
    window.RootZeI18n = RootZeI18n;
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = RootZeI18n;
  }
})(typeof window !== 'undefined' ? window : globalThis);
