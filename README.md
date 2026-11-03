# Rootze Global — Factory-Backed Industrial & Vehicle Export Portal

[![Bilingual](https://img.shields.io/badge/Language-English%20%7C%20%E4%B8%AD%E6%96%87-blue.svg)](#-襄阳如志进出口有限公司---全球工业装备与专用汽车出海门户)
[![Custom Domain](https://img.shields.io/badge/Domain-rootzeglobal.com-success.svg)](https://rootzeglobal.com)
[![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-181717.svg?logo=github)](https://rootzeglobal.com)
[![Automated Tests](https://img.shields.io/badge/Tests-36%20Passing-brightgreen.svg)](#-automated-testing--quality-verification)

> **Quick Language Switch / 语言快速跳转**:  
> 👉 [🇨🇳 Switch to Chinese Document / 中文版本](#-襄阳如志进出口有限公司---全球工业装备与专用汽车出海门户)

---

## 🌐 Official Website & Live Portal

* **Official Domain**: [https://rootzeglobal.com](https://rootzeglobal.com)
* **Corporate Entity**: Xiangyang Ruzhi Import & Export Co., Ltd. (襄阳如志进出口有限公司)
* **Brand Name**: **Rootze Global** (如志全球)
* **Headquarters & Industrial Hub**: Xiangyang, Hubei Province, China — the central manufacturing corridor for Dongfeng commercial vehicles and high-end machinery.

---

## 🏢 Corporate Background & Supply Model

**Rootze Global** (Xiangyang Ruzhi Import & Export Co., Ltd.) is an equity-backed direct export arm established for specialized industrial equipment and commercial vehicle manufacturers in Central China. 

Unlike conventional trading middlemen, Rootze operates with direct manufacturer equity alignment, providing global B2B procurement managers, EPC contractors, and international distributors with:
1. **Factory-Direct Pricing**: Direct access to top-tier manufacturing cost baselines without multi-layered intermediary markups.
2. **Factory-Backed Engineering**: In-house customization, CAD/BOM engineering reviews, and tailored voltage/power/chassis configurations.
3. **Consolidated Logistics & Quality Control**: Pre-shipment dyno/bench testing, third-party SGS/BV inspection coordination, and full container export clearance.

---

## 📦 Core Export Portfolio & Website Architecture

The Rootze Global international portal is structured as a modular, high-conversion B2B export platform comprising a single-page corporate portal (`index.html`), dedicated sector catalog subpages (`products/*.html`), and an independent news center (`news.html`).

### 1. Dedicated Product Catalog Subpages
* **[Industrial Electrical Systems](products/electrical-systems.html)** (`products/electrical-systems.html`):  
  High- and low-voltage solid-state motor soft starters (380V to 10kV, up to 15,000kW), liquid resistance starters, medium-voltage variable frequency drives (VFD), reactive power compensation cabinets, and KYN28 indoor metal-clad switchgear. Powered by technology partnerships with Renle and Leishen Electric.
* **[Railway Track Equipment & Maintenance Tools](products/railway-equipment.html)** (`products/railway-equipment.html`):  
  Precision digital railway track gauges, 0.01mm high-precision superelevation rulers, switch rail gauges, internal combustion rail tamping picks, abrasive rail cutting machines, and hydraulic rail tension adjusters. Engineered for international rail gauges (1435mm standard, 1000mm meter, 1676mm broad) in collaboration with Haite and Linkage.
* **[Special Purpose Vehicles (SPV) & Commercial Trucks](products/special-vehicles.html)** (`products/special-vehicles.html`):  
  Municipal road sweepers, high-pressure dust suppression water tankers, multi-temperature cold-chain refrigerated delivery trucks, and heavy-duty engineering dump tippers built on robust Dongfeng commercial chassis.
* **[Turnkey Brake Pad Production Lines](products/brake-pad-lines.html)** (`products/brake-pad-lines.html`):  
  Complete end-to-end manufacturing solutions for automotive disc and drum brake pads: raw material weighing & three-dimensional mixing, 200T–500T multi-cavity hydraulic hot presses, heat-treatment curing ovens, CNC outer arc grinders and multi-spindle drilling machines, automated electrostatic powder coating lines, and OE friction formulations.

### 2. Dedicated News & Industry Insights Center
* **[News & Insights Portal](news.html)** (`news.html`):  
  Features category-filtered bilingual articles (Product Updates, Industry Insights, Turnkey Solutions) with an interactive modal reader allowing global buyers to study technical whitepapers and inquire directly without page reloads.

### 3. Homepage Architecture (`index.html`)
* **Hero Banner (`#home`)**: High-impact factory-direct procurement positioning with dual CTAs.
* **About Us (`#about`)**: Xiangyang industrial heritage and equity-backed export methodology.
* **What We Supply (`#products`)**: High-spec sector showcase cards with instant specification modal dialogs.
* **Why Rootze (`#advantages`)**: Core value pillars covering direct factory equity, engineering support, regional heritage, and quality assurance.
* **How We Work (`#workflow`)**: Transparent 4-step B2B export workflow (Consultation → Factory Proposal → Production & QC → Export & After-Sales).
* **Contact & Quotation (`#contact`)**: Interactive RFQ form with category preselection, direct WhatsApp chat, and team email.

---

## 🎨 Design Philosophy & Technical Hallmarks

* **B2B Export High-Conversion Aesthetics**:  
  Professional dark automotive/industrial theme (`#070707` background, titanium accents) paired with WCAG AAA compliant contrast, crisp typography, and official transparent brand logos.
* **Zero-Refresh Native Bilingual Engine (`js/i18n.js`)**:  
  Client-side symmetric English and Chinese translation dictionaries with `data-i18n` binding. Language preferences automatically persist across pages via `localStorage`.
* **Zero-Backend Serverless Inquiry Delivery**:  
  Uses **Web3Forms** for instant direct-to-inbox inquiry delivery with a zero-lead-drop failover architecture:
  $$\text{Web3Forms AJAX} \longrightarrow \text{Smart Mailto Generator} \longrightarrow \text{Direct WhatsApp Chat}$$
* **100% Zero-Backend Static Hosting**:  
  Runs purely on GitHub Pages with global CDN caching, zero database overhead, and strict relative asset paths.

---

## 📱 Multi-Device & Responsive Adaptation

The portal is engineered and tested across mobile phones, tablets, laptops, and ultra-wide desktop monitors:

* **Fluid Responsive Grid**: Built on Bootstrap 4 Flexbox architecture with custom breakpoint styling (`css/rootze.css`).
* **Mobile-Responsive Spec Tables (No Horizontal Scroll)**:  
  Traditional wide specification tables automatically reflow into clean, stacked responsive attribute cards on small viewports (`max-width: 767px`), completely eliminating cumbersome horizontal scrollbars on mobile devices.
* **Modal Viewport Fit**:  
  Specification modals and news reading dialogs dynamically calculate viewport dimensions, providing comfortable vertical scrolling and prominent mobile touch-friendly close buttons.
* **Equal-Height Flex Card Alignment**:  
  The contact inquiry form and the WhatsApp business card enforce strict equal-height flex alignment, ensuring the submit button and chat links remain visually anchored on desktop while stacking neatly on mobile.

---

## 📞 Official Contact Channels

* **Direct WhatsApp**: [+86 15168203740](https://wa.me/8615168203740)
* **Official Corporate Email**: [sales@rootzeglobal.com](mailto:sales@rootzeglobal.com)
* **Online RFQ**: Available via the contact form on [https://rootzeglobal.com/#contact](https://rootzeglobal.com/#contact)

---

## 💻 Engineering & Developer Guide

### 1. Modular Partial Compilation Pipeline
The website utilizes a clean, dependency-free Python build script that combines modular HTML partials from `src/` into distribution HTML pages:
```bash
python3 scripts/build.py
```
* `src/partials/` $\longrightarrow$ `index.html`
* `src/partials-news/` $\longrightarrow$ `news.html`
* `src/partials-products/` $\longrightarrow$ `products/*.html`

### 2. One-Click Local Preview
Launch a local development server and automatically open your default browser:
```bash
./preview.sh
```
Or via Python:
```bash
python3 -m http.server 8000
```

### 3. Automated Testing & Quality Verification
The repository enforces a comprehensive automated test suite built with Node.js built-in test runner (`node:test`):
```bash
node --test tests/*.test.mjs
```
* `tests/assets.test.mjs`: Scaffolding integrity (`.nojekyll`, CSS, JS, fonts, images).
* `tests/i18n.test.mjs`: Complete EN/ZH key symmetry and translation validity.
* `tests/structure.test.mjs`: Semantic sections, relative asset paths, and data-i18n attributes.
* `tests/product-specs-responsive.test.mjs`: Mobile no-horizontal-scroll contracts and table card view.
* `tests/contact-alignment.test.mjs`: Equal-height flex contracts and bottom alignment.
* `tests/full-audit.test.mjs`: End-to-end GitHub Pages deployment readiness.
* `tests/readme.test.mjs`: Bilingual documentation integrity, links, and contact channels.

### 4. GitHub Pages Deployment
1. Ensure the `CNAME` file contains `rootzeglobal.com`.
2. Ensure `.nojekyll` exists in the repository root.
3. Push to `main` branch. GitHub Pages will automatically serve the site worldwide with custom SSL enabled.

---
---

<a id="-襄阳如志进出口有限公司---全球工业装备与专用汽车出海门户"></a>
# 襄阳如志进出口有限公司 — 全球工业装备与专用汽车出海门户

[![双语支持](https://img.shields.io/badge/%E8%AF%AD%E8%A8%80-%E4%B8%AD%E6%96%87%20%7C%20English-blue.svg)](#rootze-global--factory-backed-industrial--vehicle-export-portal)
[![独立域名](https://img.shields.io/badge/%E5%AE%98%E6%96%B9%E5%9F%9F%E5%90%8D-rootzeglobal.com-success.svg)](https://rootzeglobal.com)
[![GitHub Pages](https://img.shields.io/badge/%E6%89%98%E7%AE%A1-GitHub%20Pages-181717.svg?logo=github)](https://rootzeglobal.com)
[![自动化测试](https://img.shields.io/badge/%E6%B5%8B%E8%AF%95-36%20%E9%A1%B9%E9%80%9A%E8%BF%87-brightgreen.svg)](#3-自动化测试与质量验证)

> **导航快速跳转**:  
> 👉 [🌐 Back to English / 返回英文版本](#rootze-global--factory-backed-industrial--vehicle-export-portal)

---

## 🌐 官方门户与企业主体

* **官方独立域名**：[https://rootzeglobal.com](https://rootzeglobal.com)
* **企业主体全称**：**襄阳如志进出口有限公司**
* **英文名称 / 国际品牌**：**Xiangyang Ruzhi Import & Export Co., Ltd. / Rootze Global**
* **总部与产业基地**：中国·湖北省襄阳市 —— 国家级东风商用车产业基地与华中高端智能制造走廊。

---

## 🏢 企业资质与实体工厂直联出海模式

**襄阳如志进出口有限公司**（Rootze Global）是湖北襄阳高端智能装备与专用汽车制造集群的直系工厂股权合作出海平台。

不同于传统的信息倒手型外贸中间商，如志进出口与核心生产基地建立了深度股权与产销合作机制，为海外大型工矿企业、EPC 国际工程总包商、海外铁路工务段及商用车分销商提供：
1. **实体工厂直通底价**：穿透多层中间贸易环节，提供原厂制造基准价格；
2. **原厂工程师技术支持**：提供售前深度技术咨询、非标图纸参数会审（CAD/BOM）、电压制式定制与底盘上装适配；
3. **集约化品控与出口交付**：出厂台架测试、第三方（SGS/BV）验货支持、原厂配件长期供应及全集装箱集港出口。

---

## 📦 出海核心板块与网站内容全景

站点采用高转化 B2B 国际站架构，由首页门户（`index.html`）、四大独立产品深度目录页（`products/*.html`）以及独立新闻与技术中心（`news.html`）组成。

### 1. 四大独立产品深度目录页
* **[工业电气自动化及电机软起动系统](products/electrical-systems.html)** (`products/electrical-systems.html`)：  
  高低压固态软起动器（380V 至 10kV，功率覆盖至 15,000kW）、液体电阻软起动装置、中高压变频器（VFD）、无功功率补偿柜及 KYN28 户内铠装式高压开关柜。整合雷诺尔、雷神电气等行业领先制造实力。
* **[铁路工务养护及轨道测量智能装备](products/railway-equipment.html)** (`products/railway-equipment.html`)：  
  高精度数字数显轨距尺、0.01mm 测角级超高尺、支距与道岔测量仪、内燃捣固镐、内燃切轨机及液压轨缝调整器。全面支持国际标准轨距（1435mm）、米轨（1000mm）及宽轨（1676mm），由海特、联控等原厂精工制造。
* **[专用汽车及新能源商用车](products/special-vehicles.html)** (`products/special-vehicles.html`)：  
  依托襄阳东风汽车工业底盘优势，供应多功能道路洗扫车、高压抑尘雾炮洒水车、多温区冷链物流冷藏车以及矿山工程自卸车。
* **[刹车片成套生产线装备与摩擦材料](products/brake-pad-lines.html)** (`products/brake-pad-lines.html`)：  
  提供盘式/鼓式刹车片整线交钥匙出口工程：原材料精准称重与三维混合机、200T–500T 多腔精密热压成型机、热处理固化箱、CNC 双磨头外弧磨削与多孔钻床、全自动静电喷涂线、摩擦材料 OE 配方及配套剪切/摩擦试验机。

### 2. 独立新闻与技术洞察中心
* **[新闻与行业洞察中心](news.html)** (`news.html`)：  
  提供分类过滤（产品动态、行业洞察、交钥匙方案）的中英双语行业深度报告，配备免刷新模态阅读器，方便海外买家直接在线研读技术白皮书并直接发起询盘。

### 3. 首页架构模块流转（`index.html`）
* **主视觉 Hero Banner (`#home`)**：明确工厂直系出海定位，双 CTA 引导询盘与选型；
* **关于我们 Who We Are (`#about`)**：阐述襄阳工业走廊底蕴与工厂直联出海模式；
* **核心供应 What We Supply (`#products`)**：四大核心板块高规格展示卡片，支持快速弹窗查阅详细参数；
* **企业优势 Why Rootze (`#advantages`)**：工厂直销、工程定制、产业带底蕴、联合品控四大公信力支柱；
* **合作流程 How We Work (`#workflow`)**：技术会审 $\to$ 原厂报价 $\to$ 生产质检 $\to$ 出口维保 4 步透明闭环；
* **联系与询盘 RFQ (`#contact`)**：品类自动带入表单、WhatsApp 即时沟通与官方邮箱。

---

## 🎨 网站设计思路与技术选型

* **高公信力 B2B 出海视觉**：  
  采用沉稳大气的现代工业深色调（`#070707` 底色与钛金质感强调色），严格遵循 WCAG AAA 级无障碍文字高对比度标准，搭载矢量透明官方 LOGO（`images/logo-horizontal.png`、`images/logo-white.png`）。
* **轻量纯前端中英双语引擎 (`js/i18n.js`)**：  
  零依赖原生 JavaScript 字典架构，通过 `data-i18n` 属性实现整站文字瞬间切换，无需刷新页面；用户语言选择通过 `localStorage` 自动跨页面保持。
* **零服务器成本三级防丢单询盘闭环**：  
  集成 **Web3Forms** 服务，海外买家提交询盘后直飞业务负责人邮箱；同时提供自动化降级链路：
  $$\text{Web3Forms 异步提交} \longrightarrow \text{本地智能邮件唤起 (mailto)} \longrightarrow \text{WhatsApp 在线客服}$$
  确保在任何网络环境下商机 100% 留存。
* **100% 静态免维护架构**：  
  直接托管于 GitHub Pages，结合 CDN 全球极速分发，全站采用严格相对路径，零数据库、零运维隐患。

---

## 📱 多端设备全视口响应式规范

全站经过严格跨端测试，无缝适配手机、平板、笔记本及超宽桌面显示器：

* **全响应式流式布局**：基于 Bootstrap 4 Flexbox 与专用媒体查询（`css/rootze.css`）；
* **移动端参数表卡片化响应（消除横向滚动条）**：  
  针对手机等小屏幕设备（`max-width: 767px`），原有横向对比表格自动重构为自适应垂直卡片列表，**彻底消除移动端表格横向滚动带来的操作不适**；
* **弹窗视口自适应**：  
  技术参数弹窗与新闻阅读弹窗采用动态最大高度计算与纵向平滑滚动，并针对移动端设计了触控友好的关闭与直联按钮；
* **联系卡片等高 Flex 对齐**：  
  针对桌面与移动端进行弹性排版，保证询盘表单与右侧 WhatsApp 联络卡片在桌面端严格等高底部对齐，移动端自然垂直堆叠。

---

## 📞 商务联络与全球询盘

* **官方 WhatsApp 直连**：[+86 15168203740](https://wa.me/8615168203740)
* **企业官方邮箱**：[sales@rootzeglobal.com](mailto:sales@rootzeglobal.com)
* **在线询盘表单**：访问 [https://rootzeglobal.com/#contact](https://rootzeglobal.com/#contact) 提交您的规格需求

---

## 💻 工程开发与维护指南

### 1. 模块化编译流水线
站点页面采用源码 Partial 拆分架构，修改 `src/` 中的模块后运行编译脚本一键生成最终静态页面：
```bash
python3 scripts/build.py
```
* `src/partials/` $\longrightarrow$ 生成根目录 `index.html`
* `src/partials-news/` $\longrightarrow$ 生成根目录 `news.html`
* `src/partials-products/` $\longrightarrow$ 生成 `products/*.html` 各子目录页面

### 2. 本地一键预览
使用官方预览脚本（自动唤起默认浏览器）：
```bash
./preview.sh
```
或使用 Python 原生服务：
```bash
python3 -m http.server 8000
```

### 3. 自动化测试与质量验证
项目内置完善的自动化测试套件（基于 Node.js 原生 `node:test`）：
```bash
node --test tests/*.test.mjs
```
* `tests/assets.test.mjs`：基础静态资源与 `.nojekyll` 完整性校验；
* `tests/i18n.test.mjs`：中英文双语字典键值对等与对称性验证；
* `tests/structure.test.mjs`：DOM 锚点、相对路径与 `data-i18n` 属性校验；
* `tests/product-specs-responsive.test.mjs`：移动端免横向滚动与卡片化响应式契约；
* `tests/contact-alignment.test.mjs`：联系模块等高 Flex 弹性布局对齐校验；
* `tests/full-audit.test.mjs`：GitHub Pages 全站部署与死链全量审计；
* `tests/readme.test.mjs`：双语文档结构、官方主体、联系方式与超链接有效性测试。

### 4. GitHub Pages 生产发布
1. 确认根目录下 `CNAME` 文件包含 `rootzeglobal.com`；
2. 确认根目录下 `.nojekyll` 文件存在；
3. 将代码推送至 `main` 分支，GitHub Pages 将在 1–2 分钟内全球自动发布并挂载 SSL 安全证书。
