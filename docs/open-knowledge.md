# データは実際に使えるのか

## 監査結論

WHRG 2026の閉幕時、データセットは「即日、組織委員会を通じて社会へ無償開放する」と発表された。[[1]](#ref-1) しかし2026年10月10日時点で、本調査が監査した公式・公開情報からは、第三者が2500時間超のデータセットを取得するための検証可能な公開入口を確認できなかった。

| State | WHRG dataset |
| --- | --- |
| Announced | Yes（2026-08-26） |
| Access Route Identified | No |
| Accessible | Not verified |
| Downloadable | Not verified |
| License Identified | No |
| Openly Licensed | No |

監査で確認できなかったのは、次の要素である。

- landing page
- download URL
- application/request route
- data manifest
- version
- checksum
- license / terms
- API

これは不存在の証明ではない。公開情報の検索範囲と監査日を付けた **Announced + Audited Not Found** という状態であり、「dataset is not public」とは断定しない。

## 何を監査したか

今回届けられた監査は、公式WHRGサイトの公告・新聞・文件、共同発表7主体の公開チャネル、ModelScope、Hugging Face、OpenI、Gitee、GitHub、GitCode、網盤、閉幕式画像中のQR候補、中国語・英語の名称検索を対象とした。公式サイトは2026年9月の保存済み基準と2026年10月10日の全件取得を比較し、新しい取得案内を確認できなかった。

検索ログは不在を永久に証明しない。後日ページが公開される、非公開申請経路がある、名称が異なる可能性は残る。そのため結論は監査日付きで更新する。

## RoboMIND・AgiBot Worldとの運用比較

RoboMINDとAgiBot Worldは、同じembodied AI dataの領域で、第三者が取得条件を具体的に確認できる比較対象である。両者をWHRGデータセットの構成要素として扱う証拠はない。北京人形机器人创新中心や智元机器人が複数プロジェクトに関わることも、データ集合の包含関係を意味しない。

| 公開要素 | WHRG大会データ | RoboMIND | AgiBot World |
| --- | --- | --- | --- |
| landing page | 未確認 | あり | あり |
| download mechanism | 未確認 | Hugging Face / ModelScope | Hugging Face（gated） |
| dataset description / schema | 未確認 | data card、HDF5/LeRobot toolchain | WebDataset/LeRobot、task・observation説明 |
| license | 未確認 | Apache-2.0表示 | CC BY-NC-SA 4.0、非商用 |
| version / release information | 未確認 | V1.0→V2.0 | Alpha→Beta→2026段階公開 |

RoboMINDはプロジェクトサイトとrepository、配布先、version、data cardを持つ。[[2]](#ref-2) AgiBot Worldは公式サイトとHugging Face配布、community licenseの同意手順、段階的release情報を持つ。[[3]](#ref-3)[[4]](#ref-4) これは品質や価値の順位ではなく、取得・権利・版を第三者が操作的に確認できるかという差である。

## 再利用可能と判断するために必要なもの

WHRGデータセットの内容を検証し、研究や製品開発で再利用するには、少なくとも次の情報が必要である。

1. 永続的なlanding pageと入手手順
2. version付きmanifest、file size、checksum
3. 12場面・44作業・skill・taskの対応表
4. robot、sensor、frequency、format、annotation schema
5. Team・機体・期間別の収録範囲と「全量」の定義
6. privacy、portrait、competition participant consentの扱い
7. training、evaluation、commercial use、redistributionを定めるlicense/terms
8. correction、withdrawal、version updateの履歴

「無料」は利用権を定めるlicenseではない。URLから見えること、downloadできること、再配布・改変できること、研究結果を再現できることは別々に確認する。

## 大会周辺の公開resource

WHRG参加機体に関連するBICMap-Python、AgibotのURDF・simulation、Unitree SDKなどには明示的licenseを持つ公開repositoryがある。[[5]](#ref-5)[[6]](#ref-6) ただし、これらはRobot Platform一般のresourceであり、WHRG 2026の競技コード、Team model、または2500時間超の大会データそのものとは限らない。公開Platform resourceの存在を、大会データの公開状態へ代入しない。

## 参考文献

<a id="ref-1"></a>1. [南方网「全量数据集即日起通过组委会免费向社会开放」](https://news.southcn.com/node_47a8059d6c/d8963aabba.shtml)（2026年8月26日）。

<a id="ref-2"></a>2. [RoboMIND公式repository](https://github.com/x-humanoid-robomind/x-humanoid-robomind)（project、dataset card、配布先・license情報）。

<a id="ref-3"></a>3. [AgiBot World公式サイト](https://agibot-world.com)（dataset説明・配布案内）。

<a id="ref-4"></a>4. [智元机器人「AGIBOT WORLD 2026开源」](https://www.agibot.com.cn/article/315/detail/148.html)（2026年4月7日、段階的release）。

<a id="ref-5"></a>5. [Open-X-Humanoid「BICMap-Python」](https://github.com/Open-X-Humanoid/BICMap-Python)（MIT表示）。

<a id="ref-6"></a>6. [Unitree Robotics「unitree_sdk2」](https://github.com/unitreerobotics/unitree_sdk2)（BSD-3-Clause表示）。
