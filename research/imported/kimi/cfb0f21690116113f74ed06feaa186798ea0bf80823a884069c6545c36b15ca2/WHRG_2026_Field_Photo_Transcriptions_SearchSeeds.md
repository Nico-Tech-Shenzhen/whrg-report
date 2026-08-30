# WHRG 2026 Field Photo Transcriptions & Search Seeds

Purpose: This file is a text extraction layer for the WHRG 2026 research project so that Kimi does NOT need to OCR the same field photos again.

Generated from the user's field photos taken mainly on 2026-08-23 to 2026-08-26 around the World Humanoid Robot Games 2026 / National Speed Skating Oval ("Ice Ribbon") and related exhibition / ecosystem areas.

## Usage rules for Kimi

1. Do not re-OCR the photos unless this text explicitly marks a transcription as uncertain and the exact spelling is essential.
2. Treat photo text as **Field Evidence**, not automatically as verified Web evidence.
3. A photo can verify that a sign, scoreboard, booth, organization name, claim, or promotional statement was displayed on site.
4. Claims on posters/brochures still require Primary Web Source verification before being promoted to external factual claims.
5. `[UNCERTAIN]` means the visible text is not sufficiently clear. Search variants rather than treating one spelling as confirmed.
6. When a photo shows a competition result, use it as a strong search seed, but look for official schedule/result material before creating a final Competition Entry.
7. Do not infer Team = Organization, Organization = Robot Manufacturer, or Sponsor = Competition Participant.
8. For any public code/data/model/hardware found through these seeds, run `whrg-license-audit`.
9. For all Web verification, run `whrg-evidence-audit`.
10. The preferred workflow is: Field Evidence -> Search Seed -> Primary Source -> Evidence Map -> Entity / Entry / Resource.

---

# A. P0 — Competition / Entry / Result field evidence

## FP-001 — 园区管理岗 result board

Source photo:
- `IMG_20260823_182649.jpg`
- readable derivative/crop used during transcription: `parkmgmt_crop.jpg`

Observed text:

> 园区管理岗  
> 第一名　北京人形河南科技学院计算机科学与技术学院  
> 第二名　华工智元具行队  
> 第三名　北京人形机器人创新中心-深圳大学联队

Notes:
- The string in first place is preserved exactly as visually read. Do not split `北京人形` and `河南科技学院计算机科学与技术学院` without external evidence.
- This is a result board, but the exact competition hierarchy/category still needs official-rule/result confirmation.

Search seeds:
- `"园区管理岗" "北京人形河南科技学院计算机科学与技术学院"`
- `"园区管理岗" "华工智元具行队"`
- `"园区管理岗" "北京人形机器人创新中心-深圳大学联队"`
- `"世界人形机器人运动会" "园区管理岗" 成绩`
- `"世界人形机器人运动会" "华工智元具行队"`
- `"世界人形机器人运动会" "深圳大学联队" 北京人形机器人创新中心`

Research targets:
- Competition ID / final rule
- Complete entry list
- Team vs organization identity
- Robot platform/model
- Control mode
- Final ranking/result
- Formation path of the BIC–Shenzhen University joint team

---

## FP-002 — 1500米（决赛）第2组 result board

Source photo:
- `IMG_20260823_192452.jpg`
- readable derivative/crop used during transcription: `score1500_crop.jpg`

Observed text:

> 1500米（决赛）第2组  
> 成绩列表  
> 1　[UNCERTAIN: 风火闪电队 / 凤火闪电队]　2:30.22  
> 2　天工　2:33.22  
> 3　GMO Robots　7:43.89  
> 4　北京智元素队　DNS  
> 5　[UNCERTAIN: 北京灵翌队]　DNS

Notes:
- First team name: first character is not fully reliable in the photo; search both `风火闪电队` and `凤火闪电队`.
- Fifth team name appears to be `北京灵翌队`, but verify with official results.
- `DNS` is visually shown for rows 4 and 5.

Search seeds:
- `"1500米" "第2组" "2:30.22" 人形机器人`
- `"1500米" "天工" "2:33.22" 世界人形机器人运动会`
- `"1500米" "GMO Robots" "7:43.89"`
- `"北京智元素队" 1500米`
- `"北京灵翌队" 人形机器人`
- `"风火闪电队" 人形机器人 1500米`
- `"凤火闪电队" 人形机器人 1500米`
- `"世界人形机器人运动会" 1500米 决赛 成绩`

Research targets:
- Full final/group results
- Team/organization/robot identity
- GMO Robots Japan participation path
- `天工` relation to 北京人形机器人创新中心
- DNS vs registered/scheduled/started status

---

## FP-003 — 足球现场比分

Source photo:
- `IMG_20260825_204605.jpg`

Observed text:

> 下半场　05:07  
> 清华火神队　5  
> 农大青禾队　0

Search seeds:
- `"清华火神队" "农大青禾队" 5:0`
- `"清华火神队" 世界人形机器人运动会`
- `"农大青禾队" 世界人形机器人运动会`
- `"世界人形机器人运动会" 足球 清华 火神`
- `"世界人形机器人运动会" 足球 中国农业大学 青禾`

Research targets:
- Which football class/group
- Full lineup/bracket
- Robot platform
- Organization and team structure
- Whether same teams have RoboCup history
- Result source

---

## FP-004 — Robot / Entry No. 083

Source photo:
- `IMG_20260824_151751.jpg`

Observed text on robot / bib:

> 北京航空航天大学  
> [UNCERTAIN but likely] 具身智能机器人研究院  
> 083

Visual note:
- White humanoid with dark face/display and a colored X-like chest logo.
- Competition task visible on main venue screen involves manipulating box-shaped objects.

Search seeds:
- `"北京航空航天大学" 083 世界人形机器人运动会`
- `"北京航空航天大学" "具身智能机器人研究院" 世界人形机器人运动会`
- `"北航" 083 人形机器人运动会`
- `"北航" 具身智能机器人研究院 人形机器人 2026`

Research targets:
- Team name
- Competition/entry
- Robot manufacturer/model
- Whether the institute name is correct
- Development team size and support

---

# B. P1 — WHRG infrastructure / data / permanent ecosystem

## FP-005 — 中国联通：具身智能机器人管理平台

Source photo:
- `IMG_20260823_203821.jpg`

On-site header:

> 第二届世界人形机器人运动会全球合作伙伴  
> World Humanoid Robot Games 2026 Global Partners  
> 中国联通 China unicom

Title:

> 具身智能机器人管理平台

Main displayed statement:

> 具身智能机器人管理平台为机器人赋予专属网络数字身份，实现异构机器人全域状态感知与可视化，是践行具身智能战略的创新实践，为网络强国、数字中国建设贡献联通力量。

Visible capability labels include:

> 设备接入  
> 网络位置  
> 状态感知  
> 指挥调度

Displayed operational statement:

> 为赛事组织、现场保障、设备运维和指挥调度提供标准化、可视化、平台化支撑

Displayed event-scale numbers:

> 16个　覆盖国家与地区，全球化竞技舞台，汇聚顶尖智慧  
> 666支　参赛精英队伍，高校与科研机构同场竞技，巅峰对决  
> 2056台　智能机器人数量，异构机型协同，展现具身智能潜力  
> 138%　[adjacent explanatory text not fully legible]

