# Positive factual prose audit

Review date: 2026-10-28

Scope: all ten public Markdown pages (`docs/index.md`, Chapters 1–8, and `docs/appendix.md`). The audit distinguishes rhetorical negation from negative evidence that changes the factual interpretation. “Original wording” records the pre-pass wording where a sentence changed and the reviewed current wording where it did not.

| File | Original wording | Classification | Action | Revised wording |
|---|---|---|---|---|
| `docs/index.md` | 本報告が問うのは、こうした競技が何を測り、その結果を支えた技術・組織・運営がどう接続され、さらに大会後へ残るデータが第三者にとって実際に使える成果になっているのか。 | META-REPORT LANGUAGE | Rewrite | 本報告は、51種目の競技内容と評価指標、競技結果、参加チームとロボットプラットフォーム、運営基盤、2,500時間超の大会データセット、その公開状況を整理する。 |
| `docs/index.md` | 実人数・延べ人数などの集計方法は示されていない。 | LEGITIMATE NEGATIVE FACT | Retain | 実人数・延べ人数などの集計方法は示されていないため、出典を伴う報道値として扱う。 |
| `docs/index.md` | 主催者認定の来場者総数は確認できていない。 | LEGITIMATE NEGATIVE FACT | Retain | Unchanged. The negative fact limits the attributed spectator figure. |
| `docs/index.md` | 六大陸16か国から666チーム、2,056台のロボットが集まり、5日間に51種目、1,301試合・試技を実施した。 | DIRECT FACT — OK | Retain | Unchanged. |
| `docs/ch01.md` | WHRG 2026は、同じ会場で多数のロボットを走らせるだけの大会ではない。 | RHETORICAL NEGATION | Rewrite | WHRG 2026は、666チームと2,056台のロボットが、競技部門30種目と実環境タスク部門21種目に参加した大会である。 |
| `docs/ch01.md` | 主催側が共有したのは規則と競技面だけではない。 | RHETORICAL NEGATION | Rewrite | 規則、訓練予約、共通機体、充電、保管、修理、ネットワーク、結果公告は、2,056台を同じ日程で運用する基盤を構成した。 |
| `docs/ch01.md` | 21は大会プログラムの種目数であり、データセットの「12の応用場面」は利用・学習向けの別分類である。 | NECESSARY COMPARISON | Move | Chapter 1 now states only the 21 competition events. The denominator comparison appears in Chapters 3 and 6, where each taxonomy is explained. |
| `docs/ch01.md` | 以後はこの全体構造を繰り返さず、第2章で……追う。 | META-REPORT LANGUAGE | Rewrite | 参加主体、機体、運用方式を分けることで、公式チームの成績とメーカー・機体系列の集計を異なる指標として比較できる。 |
| `docs/ch01.md` | 5対5大型サッカーでは全チームがBooster T2を使用した。 | DIRECT FACT — OK | Retain | Unchanged. |
| `docs/ch02.md` | 30の競技部門は、速く動くだけでなく、曲がる、止まる、相手へ反応する……能力を別々の規則で測った。 | RHETORICAL NEGATION | Rewrite | WHRG 2026の競技部門は、陸上・跳躍、球技、格闘・力競技、体操・ダンス・武術など30種目で構成された。 |
| `docs/ch02.md` | 本章は代表種目を開始から終了まで追い、最後に……見取図を示す。 | META-REPORT LANGUAGE | Rewrite | 代表種目の課題、運用方式、採点・勝敗条件、代表結果、工学的能力に続き、実環境タスクを含む全51種目を一覧化する。 |
| `docs/ch02.md` | 試合中の遠隔操作はない。 | LEGITIMATE NEGATIVE FACT | Retain | Unchanged. It specifies the operating mode of the named event. |
| `docs/ch02.md` | リレーはバトンを渡さない方式である。 | LEGITIMATE NEGATIVE FACT | Retain | Unchanged. It defines the event mechanics. |
| `docs/ch02.md` | 全51種目は、単機の運動性能から複数機協調、長時間の実作業、指先精度までを異なる条件で記録した。 | DIRECT FACT — OK | Retain | Unchanged. |
| `docs/ch03.md` | 代表七例を、単なる種目紹介ではなく実装上の連鎖として先に示す。 | RHETORICAL NEGATION | Rewrite | 次の七例は、環境、作業列、主な知覚・操作、結果、ボトルネックを対応づける。 |
| `docs/ch03.md` | 一種類の把持を繰り返すだけでは終わらない。 | RHETORICAL NEGATION | Rewrite | 硬さの異なる対象を選び、折り、封入する操作を同じ工程へつなぐ。 |
| `docs/ch03.md` | 21は大会プログラムの種目数であり、データセットの12の応用場面とは別の分類である。 | NECESSARY COMPARISON | Retain | Unchanged. The two denominators describe different taxonomies. |
| `docs/ch03.md` | 公開資料でアルゴリズムやセンサ構成を確認できない例の方式は「未確認」である。 | LEGITIMATE NEGATIVE FACT | Retain | Unchanged. |
| `docs/ch03.md` | 電気自動車充電は西広場で、30分以内に3台を順に扱った。 | DIRECT FACT — OK | Retain | Unchanged. |
| `docs/ch04.md` | WHRGの結果は一つの総合順位ではなく……重要なのは数字を並べることではなく……である。 | RHETORICAL NEGATION | Rewrite | WHRGの結果は、時間、距離、重量、得点、審査点、試合の勝敗という複数の指標で示される。 |
| `docs/ch04.md` | 1500 mの2分21秒64は、瞬間的な出力ではなく、周回中に……管理した結果である。 | RHETORICAL NEGATION | Rewrite | 1500 mの2分21秒64は、周回中に姿勢制御を維持しながら駆動系の熱と電力を管理した結果である。 |
| `docs/ch04.md` | 公開資料は優勝機の熱設計、電力配分、冷却方式までは示していない。 | LEGITIMATE NEGATIVE FACT | Retain | Unchanged. The result cannot establish an undisclosed mechanism. |
| `docs/ch04.md` | 大会全体を一つの倍率で表す指標ではない。 | NECESSARY COMPARISON | Retain | Unchanged. It bounds the cross-year table to compatible events. |
| `docs/ch04.md` | 大型100 mを制したTiangong Ultraは、予選9.39秒、準決勝8.86秒、決勝8.64秒と大会中に記録を詰めた。 | DIRECT FACT — OK | Retain | Unchanged. |
| `docs/ch05.md` | 666チームと2,056台が同じ大会で競うには、個々のロボット性能だけでなく……が必要になる。 | RHETORICAL NEGATION | Rewrite | 666チームと2,056台が競うため、機体の導入・搬入経路、規則、訓練、充電、修理、結果記録が整えられた。 |
| `docs/ch05.md` | ここで比較しているのは企業の総合力ではなく……接続の型である。 | META-REPORT LANGUAGE | Rewrite | 五つの事例は、「機体を渡す」「競技ソフトウェアを移す」「大学が制御を実装する」「現場で反復調整する」という接続の型を示す。 |
| `docs/ch05.md` | 製品名だけでは、誰が認識、計画、制御、競技調整を担ったかは分からない。 | RHETORICAL NEGATION | Rewrite | 表は、製品提供、大学側の制御実装、競技調整の役割を分けて示す。 |
| `docs/ch05.md` | この記述は一観察者が確認した会場運用であり、全チームの運営統計ではない。 | LEGITIMATE NEGATIVE FACT | Retain | Unchanged. It limits the scope of field observation. |
| `docs/ch05.md` | 端末間遅延を30ミリ秒以内に抑えたとしている。 | DIRECT FACT — OK | Retain | Unchanged and attributed to the operator's post-event report. |
| `docs/ch06.md` | 成功した最終動作だけでなく、失敗、境界条件、長い作業列、動的な外乱までを含む。 | RHETORICAL NEGATION | Rewrite | 成功例、失敗例、境界条件、長い作業列、動的な外乱を含むと説明されている。 |
| `docs/ch06.md` | 訓練を含む点は重要である。 | META-REPORT LANGUAGE | Rewrite | 準備・訓練段階の記録には、方策の改善途中、調整に失敗した条件、反復時のばらつきが残る。 |
| `docs/ch06.md` | 12の応用場面と、競技プログラムの21の実環境タスク種目は異なる分類である。 | NECESSARY COMPARISON | Retain | Unchanged. |
| `docs/ch06.md` | 同期・ラベル・エピソード構造が実ファイルに実装済みかは確認できていない。 | LEGITIMATE NEGATIVE FACT | Retain | Unchanged. |
| `docs/ch06.md` | 規模は、12の応用場面、44種類の作業、100種類超の技能、1万件超の詳細タスクである。 | DIRECT FACT — OK | Retain | Unchanged. |
| `docs/ch07.md` | 比較対象は、データ内容や品質の優劣ではなく、配布の仕組みを見るために選んだ。 | RHETORICAL NEGATION | Rewrite | 比較対象は、配布の仕組みを確認する目的で選んだ。データ内容や品質の順位比較は対象外とする。 |
| `docs/ch07.md` | 共通しているのは、宣言の強さではなく、利用者が次の操作へ進めることだ。 | RHETORICAL NEGATION | Rewrite | これらの配布方式は、利用者が内容確認から取得、検証、引用へ進む操作経路を備える。 |
| `docs/ch07.md` | 第三者が再現できるWHRG 2026データセットの公開取得経路は確認できていない。 | LEGITIMATE NEGATIVE FACT | Retain | Unchanged. This is the dated access conclusion. |
| `docs/ch07.md` | 発表済みと取得可能は別の運用段階である。 | NECESSARY COMPARISON | Retain | Unchanged. |
| `docs/ch07.md` | 公式入口から具体的なファイルを選び、取得し、発表された2,500時間超のどの範囲かを照合する段階へは進めていない。 | DIRECT FACT — OK | Retain | Unchanged as a bounded audit result. |
| `docs/ch08.md` | 第1回から第2回への変化は、記録更新だけでは捉えられない。 | RHETORICAL NEGATION | Rewrite | 第1回から第2回にかけて、競技日程、参加規模、仕事を扱う種目、訓練・整備設備、データ化、大会後の研究・教育計画が同時に広がった。 |
| `docs/ch08.md` | 2026年は競技日程が3日間から5日間へ延びた。 | NECESSARY COMPARISON | Retain | Unchanged. The 2025 opening date is separately stated. |
| `docs/ch08.md` | 発表段階と運用確認済みは、将来構想と実績を分ける別の状態である。 | NECESSARY COMPARISON | Retain | Unchanged. |
| `docs/ch08.md` | 第三者によるデータ取得、設置先での機体利用、施設の供用開始は確認できていない。 | LEGITIMATE NEGATIVE FACT | Retain | Unchanged. |
| `docs/ch08.md` | 100 mの加速、1500 mの持久性、サッカーの複数機協調、家庭内サービスの割込み復帰、粉末計量の微細操作は、異なる成功条件と失敗モードを記録した。 | DIRECT FACT — OK | Retain | Unchanged. |
| `docs/appendix.md` | 「未確認」は結果が存在しないという意味ではなく、本調査の出典経路で確定していないことを示す。 | RHETORICAL NEGATION | Rewrite | 「未確認」は、本調査の出典経路で結果を確定できていない状態を示す。 |
| `docs/appendix.md` | 検索で見つからなかったことは永久的な不在の証明ではない。 | RHETORICAL NEGATION | Rewrite | 検索結果は監査日を伴う記録として保存する。名称変更、限定申請、後日公開の可能性があるため、未発見の状態から永久的な不在は確定できない。 |
| `docs/appendix.md` | 51種目のうち5種目で、決勝結果への直接経路が未解決である。 | LEGITIMATE NEGATIVE FACT | Retain | Unchanged. |
| `docs/appendix.md` | 重要な数字は日付、分母、単位、条件を付け、異なる定義を合算しない。 | DIRECT FACT — OK | Retain | Unchanged as an audit rule. |

## Totals

| Classification | Count | Disposition |
|---|---:|---|
| RHETORICAL NEGATION | 15 | 15 rewritten; 0 unresolved |
| LEGITIMATE NEGATIVE FACT | 11 | 11 retained with factual scope |
| NECESSARY COMPARISON | 7 | 6 retained and 1 moved to its two primary explanatory chapters |
| META-REPORT LANGUAGE | 5 | 5 rewritten as direct content |
| DIRECT FACT — OK | 10 | 10 retained |
| **Total reviewed samples** | **48** | All 10 public pages represented |

The automated positive-prose lint is narrower than this manual audit. It blocks the recurring phrase forms most likely to reintroduce rhetorical negation or chapter-process narration, while line-specific reviewed exceptions remain possible for a substantive negative fact.
