# Competition Entry と Team

## 770 Entry の検証状態

公開資料から再構成した Competition Entry は770件である。canonical verification は Verified 758件、Research Lead 12件で、Unresolved は0件である。この区分は Entry identity の確からしさを表す。全フィールドが独立に事実確認されたという意味ではなく、メーカー、Robot Platform、所属、順位などは個別に Unknown のまま残りうる。

公式成績公告は最も強い Entry 根拠である。たとえば公式の自由搏击80KG級公告は対戦結果を、400メートル大型組公告は順位と記録を提示する。[[1]](#ref-1)[[2]](#ref-2) ただし公告の形式は競技ごとに違い、予選だけ、決勝だけ、訂正公告あり、画像のみという場合がある。本調査の件数は公開公告から再構成できた範囲で、公式総参加数そのものではない。

## 参加状態の分布

現行データでは Finished 721、Scheduled 20、Started 10、DNS 15、DNF 2、Disqualified 2である。Finished は「競技を完了したことを確認」の意味で、メダル獲得や有効記録を意味しない。Scheduled と Started は、競技後であっても最終結果資料を回収できなかった Entry を含む。

競技別の Entry、Verified／Research Lead、Finished／その他の件数は「再構成データ集計表」で canonical JSON から自動生成する。本文には770行を転載しない。これにより、元データ更新時に表だけが古くなることを防ぐ。

## 競技間を移動する Team

744 Entry は356の正規化済み Team のいずれかにリンクする。同じ Team が陸上の複数距離、同系統のシナリオ課題、予選と別競技に現れるため、Entry 数は Team 数より多い。たとえば GMO Robots は宇树 G1 を二次開発し、100メートル、400メートル、1500メートルへ参加したと報じられた。[[3]](#ref-3) このようなケースは「同じ Team の複数 Entry」であり、三つの別 Team とは数えない。

一方、名称が似ていても自動的には同一 Team にしない。大学名と企業名を連結した共同 Team、同じメーカーの機体を使う別 Team、同一ブランドの都市別法人は、それぞれ追加根拠が必要である。Team identity の正規化では、公式結果の名称、競技ID、関連 Organization、公開説明を突き合わせた。

## 未解決 identity

26 Entry は Team ID を持たない。これは Team が存在しないという意味ではなく、公開名から既存 Team へ安全に統合できないという意味である。Organization も同様に、Entry の名称欄に文字列があっても法人・大学・共同体を一意に特定できない場合がある。

国際 Team では団体構成が記事中に要約されても、参加大学の完全一覧が示されない。TEAM BRAZIL は複数の RoboCup Team を統合したと報じられるが、canonical corpus は構成大学をすべて確定できていない。[[4]](#ref-4) RoboRoos も豪州三大学の合同 Team とされるが、三大学を推測で補っていない。[[4]](#ref-4)

## 数字の使い方

公式発表の666 Team、2056台と、本調査の356 Team、770 Entry、15 Robot Platform は異なる問いへの数字である。[[5]](#ref-5) 前者は大会全体の主催者集計、後者は公開資料から identity と関係を追跡できる分析集合である。本報告では「回収できた件数」を「大会に存在した総数」と言い換えない。

## 参考文献

<a id="ref-1"></a>1. [世界人形机器人运动会组委会「第二届世界人形机器人运动会自由搏击（80KG级）成绩公告」](https://www.whrgoc.com/resources//uploads/20260826/1787754089754034851.pdf)（2026年8月26日）。

<a id="ref-2"></a>2. [世界人形机器人运动会组委会「第二届世界人形机器人运动会田径400米（大型组）决赛成绩公告」](https://www.whrgoc.com/resources//uploads/20260823/1787498892357039182.pdf)（2026年8月23日）。

<a id="ref-3"></a>3. [新华网転載記事「冰丝带赛场大考：举重接力齐登场」](https://www.sohu.com/a/1067713181_120093108)（2026年8月26日）。

<a id="ref-4"></a>4. [新华社「世界舞台激荡创新的回响」](http://www.xinhuanet.com/tech/20260825/80c2eff0534e49bfa2ff19ab7603fd93/c.html)（2026年8月25日）。

<a id="ref-5"></a>5. [新浪财经「2056台机器人、666支队伍、16个国家」](https://finance.sina.com.cn/stock/t/2026-08-13/doc-inincxkw0113718.shtml)（組織委員会・北京市経済信息化局発表に基づく記事）。