Important interpretation rule:
- This photo proves China Unicom displayed a WHRG-specific embodied robot management platform and these figures.
- It does NOT by itself prove every one of the 2056 robots was technically connected to/managed by the platform.

Search seeds:
- `"具身智能机器人管理平台" 中国联通 世界人形机器人运动会`
- `"具身智能机器人管理平台" 666 2056`
- `"世界人形机器人运动会" 中国联通 机器人管理平台`
- `"中国联通" "2056" 人形机器人`
- `"第二届世界人形机器人运动会全球合作伙伴" 中国联通`

Research targets:
- Actual technical architecture
- Number of robots actually connected
- Identity/network/telemetry data collected
- API/interface
- Data retention/opening policy
- Whether platform data feeds the 2500+ hour dataset
- Vendor/subcontractors

---

## FP-006 — 中国联通：WHRG 5G-A场馆包

Source photos:
- `IMG_20260823_203842.jpg`
- `IMG_20260826_131525.jpg`
- `IMG_20260826_131611.jpg`

Displayed text:

> 5G-A智能护航，全场馆尽享领先体验  
> 世界机器人运动会・专属网络套餐  
> 5G-A大上行场馆包　10元/次

Benefits displayed:

> 权益1　专属身份  
> 点亮专属LOGO  
> “我为机器人运动会加油”

> 权益2　超级速度  
> 峰值下行 ～3Gbps  
> 峰值上行 ～500Mbps

> 权益3　流量无忧  
> 5GB 高速流量  
> 24小时有效

> 权益4　AI优化  
> 场馆内上网  
> AI优化保障，更流畅

Standalone roll-up banner additionally shows:

> 5G-A场馆包  
> 上行速率提升至500Mbps  
> 活动时间：2026年8月19日—2026年8月27日  
> 区域：北京市｜国家速滑馆  
> 联通你我　扫码订购

Displayed marketing phrase:

> 场馆看比赛，分享快人一步  
> 5G-A大上行　具身智能新突破

Search seeds:
- `"5G-A场馆包" 国家速滑馆 2026`
- `"5G-A场馆包" 世界人形机器人运动会`
- `"上行速率提升至500Mbps" 国家速滑馆`
- `"我为机器人运动会加油" 中国联通`
- `"世界机器人运动会" "专属网络套餐" 中国联通`

Research targets:
- Whether this was spectator-only connectivity or also robot/team infrastructure
- Network slicing / uplink support for competition robots
- Technical deployment at venue
- Sponsor vs core infrastructure role
- Connection with robot management platform

---

## FP-007 — 中国联通：2026北京亦庄人形机器人半程马拉松 network case

Source photos:
- `IMG_20260823_203838.jpg`
- `IMG_20260826_131614.jpg`

Important:
- This display describes the **Beijing E-Town Half Marathon / Humanoid Robot Half Marathon**, not necessarily WHRG itself.
- It is useful as evidence of China Unicom's robot-event network infrastructure before/around WHRG.

Title:

> 5G-A大上行赋能亦庄马拉松

Event graphic:

> 2026亦马启航  
> 北京亦庄半程马拉松  
> 暨人形机器人半程马拉松  
> BEIJING E-TOWN HALF MARATHON AND HUMANOID ROBOT HALF MARATHON

Displayed robot/network claims:

> 荣耀机器人夺冠  
> 中国联通大上行网络保驾护航

> 稳定时延30ms  
> 100ms心跳  
> 高精定位  
> 全程自主移动  
> 50分钟完成21km线路

Mobile technology:

> 5G-A大上行：3.5G 2CC + 2.1G SUL  
> 5G切片：保障业务资源分配  
> 智能板：调节负荷缓解话务冲击

Displayed measured values:

> 677Mbps　上行峰值速率  
> 155Mbps　上行平均速率  
> 99.6%+　上行20Mbps满足度  
> 38ms　端到端平均时延

Search seeds:
- `"5G-A大上行赋能亦庄马拉松"`
- `"677Mbps" "155Mbps" 人形机器人 马拉松`
- `"50分钟完成21km线路" 机器人`
- `"荣耀机器人夺冠" 中国联通 大上行`
- `"北京亦庄半程马拉松" 人形机器人 5G-A`

Research targets:
- Which robot/team is referred to by “荣耀机器人夺冠”
- How network was used for autonomy/telemetry
- Whether same architecture was reused at WHRG
- Infrastructure continuity across Beijing robot competitions

---

## FP-008 — 中国联通：京元模型服务平台

Source photo:
- `IMG_20260823_203829.jpg`

Title:

> 京元模型服务平台

Displayed statement:

> 全国模型日均调用量突破140万亿，Token成为智能经济核心  
> 中国联通北京市分公司推出京元平台，一站式纳管多款主流模型，赋能千行百业智能化升级

Displayed trend:

> 2024年1月　0.1万亿  
> 2025年6月　30万亿  
> 2026年2月　140万亿

Capabilities:

> 全栈模型，一站配齐  
> 通用模型、长文本、多模态、OCR、向量全场景覆盖，一站满足各类AI需求

> 低时延・高稳定  
> 标准token首字输出＜2秒  
> 生产级可用率＞99.9%  
> 支撑核心业务稳定运行

> 一站式开通＋快速迭代  
> 政企运营平台极简办理  
> 新模型线上会直接审批  
> 持续保持技术竞争力

Visible model/provider logos include:
- DeepSeek
- 智谱・AI
- BAAI
- additional logos not confidently transcribed

Interpretation:
- WHRG global-partner booth content.
- No direct evidence in the photo that 京元平台 is used for competition robot inference.

Search seeds:
- `"京元模型服务平台" 中国联通`
- `"全国模型日均调用量" 140万亿 京元`
- `"京元平台" DeepSeek 智谱 BAAI`
- `"京元模型服务平台" 世界人形机器人运动会`

---

## FP-009 — 中国联通：Agent + Token + AI云

Source photo:
- `IMG_20260823_203832.jpg`

Title:

> 构建“Agent+Token+AI云”新范式  
> 联通云提供全栈AI算力服务

Displayed statement:

> 坚持“守正创新、行稳致远”，锚定“算力”赛道的唯一核心能力底座，构建“Agent+Token+AI云”算力经营新模式

Visible architecture heading:

> 联通云全栈AI云产品能力体系

Visible elements include:

> Agent服务  
> OPC专区  
> [other agent zones]  
> WorkBuddy  
> Hermes  
> OpenClaw...

> Token  
> “联通星罗”智能中台

> AI云  
> AI云主机  
> AI云存储（3AZ）  
> [other cloud/compute services]

Right side refers to national science/technology awards and China Unicom's compute/network technology.

Interpretation:
- General global-partner technology display.
- Do not treat as WHRG competition infrastructure without separate evidence.

Search seeds:
- `"Agent+Token+AI云" 中国联通`
- `"联通星罗" 智能中台`
- `"OpenClaw" 中国联通 联通云`
- `"Agent+Token+AI云" 世界人形机器人运动会`

---

## FP-010 — 中国联通：其他partner展示（低优先）

Source photos:
- `IMG_20260823_203823.jpg`
- `IMG_20260823_203826.jpg`

Visible titles:

