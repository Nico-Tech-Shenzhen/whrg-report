# WHRG 2026 Master v1 → v2 Migration Handoff

## Files

| File | SHA-256 |
|---|---|
| `WHRG_2026_Master.xlsx` | `5ba0c2de6a1afd4028ec8f797a5d81db43c572f979d1bff12277a53502d1dc3c` |
| `WHRG_2026_Master_v2.xlsx` | `e4e77e86b53c123d1d326fa8659bd99779fb2f08f6ad767c0c54d848b7a4f05c` |
| `references/master-schema-v2.md` | `9941263fcf24cac1ba8f97be450e25b6c7deba1f4ea24bc459ad4b701f8571ca` |

## Metadata

- **Migration date:** 2026-08-31
- **Source Master:** `WHRG_2026_Master.xlsx` (unchanged, read-only)
- **Candidate v2:** `WHRG_2026_Master_v2.xlsx` (frozen pending external review)
- **Sheet count before:** 16
- **Sheet count after:** 19 (+ Entry Source Map, ID Crosswalk, Schema Migration Log)

## Competition Entry Map: 35 original → 22 canonical

The original Master contained 35 data rows (plus 1 template row) in `Competition Entry Map`. After deduplication and canonicalization, v2 contains 22 canonical data rows (plus 1 template row).

| # | Original Entry ID | Competition | Team Name | Result | v2 Action | v2 Canonical Entry ID | v2 Verification Status |
|---|---|---|---|---|---|---|---|
| 1 | `[Template]` | — | `[Template]` | — | Retained | `[Template]` | `Unresolved` (fixed from `Verified`) |
| 2 | `E-005-01` | C-005 | 天卓队 | 2:21.63 | **Kept** | `E-005-01` | `Verified` |
| 3 | `E-005-02` | C-005 | 飞雷神 | 2:30.00 | **Kept** | `E-005-02` | `Verified` |
| 4 | `E-005-03` | C-005 | 风火闪电队 | 2:30.22 | **Kept** | `E-005-03` | `Verified` |
| 5 | `E-005-04` | C-005 | GMO Robots | 7:43.89 | **Kept** | `E-005-04` | `Research Lead` |
| 6 | `E-005-05` | C-005 | 北京智元素队 | DNS | **Kept** | `E-005-05` | `Research Lead` |
| 7 | `E-005-06` | C-005 | 北京灵翌队 | DNS | **Kept** | `E-005-06` | `Research Lead` |
| 8 | `E-005-07` | C-005 | 荣耀双驰战队 | 2:36.73 | **Kept** | `E-005-07` | `Verified` |
| 9 | `E-004-01` | C-004 | 天工队 | 38.15 | **Kept** | `E-004-01` | `Verified` |
| 10 | `E-004-02` | C-004 | 追风仔仔队 | 39.45 | **Kept** | `E-004-02` | `Verified` |
| 11 | `E-004-03` | C-004 | 动力队 | 39.66 | **Kept** | `E-004-03` | `Verified` |
| 12 | `E-004-04` | C-004 | 荣耀双驰战队 | 40.08 | **Kept** | `E-004-04` | `Verified` |
| 13 | `E-042-01` | C-042 | 北京人形河南科技学院计算机科学与技术学院 | Unknown | **Kept** | `E-042-01` | `Research Lead` |
| 14 | `E-042-02` | C-042 | 华工智元具行队 | Unknown | **Kept** | `E-042-02` | `Research Lead` |
| 15 | `E-042-03` | C-042 | 北京人形机器人创新中心-深圳大学联队 | Unknown | **Kept** | `E-042-03` | `Research Lead` |
| 16 | `E-036-01` | C-036 | 优理奇暗码觉醒队 | Disqualified | **Kept** | `E-036-01` | `Verified` |
| 17 | `E-040-01` | C-040 | Simbot战队 | Disqualified | **Kept** | `E-040-01` | `Verified` |
| 18 | `E-C005-01` | C-005 | 天卓队 | 2:21.63 | **Merged** into `E-005-01` | — | — |
| 19 | `E-C005-02` | C-005 | 飞雷神 | 2:30.00 | **Merged** into `E-005-02` | — | — |
| 20 | `E-C005-03` | C-005 | 风火闪电队 | 2:30.22 | **Merged** into `E-005-03` | — | — |
| 21 | `E-C005-04` | C-005 | GMO Robots | 7:43.89 | **Merged** into `E-005-04` | — | — |
| 22 | `E-C005-05` | C-005 | 北京智元素队 | DNS | **Merged** into `E-005-05` | — | — |
| 23 | `E-C005-06` | C-005 | 北京灵翌队 | DNS | **Merged** into `E-005-06` | — | — |
| 24 | `E-C005-07` | C-005 | 荣耀双驰战队 | 2:36.73 | **Merged** into `E-005-07` | — | — |
| 25 | `E-C005-08` | C-005 | 天工队 | — | **Kept** (new canonical) | `E-C005-08` | `Verified` |
| 26 | `E-B01-004-01` | C-004 | 天工队 | 38.15 | **Merged** into `E-004-01` | — | — |
| 27 | `E-B01-004-02` | C-004 | 追风仔仔队 | 39.45 | **Merged** into `E-004-02` | — | — |
| 28 | `E-B01-004-03` | C-004 | 动力队 | 39.66 | **Merged** into `E-004-03` | — | — |
| 29 | `E-B01-004-04` | C-004 | 荣耀双驰战队 | 40.08 | **Merged** into `E-004-04` | — | — |
| 30 | `E-B01-012-01` | C-012 | 旗袭者 | 11:1 | **Kept** (new canonical) | `E-B01-012-01` | `Verified` |
| 31 | `E-B01-012-02` | C-012 | 八中石景山 | 1:11 | **Kept** (new canonical) | `E-B01-012-02` | `Verified` |
| 32 | `E-B01-040-01` | C-040 | 优理奇 | 金牌 | **Kept** (new canonical) | `E-B01-040-01` | `Verified` |
| 33 | `E-B01-040-02` | C-040 | Simbot战队 | Disqualified | **Merged** into `E-040-01` | — | — |
| 34 | `E-B01-040-03` | C-040 | 北航智元联合队 | — | **Kept** (new canonical) | `E-B01-040-03` | `Verified` |
| 35 | `E-B01-036-01` | C-036 | 智元 | 金牌 | **Kept** (new canonical) | `E-B01-036-01` | `Verified` |
| 36 | `E-B01-036-02` | C-036 | 优理奇暗码觉醒队 | Disqualified | **Merged** into `E-036-01` | — | — |

