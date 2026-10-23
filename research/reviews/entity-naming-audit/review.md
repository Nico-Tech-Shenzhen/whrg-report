# Entity naming audit

Review date: 2026-10-23

## Decision rule

Reader-facing prose uses one stable name for one entity. A verified public English or international brand is the default for a company or brand. Organizations without a suitable brand use a natural Japanese organization name. Product and platform names remain distinct from manufacturers, official competition team names remain in their official form where results depend on that identity, and legal names appear only when legal identity is the subject. Source titles, quotations, URLs, identifiers and marked official names retain source text.

## Audit

| Raw form | Entity identity | Type | Canonical public form | Files found before correction | Replacement decision | Evidence |
|---|---|---|---|---|---|---|
| 加速进化／加速進化／Booster | Beijing Booster Robotics Technology Co., Ltd. public brand | company / brand | Booster Robotics | `docs/ch05.md` (company), `docs/ch01.md`, `docs/ch02.md`, `docs/ch04.md`, `docs/ch05.md` (product family) | Company references become Booster Robotics. Product references use Booster T2. Bare Booster is allowed only inside a product name. | Existing terminology audit `B-Proper Nouns!A6:H6`; Booster Robotics official “About us” identifies 加速进化（Booster Robotics） and Booster T2. |
| Booster T2 | T2 humanoid platform | product / platform | Booster T2 | `docs/ch01.md`, `docs/ch02.md`, `docs/ch04.md`, `docs/ch05.md` | Keep. First ecosystem use may state “Booster RoboticsのBooster T2”. | Booster Robotics official product/history pages; Tsinghua University football report. |
| 智元机器人／智元ロボティクス／智元 | AGIBOT public brand | company / brand | AGIBOT | `docs/ch04.md`, `docs/ch05.md`, `docs/ch06.md`; official team names in `docs/ch03.md`, `docs/appendix.md` | Company references become AGIBOT. Do not rewrite 智元 inside marked official team names. | Existing audit `B-Proper Nouns!A3:H3`; AGIBOT official English/Japanese sites and corporate footer. |
| OmniHand O10 | AGIBOT dexterous-hand product | product | OmniHand O10 | `docs/ch05.md` | Keep product name; do not use it as company or team name. | AGIBOT official product catalog; Wuhan University case source. |
| 银河通用／銀河通用 | Galbot public identity | company / brand | Galbot | `docs/ch04.md`, `docs/ch06.md`; official team names in `docs/ch03.md`, `docs/appendix.md` | Company references become Galbot. Preserve 北京银河星数 as a marked official team name. | Existing audit `B-Proper Nouns!A4:H4`; Galbot official site and About page. |
| Galbot G1 | Galbot robot model | product / platform | Galbot G1 | research records; added only where a source identifies the model | Keep distinct from Galbot company and 北京银河星数 team. | Galbot official site; canonical platform review. |
| 宇树科技／宇樹科技／Unitree | Unitree public brand | company / brand | Unitree Robotics | `docs/ch04.md`, `docs/ch05.md`, `docs/ch07.md` | Company references become Unitree Robotics. Unitree alone remains only in official repository/dataset names or URLs. | Existing audit `B-Proper Nouns!A5:H5`; Unitree Robotics official site. |
| Unitree G1 | G1 humanoid platform | product / platform | Unitree G1 | `docs/ch05.md` | Keep. GMO Robots remains the team/operator, not a Unitree Robotics team. | Unitree Robotics official G1 page; GMO case source and canonical relationship review. |
| 北京人形机器人创新中心／北京人形 | Beijing Humanoid Robot Innovation Center organization | organization | 北京人型ロボットイノベーションセンター | `docs/ch04.md`, `docs/ch05.md`, `docs/ch06.md`; official team names in `docs/ch03.md`, `docs/appendix.md` | Use the Japanese organization name when the institution is the actor. Preserve 北京人形 inside marked official team names. Do not collapse the organization into X-Humanoid. | Existing audit `B-Proper Nouns!A2:H2`; organization-controlled About page. |
| X-Humanoid | public English identity/site identity of the center | brand / site identity | X-Humanoid | `docs/ch07.md` in RoboMIND account name | Keep only where the brand/account identity is the subject. | X-Humanoid official About page and official domain. |
| 天工／Tiangong／Tien Kung | robot family developed by the center | product family | Tiangong | `docs/ch03.md`, `docs/ch04.md`, `docs/ch05.md`, `docs/appendix.md` | Product prose uses Tiangong; exact official team names such as 天工 remain marked and unchanged. | X-Humanoid official Tiangong launch/product pages. |
| 天工Ultra／Tiangong Ultra | high-performance Tiangong model | product / platform | Tiangong Ultra | research records; added to Chapters 4–5 where model is evidenced | Use model name, not the organization or family name, for model-specific results. | X-Humanoid official WHRG result pages. |
| 星动纪元／星動紀元 | RobotEra public brand | company / brand | RobotEra | official team/product strings only in `docs/appendix.md` and research | Company prose becomes RobotEra if introduced. Do not rewrite source/team strings. | Existing audit `B-Proper Nouns!A8:H8`; RobotEra official domain and branded product material. |
| 星海图／星海図 | Galaxea public brand | company / brand | Galaxea | `docs/ch06.md`; official team name in `docs/appendix.md` | Company references become Galaxea. Preserve 星海图星舰队 as a marked official team name. | Existing audit `B-Proper Nouns!A9:H9`; Galaxea official About/legal pages. |
| Galaxea R1 Pro | Galaxea robot model | product / platform | Galaxea R1 Pro | canonical research only | Keep distinct from Galaxea organization and official team identity. | Canonical platform review; Galaxea official product material. |
| 松延动力／松延動力 | Noetix Robotics public brand | company / brand | Noetix Robotics | no public prose occurrence before correction | Use Noetix Robotics if introduced. | Existing audit `B-Proper Nouns!A7:H7`; Noetix Robotics official domain. |
| 优理奇／優理奇 | UniX AI public brand | company / brand | UniX AI | official team name in `docs/ch03.md`, `docs/appendix.md` | Use UniX AI for the company; preserve 优理奇黑豹队 as marked official team name. | Existing audit `B-Proper Nouns!A10:H10`; UniX AI official About page. |
| 灵心巧手／霊心巧手 | Linkerbot public company brand | company / brand | Linkerbot | company/team ambiguity in `docs/ch03.md`, `docs/ch05.md`, `docs/appendix.md` | Company actor becomes Linkerbot. Preserve 灵心巧手 only when the official result names that competition team. | Existing audit `B-Proper Nouns!A11:H11`; Linkerbot official About page. |
| Linker Hand | Linkerbot dexterous-hand product series | product | Linker Hand | `docs/ch05.md` | Keep as product name; identify Linkerbot as provider only when relevant. | Linkerbot official product page. |
| 万境千寻／千寻智能／千尋智能 | Spirit AI public brand; official team identity differs | company / brand / team | Spirit AI (company); 千寻智能 (official team only) | `docs/ch06.md`; official team in `docs/ch03.md`, `docs/appendix.md` | Company/legal-release references become Spirit AI. Preserve 千寻智能 as a marked official team name. | Existing audit `B-Proper Nouns!A13:H13`; Spirit AI official About page and registration disclosure. |
| 万境千寻（北京）科技有限公司 | legal entity associated with Spirit AI | legal entity | 万境千寻（北京）科技有限公司 | `docs/ch06.md` | Use only in a legal-identity annotation or source title, not ordinary prose. | Spirit AI official About page; unified social credit code record in existing review. |
| 荣耀／荣耀终端／宇樹系 | HONOR public brand | company / brand | HONOR | `docs/ch04.md` contains only series-level comparison; official team strings in appendix/research | Company references become HONOR. Preserve 荣耀 inside marked official team names. | Existing audit `B-Proper Nouns!A12:H12`; HONOR trademark policy and official global site. |
| 赛迪研究院 | China Center for Information Industry Development | research institute | CCID | `docs/ch06.md` | Replace raw source form; do not invent a Japanese corporate translation. | Chinese government profile states the full institution name and abbreviation CCID. |
| 北奥集团 | Beijing Beiao Group Corp., Ltd. public short identity | organization / event operator | Beiao Group | `docs/ch06.md` | Replace raw source form with verified English short identity. | Beiao Group official profile and bilingual corporate brochure. |

## Allowed-context controls

- Official competition teams remain source-accurate inside `<span lang="zh">…</span>` because the result denominator is the team, not the company or platform.
- Product names such as Booster T2, Unitree G1, OmniHand O10, Linker Hand and Tiangong Ultra are not aliases for their manufacturers.
- Source titles and quotations remain untouched.
- A legal entity may appear in a marked first-use annotation when identity is materially relevant; it is not the default public name.

## Review result

Initial status: **NEEDS EDIT**. The public report mixed public brands with Japanese-kanji renderings and raw Chinese organization names, especially in Chapters 4–6. Official team names were generally correctly marked and must not be normalized into company names.

Final status: **PASS**. `dic.md` now establishes one stable public name per entity type, Chapters 4–7 use those names, and official team/source/legal contexts remain separately marked. The terminology validator now masks verified product/resource phrases rather than exempting a brand globally. Negative controls cover a rejected company alias and allowed official-team, product, dataset-title, source-title and legal-annotation contexts.