> 明曦智教大模型赋能AI校园，推动教育范式重构

> “墨攻”产品体系架构

Interpretation:
- These are visible at the WHRG global-partner display but appear to be general China Unicom education/security products.
- Low priority unless researching sponsor exhibition breadth.

Search seeds:
- `"明曦智教大模型" 中国联通`
- `"墨攻" 产品体系架构 中国联通`

---

# C. P1 — 冰丝带具身智能创新工坊 / IREA HUB

## FP-011 — “1+4+8” service system

Source photo:
- `IMG_20260825_164109.jpg`

Title:

> 以“1+4+8”把分散资源组织成可持续服务系统  
> Build a Sustainable Service System with the “1+4+8” Model

### 8项服务能力

> 面向企业全生命周期的专业服务矩阵

1. 技术研发 — Technology R&D  
2. 硬件制造 — Hardware Manufacturing  
3. 质量保障 — Quality Assurance  
4. 综合孵化 — Integrated Incubation  
5. 创投融资 — Venture Investment & Financing  
6. 人才培育 — Talent Development  
7. 国际合作 — International Cooperation  
8. 场景赋能 — Scenario Enablement

### 4大平台引擎

> 四大平台协同驱动资源高效配置

1. 成果转化平台 — Commercialization Platform  
2. 中试熟化平台 — Pilot Maturation Platform  
3. 供应链服务平台 — Supply Chain Services Platform  
4. 赛事联动平台 — Competition Collaboration Platform

### 1个核心空间载体

> 冰丝带具身智能创新工坊  
> Ice Ribbon Embodied Intelligence Innovation Workshop

> 共建共享的创新载体  
> 承载全链服务生态  
> A Co-built, Shared Innovation Hub Supporting a Full-chain Service Ecosystem

Displayed value-chain statement:

> 形成技术—产品—供应链—场景—市场的专业服务骨架  
> Building a Professional Service Framework Across Technology, Products, Supply Chain, Scenarios, and Market

Right-side branding:

> 冰丝带具身智能创新工坊  
> IREA HUB  
> 欢迎您  
> 让技术从冰丝带出发，走进真实世界

Search seeds:
- `"冰丝带具身智能创新工坊" "1+4+8"`
- `"IREA HUB" 冰丝带 具身智能`
- `"赛事联动平台" 冰丝带 具身智能`
- `"成果转化平台" "中试熟化平台" "供应链服务平台" "赛事联动平台"`

Research targets:
- Operator/legal entity
- Funding
- Connection to WHRG organizer
- Services actually delivered
- Users/teams/companies
- Post-WHRG operation
- Whether competition output is systematically transferred into pilots/products

---

## FP-012 — First 2,000 m² integrated facility

Source photo:
- `IMG_20260825_164106.jpg`

Title:

> 首期2000平方米形成研发、验证、交流与展示一体化空间  
> The first 2,000 m² Integrates R&D, Validation, Exchange, and Exhibition

Clearly visible functional labels:

> 场景测试区 — Scenario Testing Area  
> 概念验证与中试工坊 — Proof-of-Concept Validation & Pilot Workshop  
> 研发实验室 — R&D Laboratory  
> 成果展示区 — Results Exhibition Area  
> [additional exchange/meeting area visible]

Bottom:

> 首期 / Initial Phase  
> 2000 m²

Search seeds:
- `"冰丝带具身智能创新工坊" 2000平方米`
- `"场景测试区" "冰丝带具身智能创新工坊"`
- `"概念验证与中试工坊" 冰丝带`
- `"Proof-of-Concept Validation" "Ice Ribbon"`

Research targets:
- Facility floor plan
- Test equipment
- RoboCup@Home-like scenario layout
- Motion capture / OptiTrack
- Companies using the space
- Data collection infrastructure

---

## FP-013 — Office / event support

Source photo:
- `IMG_20260825_164104.jpg`

Title:

> 不止研发，办公与活动配套同样齐全  
> Beyond R&D, Office and Event Facilities Are Equally Comprehensive

Visible functions:

> 展示接待 — Exhibition & Reception  
> 咖啡休闲 — Café & Leisure  
> 洽谈交流 — Meetings & Networking  
> 会议办公 — Meetings & Office Work  
> 活动配套场地“熊猫眼” — Supporting Event Venue “Panda Eye”

Bottom statement:

> 从日常办公协作到创新活动承载，为团队提供完整空间支持  
> From Daily Office Collaboration to Innovative Event Hosting, Providing Teams with Comprehensive Spatial Support

Search seeds:
- `"熊猫眼" 冰丝带 具身智能`
- `"冰丝带具身智能创新工坊" 熊猫眼`
- `"活动配套场地" 熊猫眼 机器人`

---

## FP-014 — Bot on Ice event agenda

Source photo:
- `IMG_20260825_163734.jpg`

Visible title:

> Bot on Ice

Event information:

> 活动时间：8月25日 13:30—16:40（拟）  
> 活动地点：冰丝带具身智能创新工坊（拟）

Agenda:

> 13:30—14:00　活动签到  
> 14:00—14:05　主持开场  
> 14:05—14:10　领导致辞  
> 14:10—14:30　主旨分享：具身智能从“样机”到“产品”：高校成果转化的路径与挑战  
> 14:30—14:40　冰丝带具身智能工坊服务体系介绍  
> 14:40—14:45　工坊特邀专家颁发证书  
> 14:45—16:30　项目路演及专家互动交流  
> 16:30—16:40　自由交流

Footer:

> *以活动当日实际安排为准  
> 报名专区

Search seeds:
- `"Bot on Ice" 冰丝带 8月25日`
- `"具身智能从样机到产品" 高校成果转化 路径 挑战`
- `"Bot on Ice" 具身智能创新工坊`
- `"冰丝带具身智能工坊服务体系介绍"`

Research target:
- Speakers/projects
- Universities/startups participating
- Whether WHRG teams transitioned directly into this commercialization event

---

## FP-015 — Innovation Workshop open day + post-WHRG ecosystem events

Source photo:
- `IMG_20260825_163740.jpg`

### 1) 冰丝带具身智能创新工坊开放日

> 冰丝带具身智能创新工坊开放日  
> 创新平台启幕 8.18

Displayed text:

> 赛事开场，产业空间同步上线。  
> 冰丝带具身智能创新工坊，为具身智能企业和创新团队提供研发、测试、概念验证、中试、成果展示和产业交流等连续支撑。

> 目前，创新工坊一期即将正式投入使用，已有27家具身智能企业提出约4600平方米入驻需求，首批企业经过多轮筛选，即将正式入驻；二期扩建空间也已进入推进阶段。

> 活动期间，还将共同见证：  
> 首批生态伙伴加入  
> 首批入驻企业签约  
> 让项目和团队真正有空间入驻、有场景验证、有资源链接

Search:
- `"冰丝带具身智能创新工坊开放日" 8.18`
- `"27家" "4600平方米" 具身智能 冰丝带`
- `"首批生态伙伴" 冰丝带 具身智能`
- `"首批入驻企业" 冰丝带 具身智能`

### 2) WHRG After Party /成果转化

> 探月登陆・集结奥运村  
> 世界人形机器人运动会 After Party  
> 成果转化探索 8.23

Displayed text:

> 比赛有胜负，产业交流没有终场。

> 奥运村街道联动清华MBA具身智能俱乐部、探月具身智能社区、高校具身智能联盟等高校及产业创新力量，举办世界人形机器人运动会专场产业交流活动。

Displayed named participants include:

> 清华具身智能与机器人研究院院长 张涛  
> 北京智源人工智能研究院研究科学家 迟程  
> 智在无界  
> 灵御智能  
> 鹿明机器人  
> [UNCERTAIN company name: 帕百尼人工智能 / similar]

Displayed purpose includes discussing technical breakthroughs and industrial future, linking research, companies, and industry partners, and moving competition innovation toward wider industrial applications.

Search:
- `"探月登陆 集结奥运村" 世界人形机器人运动会 After Party`
- `"清华MBA具身智能俱乐部" 世界人形机器人运动会`
- `"探月具身智能社区" WHRG`
- `"高校具身智能联盟" 世界人形机器人运动会`
- `"张涛" "迟程" 世界人形机器人运动会 After Party`

### 3) 火星之夜

> 火星之夜・世界人形机器人运动会专场  
> 产才融合链接 8.24

Displayed text:

> 奥运村街道再次联动具身智能人才社区火星加速器，举办第三期“火星之夜”——世界人形机器人运动会专场。

The panel says prior sessions attracted company representatives, entrepreneurs, investors, and scenario-side participants; the WHRG special edition brings entrepreneurs, investors, companies, and scenario providers together around technology, talent, capital, and real demand.

Search:
- `"火星之夜" 世界人形机器人运动会`
- `"火星加速器" 具身智能 奥运村`
- `"第三期 火星之夜" 人形机器人`

### 4) 睿尔曼 ecosystem partner salon

> 睿尔曼生态伙伴交流沙龙  
> 大中小融通协同 8.25

Displayed text:

> 具身智能不是单一技术的竞争，更是一场关于本体、零部件、算法、数据、场景和服务能力的系统协同。

> 奥运村街道联合具身智能头部企业睿尔曼，围绕其上下游生态伙伴举办产业交流沙龙。

The panel describes linking robot bodies, core components, algorithms, application scenarios, and upstream/downstream companies to create real business/ecosystem cooperation.

Search:
- `"睿尔曼生态伙伴交流沙龙" 8.25`
- `"大中小融通协同" 睿尔曼`
- `"奥运村街道" 睿尔曼 具身智能`

Research significance:
- Strong field evidence that the event was connected to commercialization, incubation, investment, talent, supplier and scenario-matching activities around the competition dates.

---

# D. P1 — Data infrastructure / FirstmoveAI

## FP-016 — FirstmoveAI / 第一推动 Ego-Exo 数据基座

Source photo:
- `IMG_20260825_164115.jpg`

Brand:

> FirstmoveAI  
> 第一推动

Main statement:

> 为具身智能大模型提供  
> 开箱即用的真实世界 Ego-Exo 数据基座

Visible feature tags:

> 真实场景全覆盖  
> 多模态严格对齐  
> 毫米级精度标注  
> Data-Ready直接入库

Heading:

> 五大数据类型

Visible data-type labels:

> EGO  
> UMI  
> 五指触觉  
> 世界模型  
> WHOLE BODY

The detailed subtext below each type is too small to transcribe with high confidence; do not invent it.

Scene examples visibly shown include multiple household, manipulation, medical, kitchen, hotel, imaging, tactile/hand and other environments/tasks.

Scale statement:

> 68大类 - 1900+ 细分场景

Visible top-level scene labels include:

> 居住空间  
> 工作职业  
> 餐饮消费  
> 工业制造  
> 医疗健康  
> 交通出行  
> 商业购物  
> 体育娱乐  
> 旅游观光  
> 社交活动  
> 学习教育  
> 个人护理  
> 儿童活动  
> [additional categories]  
> +43大类更多

Bottom includes photos captioned:

> 北京大学联合实验室的签约揭牌仪式

Website visible at bottom:

> thefirstmove.ai

Search seeds:
- `"FirstmoveAI" "Ego-Exo 数据基座"`
- `"第一推动" 具身智能 Ego-Exo`
- `"68大类" "1900+" 具身智能 数据`
- `"五大数据类型" EGO UMI 五指触觉 世界模型 "WHOLE BODY"`
- `site:thefirstmove.ai Ego Exo`
- `"FirstmoveAI" 北京大学 联合实验室`
- `"第一推动" 北京大学 联合实验室`

Research targets:
- Actual dataset access
- Licensing
- Data formats/modalities
- Collection methods
- Pricing/access controls
- Commercial/model-training terms
- WHRG relation
- Whether this company contributes to the announced WHRG 2500+ hour dataset
- Mulan/OpenAtom/custom data license usage

---

# E. P1 — 朝阳区 robot industry policy and infrastructure

## FP-017 — 智能机器人产业创新应用三年行动计划

Source photo:
- `IMG_20260825_172538.jpg`

Title:

> 产业行动纲领  
> 智能机器人产业创新应用三年行动计划

Displayed explanatory paragraph states that Chaoyang District and the Beijing Municipal Bureau of Economy and Information Technology jointly issued the plan, with the general path:

> “场景牵引、平台支撑、生态赋能、集群发展”

It describes five major task areas covering technical R&D, product iteration, enterprise cultivation, talent/finance and other lifecycle elements.

Headline:

> 提升关键技术创新能力，丰富基础部组件支撑能力，  
> 夯实算力数据供给能力，扩大重点产品影响力。

### Displayed quantitative targets

**2026年底**
> 累计培育 20个以上 高价值应用场景  
> 建成不少于 2个 创新支撑平台  
> 产业规模达 10亿元

**2027年底**
> 累计培育 30个以上 应用场景  
> 建成不少于 5个 创新支撑平台  
> 产业规模达 50亿元

**2028年底**
> 累计培育 50个以上 高价值应用场景  
> 建成不少于 10个 创新支撑平台  
> 产业规模达 100亿元  
> 引育 20个以上 优秀项目

### Space planning

> 空间牵引规划  
> 奥林匹克中心区机器人创新公园建设方案

> “一核引领、多点协同”空间格局  
> 核心引擎：国家速滑馆及周边区域

Visible functional keywords:

> 技术研发  
> 运营调度  
> 产业孵化  
> 赛训验证

Search seeds:
- `"智能机器人产业创新应用三年行动计划" 朝阳区`
- `"场景牵引 平台支撑 生态赋能 集群发展" 机器人 朝阳`
- `"奥林匹克中心区机器人创新公园建设方案"`
- `"一核引领 多点协同" 机器人 创新公园`
- `"国家速滑馆及周边区域" 机器人 创新公园`
- `"2028" "产业规模达100亿元" 智能机器人 朝阳`

Research targets:
- Official policy PDF/notice
- Issuing authorities/date
- Direct relationship to WHRG
- Whether WHRG is explicitly used as a policy implementation mechanism
- Funding and implementation entities

---

## FP-018 — 朝阳区促进智能机器人产业创新发展若干措施

Source photo:
- `IMG_20260825_172541.jpg`

Title:

> 朝阳区促进智能机器人产业创新发展若干措施

### 01 支持关键技术和产品攻关

