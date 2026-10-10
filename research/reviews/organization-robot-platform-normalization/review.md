# Organization / Robot Platform relationship normalization review

## Methodology

This review audited all 356 Team entities and 770 Competition Entries before changing canonical data. It used only canonical Evidence, immutable official-archive source rows, historical imported snapshots already represented in canonical provenance, and normalized Team identities. No web research was performed.

Organization identity, team affiliation, manufacturer, platform provider, sponsorship, technical support, and robot use are modeled as separate typed relationships. A manufacturer or sponsor was never treated as the Team owner. Joint Teams retain one relationship per supported participant; their `organization_id` remains empty because that scalar cannot represent multiple organizations. Robot Platform use was not copied from a Team to all of its Entries.

## Before / after coverage

| Metric | Before | After |
| --- | ---: | ---: |
| Canonical records | 1683 | 1711 |
| Organizations | 46 | 64 |
| Teams linked to at least one Organization | 53 | 88 |
| Entries linked through Team/Organization relationships | 220 | 263 |
| Entries with direct Organization relationships | 83 | 93 |
| Entries with scalar Organization ID | 83 | 84 |
| Joint-Team Organization relationships | 0 | 60 |
| Robot Platforms | 5 | 15 |
| Entries linked to Robot Platform | 4 | 5 |
| Teams with at least one known Robot Platform | 3 | 12 |
| Unique manufacturers linked from Robot Platforms | 3 | 8 |
| Unique robot families | 5 | 12 |
| Unique Robot Platform models/versions | 5 | 15 |

Before normalization, 2 Teams had Organization text but no Organization relationship, 5 Teams carried manufacturer/provider text, and 0 Entries had structured robot manufacturer/model text without a Robot Platform ID. Ten Entries had Organization text but no scalar ID; nine were multi-organization Teams and remain scalar-null while gaining typed relationships, and one malformed source alias was resolved to a canonical Organization ID.

## Distinct raw-string audit