## Duplicate Mappings

### 13 Confirmed Same

| Legacy ID | Canonical ID | Competition | Team Name | Result |
|---|---|---|---|---|
| `E-C005-01` | `E-005-01` | C-005 | 天卓队 | 2:21.63 |
| `E-C005-02` | `E-005-02` | C-005 | 飞雷神 | 2:30.00 |
| `E-C005-03` | `E-005-03` | C-005 | 风火闪电队 | 2:30.22 |
| `E-C005-04` | `E-005-04` | C-005 | GMO Robots | 7:43.89 |
| `E-C005-05` | `E-005-05` | C-005 | 北京智元素队 | DNS |
| `E-C005-06` | `E-005-06` | C-005 | 北京灵翌队 | DNS |
| `E-C005-07` | `E-005-07` | C-005 | 荣耀双驰战队 | 2:36.73 |
| `E-B01-004-01` | `E-004-01` | C-004 | 天工队 | 38.15 |
| `E-B01-004-02` | `E-004-02` | C-004 | 追风仔仔队 | 39.45 |
| `E-B01-004-03` | `E-004-03` | C-004 | 动力队 | 39.66 |
| `E-B01-004-04` | `E-004-04` | C-004 | 荣耀双驰战队 | 40.08 |
| `E-B01-040-02` | `E-040-01` | C-040 | Simbot战队 | Disqualified |
| `E-B01-036-02` | `E-036-01` | C-036 | 优理奇暗码觉醒队 | Disqualified |

### 1 Unresolved