> 机器人关键技术、核心部组件攻关并完成首发首试，最高支持1000万元。

> 国家级、省部级机器人科创项目立项配套，[amount text should be verified from official document before use]

> 主导制（修）订标准，国际标准最高支持50万元；国家标准最高支持30万元；行业标准最高支持10万元。

### 02 支持创新平台建设

> 建设创新联合体、联合实验室、协同创新中心等新型创新载体，最高支持500万元。

> 建设数据采集训练、中试验证、检验检测等共性技术平台，最高支持500万元。

> 建设国际合作、孵化加速、科普教育、场景对接等公共服务平台，最高支持500万元。

### 03 支持数据要素供给和交易

> 建设机器人领域高质量数据集、语料库，最高支持200万元。

### 04 支持场景拓展应用

> 开放应用场景，根据任务（文旅、养老、医疗、城管等）最高支持500万元。

> 打造机器人MALL、机器人餐厅、体验店等消费新业态，最高支持1000万元。

### 05 支持服务模式创新

> 鼓励机器人租赁服务，最高支持1000万元。

> 发放机器人租赁券，支持企业/高校科研测试，最高支持2000万元。

> 发放机器人企业保险保费补贴，最高支持200万元。

### 06 支持特色园区建设

> 建设机器人产业园、创新公园等载体，建设公共路演厅、发布厅、会议室等公共服务设施，最高支持500万元。

### 07 支持创新型企业发展

> 产业链关键环节实现技术突破的机器人创新企业，最高支持3000万元。

### 08 支持举办机器人品牌赛事活动

> 举办高水平机器人赛事/挑战赛，最高支持500万元。

> 举办学术会议、论坛、展会品牌活动，最高支持100万元。

Search seeds:
- `"朝阳区促进智能机器人产业创新发展若干措施"`
- `"机器人租赁券" "2000万元" 朝阳`
- `"高质量数据集" "200万元" 机器人 朝阳`
- `"机器人赛事" "500万元" 朝阳区`
- `"机器人MALL" "1000万元" 朝阳`
- `"数据采集训练" "中试验证" "检验检测" 500万元 朝阳`

Research significance:
- Highly relevant to the research question of how teams, data, test facilities and robot access are intentionally created/subsidized.
- Must be verified against the official policy text before using amounts as final report facts.

---

## FP-019 — 朝阳区产业生态矩阵

Source photos:
- `IMG_20260825_172532.jpg`
- `IMG_20260825_172547.jpg`

Title:

> 产业生态矩阵

### （一）人形机器人赛训基地及产业园

#### 1. 人形机器人产业生态赛训基地

Displayed paragraph states that Chaoyang District and 北奥集团 jointly built an embodied/humanoid robot training/competition base and industrial park.

Clearly readable function list:

> 新兴赛事  
> 数据采集  
> 技术验证  
> 产品测试  
> 产业孵化  
> 展览展示  
> 公众科普  
> 国际交流  
> 商业配套

The paragraph says the base is intended to attract global humanoid-robot innovation resources and mentions multiple sub-sites, including `熊猫眼` and `冰丝带`.

It also visibly references:
- 加速进化
- 灵心巧手
- [other companies/teams not all reliably transcribed]
- 清华大学
- 北京大学
- Robo Summit
- robot-football-related activities

Search:
- `"人形机器人产业生态赛训基地" 朝阳`
- `"北奥集团" "人形机器人产业生态赛训基地"`
- `"熊猫眼" 人形机器人 赛训基地`
- `"Robo Summit" 朝阳 人形机器人`
- `"加速进化" "赛训基地" 朝阳`

#### 2. 人形机器人产业生态测评基地

Displayed paragraph states the base integrates:

> 机器人训练  
> 测评  
> 中试  
> 认证  
> [and related technical services]

and describes four major functions including real-scene training, diagnostic/evaluation, professional testing and exchange/cooperation.

Important visible statement:

> 已面向世界人形运动会参赛队伍开放，承接场景赛参赛队伍训练工作

Search:
- `"人形机器人产业生态测评基地" 世界人形机器人运动会`
- `"承接场景赛参赛队伍训练工作"`
- `"人形机器人产业生态测评基地" 国家速滑馆`
- `"赛迪研究院" 人形机器人 生态测评基地 朝阳`

#### 3. 冰丝带具身智能创新工坊

Displayed text includes:
- joint construction involving Chaoyang-side entities and 北奥集团
- location in/near the Ice Ribbon
- initial 2000 m²
- R&D labs, scene testing, concept validation, pilot maturation, result exhibition
- startup incubation, technical pilot maturation and competition-result commercialization

Visible dates:

> 2026年7月16日正式启动  
> 2026年8月18日正式对外运营

Search:
- `"冰丝带具身智能创新工坊" "2026年7月16日"`
- `"冰丝带具身智能创新工坊" "2026年8月18日"`
- `"赛事成果转化" 冰丝带 具身智能`

---

### （二）产业服务平台

#### 1. 具身智能测试实验室

Displayed text:
- located in AI Space / AISPACE industrial park
- around 1000 m²
- multiple testing zones and specialized labs
- provides a chain of technical support / test validation / scene matching
- says it has connected with over 100 industry-side suppliers/users/companies/research institutions

Search:
- `"具身智能测试实验室" AISPACE 朝阳`
- `"具身智能测试实验室" 1000平方米`
- `"具身智能测试实验室" 100余家`

#### 2. RCAP亚太机器人世界杯北京国际交流平台

Displayed title:

> RCAP亚太机器人世界杯北京国际交流平台

Displayed description says it is jointly built by Chaoyang-side authorities and RCAP / RoboCup Asia-Pacific-related international organization, located in AI Space industrial park, and links:

> 国际赛事  
> 专家团队  
> 科研机构  
> 产业资源  
> 国际项目导入  
> 技术交流  
> 场景验证  
> 标准研究  
> 成果转化

Visible date reference:

> 2026年6月2日 [platform-related launch/signing activity]

Search:
- `"RCAP亚太机器人世界杯北京国际交流平台"`
- `"RCAP" AISPACE 北京 国际交流平台`
- `"2026年6月2日" RCAP 朝阳`
- `"RoboCup Asia-Pacific" 朝阳 AISPACE`

Research significance:
- High-value lead for how international WHRG teams may have been recruited/connected.

#### 3. 机器人大学堂场景对接平台

Displayed text says the platform is jointly built with `机器人大学堂` and supports:
- scenario collection
- demand analysis / professional screening
- publishing scenario lists
- technical-provider matching
- scenario skill competitions
- scenario deployment / industrial development

Search:
- `"机器人大学堂场景对接平台" 朝阳`
- `"机器人大学堂" 场景技能赛`
- `"机器人大学堂" 北辰时代大厦`

#### 4. 机器人产业金融服务平台

Displayed title:

> 机器人产业金融服务平台

Displayed text says Chaoyang District worked with 光大集团 and launched the platform on:

> 2026年6月26日

It describes integration of financial institutions and services such as:
- credit
- equity investment
- listing/IPO guidance
- financing/leasing-related services
- industrial funds
- roadshows
- support for technical R&D, platform building and scene deployment

Search:
- `"机器人产业金融服务平台" "2026年6月26日"`
- `"光大集团" 机器人产业金融服务平台 朝阳`
- `"机器人产业金融服务平台" 融资租赁`

