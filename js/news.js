/**
 * RootZe News Subpage Interactive Controller
 */
(function($) {
  'use strict';

  var newsDatabase = {
    'art1': {
      category_en: 'Product Update',
      category_zh: '产品更新',
      date_en: 'November 2, 2026',
      date_zh: '2026年11月2日',
      title_en: 'Heavy-Duty Motor Starting Solutions: Selecting Solid-State Soft Starters for Harsh Industrial Environments',
      title_zh: '矿山与重工业电机平稳启动：高低压固态软起动器在海外工况中的选型要点',
      body_en: '<p>Direct-on-line (DOL) starting of large three-phase induction and synchronous motors typically draws starting currents 6 to 8 times nominal full-load current. In weak overseas industrial power grids—such as remote mining pits, cement manufacturing facilities, and irrigation pump stations—this severe inrush current triggers line voltage dips, trips upstream protection relays, and induces catastrophic mechanical shock on gearboxes, couplings, and pump impellers.</p>' +
        '<p>Rootze provides high and low-voltage solid-state soft starters engineered with heavy-duty anti-parallel thyristors (SCRs), closed-loop current limiting algorithms, and automatic vacuum bypass contactors. By controlling the firing angle of the thyristors during acceleration, starting current is smoothly clamped to 1.5–3.5 times rated current, guaranteeing soft torque ramp-up without grid disruption.</p>' +
        '<p>Key engineering specifications to consider during export selection include grid harmonic mitigation, tropical ambient thermal margins (-25°C to +50°C), IP54 dustproof enclosures with conformal board coatings, and direct RS485 / Modbus-RTU remote telemetry for centralized SCADA integration.</p>',
      body_zh: '<p>在工业重载工况下，大功率三相异步电机与同步电机若采用全压直接起动（DOL），起动瞬间电流通常达到额定电流的 6 到 8 倍。在海外一些电网容量受限的偏远矿区、水泥厂排风系统及农田水利引水泵站，剧烈的起动冲击会导致母线电压瞬间暴跌，引发上级保护跳闸，并对电机转子、减速机齿轮箱、联轴器及水泵叶轮产生严重的机械扭矩冲击与机械疲劳磨损。</p>' +
        '<p>襄阳如志进出口有限公司（Rootze）联合原厂研发团队，直供 380V-690V 低压及 3kV-10kV 高压智能固态软起动成套装置。系统采用大功率反并联晶闸管（SCR）核心功率组件，配合先进的微电脑闭环限流起动与双斜坡平滑起动控制算法。电机完成平稳起动后，智能切换至内置的高可靠真空交流接触器旁路连续运行，彻底杜绝晶闸管长期通电的发热损耗。</p>' +
        '<p>在海外工程选型与订购中，如志技术团队可协助客户根据海拔、现场环境温度（-25°C 至 +50°C 宽温耐受）、粉尘腐蚀防护（IP40/IP54）以及远端 DCS / SCADA 通信协议（Modbus-RTU / Profibus-DP）出具全套非标设计与出厂配电柜图纸。</p>'
    },
    'art2': {
      category_en: 'Industry Insights',
      category_zh: '行业深度',
      date_en: 'October 28, 2026',
      date_zh: '2026年10月28日',
      title_en: 'Precision Railway Maintenance: High-Accuracy Track Geometry Measurement Systems for Overseas Corridors',
      title_zh: '铁路轨道毫米级巡检与养护：高精度轨距轨向综合检测仪在海外线路中的应用',
      body_en: '<p>With global railway networks expanding cross-border freight corridors and accelerating commuter transit lines, track geometry tolerances have become critical safety parameters. Minute deviations in track gauge, cant (superelevation), flangeway clearance, or turnout alignment can lead to wheel-climb derailments or accelerated railhead wear.</p>' +
        '<p>Traditional mechanical track gauges suffer from parallax reading errors, thermal expansion drift, and tedious manual paperwork. Rootze delivers digital high-precision track geometry measuring instruments developed by proprietary rail tooling partners in Central China. Engineered with aviation-grade aluminum alloy and automatic temperature compensation, these digital systems guarantee ±0.1mm measurement precision across track gauge, cant, and turnout cross-sections.</p>' +
        '<p>The on-board OLED display delivers crisp readability under direct sunlight, while integrated Bluetooth wirelessly syncs inspection records to tablets and railway management cloud systems, eliminating manual data entry and enabling predictive track maintenance scheduling.</p>',
      body_zh: '<p>随着跨国重载货运铁路线路的提速扩能以及海外城市轨道交通的密集运营，轨道几何尺寸与线路平顺度成为关乎行车安全的生命线。轨距超差、水平（超高）不良、道岔查照间隔与护轨轮缘槽宽度的细微形变，都会大幅加剧轮轨磨耗，严重时极易引发脱轨安全事故。</p>' +
        '<p>传统机械式铁路道尺与目测工具受环境温差变形影响显著，且人工现场记录繁琐、容易发生读数视差。Rootze 依托中国中部铁路工务养护专用设备智造产业带，为海外铁路局及基建承包商供应具有自主核心技术的便携式数字显示高精度轨道几何状态综合检测仪。</p>' +
        '<p>该系列仪器采用高强度航空铝合金一体拉拔机身，内置环境温度自动补偿传感器，将轨距、水平/超高测量误差严格控制在 ±0.1mm 极窄公差范围内。机载大容量存储器结合蓝牙无线同步功能，可将现场采集的道岔全断面几何数据秒级上传至数字化运维系统，为海外客户大幅缩减巡检停运窗口期。</p>'
    },
    'art3': {
      category_en: 'Turnkey Solutions',
      category_zh: '交钥匙产线',
      date_en: 'October 20, 2026',
      date_zh: '2026年10月20日',
      title_en: 'Turnkey Export: Establishing an Automated Automotive Brake Pad Production Line Abroad',
      title_zh: '交钥匙工程：如何在海外快速搭建一条年产数百万套的汽车刹车片全自动生产线',
      body_en: '<p>Rising tariffs, shipping costs, and localized industrialization mandates are driving global automotive aftermarket distributors to establish domestic friction material manufacturing facilities. However, building an automotive brake pad plant requires synchronized integration across disparate engineering disciplines: formula chemistry, raw material mixing, thermal compression, CNC grinding, and powder coating.</p>' +
        '<p>Rootze leverages Xiangyang\'s automotive component manufacturing heritage—anchored in the Dongfeng automotive corridor—to deliver complete turnkey brake pad production solutions. We supply the entire equipment workflow from automated micro-loss loss-in-weight batching systems and high-speed plough mixers to multi-cavity automated hot-press molding machines (200T-600T), mesh belt curing ovens, and dual-head outer arc CNC grinding stations.</p>' +
        '<p>Beyond machinery, Rootze provides essential intellectual property transfer: proven friction formulas (ceramic, low-metallic, semi-metallic), custom steel back stamping molds, factory floor layout blueprints, dust extraction and ISO/TS 16949 compliant quality assurance protocols, backed by on-site overseas installation and commissioning engineers.</p>',
      body_zh: '<p>面对日益上涨的国际海运成本、关税壁垒以及海外多国对本土工业制造的政策支持，越来越多的海外汽车零部件贸易商与主机厂配套商希望在本地投资建设汽车摩擦材料（刹车片）组装与生产工厂。然而，刹车片制造涉及配方化学混料、高温热压成型、高精磨削与表面防腐等跨专业工序，单一采购单机设备极易出现工艺脱节与良品率低下。</p>' +
        '<p>依托湖北襄阳深厚的汽车零部件全产业链集群底蕴（中国著名东风轻型车与商用车制造基地），Rootze 为海外投资客户提供从厂房规划、配料混料、热压固化、精密研磨到自动化包装的“交钥匙工程（Turnkey Solution）”。整线年产能可按需定制（年产 50 万片、100 万片、300 万片至 500 万片）。</p>' +
        '<p>除了提供重载犁刀干混机、多模腔自动化热压机、隧道式后固化烘箱与数控双端外弧磨床等全套智能设备外，Rootze 更提供极具价值的核心技术输出：成熟的高性能陶瓷配方、少金属与半金属摩擦工艺、全套冷热压精密模具，并派遣资深工程技师团队赴海外进行现场安装调试与工人实操培训，确保工厂投产即达标。</p>'
    }
  };

  $(document).ready(function() {
    // 1. Initialize i18n
    if (window.RootZeI18n) {
      window.RootZeI18n.init();
    }

    // 2. Language Switcher Buttons
    $('.lang-btn').on('click', function(e) {
      e.preventDefault();
      var lang = $(this).attr('data-lang');
      if (window.RootZeI18n) {
        window.RootZeI18n.setLanguage(lang);
      }
    });

    // 3. AOS Animation
    if (typeof AOS !== 'undefined') {
      AOS.init({
        duration: 800,
        easing: 'slide',
        once: true
      });
    }

    // 4. Sticky Navbar Behavior
    $(window).scroll(function() {
      var st = $(this).scrollTop();
      var navbar = $('#ftco-navbar');
      if (st > 150) {
        if (!navbar.hasClass('scrolled')) {
          navbar.addClass('scrolled');
        }
      }
      if (st < 150) {
        if (navbar.hasClass('scrolled')) {
          navbar.removeClass('scrolled sleep');
        }
      }
      if (st > 350) {
        if (!navbar.hasClass('awake')) {
          navbar.addClass('awake');
        }
      }
      if (st < 350) {
        if (navbar.hasClass('awake')) {
          navbar.removeClass('awake');
          navbar.addClass('sleep');
        }
      }
    });

    // 3. Category Filter Logic
    $('.news-filter-btn').on('click', function(e) {
      e.preventDefault();
      $('.news-filter-btn').removeClass('active');
      $(this).addClass('active');

      var filter = $(this).attr('data-filter');
      if (filter === 'all') {
        $('.news-card-wrapper').fadeIn(300);
      } else {
        $('.news-card-wrapper').each(function() {
          var cardCategory = $(this).attr('data-category');
          if (cardCategory === filter) {
            $(this).fadeIn(300);
          } else {
            $(this).fadeOut(200);
          }
        });
      }
    });

    // 4. News Detail Modal Trigger
    $('.read-news-btn').on('click', function(e) {
      e.preventDefault();
      var artId = $(this).attr('data-article-id');
      var art = newsDatabase[artId];
      if (!art) return;

      var currentLang = (window.RootZeI18n && window.RootZeI18n.getLanguage()) || 'en';
      var isZh = (currentLang === 'zh');

      var category = isZh ? art.category_zh : art.category_en;
      var date = isZh ? art.date_zh : art.date_en;
      var title = isZh ? art.title_zh : art.title_en;
      var body = isZh ? art.body_zh : art.body_en;

      $('#newsModalTag').text(category);
      $('#newsModalDate').text(date);
      $('#newsModalTitle').text(title);
      $('#newsModalBody').html(body);

      $('#newsDetailModal').modal('show');
    });
  });

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
      newsDatabase: newsDatabase
    };
  }
})(typeof jQuery !== 'undefined' ? jQuery : function() { return { on: function(){}, ready: function(fn){ fn(); } }; });