- Organization (105): `GMO Robots`, `IT之家/ithome.com`, `Multiple`, `Multiple/163.com`, `Open X-Humanoid`, `OpenHUTB`, `Portugal, Japan`, `WHRG`, `WHRG组委会`, `guanyexinguancha.com`, `sina.cn`, `sohu.com`, `whrgoc.com`, `上海体育大学、北京智元新创技术有限公司`, `上海戏剧学院、北京智元新创技术有限公司`, `上海荣耀智慧科技开发有限公司`, `上海高弈科技有限公司`, `上观新闻/jfdaily.com`, `东方财富网/eastmoney.com`, `中国人民大学`, `中国农业大学/news.cau.edu.cn`, `中国农业大学工学院`, `中山大学人工智能学院`, `中科院自动化研究所`, `京奥（北京）科技有限公司`, `人形机器人（上海）有限公司`, `众擎机器人`, `优理奇`, `养老护理机器人联合实验室`, `养老护理机器人联合实验室（河北工业大学-北京人形机器人创新中心）`, `农大山海队`, `加速进化`, `北京交通大学`, `北京人形+河南科技学院`, `北京人形机器人创新中心`, `北京人形机器人创新中心+深圳大学`, `北京人形机器人创新中心有限公司`, `北京人形机器人创新中心有限公司和北京信息科技大学`, `北京信息科技大学`, `北京北大方正软件职业技术学院`, `北京卓越星空科技有限公司`, `北京大学`, `北京市政府`, `北京市科学技术委员会`, `北京新闻(WeChat)`, `北京日报/bjd.com.cn`, `北京智元新创技术有限公司`, `北京本地宝(WeChat)`, `北京松延动力深饪餐饮有限公司`, `北京林业大学工学院 MV&AI 实验室`, `北京泡泡工坊科技有限公司`, `北京灵翌科技有限公司`, `北京科技大学`, `北京科技大学、中国戏曲学院、北京智元新创技术有限公司`, `北京耀昇终端有限公司`, `北京舞蹈学院、北京智元新创技术有限公司`, `北京航空航天大学/智元`, `北京荣耀终端有限公司`, `北京警察学院`, `北京邮电大学`, `华北电力大学`, `哈尔滨工业大学`, `国际科技创新中心/ncsti.gov.cn`, `宇树科技`, `宇树科技股份有限公司`, `寒武纪/Cambricon`, `工业具身智能机器人联合实验室`, `工业具身智能机器人联合实验室（华中科技大学-北京人形机器人创新中心）`, `巴西多所大学RoboCup团队`, `微信公众号(FM1007福建交通广播)`, `微信公众号(具身人工智能)`, `微信公众号(行者吴江)`, `微信公众号(财联社AI daily)`, `情感智能应用联合实验室`, `情感智能应用联合实验室（北京大学-北京人形机器人创新中心）`, `成都星宇纪元科技有限公司`, `新华社`, `星动纪元`, `星海图`, `智元`, `智元创新（上海）科技股份有限公司`, `智元创新（宁夏）科技有限公司`, `智元创新（成都）科技有限公司`, `智元创新（无锡）科技有限公司`, `智元创新（深圳）科技有限公司`, `智元机器人`, `松延动力`, `柏奥尼克机器人队伍`, `江西理工大学`, `深圳荣耀智慧科技开发有限公司`, `清华大学`, `清华大学/tsinghua.edu.cn`, `清华大学自动化系`, `清华火神队`, `澳大利亚三所高校`, `百度百科/baike.baidu.com`, `知乎专栏`, `者北京星动纪元科技股份有限公司`, `财新/caixin.com`, `财新/photos.caixin.com`, `财联社/cls.cn`, `郑州铁路职业技术大学`, `重庆大学`, `钛媒体/tmtpost.com`, `银河通用`
- University (33): `上海体育大学、北京智元新创技术有限公司`, `上海戏剧学院、北京智元新创技术有限公司`, `中国人民大学`, `中国农业大学/news.cau.edu.cn`, `中国农业大学工学院`, `中山大学人工智能学院`, `养老护理机器人联合实验室（河北工业大学-北京人形机器人创新中心）`, `北京交通大学`, `北京人形+河南科技学院`, `北京人形机器人创新中心+深圳大学`, `北京人形机器人创新中心有限公司和北京信息科技大学`, `北京信息科技大学`, `北京北大方正软件职业技术学院`, `北京大学`, `北京林业大学工学院 MV&AI 实验室`, `北京科技大学`, `北京科技大学、中国戏曲学院、北京智元新创技术有限公司`, `北京舞蹈学院、北京智元新创技术有限公司`, `北京航空航天大学/智元`, `北京警察学院`, `北京邮电大学`, `华北电力大学`, `哈尔滨工业大学`, `工业具身智能机器人联合实验室（华中科技大学-北京人形机器人创新中心）`, `巴西多所大学RoboCup团队`, `情感智能应用联合实验室（北京大学-北京人形机器人创新中心）`, `江西理工大学`, `清华大学`, `清华大学/tsinghua.edu.cn`, `清华大学自动化系`, `澳大利亚三所高校`, `郑州铁路职业技术大学`, `重庆大学`
- Research Institute / Lab (13): `中科院自动化研究所`, `养老护理机器人联合实验室`, `养老护理机器人联合实验室（河北工业大学-北京人形机器人创新中心）`, `北京人形机器人创新中心`, `北京人形机器人创新中心+深圳大学`, `北京人形机器人创新中心有限公司`, `北京人形机器人创新中心有限公司和北京信息科技大学`, `北京林业大学工学院 MV&AI 实验室`, `国际科技创新中心/ncsti.gov.cn`, `工业具身智能机器人联合实验室`, `工业具身智能机器人联合实验室（华中科技大学-北京人形机器人创新中心）`, `情感智能应用联合实验室`, `情感智能应用联合实验室（北京大学-北京人形机器人创新中心）`
- Manufacturer (10): `众擎机器人`, `加速进化`, `北京人形机器人创新中心`, `宇树科技`, `星动纪元`, `星海图`, `智元机器人`, `松延动力`, `荣耀`, `银河通用`
- Robot Manufacturer (3): `加速进化 (中国)`, `北京人形机器人创新中心`, `宇树科技 (中国)`
- Robot Family-level source strings (3): `Q5`, `天工`, `夸父(Kuavo)`
- Robot Model (11): `Booster T1/K1`, `Galbot G1`, `H1/G1`, `天工Ultra`, `天工Ultra/天工3.0/天轶2.0`, `小顽童`, `星动L7`, `格斗机器人"豆汁""卤煮"`, `精灵G2`, `远征A3/精灵G2/灵犀X2`, `远征A3/精灵G2/灵犀X2/OmniHand`
- Robot Platform (9): `Multiple`, `Q5`, `加速进化 K1/T1/T2`, `加速进化Booster T1`, `加速进化Booster T1/K1`, `加速进化T1`, `天工`, `夸父(Kuavo)`, `宇树 G1`
- Platform Provider (3): `GALAXEA`, `加速进化 (中国)`, `宇树科技 (中国)`