---

### （三）产业承载空间

#### 智能机器人创新应用基地（北辰时代大厦）

Displayed text:

> 位于朝阳区北辰东路8号  
> 首期2万平方米产业空间  
> 楼宇单层约2100平方米无柱大开间

It states the space supports users from startup desks to whole-floor customized use and contains a one-stop robot-industry service center with:

> 展示中心  
> 共享办公  
> 孵化加速

Visible contact:

> 18600474233

Search:
- `"智能机器人创新应用基地" "北辰时代大厦"`
- `"北辰东路8号" 机器人 创新应用基地`

#### AISPACE产业园（望京数字创意园）

Displayed text:

> 位于朝阳区望京东路1号  
> 总建筑面积2.97万平方米

The park focuses on embodied intelligence and mentions:
- intelligent "brain"/AI
- multi-agent collaboration
- model-training integration
- `AIMate场景对接`
- seven professional service platforms
- 具身智能测试实验室
- RCAP亚太机器人世界杯北京中心

Visible contact:

> 18813010903

Search:
- `"AISPACE产业园" "望京数字创意园"`
- `"望京东路1号" AISPACE`
- `"AIMate场景对接" AISPACE`
- `"RCAP亚太机器人世界杯北京中心" AISPACE`

Other space names visible at the bottom of the brochure:
- `[UNCERTAIN exact name] 北京…机器人…产业园`
- `电通创意广场`
- `北控智能制造产业园`
- `UCP恒通国际创新园`
- `[UNCERTAIN] 金辉时八区 / similar`

Do not use uncertain park names as facts until verified.

---

# F. P1 — Robot leasing / access to hardware

## FP-020 — 北京机器人融资租赁股份有限公司

Source photo:
- `IMG_20260823_200617.jpg`

Banner title:

> 北京机器人融资租赁股份有限公司  
> BEIJING ROBOT FINANCIAL LEASING CO., LTD

Company description (readable core):

> 按照北京市政府工作部署，2025年初，北京机器人融资租赁股份有限公司应势成立。公司推动融资租赁与场景支持有机结合，积极引导机器人产业落地生根与技术迭代，有效填补产业发展关键空白环节，切实解决机器人产品应用“最后一公里”难题。

Displayed examples include:

> 作为北京市首家全品类机器人应用服务商，公司取得多项标志性场景落地成果：

Medical:
> 医疗场景率先在三甲医院落地手术机器人租赁，搭建机器人院应用评价体系

Parks:
> 园林场景规模化投放72台机器人进驻14家市属公园，打造智慧园林标杆

Education:
> 教育场景推进“机器人进校园”

Platform branding:

> 租机器人就上“暖机租”  
> 线上平台：“暖机租”小程序  
> 一键智租　全程省心  
> 省心租好机，就上暖机租

QR label:

> 北京机器人租赁公司公众号

Search seeds:
- `"北京机器人融资租赁股份有限公司"`
- `"北京机器人租赁公司" 暖机租`
- `"暖机租" 机器人 小程序`
- `"72台机器人" "14家市属公园" 租赁`
- `"机器人进校园" 北京机器人融资租赁`
- `"北京机器人融资租赁" 世界人形机器人运动会`
- `"北京机器人融资租赁" Booster`
- `"北京机器人融资租赁" 加速进化`

Research targets:
- WHRG robot leasing/support cases
- Robot inventory/models
- Loan vs lease vs sponsorship
- Pricing
- Government subsidy / rental voucher linkage
- Teams/universities supported
- Booster T1/T2 relationship

---

# G. P2 — Developer / innovation communities

## FP-021 — OPC一曜社区

Source photo:
- `IMG_20260823_200621.jpg`

Title:

> OPC一曜社区

Subtitle:

> 北京未来数字空间创新试验区  
> 首个文化与科技融合场景OPC社区

Displayed description says the community focuses on OPC companies and creators, uses AI-based service capabilities, and connects multiple links of the digital-industry ecosystem.

Heading:

> 八大能力赋能OPC社区运转引擎

Visible capabilities:

1. IP孵化  
2. 内容共创  
3. AI增效  
4. 全域增长  
5. 商业变现  
6. 资源链接  
7. 品牌出海  
8. 融资加速

Scale:

> 20.5万平方米 产业空间  
> 507套 人才公寓

Partnership:

> 首钢集团战略合作

Three bottom modules:

> 产业创新中心  
> 创意内容社区  
> 人才生活社区

Search seeds:
- `"OPC一曜社区"`
- `"北京未来数字空间创新试验区" OPC`
- `"首个文化与科技融合场景OPC社区"`
- `"一曜社区" 首钢集团`
- `"OPC一曜社区" 机器人 具身智能`

Interpretation:
- Not confirmed as a WHRG team-forming mechanism.
- Useful lead for developer/creator community and Shougang-linked innovation ecosystem.

---

# H. P2/P3 — Suppliers / exhibitors / public experience

## FP-022 — 永轴智造 / YZTECH MFG

Source photo:
- `IMG_20260826_132745.jpg`

Visible branding:

> 永轴智造  
> YZTECH MFG

Main product:

> 精密高刚性  
> 摆线减速器

Subtitle:

> 轻量化　小体积

WHRG 2026 logo is displayed on the booth backdrop.

Search seeds:
- `"永轴智造" 摆线减速器`
- `"YZTECH MFG" cycloidal reducer humanoid`
- `"永轴智造" 世界人形机器人运动会`
- `"精密高刚性摆线减速器" 人形机器人`

Research target:
- Supplier relationship to WHRG/teams
- Humanoid joint applications
- Customers/teams
- Sponsorship/exhibitor vs actual component use

---

## FP-023 — BAIC / 北汽集团 exhibition

Source photo:
- `IMG_20260826_144044.jpg`

Visible branding:

> BAIC 北汽集团  
> 北汽元境智能 / BAIC KOSMOS INTELLIGENCE [visible branding]

Exhibition area shows multiple vehicles and audience entrance signage.

Interpretation:
- Public/exhibition-side ecosystem evidence, not a robot competition entry by itself.

Search seeds:
- `"北汽集团" 世界人形机器人运动会`
- `"北汽元境智能" 世界人形机器人运动会`

---

## FP-024 — DaxAI Robot / 大咖机器人

Source photo:
- `IMG_20260826_180340.jpg`

Event-side branding:

> 嗨FUN 机器人潮玩集  
> DaxAI Robot  
> 大咖机器人

Displayed slogan:

> 全球重载机器马开创者

Other visible public-experience text includes:

> 生活新伙伴  
> 这台机器马我先骑了

Visual:
- Large rideable/vehicle-like robot on public display with children/visitors interacting.

Search seeds:
- `"DaxAI Robot" 大咖机器人`
- `"大咖机器人" 重载机器马`
- `"全球重载机器马开创者"`
- `"DaxAI Robot" 世界人形机器人运动会`
- `"嗨FUN机器人潮玩集"`

Research significance:
- Public engagement / robot exposure around WHRG.
- Do not classify as humanoid competition participant unless separately confirmed.

---

## FP-025 — unclear AGILINK-like logo

Source photo:
- `IMG_20260824_152027.jpg`

