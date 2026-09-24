# Canonical entity normalization review

## Method

All 770 canonical Competition Entries were audited without web research or re-extraction. Raw source spelling remains in each Entry. Canonical IDs were linked only from direct canonical source fields, exact names, or the six documented alias decisions in `decisions.json`. Similar names, joint-organization strings, generic labels, measurement-like strings, and truncated strings were not silently merged.

The existing provenance rule required a source ID to equal every derived canonical entity ID. That prevented honest creation of a Team, Organization, or Robot Platform from an Entry/Team source row. Validation now permits the mismatch only for review-declared `identity_derivation` records whose source entities, exact source rows, and canonical hashes are checked by the normalization validator.

## Before and after

| Metric | Before | After |
| --- | ---: | ---: |
| Canonical records | 1355 | 1683 |
| Competition Entries | 770 | 770 |
| Teams | 75 | 356 |
| Organizations | 4 | 46 |
| Robot Platforms | 0 | 5 |
| Entries linked to Team IDs | 79 | 744 |
| Entries linked to Organization IDs | 0 | 83 |
| Entries linked to Robot Platform IDs | 0 | 4 |

Before normalization, all 770 Entries had Team Name text: 79 had a Team ID and 691 did not. Ninety-three Entries had Organization Name text without an Organization ID. Four Entries had Robot Manufacturer/Model text without a Robot Platform ID. After normalization, 26 Team-name Entries, 10 Organization-name Entries, and zero Robot-text Entries remain without the corresponding canonical ID.

Distinct normalized/source-field strings before normalization: Team Name 363/407; Organization Name 51/51; Robot Manufacturer 1/1; Robot Model 2/2.

## Team decisions

- 69 existing Team IDs are used after normalization; 281 new Team entities were created from distinguishable source names.
- Resolved aliases: `天工队` -> `TR-005`; compatibility-glyph variants of 无锡智元赛队, 北方工大博远智行-璇玑队, and 二进制齿轮 -> their existing `TR-*` IDs; `上海高奕队` -> `TR-021`; `RUC-HiLigh` -> `TR-069`.
- Alias candidates not merged: 木心铁骨/木芯铁骨; 星海图星舰队/星舰队; 啊对队/啊对对队; 北京邮电大学bbox/北邮BBOX队.
- Unlinked identities: three measurement-like strings, eleven generic `机器人战队` Entries, and twelve Entries carrying three visibly truncated long names. Verification, participation, results, and rankings remain unchanged; these are recorded as factual identity conflicts rather than rewritten.
- Exact per-name decisions and IDs are in [decisions.json](decisions.json).

## Organization and Robot Platform decisions

- Organization links use direct Organization fields. BIC, AGIBOT, and UNITREE are reused only for documented name variants. Joint/multi-party strings and one visibly malformed string remain unlinked.
- New Organization identities retain the exact source name. Platform-provider and manufacturer relationships are distinct from Team affiliation.
- Five clear Robot Platform models were created: 天工Ultra, 精灵G2, Galaxea R1 Pro, Booster T1, and 宇树 G1. Only the four Entries with explicit Robot Model text receive Entry-level Robot Platform IDs. Team hardware-support relationships do not assert Entry ownership or use.

## Duplicate Entry audit

No Entry was consolidated. The only repeated exact Team identity within one Competition is 宁夏智元赛队 in C-028; `TR-062` (58KG) and `TR-086` (40KG) remain distinct class Entries. Historical/result evidence is unchanged.

## Recent transcription import

The prior import correctly reused zero Team IDs because none of the 68 transcription Team identities existed in the canonical corpus before that import. It created those Teams and linked its 79 Entries. The remaining gap was cross-corpus normalization: older and official-archive Entries with the same supported identities had not yet been linked to the newly created `TR-*` IDs.

## Verification safety and QA

Verified/Research Lead status, Participation Status, Result, and Ranking are hash-protected and unchanged. All required QA passed: repository and import validators; four normalization, five transcription, six prior-import, seven official-archive, and six frozen-v2.1 negative controls; checkpoint audit; 43 unit tests; strict MkDocs build; PDF build; and Git diff checks.