| Legacy ID | Canonical ID | Status | Reason |
|---|---|---|---|
| `FP-002` | `[Unresolved]` | `Unresolved` | Referenced by entries but not found in Evidence Map. Referenced by: `E-005-04`, `E-C005-03`, `E-C005-04`, `E-C005-05`, `E-C005-06`. |

## Entries Downgraded to Research Lead

| Entry ID | Competition | Team Name | Original Evidence IDs | Downgrade Reason |
|---|---|---|---|---|
| `E-005-04` | C-005 | GMO Robots | `EV-ESM-005A,FP-002` | Contains `FP-002`, which does not exist in Evidence Map. Cannot be Verified without resolvable primary evidence. |
| `E-005-05` | C-005 | 北京智元素队 | `FP-002` | Evidence ID `FP-002` not found in Evidence Map. Field/missing evidence alone cannot support Verified status. |
| `E-005-06` | C-005 | 北京灵翌队 | `FP-002` | Same as above. |
| `E-042-01` | C-042 | 北京人形河南科技学院计算机科学与技术学院 | `EV-ESM-042` | Evidence `EV-ESM-042` is Field Evidence (`Source Type = Field`). Field Evidence alone cannot support Verified status. |
| `E-042-02` | C-042 | 华工智元具行队 | `EV-ESM-042` | Same as above. |
| `E-042-03` | C-042 | 北京人形机器人创新中心-深圳大学联队 | `EV-ESM-042` | Same as above. |

## Team Name = Organization Name Warnings

| Entry ID | Competition | Team Name / Organization Name | Warning |
|---|---|---|---|
| `E-B01-040-01` | C-040 | `优理奇` | Team Name equals Organization Name. Source data confirms single-entity team, but schema rule recommends distinguishing Team from Organization. |
| `E-B01-036-01` | C-036 | `智元` | Same as above. |

These are recorded as `WARNING` in `Schema Migration Log` and do not block migration.

## Stable IDs Preserved

All existing stable IDs in the original Master were preserved and never renumbered:

- **Evidence IDs:** `EV-001` through `EV-ESM-050`, `EV-ESM-051`, `EV-ESM-004A`, `EV-ESM-012A`, `EV-ESM-021A`, `EV-ESM-040A`–`C`, `EV-ESM-036A`–`B` — all 100 IDs retained.
- **Competition IDs:** `C-001` through `C-051` — all 51 IDs retained.
- **Entry IDs:** All canonical Entry IDs (`E-005-01` through `E-B01-036-01`) retained. Legacy duplicate IDs recorded in `ID Crosswalk`.
- **Unknown Question IDs:** `Q-001` through `Q-031` — all retained.

## IDs Removed, Merged, or Replaced

| ID | Action | Details |
|---|---|---|
| `E-C005-01` → `E-C005-07` | Merged | Duplicate of `E-005-01` → `E-005-07`. Recorded in `ID Crosswalk` as `Confirmed Same`. |
| `E-B01-004-01` → `E-B01-004-04` | Merged | Duplicate of `E-004-01` → `E-004-04`. Recorded in `ID Crosswalk`. |
| `E-B01-040-02` | Merged | Duplicate of `E-040-01`. Recorded in `ID Crosswalk`. |
| `E-B01-036-02` | Merged | Duplicate of `E-036-01`. Recorded in `ID Crosswalk`. |
| `FP-002` | Unresolved | Referenced by entries but missing from Evidence Map. Recorded in `ID Crosswalk` as `Unresolved`. |

No IDs were deleted from the original Master file itself. The original Master remains unchanged.

## Final Validation Result

- **Checks run:** 21
- **PASS:** 20
- **FAIL (structural):** 0
- **Documented warnings (factual):** 2 (Team Name = Organization Name)
- **Overall status:** `PASS with documented warnings`

## Notes for Reviewer

- `WHRG_2026_Master.xlsx` is read-only. Do not modify.
- `WHRG_2026_Master_v2.xlsx` is the frozen candidate. Review before replacing the current Master.
- If approved, replace `WHRG_2026_Master.xlsx` with `WHRG_2026_Master_v2.xlsx` and archive the old file.
- All future staging outputs should conform to `references/master-schema-v2.md`.