Visible logo/text:
- `[UNCERTAIN] AGILINK / AgiLink / similar`

The photo is a magnified venue-screen image with strong scanline interference.

Search only if needed:
- `"AgiLink" robot WHRG 2026`
- `"AGILINK" humanoid robot China`

Do not create an entity from this photo alone.

---

## FP-026 — WHRG photo point / public-facing event branding

Source photo:
- `IMG_20260826_171905.jpg`

Visible text:

> 第二届世界人形机器人运动会  
> WORLD HUMANOID ROBOT GAMES 2026

Visual:
- Public photo area with two humanoid robots and a human visitor.

Research significance:
- Field evidence of public-facing robot interaction/photo experience.
- No additional technical inference.

---

# I. User's prior field-note / video-outline derived search seeds

The following are not OCR from the photos above. They come from the user's prior field report / video outline and should be treated as **Field Observation / User Note** until externally verified.

## UF-001 — Galbot retail / convenience-store robot

User note:
- Galbot convenience-store / retail robot seen at venue.

Search:
- `"Galbot" 世界人形机器人运动会`
- `"银河通用" Galbot 世界人形机器人运动会`
- `"银河通用" 零售机器人 国家速滑馆`
- `"Galbot" 便利店 人形机器人 2026`

Research:
- Competition vs exhibition
- Commercial deployment
- Dataset relation
- Public interaction

---

## UF-002 — Unitree + motion capture

User note:
- Unitree robot combined with motion-capture demo.

Search:
- `"Unitree" motion capture 世界人形机器人运动会`
- `"宇树" 动作捕捉 世界人形机器人运动会`
- `"宇树" OptiTrack WHRG`
- `"OptiTrack" 世界人形机器人运动会`
- `"动作捕捉" 国家速滑馆 人形机器人`

Research:
- OptiTrack supplier
- Motion capture system purpose
- Training/data collection
- Whether used by teams or demonstration only

---

## UF-003 — Robot coffee / ice cream / service demonstrations

User note:
- Robot coffee
- Robot ice cream
- service demos
- ordinary visitors could interact with robots

Search:
- `"机器人咖啡" 世界人形机器人运动会`
- `"机器人冰淇淋" 世界人形机器人运动会`
- `"国家速滑馆" 机器人咖啡 2026`
- `"世界人形机器人运动会" 互动体验`

---

## UF-004 — AgiBot / 智元 service demonstration

User note:
- AgiBot / 智元 humanoid practical/service demo.

Search:
- `"智元机器人" 世界人形机器人运动会 展示`
- `"AgiBot" World Humanoid Robot Games 2026`
- `"智元" 国家速滑馆 具身智能 展示`
- `"智元" 世界人形机器人运动会 服务`

Research:
- Competition entries vs exhibition
- Open artifacts actually linked to competition
- Mulan license only if specific competition-related resource exists

---

## UF-005 — Astribot / 星尘智能 service demonstration

User note:
- Astribot / 星尘智能 practical/service demonstration.

Search:
- `"Astribot" 世界人形机器人运动会`
- `"星尘智能" 世界人形机器人运动会`
- `"Astribot" 国家速滑馆 2026`

---

## UF-006 — 首钢基金 / corporate support

User note:
- Shougang Fund / 首钢基金 visible in event-support/sponsor context.

Search:
- `"首钢基金" 世界人形机器人运动会`
- `"首钢基金" 具身智能 机器人 投资`
- `"首钢" 世界人形机器人运动会 机器人`

Research:
- Sponsor/investor/support role
- Investment portfolio linked to participants
- Avoid inferring investment in a team without evidence

---

## UF-007 — “硅基生命” / coexistence messaging

User note:
- Venue messaging around “silicon life” and human-robot coexistence.

Search:
- `"硅基生命" 世界人形机器人运动会`
- `"人机共生" 世界人形机器人运动会`
- `"硅基生命" 国家速滑馆 机器人`

Research:
- Organizer narrative/public engagement
- Education/public acceptance framing

---

## UF-008 — 投壶 / traditional culture robot activity

User note:
- Traditional Chinese `投壶` performed with robots.

Search:
- `"投壶" 世界人形机器人运动会`
- `"机器人投壶" 2026 北京`
- `"投壶机器人" 国家速滑馆`

Research:
- Competition vs exhibition
- Rule/task design
- Cultural/public-experience layer

---

## UF-009 — Engineer visibility / “engineers as stars”

User observation:
- Engineers and pit activity were highly visible to spectators.
- Children gathered around pits.
- Engineering work itself appeared to be part of the spectacle.

Search:
- `"世界人形机器人运动会" 工程师 赛场`
- `"世界人形机器人运动会" 维修区 观众`
- `"世界人形机器人运动会" 青少年 科普`
- `"世界人形机器人运动会" 儿童 互动`

Research:
- Pit openness
- Public access
- STEM/education programs
- Engineer interviews/awards
- Audience design

---

## UF-010 — RoboCup Asia-Pacific / RCAP connection

User note:
- User entered/observed a pit with RoboCup Asia-Pacific organizers/members.
- RCAP/RoboCup people were involved around Booster Robotics.

Search:
- `"RoboCup Asia-Pacific" 世界人形机器人运动会`
- `"RCAP" 世界人形机器人运动会 2026`
- `"RoboCup" WHRG 2026 Beijing`
- `"RCAP亚太机器人世界杯北京国际交流平台" WHRG`
- `"Booster Robotics" RCAP WHRG`

Research:
- International-team recruitment connector
- RCAP formal role
- Team invitation/support
- Shared staff/organizers
- Platform/equipment support

---

## UF-011 — Booster Robotics pit / pre-release Booster T2

User note:
- Booster Robotics tuning/engineering activity observed in pit.
- Pre-release `Booster T2` observed kicking a soccer ball against/with a human.

Search:
- `"Booster T2" 世界人形机器人运动会`
- `"Booster Robotics" T2 WHRG 2026`
- `"加速进化" T2 世界人形机器人运动会`
- `"Booster T2" RoboCup 2026`
- `"加速进化" 世界人形机器人运动会 国际团队`

Research:
- Product release timeline
- Why pre-release hardware was used
- Teams using Booster robots
- Hardware provision / technical support
- Competition as product validation
- RoboCup -> WHRG network

---

## UF-012 — RoboCup 2050 goal

User note:
- RoboCup relation discussed with the classic goal of defeating human world champions by 2050.

Search:
- `"2050年" RoboCup 人类世界冠军 足球`
- `"RoboCup" 2050 world champion goal`
- `"RoboCup" 世界人形机器人运动会 2050`

Use:
- Background/context only; do not imply WHRG has the same formal goal.

---

## UF-013 — RoboCup@Home-like test / life-task facility

User note:
- A test facility resembling RoboCup@Home / everyday-living task environments was observed.
- Planned for learning/evaluation after the event as well.

Search:
- `"RoboCup@Home" 冰丝带 具身智能创新工坊`
- `"场景测试区" RoboCup@Home 冰丝带`
- `"人形机器人产业生态测评基地" 场景赛 训练`
- `"国家速滑馆" 生活场景 人形机器人 测试`
- `"冰丝带" 具身智能 场景测试`

Research:
- Permanent post-event facility
- Scenario definitions
- Evaluation protocols
- Dataset generation
- Teams allowed to use it
- Open/shared access