The corpus has no dedicated Robot Family source column. Family-level strings and normalized family assignments are therefore recorded in `decisions.json`, not added as a new schema field.

## Organizations created / reused

Created 18 Organization identities:

- `CNO-043` 清华大学
- `CNO-044` 中国农业大学
- `CNO-045` 河南科技学院
- `CNO-046` 深圳大学
- `CNO-047` 北京航空航天大学
- `CNO-048` 上海戏剧学院
- `CNO-049` 上海体育大学
- `CNO-050` 北京舞蹈学院
- `CNO-051` 中国戏曲学院
- `CNO-052` 北京星动纪元科技股份有限公司
- `CNO-053` 河北工业大学
- `CNO-054` 华中科技大学
- `CNO-055` 松延动力
- `CNO-056` 首都体育学院
- `CNO-057` 银河通用
- `CNO-058` 中国科学院自动化研究所
- `CNO-059` 武汉大学
- `CNO-060` 智树天成

Reused 8 existing Organization IDs: `AGIBOT`, `BIC`, `CNO-011`, `CNO-013`, `CNO-017`, `CNO-022`, `GALAXEA`, `UNITREE`.

## Team -> Organization relationships

- `CTN-062` — `university_team` -> `CNO-044`
- `CTN-216` — `university_team` -> `CNO-043`
- `CTN-265` — `company_team` -> `CNO-057`
- `CTN-279` — `company_team` -> `CNO-052`
- `CTN-119` — `joint_team_member` -> `BIC`
- `CTN-119` — `joint_team_member` -> `CNO-045`
- `CTN-118` — `joint_team_member` -> `BIC`
- `CTN-118` — `joint_team_member` -> `CNO-046`
- `CTN-150` — `joint_team_member` -> `CNO-047`
- `CTN-150` — `joint_team_member` -> `AGIBOT`
- `TR-046` — `joint_team_member` -> `CNO-048`
- `TR-046` — `joint_team_member` -> `CNO-017`
- `TR-048` — `joint_team_member` -> `CNO-049`
- `TR-048` — `joint_team_member` -> `CNO-017`
- `TR-050` — `joint_team_member` -> `CNO-049`
- `TR-050` — `joint_team_member` -> `CNO-017`
- `TR-055` — `joint_team_member` -> `CNO-050`
- `TR-055` — `joint_team_member` -> `CNO-017`
- `TR-061` — `joint_team_member` -> `CNO-022`
- `TR-061` — `joint_team_member` -> `CNO-051`
- `TR-061` — `joint_team_member` -> `CNO-017`
- `TR-068` — `joint_team_member` -> `BIC`
- `TR-068` — `joint_team_member` -> `CNO-013`
- `CTN-132` — `joint_team_member` -> `CNO-050`
- `CTN-132` — `joint_team_member` -> `AGIBOT`
- `CTN-133` — `joint_team_member` -> `CNO-050`
- `CTN-133` — `joint_team_member` -> `CNO-055`
- `CTN-278` — `joint_team_member` -> `CNO-056`
- `CTN-278` — `joint_team_member` -> `CNO-055`
- `CTN-149` — `joint_team_member` -> `CNO-050`
- `CTN-149` — `joint_team_member` -> `BIC`
- `CTN-134` — `joint_team_member` -> `CNO-047`
- `CTN-134` — `joint_team_member` -> `BIC`
- `CTN-104` — `joint_team_member` -> `CNO-047`
- `CTN-104` — `joint_team_member` -> `BIC`
- `CTN-105` — `joint_team_member` -> `CNO-047`
- `CTN-105` — `joint_team_member` -> `BIC`
- `CTN-116` — `joint_team_member` -> `BIC`
- `CTN-116` — `joint_team_member` -> `CNO-022`
- `CTN-116` — `joint_team_member` -> `CNO-047`
- `CTN-199` — `joint_team_member` -> `CNO-060`
- `CTN-199` — `joint_team_member` -> `CNO-059`
- `CTN-065` — `joint_team_member` -> `CNO-058`
- `CTN-065` — `joint_team_member` -> `AGIBOT`
- `CTN-215` — `joint_team_member` -> `CNO-043`
- `CTN-215` — `joint_team_member` -> `AGIBOT`
- `CTN-161` — `joint_team_member` -> `AGIBOT`
- `CTN-209` — `joint_team_member` -> `CNO-059`
- `CTN-209` — `joint_team_member` -> `AGIBOT`
- `CTN-157` — `joint_team_member` -> `CNO-054`
- `CTN-157` — `joint_team_member` -> `AGIBOT`
- `CTN-158` — `joint_team_member` -> `CNO-054`
- `CTN-158` — `joint_team_member` -> `AGIBOT`
- `CTN-155` — `joint_team_member` -> `AGIBOT`
- `CTN-156` — `joint_team_member` -> `AGIBOT`
- `CTN-243` — `joint_team_member` -> `AGIBOT`
- `CTN-252` — `joint_team_member` -> `AGIBOT`
- `CTN-247` — `joint_team_member` -> `CNO-043`

