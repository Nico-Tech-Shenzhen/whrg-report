# 調査方法

## 対象と更新単位

本報告は2026年10月10日時点の canonical corpus を使う。公開ページ、公式添付資料、機関・Team・企業の発表、repository を Evidence とし、Competition、Competition Entry、Team、Organization、Robot Platform、Rule Version を別の entity として記録する。本文の集計は canonical JSON から再生成できる。

構造検証に通ることは事実確認の完了を意味しない。Evidence の publisher、title、date、URL、scope、confidence、verification status を残し、読者向け本文では内部の取込元ではなく、根拠となる公開 source を引用する。

## 中国公式アーカイブの復元

公式サイトの announcement、news、document の一覧と個別ページを追い、添付PDF、DOCX、画像への公開URLを対応付けた。2025年の規程・日程・規則変更と、2026年の規程・競技別結果を同じ方法で保存した。[[1]](#ref-1)[[2]](#ref-2) 公開ページと添付ファイルの表題が重複する場合は、同じ source の別表現として扱い、Evidence 件数をそのまま独立 claim 数とはみなさない。

## 公式添付資料と画像結果

PDF の表は競技名、組別、Team 名、結果、順位を読み取り、Competition Entry へ対応付けた。画像だけの結果は目視転記を経て、画像 source と行単位の値を保持した。公式の訂正公告がある場合は先行値を消さず、最新値と履歴を区別する。たとえば家庭シナリオ競技には決勝結果の訂正通知がある。[[3]](#ref-3)

OCR や転記の値は、画像が公式だから自動的に完全とはしない。判読困難、単位不明、同名 Team、予選・決勝の区別が曖昧な箇所は Research Lead または Unknown とする。

## Entry identity の正規化

Entry は「特定 Competition への参加」である。競技ID、Team 名、組別、結果、順位、source を組み合わせ、同じ結果行の重複取込を統合した。Team は複数 Entry にまたがるため、名称、Organization、国・地域、Robot Platform、公開説明を照合して別 entity にする。

Verified は Entry identity が現行 policy の根拠を満たす状態、Research Lead は候補として保持するが追加確認が必要な状態である。公式 source がある場合でも、そこに記載されない affiliation や manufacturer を Verified に引き上げない。

## Team・Organization・Robot の正規化

すべての356 Team と770 Entry を対象に、Organization 名、大学名、研究機関名、manufacturer、robot model、platform provider の raw string を監査した。既存 identity を優先し、根拠のある場合だけ Organization と Robot Platform を追加した。

関係は affiliation、joint team、manufacturer、provider、sponsor、technical support、robot use を別々に保持する。TEAM BRAZIL と RoboRoos の報道のように、Team 構成と Platform 支援が同時に説明される場合も混ぜない。[[4]](#ref-4) 共同 Team は複数 Organization への関係を持ち、単一の `organization_id` へ押し込まない。

## source の優先順位

公式の版付き規程・結果公告を最優先し、次に政府・大学・研究機関・Team・企業の直接発表、repository、帰属可能な報道を用いる。検索結果、出所不明の転載、非公開資料だけでは公開 claim を確定しない。公式結果の例として400メートル大型組決勝公告を参照できる。[[5]](#ref-5)

ライセンスは repository の明示表示を確認し、公開 visibility から推測しない。大会 dataset も発表記事だけでは Accessible / Downloadable / Openly Licensed に進めない。

## 方法上の主要制約

公式アーカイブは競技ごとに形式と粒度が違い、完全 roster を常に提供しない。2025年の280 Team 完全名簿は未回収である。2026年も、Entry は770件まで復元したが、主催者集計666 Team・2056台との一対一対応はできない。[[6]](#ref-6) Organization・Robot Platform リンク、開発者数、準備期間、所有、Team-level artifact は欠測が多い。

また、公開ページは更新・削除されうる。本報告は取得時点の Evidence metadata を保持するが、読者が将来同じ URL へアクセスできることを保証しない。数値は corpus 更新時に変わりうるため、本サイトを作業版として公開する。

## 参考文献

<a id="ref-1"></a>1. [世界人形机器人运动会组委会「2025世界人形机器人运动会竞赛规程」](https://www.whrgoc.com/announcements/1940613242325237760?cid=4ol61bbh)（2025年）。

<a id="ref-2"></a>2. [世界人形机器人运动会组委会「第二届世界人形机器人运动会竞赛规程总则」](https://www.whrgoc.com/documents/2072500150398033920)（2026年7月2日）。

<a id="ref-3"></a>3. [世界人形机器人运动会组委会「家庭场景—家政服务岗—决赛成绩更正通知」](https://www.whrgoc.com/resources//uploads/20260823/1787451965643042823.pdf)（2026年8月23日）。

<a id="ref-4"></a>4. [新华社「世界舞台激荡创新的回响」](http://www.xinhuanet.com/tech/20260825/80c2eff0534e49bfa2ff19ab7603fd93/c.html)（2026年8月25日）。

<a id="ref-5"></a>5. [世界人形机器人运动会组委会「第二届世界人形机器人运动会田径400米（大型组）决赛成绩公告」](https://www.whrgoc.com/resources//uploads/20260823/1787498892357039182.pdf)（2026年8月23日）。

<a id="ref-6"></a>6. [新浪财经「2056台机器人、666支队伍、16个国家」](https://finance.sina.com.cn/stock/t/2026-08-13/doc-inincxkw0113718.shtml)（組織委員会・北京市経済信息化局発表に基づく記事）。
