# 開かれた知識と再利用可能性

## 二つの開放水準

イベント水準の開放とは、規程、成績、訓練機会、大会データが参加者や社会に提供されることを指す。Team 水準の開放とは、個々の Team がコード、モデル、学習データ、設計、実験手順を再利用可能な条件で公開することを指す。前者が存在しても後者は自動的に成立しない。

本調査は各 Resource を **Announced → Accessible → Downloadable → Openly Licensed** の四段階で見る。Announced は発表だけ、Accessible は閲覧先を確認、Downloadable は実体を取得可能、Openly Licensed は明示的ライセンスで再利用権を確認した状態である。「無料」「公開」「GitHub にある」は Openly Licensed の同義語ではない。

さらに WHRG との関係を **Direct / Competition-related / Platform-related / Organization-related / Unconfirmed** に分ける。WHRG 公式資料そのものは Direct、競技参加を説明する Team 記事は Competition-related、使用プラットフォーム一般の SDK は Platform-related、参加 Organization の別プロジェクトは Organization-related、関係を確認できないものは Unconfirmed とする。

## 大会が発表した全量データセット

新华社は、複数機関が世界級人形ロボット競技会の「全量データセット」を共同発表し、多視点映像、関節運動、本体状態、タスク結果、失敗例、意味ラベル、長時間操作軌跡などを含むと報じた。[[1]](#ref-1) 別報道は2500時間超、12の応用場面、44作業、100超の skill、1万超の細分化 task と説明する。[[2]](#ref-2)

| 対象 | Announced | Accessible | Downloadable | Openly Licensed | WHRG Relation |
| --- | --- | --- | --- | --- | --- |
| WHRG 2026 全量データセット | 確認 | 取得先未確認 | 未確認 | 未確認 | Direct |

したがって本報告は、内容規模を「発表された値」として記すが、データが実際に配布されている、第三者がダウンロードできる、Open Data であるとは書かない。利用規約、バージョン、永続URL、ファイル manifest が確認できるまで評価は Announced にとどまる。

## Team 水準のコード・モデル・データ

現在の canonical Evidence からは、770 Entry 全体について Team 固有のコード、モデル、データ、文書を網羅的に対応付けられない。Team 名と同名の repository があっても、競技に使った commit やモデルである証拠が必要である。Team-level openness の欠測を、非公開と判定してはならない。

大会成績公告、規程、予約訓練通知は Accessible / Downloadable な competition artifact であるが、通常はソフトウェア・データの再利用ライセンスを示さない。[[3]](#ref-3) 公開資料として引用できることと、内容を自由に再配布・改変できることを分ける。

## Robot Platform の公開資源

WHRG で使用が確認されたメーカー・Platform に関連する repository には、明示的ライセンスを持つものがある。ただし、これらは主として Platform-related であり、WHRG 競技コードそのものとは限らない。

| Resource | 確認したライセンス | WHRG Relation |
| --- | --- | --- |
| BICMap-Python | MIT | Platform-related |
| agibot_x2_urdf | Mulan PSL v2 | Platform-related |
| A3_Ultra_usd | Mulan PSL v2 | Platform-related |
| genie_sim | MPL 2.0 | Platform-related |
| Unitree SDK2 | BSD-3-Clause | Platform-related |
| unitree_rl_gym | BSD-3-Clause | Platform-related |
| unitree_sim_isaaclab | Apache-2.0 | Platform-related |
| roboto_origin | GPL-3.0 | Organization-related |

BICMap-Python は repository 上で MIT を、智元の URDF / USD 資源は Mulan PSL v2 を示す。[[4]](#ref-4)[[5]](#ref-5) genie_sim は原則 MPL 2.0 と記載する。[[6]](#ref-6) Unitree の SDK、強化学習、Isaac Lab 関連 repository はそれぞれ BSD-3-Clause、BSD-3-Clause、Apache-2.0 を明示する。[[7]](#ref-7)[[8]](#ref-8)[[9]](#ref-9)

一方、公開 repository でも license file を確認できない agibot_x1_train は Openly Licensed としない。[[10]](#ref-10) Galaxea G0.5 の Community License は名称だけで一般的な Open Source license と同等と判断せず、条項の追加確認が必要である。[[11]](#ref-11)

## 競技・組織に関係する artifact

公式規程、結果PDF、画像公告、訓練通知は Direct な大会 artifact である。大学・企業の記事、研究室紹介、製品ページは Competition-related または Organization-related になりうる。これらは Team formation や支援関係を説明できるが、公開コードやデータの存在を代替しない。

現段階の慎重な結論は、WHRG 周辺に再利用可能な Platform resource が複数存在し、大会側も大規模 dataset を発表した一方、Team-level artifact と大会 dataset の取得・権利・版の確認は不足している、というものである。

## 参考文献

<a id="ref-1"></a>1. [新华社「全球首个世界级人形机器人运动会全量数据集」](https://www.xinhuanet.com/20260827/a1e362cfbe29446b9ac685d91f183d76/c.html)（2026年8月27日）。

<a id="ref-2"></a>2. [新浪财经「数据集包含2500+小时数据、12个场景、44项作业」](https://finance.sina.com.cn/jjxw/2026-08-27/doc-inipsrra0621740.shtml)（2026年8月27日）。

<a id="ref-3"></a>3. [世界人形机器人运动会组委会「关于发布第一批赛项规则的公告」](https://www.whrgoc.com/announcements/2067566603371487232?cid=4ol61bbh)（2026年）。

<a id="ref-4"></a>4. [Open-X-Humanoid「BICMap-Python」](https://github.com/Open-X-Humanoid/BICMap-Python)（MIT 表示を確認）。

<a id="ref-5"></a>5. [AgibotTech「agibot_x2_urdf」](https://github.com/AgibotTech/agibot_x2_urdf)（Mulan PSL v2 表示を確認）。

<a id="ref-6"></a>6. [AgibotTech「genie_sim」](https://github.com/AgibotTech/genie_sim)（MPL 2.0 表示を確認）。

<a id="ref-7"></a>7. [Unitree Robotics「unitree_sdk2」](https://github.com/unitreerobotics/unitree_sdk2)（BSD-3-Clause 表示を確認）。

<a id="ref-8"></a>8. [Unitree Robotics「unitree_rl_gym」](https://github.com/unitreerobotics/unitree_rl_gym)（BSD-3-Clause 表示を確認）。

<a id="ref-9"></a>9. [Unitree Robotics「unitree_sim_isaaclab」](https://github.com/unitreerobotics/unitree_sim_isaaclab)（Apache-2.0 表示を確認）。

<a id="ref-10"></a>10. [Gitee「agibot_x1_train」](https://gitee.com/mywisdomcode/agibot_x1_train)（明示的 LICENSE 未確認）。

<a id="ref-11"></a>11. [GalaxeaAI「Galaxea-G0.5」](https://github.com/GalaxeaAI/Galaxea-G0.5)（Community License、条項要確認）。
