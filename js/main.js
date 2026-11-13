/**
 * RootZe Main Interactive Script
 */
(function($) {
  'use strict';

  // Product specification database for modal view
  var productSpecs = {
    'elec-softstarters': {
      title_en: 'Industrial Electrical Systems & Solid-State Soft Starters',
      title_zh: '工业电气系统与高低压固态软起动柜',
      table_en: [
        ['Voltage Class', 'Low Voltage (380V - 690V) / Medium & High Voltage (3kV - 10kV)'],
        ['Rated Power Range', '15 kW to 10,000 kW Heavy-Duty Motor Direct Control'],
        ['Starting Control Modes', 'Voltage Ramp, Current Limit, Kickstart, Soft Stop, Dual-ramp'],
        ['Bypass Mechanism', 'Built-in Vacuum Bypass Contactor for Continuous Energy-Saving Operation'],
        ['Thyristor / SCR Rating', 'High PIV Industrial Grade Silicon Controlled Rectifiers with RC snubber'],
        ['Cooling & Protection', 'Forced Air-Cooled / IP40 or IP54 Dust & Moisture Enclosure'],
        ['Industrial Communication', 'RS485 Modbus-RTU, Profibus-DP, Ethernet / Cloud Remote Telemetry'],
        ['Motor Protections', 'Overload, Phase Loss, Phase Unbalance, Overcurrent, Under-voltage, Ground Fault'],
        ['Typical Applications', 'Mining Crushers, Water Supply Pump Stations, Ball Mills, Air Compressors'],
        ['Standards & Compliance', 'IEC 60947-4-2, GB 14048.6, CE, ISO 9001 Factory Certificate']
      ],
      table_zh: [
        ['工作电压等级', '低压 380V - 690V / 中高压 3kV - 10kV 全系列'],
        ['适配电机功率', '15 kW 至 10,000 kW 重载三相异步及同步电动机'],
        ['起动控制模式', '限流起动、电压斜坡、突跳起动、软停车、双斜坡平滑起动'],
        ['旁路运行机构', '内置高可靠真空交流接触器，起动完毕自动无缝切入旁路运行节能'],
        ['可控硅 SCR 配置', '工业重载级反并联晶闸管组件，配备先进 RC 阻容吸收过电压保护'],
        ['散热与整柜防护', '强迫风冷智能温控系统，标配 IP40 / 可选配 IP54 防尘防溅外壳'],
        ['工业总线通讯', '标配 RS485 (Modbus-RTU 协议)，可选配 Profibus-DP、以太网远程监控'],
        ['多重综合保护', '过载、断相、三相不平衡、过流、欠压、晶闸管过热、对地漏电保护'],
        ['典型应用场景', '大型矿山破碎机、自来水厂及引水泵站、水泥球磨机、重型风机压缩机'],
        ['执行与认证标准', 'IEC 60947-4-2, GB 14048.6, CE 认证, ISO 9001 原厂出厂检验合格证']
      ]
    },
    'rail-track': {
      title_en: 'Railway Track Inspection & Maintenance Equipment',
      title_zh: '铁路工务养护设备与高精轨道检测仪器',
      table_en: [
        ['Measurement Parameters', 'Track Gauge, Cant / Superelevation, Flangeway Width, Check Rail Clearance'],
        ['Measurement Accuracy', 'Track Gauge: ±0.1 mm, Superelevation: ±0.1 mm, Flangeway: ±0.1 mm'],
        ['Instrument Construction', 'Aviation-Grade High-Strength Aluminum Alloy Body, Anodized Weatherproof Finish'],
        ['Display & Readout', 'High-Contrast OLED Digital Screen with Instant Temperature Compensation'],
        ['Data Storage & Sync', 'Built-in 100,000+ Points Data Logger with Bluetooth / USB Cloud Export'],
        ['Battery & Runtime', 'Rechargeable High-Capacity Li-ion Pack (≥ 24 Hours Continuous Field Use)'],
        ['Operating Temperature', '-30°C to +60°C Extreme Climatic Operating Range'],
        ['Associated Line Tools', 'Hydraulic Rail Lifters, Gap Adjusters, Internal Combustion Rail Drills & Cutters'],
        ['Track Scope', 'Standard Gauge 1435mm, Broad Gauge (1520/1676mm), Narrow Gauge (1000/1067mm)'],
        ['Certification & Calib', 'CRCC Railway Standards, Traceable National Metrology Calibration Certificate']
      ],
      table_zh: [
        ['核心测量指标', '标准轨距、水平/超高、道岔查照间隔、护轨轮缘槽宽度、导曲线支距'],
        ['综合测量精度', '轨距测量精度 ±0.1 mm，水平/超高精度 ±0.1 mm，查照/护背距离 ±0.1 mm'],
        ['机身材质工艺', '航空级高强度铝合金一体拉拔成型机身，防刮耐磨阳极氧化军工涂装'],
        ['显示与读数单元', '高亮度广温 OLED 数字液晶屏，具备自动环境温度补偿与阳光直读特性'],
        ['数据存储与导出', '机载超 100,000 组实测点存储容量，支持蓝牙即时无线传输与 USB 导出'],
        ['电源续航能力', '大容量工业锂电池组供电，单次充电现场连续巡检作业 ≥ 24 小时'],
        ['环境耐受温度', '-30°C 至 +60°C 恶劣户外高低温、高湿、粉尘环境可靠工作'],
        ['配套工务养护工具', '液压起拨道器、轨缝调整器、内燃钢轨钻孔机、切轨机、液压捣固镐'],
        ['适配轨距标准', '标准轨距 1435mm、宽轨 (1520/1676mm)、窄轨米轨 (1000/1067mm) 定制'],
        ['检验与计量检定', '符合铁路产品质量认证标准，出厂随附国家法定计量检定证书']
      ]
    },
    'spv-trucks': {
      title_en: 'Special Purpose Vehicles & Commercial Trucks',
      title_zh: '特种专用汽车与商用改装车',
      table_en: [
        ['Vehicle Categories', 'Cold-Chain Refrigerated Trucks, Fluid/Fuel Tankers, Municipal Sweepers, Aerial Platforms'],
        ['Chassis Manufacturers', 'Dongfeng (DFAC), Sinotruk (HOWO), Shacman, Foton, Isuzu Chassis Platforms'],
        ['Drive & Steer Options', '4x2, 6x2, 6x4, 8x4 configurations; Factory Left-Hand (LHD) or Right-Hand Drive (RHD)'],
        ['Refrigerated Bodywork', 'High-density Polyurethane Insulated Sandwich Panel (-20°C Carrier/Thermo King/Bizer)'],
        ['Tanker Construction', 'Carbon Steel Q235, Aluminum Alloy 5083, or Stainless Steel 304 with Wave Baffles'],
        ['Municipal Equipment', 'Four-brush Central Sweeper, High-pressure Washing Guns, Rear Dust Suppressor Cannon'],
        ['Engine Standards', 'Euro 3, Euro 4, Euro 5, and Euro 6 Diesel Engine Options from 120HP to 480HP'],
        ['Seaworthy Packaging', 'Marine Protective Wax Coating, Rust Inhibitor Wrap, RORO or Flat Rack Container Prep'],
        ['Export Certifications', 'CCC, ISO 9001, GCC, ADR Hazardous Transport Compliance, E-Mark Lighting'],
        ['Customization Scope', 'Custom Box Dimensions, Tail-lifts, Multi-compartment Tanks, PTO Hydraulic Units']
      ],
      table_zh: [
        ['车型矩阵覆盖', '冷链医药食品冷藏车、洒水/供水车、燃油与危化品专用罐车、多功能清扫车'],
        ['出海底盘品牌', '湖北襄阳东风 (DFAC)、中国重汽 (HOWO)、陕汽重卡、北汽福田等大厂底盘'],
        ['驱动与方向布局', '4x2、6x2、6x4、8x4 驱动形式；原厂左舵 (LHD) 或右舵 (RHD) 适配出口'],
        ['冷藏厢体配置', '内外高强度玻璃钢三明治高密度聚氨酯发泡保温厢，可选开利/冷王/国产冷机 (-20°C)'],
        ['罐式上装材质', '国标碳钢 Q235、航空级 5083 铝合金、或 304/316L 不锈钢（内置防波隔板）'],
        ['市政环卫功能', '四盘中置扫盘、吸盘组合，前冲后洒高压水炮，选装尾部环保抑尘雾炮机'],
        ['排放标准范围', '国五/国六、欧三 (Euro 3)、欧四 (Euro 4)、欧五 (Euro 5) 柴油机 (120-480HP)'],
        ['适航防腐交付', '整车海运专用防锈蜡喷涂、敏感部件防潮密封保护，适配滚装船与框架箱出海'],
        ['出海合规资质', 'CCC 强制认证、ISO 9001 质量认证、中东 GCC、危化品 ADR 运输出口合规'],
        ['非标深度定制', '支持定制箱体容积、液压液压尾板、罐体多仓分仓自流、特种取力器 (PTO) 系统']
      ]
    },
    'auto-brakelines': {
      title_en: 'Automotive Brake Pad Turnkey Production Lines',
      title_zh: '汽车零部件整线装备（刹车片自动化生产线）',
      table_en: [
        ['Annual Output Capacity', 'Turnkey Plant Configurations: 500,000 pcs to 5,000,000 pcs / year output'],
        ['Raw Material Section', 'Multi-ingredient Micro-Loss Batching System & High-Speed Plough Shear Dry Mixer'],
        ['Thermal Pressing Unit', 'Multi-Cavity Automated Hydraulic Hot Pressing Stations (200T - 600T Clamp Pressure)'],
        ['Heat Treatment & Baking', 'Continuous Mesh Belt Post-Curing Tunnel Oven (200°C - 300°C Precision Uniform Heating)'],
        ['Finishing & Grinding', 'Dual-Head Outer Arc Grinder, Slotting & Chamfering Machine with Optical Gauging'],
        ['Surface Coating & Assembly', 'Electrostatic Powder Spray Line, High-Speed Shim Staking & Anti-Noise Riveter'],
        ['Control Architecture', 'Siemens / Omron PLC Central Automation with Touchscreen SCADA Operation'],
        ['Dust Collection & Safety', 'High-Efficiency Pulse Jet Baghouse Filter with Explosion-Proof Air Ducts'],
        ['Formula & Engineering', 'Full Friction Formulation Support (Ceramic, Semi-Metallic, Low-Metallic) & Molds'],
        ['Standards & Turnkey Svc', 'ISO/TS 16949 / IATF 16949 Standards, Factory Floor Layout Design, Commissioning']
      ],
      table_zh: [
        ['整线年产能设计', '提供年产 50 万片、100 万片、300 万片至 500 万片一站式交付方案'],
        ['配料与混料工段', '高精度多组份失重式自动计量配料系统 + 重载高速多犁刀强制干混机'],
        ['热压成型单元', '多工位自动液压热压成型机组（单机 200T - 600T 吨位，多模腔自动模内推料）'],
        ['热处理固化烘道', '网带式连续高温后固化隧道烘箱（200°C - 300°C 均衡控温，消除内部应力）'],
        ['精密磨削与倒角', '高精度双工位外弧双端面研磨机、全自动数控开槽倒角机（配激光光电测厚）'],
        ['表面喷涂与组装', '全自动静电粉末喷涂固化流水线、自动消音片（降噪片）铆接装配线'],
        ['电气控制系统', '西门子 (Siemens) / 欧姆龙 PLC 集中自动化控制，带彩色触摸屏集中数据监视'],
        ['环保与除尘配套', '全线脉冲布袋高负压集中除尘机组，粉尘收集达标，配备防爆阻火安全阀'],
        ['工艺配方技术赋能', '原厂提供高品质陶瓷基、少金属、半金属配方工艺转让与全套冷热压模具'],
        ['交付与工程标准', '符合 IATF 16949 国际汽车工业标准，负责厂房布局、设备就位与海外调试培训']
      ]
    },
    // Legacy fallback keys
    'cell-lfp': {
      title_en: 'Prismatic LFP & NMC Traction Cells',
      title_zh: '动力方形 LFP 与三元锂电芯',
      table_en: [
        ['Chemistry Type', 'Lithium Iron Phosphate (LiFePO4) / Ternary Lithium (NMC)'],
        ['Available Capacities', '100Ah / 280Ah / 304Ah / 314Ah (Grade A Genuine)'],
        ['Nominal Cell Voltage', '3.2V (LFP) / 3.7V (NMC)']
      ],
      table_zh: [
        ['化学材料体系', '磷酸铁锂 (LiFePO4) / 高能量密度三元锂 (NMC)'],
        ['标准容量型号', '100Ah / 280Ah / 304Ah / 314Ah（正品全新 A 规）'],
        ['标称单体电压', '3.2V (磷酸铁锂) / 3.7V (三元锂)']
      ]
    },
    'ess-ci': {
      title_en: 'Commercial & Industrial Energy Storage System (ESS)',
      title_zh: '工商业户外储能一体柜 (C&I ESS)',
      table_en: [
        ['Rated Storage Capacity', '100kWh / 215kWh / 372kWh / Modular expandable up to 2MWh+'],
        ['Cell Type & Integration', 'Tier-1 280Ah / 314Ah LFP Prismatic Cells with 1P16S modular clusters']
      ],
      table_zh: [
        ['系统额定储能容量', '100kWh / 215kWh / 372kWh / 多机并联扩展至 2MWh+'],
        ['电芯架构与集成', '一线大厂 280Ah / 314Ah LFP 方形电芯，1P16S 模组化串联']
      ]
    },
    'ess-res': {
      title_en: 'Residential Stackable & Wall-Mount ESS',
      title_zh: '家庭堆叠式与壁挂式储能系统',
      table_en: [
        ['Usable Storage Capacity', '5.12kWh to 20.48kWh (Scalable up to 8 units parallel, 40kWh max)'],
        ['Nominal Battery Voltage', '51.2V Low Voltage / High Voltage Stack (102V - 409V) options']
      ],
      table_zh: [
        ['可用储能容量', '5.12kWh 至 20.48kWh（支持最多 8 台并联扩展至 40.96kWh）'],
        ['电池标称电压', '51.2V 低压系统 / 高压串联堆叠 (102V - 409V) 可选']
      ]
    }
  };

  // Document Ready Initialization
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

    // 4. Smooth Anchor Scrolling
    $('a[href^="#"]').on('click', function(event) {
      var target = $(this.getAttribute('href'));
      if (target.length) {
        event.preventDefault();
        var navHeight = $('#ftco-navbar').outerHeight() || 70;
        $('html, body').stop().animate({
          scrollTop: target.offset().top - navHeight + 10
        }, 600);

        // Collapse mobile nav if open
        if ($('.navbar-collapse').hasClass('show')) {
          $('.navbar-toggler').click();
        }
      }
    });

    // 5. Sticky Navbar Behavior
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

    // 6. Product Spec Modal Trigger
    $('.view-spec-btn').on('click', function(e) {
      e.preventDefault();
      var specId = $(this).attr('data-spec-id');
      var spec = productSpecs[specId];
      if (!spec) return;

      var currentLang = (window.RootZeI18n && window.RootZeI18n.getLanguage()) || 'en';
      var title = (currentLang === 'zh') ? spec.title_zh : spec.title_en;
      var rows = (currentLang === 'zh') ? spec.table_zh : spec.table_en;

      $('#specModalTitle').text(title);

      var tableBody = '';
      for (var i = 0; i < rows.length; i++) {
        tableBody += '<tr>';
        tableBody += '<td class="font-weight-bold" data-label="Parameter" style="width: 30%; color: #334155; font-size: 13.5px;">' + rows[i][0] + '</td>';
        tableBody += '<td data-label="Value" style="color: #475569; font-size: 13.5px;">' + rows[i][1] + '</td>';
        tableBody += '</tr>';
      }
      $('#specModalTableBody').html(tableBody);

      // Pre-select category in contact form when clicked
      $('#specModalInquireBtn').off('click').on('click', function() {
        $('#specModal').modal('hide');
        var catSelect = $('#inqCategory');
        if (specId === 'elec-softstarters') {
          catSelect.val('Industrial Electrical Systems (Soft Starters)');
        } else if (specId === 'rail-track') {
          catSelect.val('Railway Track Equipment & Maintenance Tools');
        } else if (specId === 'spv-trucks') {
          catSelect.val('Special Purpose Vehicles (SPV & Trucks)');
        } else if (specId === 'auto-brakelines') {
          catSelect.val('Automotive Manufacturing Lines (Brake Pads)');
        } else if (specId === 'cell-lfp') {
          catSelect.val('Industrial Electrical Systems (Soft Starters)');
        }
      });

      $('#specModal').modal('show');
    });

    // Pre-select category in contact form when card Inquire button clicked
    $('.car-wrap a[href="#contact"]').on('click', function() {
      var cat = $(this).attr('data-inquire-cat');
      if (cat) {
        if ($('#inqCategory option[value="' + cat + '"]').length > 0) {
          $('#inqCategory').val(cat);
        } else {
          var curMsg = $('#inqMessage').val() || '';
          if (curMsg.indexOf(cat) === -1) {
            $('#inqMessage').val('Inquiry regarding: ' + cat + (curMsg ? '\n' + curMsg : ''));
          }
        }
      }
    });

    // Auto-fill inquiry form from URL parameters (e.g. from vehicle detail page "Request a Quote" CTA)
    try {
      if (window.location && window.location.search) {
        var urlParams = new URLSearchParams(window.location.search);
        var inqVehicle = urlParams.get('inquire');
        var inqModel = urlParams.get('model');
        if (inqVehicle) {
          var currentLang = (window.RootZeI18n && window.RootZeI18n.getLanguage()) || 'en';
          var prefix = (currentLang === 'zh') ? '咨询意向车型：' : 'Inquiry regarding: ';
          var modelSnippet = inqModel ? ' (' + ((currentLang === 'zh') ? '公告型号: ' : 'Model: ') + inqModel + ')' : '';
          var vehicleInquiryText = prefix + decodeURIComponent(inqVehicle) + modelSnippet;
          var curMsg = $('#inqMessage').val() || '';
          if (curMsg.indexOf(inqVehicle) === -1) {
            $('#inqMessage').val(vehicleInquiryText + (curMsg ? '\n\n' + curMsg : ''));
          }
          if ($('#inqCategory option[value="Special Purpose Vehicles"]').length > 0) {
            $('#inqCategory').val('Special Purpose Vehicles');
          }
        }
      }
    } catch (e) {
      console.warn('Inquiry URL param parse failed:', e);
    }

    // Expand All / Collapse All controls for SPV Accordion
    $('#btnExpandAll').on('click', function() {
      $('#spvAccordion .collapse').collapse('show');
    });
    $('#btnCollapseAll').on('click', function() {
      $('#spvAccordion .collapse').collapse('hide');
    });

    // High-resolution vehicle image lightbox
    if ($('.image-popup').length > 0 && $.fn.magnificPopup) {
      $('.image-popup').magnificPopup({
        type: 'image',
        closeOnContentClick: true,
        mainClass: 'mfp-img-mobile',
        image: {
          verticalFit: true
        }
      });
    }

    // 7. B2B Inquiry Form Submission (Web3Forms AJAX with graceful fallback)
    $('#inquiryForm').on('submit', function(e) {
      e.preventDefault();
      var form = this;
      var name = ($('#inqName').val() || '').trim();
      var company = ($('#inqCompany').val() || '').trim();
      var contact = ($('#inqContact').val() || '').trim();
      var category = $('#inqCategory').val() || 'General Inquiry';
      var quantity = ($('#inqQuantity').val() || '').trim() || 'N/A';
      var message = ($('#inqMessage').val() || '').trim() || 'No additional notes provided.';
      var accessKey = ($('#web3formsAccessKey').val() || '').trim();

      var currentLang = (window.RootZeI18n && window.RootZeI18n.getLanguage()) || 'en';
      var payload = buildInquiryPayload(name, company, contact, category, quantity, message, currentLang);

      // Setup clipboard copy handler on the modal
      $('#modalCopyBtn').off('click').on('click', function() {
        if (navigator && navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(payload.body).then(function() {
            var copiedText = (window.RootZeI18n && window.RootZeI18n.t('contact.modal_copied')) || 'Copied!';
            $('#modalCopyBtnText').text(copiedText);
            setTimeout(function() {
              var defaultText = (window.RootZeI18n && window.RootZeI18n.t('contact.modal_btn_copy')) || 'Copy Inquiry Text';
              $('#modalCopyBtnText').text(defaultText);
            }, 2500);
          });
        }
      });

      function showFallbackModal() {
        $('#inquirySuccessModalLabel').text((window.RootZeI18n && window.RootZeI18n.t('contact.success_title')) || 'Inquiry Prepared Successfully!');
        $('#inquirySuccessModal .modal-body > p').text((window.RootZeI18n && window.RootZeI18n.t('contact.success_desc')) || 'Your inquiry details have been formatted. Click below to launch your email client or chat directly on WhatsApp.');
        $('#modalInquirySummary').text(payload.body);
        $('#modalMailtoLink').attr('href', payload.mailtoUrl);
        $('#modalWhatsappLink').attr('href', payload.waUrl);
        $('#inquirySuccessModal').modal('show');
        try {
          window.location.href = payload.mailtoUrl;
        } catch (err) {}
      }

      // Check if Web3Forms access key is configured
      if (accessKey && accessKey !== 'YOUR_WEB3FORMS_ACCESS_KEY') {
        var submitBtn = $('#inqSubmitBtn');
        var submitBtnText = $('#inqSubmitBtnText');
        var originalBtnText = submitBtnText.text();
        var sendingText = (window.RootZeI18n && window.RootZeI18n.t('contact.btn_sending')) || 'Sending...';

        submitBtn.prop('disabled', true);
        submitBtnText.text(sendingText);

        var formData = new FormData(form);
        if (!formData.get('access_key') || formData.get('access_key') === 'YOUR_WEB3FORMS_ACCESS_KEY') {
          formData.set('access_key', accessKey);
        }
        formData.set('subject', payload.subject);
        formData.set('from_name', 'Rootze Global Web Inquiry');

        fetch('https://api.web3forms.com/submit', {
          method: 'POST',
          body: formData
        })
        .then(function(response) { return response.json(); })
        .then(function(data) {
          if (data && (data.success || data.ok)) {
            // Success: Direct email delivery confirmed
            $('#inquirySuccessModalLabel').text((window.RootZeI18n && window.RootZeI18n.t('contact.sent_direct_title')) || 'Inquiry Delivered to Our Inbox!');
            $('#inquirySuccessModal .modal-body > p').text((window.RootZeI18n && window.RootZeI18n.t('contact.sent_direct_desc')) || 'Your inquiry has been delivered directly to our team inbox.');
            $('#modalInquirySummary').text(payload.body);
            $('#modalMailtoLink').attr('href', payload.mailtoUrl);
            $('#modalWhatsappLink').attr('href', payload.waUrl);
            $('#inquirySuccessModal').modal('show');
            form.reset();
          } else {
            showFallbackModal();
          }
        })
        .catch(function() {
          showFallbackModal();
        })
        .finally(function() {
          submitBtn.prop('disabled', false);
          submitBtnText.text(originalBtnText);
        });
      } else {
        // Fallback for immediate operation prior to user setting their access key
        showFallbackModal();
      }
    });
  });

  // Localized inquiry payload builder
  function buildInquiryPayload(name, company, contact, category, quantity, message, lang) {
    lang = lang || 'en';
    var isZh = (lang === 'zh');

    var subject = isZh
      ? '[RootZe 工业装备与特种车辆业务咨询] ' + category + ' — ' + company
      : '[RootZe Industrial Equipment Inquiry] ' + category + ' — ' + company;

    var body = isZh
      ? '尊敬的 RootZe 业务团队：\n\n' +
        '我方希望就以下产品采购获取一手工厂报价、规格书与交付周期：\n\n' +
        '--------------------------------------------------\n' +
        '* 采购意向品类：' + category + '\n' +
        '* 联络人姓名：' + name + '\n' +
        '* 企业名称：' + company + '\n' +
        '* 联络方式（邮箱/微信/WhatsApp）：' + contact + '\n' +
        '* 预估采购量 / 目标交付国：' + quantity + '\n' +
        '* 详细采购需求或定制规格：' + message + '\n' +
        '--------------------------------------------------\n\n' +
        '期待您的快速回复与支持。\n\n' +
        '顺祝商祺，\n' + name
      : 'Dear RootZe Distribution Team,\n\n' +
        'I would like to request an official factory-direct quotation with the following specifications:\n\n' +
        '--------------------------------------------------\n' +
        '* Interested Product Category: ' + category + '\n' +
        '* Full Name: ' + name + '\n' +
        '* Company Name: ' + company + '\n' +
        '* Contact Details (Email/WhatsApp): ' + contact + '\n' +
        '* Target Quantity / Destination: ' + quantity + '\n' +
        '* Project Description: ' + message + '\n' +
        '--------------------------------------------------\n\n' +
        'Please provide factory pricing tiers, technical datasheets, and export delivery lead times.\n\n' +
        'Best regards,\n' + name;

    var mailtoUrl = 'mailto:sales@rootzeglobal.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);

    var waQuantity = (quantity && quantity !== 'N/A') ? (isZh ? '（采购量：' + quantity + '）' : ' (' + quantity + ')') : '';
    var waMsg = isZh
      ? '您好 Rootze 团队，我是来自 ' + company + ' 的 ' + name + '。希望咨询关于 ' + category + waQuantity + ' 的原厂出口方案。'
      : 'Hello Rootze Team, I am ' + name + ' from ' + company + '. Inquiring about factory-direct supply for ' + category + waQuantity + '.';

    var waUrl = 'https://wa.me/8615168203740?text=' + encodeURIComponent(waMsg);

    return {
      subject: subject,
      body: body,
      mailtoUrl: mailtoUrl,
      waUrl: waUrl
    };
  }

  // Export specs and helpers for test environment inspection
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
      productSpecs: productSpecs,
      buildInquiryPayload: buildInquiryPayload
    };
  }
})(typeof jQuery !== 'undefined' ? jQuery : function() { return { on: function(){}, val: function(){ return ''; }, ready: function(fn){ fn(); } }; });
