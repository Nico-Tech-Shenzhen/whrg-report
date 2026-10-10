# 残る調査課題

## Team identity の残件

770 Competition Entry のうち26件は Team ID を確定できていない。同名・類似名、競技ごとの短縮表記、共同名の一部省略を、文字列一致だけで統合しないためである。次の改善には、公式登録 roster、Team 自身の参加記録、Organization が公開する構成員情報が必要になる。

## Organization 関係の空白

Organization 関係を確認できた Team は88／356である。残る268 Team が無所属という意味ではない。結果公告は Team 名と成績を示しても、所属法人・大学を示さないことが多い。公式発表の666 Team 全体に対しても Organization coverage を計測できていない。[[1]](#ref-1)

未解決 alias には、ブラジルの複数大学、豪州三大学、联合实验室の短縮名、荣耀・智元のブランド名と都市別法人、略称だけの大学・研究機関がある。法人関係や同一性が明示されるまで Unknown を維持する。

## Robot Platform の空白

正規化した Robot Platform は15件だが、Entry へ直接リンクできたのは5／770、Team の使用関係を確認できたのは12／356である。これは15機種しか使われなかったという意味ではない。公式結果が Robot model を記載しない競技が多く、報道の複合表記から個別機種を安全に分けられない場合もある。

Q5 は現 Evidence が別大会を指し、Kuavo は WHRG Team／Entry とのリンクが未確認である。豆汁・卤煮は個体名か再利用可能 model か不明、OmniHand は hand component、松延 N2／E1 は現 corpus に裏付けがないため Robot Platform identity を作っていない。

## 2025年参加者一覧の欠落

2025年の公式総数は16か国、280 Team、500台超と確認できる。[[2]](#ref-2) しかし280 Team の完全な公式 roster は未回収である。このため2025→2026の個別継続率、新規 Team 数、退出 Team 数、Platform 移行を計算できない。公式日程・結果から部分 roster を作ることと、完全 roster を回収したと主張することを分ける。

## Dataset の取得と権利

WHRG 2026 全量 dataset は発表され、内容規模も報じられた。[[3]](#ref-3) しかし canonical Evidence では、公式 landing page、download URL、manifest、version、checksum、license を確認できていない。今後は実体の Accessible / Downloadable を検証し、利用条件を原文で確認する必要がある。「無料開放」という報道だけで Open Data としない。

## 不完全な競技 source coverage

51 Competition すべてに同じ種類の source が揃っているわけではない。決勝結果だけ、予選だけ、訂正公告あり、画像だけ、日程だけという差がある。公式の規程総則は全体構造を与えるが、個別 Entry の完了状態を埋めない。[[4]](#ref-4) Scheduled 20件、Started 10件について最終結果 source を追加探索する余地がある。

## 再利用を測る指標

中央の研究問いに答えるには、接続の存在だけでなく、その後の再利用を測る必要がある。必要な指標は、共通 Robot Platform 上の成果移転、Team 間で再利用された code / model / data、訓練施設の利用、競技後の共同研究、公開 artifact の版と license、第三者による reproduction である。

現在確認できるのは、公式訓練、機体提供、技術支援、共同 Team、Platform-related repository、大会 dataset の発表である。公式訓練通知は制度の存在を示すが、利用成果までは示さない。[[5]](#ref-5) 次版では「存在」「利用」「公開」「再利用」を別々に記録する。

## 参考文献

<a id="ref-1"></a>1. [新浪财经「2056台机器人、666支队伍、16个国家」](https://finance.sina.com.cn/stock/t/2026-08-13/doc-inincxkw0113718.shtml)（組織委員会・北京市経済信息化局発表に基づく記事）。

<a id="ref-2"></a>2. [北京市政府「2025 WHRG: 16 countries, 280 teams, 500+ robots」](https://www.beijing.gov.cn/ywdt/gqrd/202508/t20250811_4170832.html)（2025年8月11日）。

<a id="ref-3"></a>3. [新华社「全球首个世界级人形机器人运动会全量数据集」](https://www.xinhuanet.com/20260827/a1e362cfbe29446b9ac685d91f183d76/c.html)（2026年8月27日）。

<a id="ref-4"></a>4. [世界人形机器人运动会组委会「第二届世界人形机器人运动会竞赛规程总则」](https://www.whrgoc.com/documents/2072500150398033920)（2026年7月2日）。

<a id="ref-5"></a>5. [世界人形机器人运动会组委会「关于组织开展第二届世界人形机器人运动会官方训练的通知」](https://www.whrgoc.com/announcements/2088592011449540608?cid=4ol61bbh)（2026年8月15日）。