The three full joint-lab Organizations retain their own identities and gain `joint_lab_member` relationships to their supported constituent institutions. Their shorter labels remain separate unresolved alias candidates. Existing `affiliated_with` relationships are preserved; specific new relationships do not rewrite prior source claims.

## Robot Platforms created / reused

Created 10 Robot Platform identities:

- `CRP-006` Booster K1 — family `Booster`, manufacturer `CNO-011`
- `CRP-007` Booster T2 — family `Booster`, manufacturer `CNO-011`
- `CRP-008` Unitree H1 — family `H1`, manufacturer `UNITREE`
- `CRP-009` 灵犀X2 — family `灵犀`, manufacturer `AGIBOT`
- `CRP-010` 远征A3 — family `远征`, manufacturer `AGIBOT`
- `CRP-011` 天工3.0 — family `天工`, manufacturer `BIC`
- `CRP-012` 天轶2.0 — family `天轶`, manufacturer `BIC`
- `CRP-013` 星动L7 — family `星动`, manufacturer `CNO-052`
- `CRP-014` 小顽童 — family `小顽童`, manufacturer `CNO-055`
- `CRP-015` Galbot G1 — family `Galbot`, manufacturer `CNO-057`

Reused: `CRP-001`, `CRP-002`, `CRP-003`, `CRP-004`, `CRP-005`. Existing `CRP-002` 精灵G2 and `CRP-003` Galaxea R1 Pro gain their previously missing manufacturer relationships. The family/model mapping is review metadata and does not change the entity schema.

## Entry -> Robot Platform relationships

- `E-005-04` — `used_robot_platform` -> `CRP-005` (EV-021)

`EV-021` explicitly states that GMO Robots used Unitree G1 in 100 m, 400 m, and 1500 m; the corpus has one exact GMO Entry, the 1500 m Entry above. No Team-level platform was propagated to other Entries.