---

## UF-014 — OptiTrack motion-capture infrastructure

User note:
- OptiTrack seen as a technical supplier/infrastructure element.

Search:
- `"OptiTrack" 世界人形机器人运动会`
- `"OptiTrack" 冰丝带 机器人`
- `"OptiTrack" 人形机器人 国家速滑馆`
- `"OptiTrack" Unitree 北京 2026`

Research:
- Competition vs training/test facility
- Data captured
- Supplier relationship
- Open dataset connection

---

## UF-015 — iFLYTEK / 科大讯飞

User note:
- iFLYTEK visible among technical suppliers/sponsors.

Search:
- `"科大讯飞" 世界人形机器人运动会`
- `"iFLYTEK" World Humanoid Robot Games 2026`
- `"科大讯飞" 国家速滑馆 人形机器人`

Research:
- Actual role: sponsor / speech / model / voice / infrastructure / demo
- Do not infer technical use from sponsor logo alone

---

## UF-016 — Audience cheering slow robots

User observation:
- In the 100m, spectators loudly cheered “加油” even for slower robots.
- User views this as part of the event's social/public meaning.

Search:
- `"世界人形机器人运动会" 100米 观众 加油`
- `"世界人形机器人运动会" 观众 机器人 慢`
- `"世界人形机器人运动会" 科普 公众`
- `"世界人形机器人运动会" 门票 观众人数`

Research:
- Audience counts
- Ticketing
- children/family attendance
- organizer public-engagement goals
- educational activities
- media descriptions of crowd response

---

# J. Recommended search-task bundles for Kimi

Do not investigate all seeds in one chat.

## Bundle 1 — Competition Entry recovery from field scoreboards
Priority P0:
- 园区管理岗
- 1500米决赛第2组
- 清华火神队 vs 农大青禾队
- 北航 Robot #083

Goal:
- Find official schedules/results/group tables.
- Populate Competition Entry Map.

## Bundle 2 — Permanent WHRG-to-industry infrastructure
Priority P1:
- 冰丝带具身智能创新工坊
- 1+4+8
- 人形机器人产业生态赛训基地
- 人形机器人产业生态测评基地
- Bot on Ice
- 27 companies / 4600 m²
- After Party / 火星之夜 / 睿尔曼沙龙

Goal:
- Determine whether WHRG has a deliberate post-event commercialization/testing pipeline.

## Bundle 3 — Open data / data policy
Priority P1:
- FirstmoveAI / 第一推动
- Ego-Exo data base
- 68大类 / 1900+细分场景
- Chaoyang data-subsidy policy
- WHRG 2500+ hour dataset
- robot-management-platform data

Goal:
- Map who collects data, who can access it, and under what license.

## Bundle 4 — Team formation through hardware access / leasing
Priority P1:
- 北京机器人融资租赁股份有限公司
- 暖机租
- 机器人租赁券
- Booster / 加速进化
- university/team robot access

Goal:
- Test whether robot leasing/support materially lowers the entry barrier to WHRG.

## Bundle 5 — International-team recruitment
Priority P1/P2:
- RCAP international exchange platform
- RoboCup Asia-Pacific
- TEAM BRAZIL
- RoboRoos
- GMO Robots
- Booster Robotics

Goal:
- Reconstruct connector -> invitation -> robot -> support -> WHRG participation path.

## Bundle 6 — Competition/public engagement
Priority P2/P3:
- Galbot
- AgiBot
- Astribot
- robot coffee/ice cream
- DaxAI Robot
- 投壶
- children / pits / cheering
- engineers as visible protagonists

Goal:
- Evaluate whether WHRG is designed as public technology exposure, not only a competition.

---

# K. Photo coverage manifest

The following original photo files are represented in this transcription file.

- `IMG_20260823_182649.jpg` -> FP-001
- `IMG_20260823_192452.jpg` -> FP-002
- `IMG_20260823_200617.jpg` -> FP-020
- `IMG_20260823_200621.jpg` -> FP-021
- `IMG_20260823_203821.jpg` -> FP-005
- `IMG_20260823_203823.jpg` -> FP-010
- `IMG_20260823_203826.jpg` -> FP-010
- `IMG_20260823_203829.jpg` -> FP-008
- `IMG_20260823_203832.jpg` -> FP-009
- `IMG_20260823_203838.jpg` -> FP-007
- `IMG_20260823_203842.jpg` -> FP-006
- `IMG_20260824_151751.jpg` -> FP-004
- `IMG_20260824_152027.jpg` -> FP-025
- `IMG_20260825_163734.jpg` -> FP-014
- `IMG_20260825_163740.jpg` -> FP-015
- `IMG_20260825_164104.jpg` -> FP-013
- `IMG_20260825_164106.jpg` -> FP-012
- `IMG_20260825_164109.jpg` -> FP-011
- `IMG_20260825_164115.jpg` -> FP-016
- `IMG_20260825_172529.jpg` -> FP-017/FP-019 contextual overview; detailed small text intentionally not fully transcribed
- `IMG_20260825_172532.jpg` -> FP-019
- `IMG_20260825_172538.jpg` -> FP-017
- `IMG_20260825_172541.jpg` -> FP-018
- `IMG_20260825_172547.jpg` -> FP-019
- `IMG_20260825_204605.jpg` -> FP-003
- `IMG_20260826_131525.jpg` -> FP-006
- `IMG_20260826_131611.jpg` -> FP-006
- `IMG_20260826_131614.jpg` -> FP-007
- `IMG_20260826_132745.jpg` -> FP-022
- `IMG_20260826_144044.jpg` -> FP-023
- `IMG_20260826_171905.jpg` -> FP-026
- `IMG_20260826_180340.jpg` -> FP-024

Derived crops/contact sheets are not separate evidence; they were only used to improve legibility during transcription.

---

# L. Highest-value claims to verify first

1. `人形机器人产业生态测评基地` was already open to WHRG teams and undertook scenario-competition team training.
2. `冰丝带具身智能创新工坊` launched around WHRG and explicitly includes a `赛事联动平台`, commercialization, pilot maturation and supply-chain services.
3. The workshop reported 27 embodied-intelligence companies requesting ~4600 m² of space.
4. Chaoyang policy explicitly subsidizes:
   - robot high-quality datasets / corpora,
   - data collection/training/test platforms,
   - robot leasing,
   - robot leasing vouchers for companies/universities,
   - robot competitions/challenges.
5. `RCAP亚太机器人世界杯北京国际交流平台` may be a concrete institutional connector for international WHRG team recruitment.
6. `北京机器人融资租赁股份有限公司` may be a concrete mechanism for providing expensive robots to universities/teams.
7. China Unicom displayed a WHRG-specific robot management platform, but the actual connected robot count and data usage remain unverified.
8. FirstmoveAI claims a large embodied-AI Ego-Exo data base; access/license/WHRG relationship need verification.
9. Field scoreboards provide direct leads for reconstructing competition entries that were missing from public Web census work.
10. Current field evidence strongly suggests the research should distinguish:
    - competition rules/results,
    - team formation,
    - hardware access,
    - test/training infrastructure,
    - data infrastructure,
    - commercialization/finance,
    - international recruitment,
    - public engagement.