## Manufacturer / platform-provider distinctions

- GALAXEA remains organizationally separate from `DOM-002`; it is recorded as platform provider and sponsor, not Team owner.
- 加速进化 (`CNO-011`) is a platform provider for `DOM-003`, `INT-001`, and `INT-002`; technical-support relationships are retained for both international Teams.
- UNITREE is the manufacturer/provider of GMO Robots' purchased G1 platform, while GMO Robots remains affiliated with `CNO-001`.
- Platform manufacturer relationships are attached to Robot Platforms. Team affiliations are attached independently and never inferred from robot manufacture.
- Multi-Team providers: `CNO-011: DOM-003, INT-001, INT-002`
- Manufacturer platforms used by organizationally independent Teams: 7 reviewed Team cases, enumerated in `organization-robot-platform-normalization.json`.

## Joint Teams

29 Teams have at least one newly reviewed `joint_team_member` relationship. Multi-party source strings retain every supported Organization. Partial mappings are intentional where a joint label also contains an unresolved abbreviation; no synthetic combined Organization was created.

## Aliases resolved

- Organization aliases: 12; Robot Platform aliases: 17.
- Every decision retains the raw label, normalized display label, and canonical ID in `decisions.json`.
- The visibly malformed `者北京星动纪元科技股份有限公司` source string maps to `CNO-052`; the raw source row is unchanged.

## Aliases unresolved / unsupported relationships left unknown

- Organization: `巴西多所大学RoboCup团队` — consortium wording does not identify each university
- Organization: `澳大利亚三所高校` — consortium wording does not identify each university
- Organization: `养老护理机器人联合实验室 / 养老护理机器人联合实验室（河北工业大学-北京人形机器人创新中心）` — short and expanded labels may denote the same lab, but identity continuity is not explicit
- Organization: `工业具身智能机器人联合实验室 / 工业具身智能机器人联合实验室（华中科技大学-北京人形机器人创新中心）` — short and expanded labels may denote the same lab, but identity continuity is not explicit
- Organization: `情感智能应用联合实验室 / 情感智能应用联合实验室（北京大学-北京人形机器人创新中心）` — short and expanded labels may denote the same lab, but identity continuity is not explicit
- Organization: `北京松延动力深饪餐饮有限公司 / 松延动力` — malformed-looking legal name is not silently merged with the manufacturer label
- Organization: `荣耀 / 上海荣耀 / 深圳荣耀 / 北京荣耀` — generic brand evidence does not establish a parent or subsidiary relationship
- Organization: `智元 / 智元创新（城市）公司 / 北京智元新创技术有限公司` — brand similarity does not establish corporate ownership or subsidiary relationships
- Organization: `华工、同济、上交、苏大、计算所、国科大、湖北人形、荔枝` — abbreviated joint-team labels are insufficient for new canonical identities
- Robot Platform: `Q5` — Evidence explicitly scopes it to WRC, not WHRG
- Robot Platform: `夸父(Kuavo)` — platform evidence is not linked to a WHRG Team or Entry
- Robot Platform: `格斗机器人“豆汁”“卤煮”` — named robot instances are not established as reusable platform models
- Robot Platform: `OmniHand` — dexterous-hand component is not normalized as a Robot Platform
- Robot Platform: `松延 N2 / 松延 E1` — no canonical Evidence in the current corpus supports these review targets

These cases remain unknown rather than being merged through brand similarity, abbreviated naming, sponsorship, manufacturer identity, or platform provision. No Organization ownership, subsidiary relationship, Entry result, ranking, participation status, or verification status was inferred or changed.

## QA

The normalization state hashes every added and updated record, protects Entry verification/participation/result/ranking fields, and is covered by positive and mutation-control tests. Repository validators, import and archive controls, frozen-v2.1 and checkpoint audits, unit tests, strict MkDocs, PDF generation, and Git whitespace checks are run before commit; the final command results are reported with the commit.
