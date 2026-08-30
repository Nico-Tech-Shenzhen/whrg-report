# WHRG 2026 Master Schema v2

## Overview

This document defines the stable schema for `WHRG_2026_Master_v2.xlsx`. It is the canonical reference for all data collection, staging, and validation workflows.

Rules:
- Do NOT duplicate these rules into individual Skill files. Reference this document instead.
- Controlled vocabulary values are normative. Use only the values listed.
- Unknown / unresolvable facts are recorded explicitly. Do NOT guess to fill gaps.

---

## Workbook Sheets

| Sheet | Purpose | Origin |
|---|---|---|
| Instructions | Human-readable guide | Original |
| Competition Master | Canonical list of 51 competitions | Original |
| Entry Source Map | Per-competition source discovery status | Phase 1 staging |
| Competition Entry Map | Confirmed competition entries | Merged from staging |
| Evidence Map | Canonical evidence registry | Migrated |
| Participant Census | Aggregate counts with provenance | Migrated |
| ID Crosswalk | Legacy-to-canonical ID mappings | **New in v2** |
| Schema Migration Log | Audit trail of schema changes | **New in v2** |
| Unknown Questions | Open research questions | Original |
| Open-Data Audit | Dataset openness audit | Original |
| License Audit | License compliance audit | Original |
| Open-Knowledge Matrix | Team knowledge openness | Original |
| Recruitment Map | Team formation tracking | Original |
| Team Map | Team details | Original |
| Organization Master | Organization registry | Original |
| Rule Version Map | Rule version tracking | Original |
| Important Rule Changes | Rule change log | Original |
| Case Study Summary | Selected case studies | Original |
| Recovery Log | Data recovery history | Original |

---

## Competition Entry Map Schema

One row per confirmed Entry. Only populate when source material is reliable.

| Field | Type | Required | Notes |
|---|---|---|---|
| `Entry ID` | String | Yes | Internal unique ID. Never renumber stable IDs. |
| `Competition ID` | String | Yes | Reference to Competition Master |
| `Team ID` | String | No | Internal Team ID, if resolved |
| `Organization ID` | String | No | Internal Org ID, if resolved |
| `Country / Region` | String | No | ISO code or region name |
| `Team Name` | String | Yes | Official team name. If source only lists Org, use `Unknown` |
| `Organization Name` | String | No | Confirmed organization name. NOT the same as Team Name. |
| `Robot ID` | String | No | If source includes robot identifiers |
| `Robot Manufacturer` | String | No | If directly stated in source |
| `Robot Model` | String | No | If directly stated in source |
| `Participation Status` | Enum | Yes | See controlled values below |
| `Result` | String | No | Raw result value (time, score, distance, etc.) |
| `Ranking` | Integer | No | Final rank, if available |
| `Evidence IDs` | String | Yes | Comma-separated Evidence IDs |
| `Verification Status` | Enum | Yes | **New in v2**. See controlled values below. |
| `Verification Basis` | String | No | Short explanation of why status was assigned |
| `Notes` | Text | No | Additional context |

### Verification Status Controlled Values

| Value | Definition |
|---|---|
| `Verified` | Supported by Primary Web Evidence (URL-based, not Field Evidence alone). |
| `Research Lead` | Supported only by Field Evidence, missing evidence, or insufficient primary sources. NOT counted as verified. |
| `Unresolved` | No evidence IDs or status cannot be determined. |

Rules:
- `Field Evidence` alone (FP-xxx or EV-ESM-042) cannot support `Verified`.
- `Research Lead` entries are NOT counted in verified entry totals.
- If historical data only supports `Research Lead`, it must be downgraded.

### Participation Status Controlled Values

| Value | Definition |
|---|---|
| `Registered` | On official registration list |
| `Scheduled` | Appears in schedule / grouping / start list |
| `Started` | Confirmed to have started the competition |
| `Finished` | Completed the competition (has a result) |
| `DNF` | Did Not Finish (started but did not complete) |
| `DNS` | Did Not Start (scheduled but did not start) |
| `Disqualified` | Removed from results after start |
| `Unknown` | No source found to determine status |

Rule: A Registration list alone supports `Registered` only. To claim `Started` or `Finished`, require schedule/result evidence.

---

## Evidence Map Schema

One row per canonical evidence item.

| Field | Type | Required | Notes |
|---|---|---|---|
| `Evidence ID` | String | Yes | Stable unique ID. Never renumber. |
| `Topic` | String | Yes | e.g., `competition-entry`, `unified-result-system` |
| `Source Title` | String | Yes | Title of the source document/page |
| `Source Organization` | String | No | Publisher or issuing organization |
| `Source Type` | Enum | Yes | Type of source material. See controlled values. |
| `Source Class` | Enum | Yes | **New in v2**. Class of source for provenance tracking. |
| `Source URL` | URL | No | Primary URL |
| `Publication Date` | Date | No | Date the source was published |
| `Audit Date` | Date | Yes | **New in v2**. Date this evidence was recorded/audited |
| `Scope` | String | No | Which competitions/entities this covers |
| `Confidence` | Enum | Yes | H / M / L |
| `Notes` | Text | No | Limits, gaps, assumptions |

### Source Type / Source Class Controlled Values

**Source Type** (what the material is):

| Value | Use For |
|---|---|
| `Official-Org` | Official registration, schedule, results from organizer |
| `State-Media` | Xinhua, CCTV, beijing.gov.cn |
| `Media-Clue` | News article providing a lead but not full data |
| `Media-Secondary` | Media report used as secondary corroboration |
| `Team-Source` | Team self-report, social media, GitHub |
| `Research-Self` | Internal research notes or calculations |
| `Enterprise` | Company press release or product page |
| `Field` | On-site photo, observation, field scoreboard |
| `Unknown` | Cannot determine |

**Source Class** (how to treat the source for counts/claims):

| Value | Use For |
|---|---|
| `Official-Org` | Treat counts as Official |
| `State-Media` | Treat as reported/secondary |
| `Media-Secondary` | Explicitly secondary; do NOT treat as official count |
| `Media-Clue` | Clue only; not a count source |
| `Team-Source` | Cross-check only |
| `Research-Self` | Internal; not external evidence |
| `Enterprise` | Vendor claim; verify independently |
| `Field` | Search seed only; verify with web evidence |
| `Unknown` | Cannot determine |

Rule: `Source Class` may differ from `Source Type`. For example, a `Media-Clue` source can have `Source Class = Media-Secondary` when it reports a specific number.

---

## Participant Census Schema

Aggregate metrics with provenance.

| Field | Type | Required |
|---|---|---|
| `Metric` | String | Yes |
| `Value` | String/Number | Yes |
| `Source` | String | No |
| `Confidence` | Enum | Yes |
| `Notes` | Text | No |
| `Count Type` | Enum | **New in v2** |
| `Source Class` | Enum | **New in v2** |

### Count Type Controlled Values

| Value | Definition |
|---|---|
| `Official` | Source explicitly states the number (organizer or government). |
| `Reported` | Number reported by media or secondary source. |
| `Calculated` | Derived by counting entries in a reconstructed list. |
| `Known minimum` | At least this many confirmed, but total may be higher. |
| `Partial` | Count covers only a subset (e.g., one heat). |
| `Unknown` | Cannot determine count type. |

---

## Entry Source Map Schema

One row per Competition. Tracks what source material was found.

| Field | Type | Notes |
|---|---|---|
| `Competition ID` | String | Reference to master |
| `Competition Name` | String | Canonical name |
| `Category` | Enum | e.g., "竞技赛", "场景赛" |
| `Registration List Found?` | Boolean | |
| `Schedule Found?` | Boolean | |
| `Grouping Found?` | Boolean | Heat / draw / bracket tables |
| `Start List Found?` | Boolean | |
| `Results Found?` | Boolean | Scoreboard / result tables |
| `Ranking Found?` | Boolean | |
| `Award List Found?` | Boolean | |
| `Official Live Data Found?` | Boolean | |
| `Best Source Type` | Enum | Registration / Schedule / Grouping / StartList / Results / Ranking / Awards / Live / News / None |
| `Best Source URL` | URL | |
| `Source Date` | Date | Publication date, or `[Unknown]` |
| `Evidence ID` | String | Reference to best Evidence entry |
| `Coverage Type` | Enum | See below |
| `Estimated Recoverability` | Enum | See below |
| `Notes` | Text | |

### Coverage Type Controlled Values

| Value | Definition |
|---|---|
| `Complete` | All actual entries covered by source material. |
| `Likely Complete` | Strong indication of near-full coverage; minor gaps possible. |
| `Partial` | Some entries confirmed, but not the full set. |
| `Winners Only` | Only top-N / medalists / award recipients confirmed. |
| `No Entry Data Found` | No source material located after reasonable search. |

### Recoverability Controlled Values

| Value | Definition |
|---|---|
| `High` | Official unified system or complete documents available. |
| `Medium` | Partial official documents exist; reconstruction feasible. |
| `Low` | Only scattered secondary sources available. |
| `Unknown` | Insufficient information to judge. |

---

## ID Crosswalk Schema

Tracks legacy IDs, duplicates, and unresolved mappings.

| Field | Type | Required |
|---|---|---|
| `Record Type` | Enum | Yes | Entry / Evidence / Team / Organization / Robot / Other |
| `Legacy ID` | String | Yes | Old or duplicate ID |
| `Canonical ID` | String | No | Current canonical ID, or `[Unresolved]` |
| `Status` | Enum | Yes | See below |
| `Reason` | Text | No | Why this mapping exists |
| `Source Sheet` | String | No | Where the duplicate/legacy was found |
| `Notes` | Text | No | |

### Crosswalk Status Controlled Values

| Value | Definition |
|---|---|
| `Confirmed Same` | Legacy and Canonical refer to the same entity. |
| `Confirmed Different` | Legacy and Canonical are distinct entities. |
| `Possible Duplicate` | Likely same but not fully confirmed. |
| `Unresolved` | Cannot determine relationship. |

---

## Schema Migration Log Schema

Audit trail of all schema changes.

| Field | Type | Required |
|---|---|---|
| `Timestamp` | DateTime | Yes |
| `Action` | Enum | Yes | ADD_COLUMN / REMOVE_COLUMN / RENAME / STANDARDIZE / DEDUPLICATE / SPLIT / DOWNGRADE / CREATE_SHEET / OVERRIDE |
| `Sheet` | String | Yes |
| `Field` | String | No |
| `Old Value` | Text | No |
| `New Value` | Text | No |
| `Reason` | Text | No |

---

## Entity ID Rules

Applies to Organization, Team, Robot Platform, Resource, Dataset, License.

- Existing IDs are NEVER renumbered.
- Create new IDs only when identity can be uniquely confirmed.
- When identity is ambiguous, keep `Unknown` / `Unresolved`.
- Do NOT merge Organization and Team just because names are similar.
- Do NOT launch web searches solely to fill Entity IDs.

---

## Date Field Rules

- Do NOT mix different semantic dates in the same field.
- Distinguish at minimum: `Event Date`, `Publication Date`, `Audit Date`.
- If historical records cannot determine date semantics, keep the original value and set `Date Type = Unknown`.
- Do NOT guess.

---

## Validation Checklist

Before accepting staging or master updates, verify:

- [ ] All Competition IDs resolve to known competitions (51 total).
- [ ] No duplicate Entry IDs in canonical records.
- [ ] No `Team = Organization` assumptions without evidence.
- [ ] No registration counted as actual participation without schedule/result evidence.
- [ ] Coverage Type classification is internally consistent.
- [ ] Count Type identifies `Official` / `Reported` / `Calculated` / `Known minimum` / `Partial`.
- [ ] Master sheet was NOT modified directly by research tasks.
- [ ] Staging does NOT silently overwrite master data.
- [ ] `Field Evidence` alone does NOT support `Verified` status.
- [ ] `Research Lead` entries are NOT counted as verified.
- [ ] Evidence IDs referenced by entries exist in Evidence Map (or are recorded in ID Crosswalk as unresolved).
- [ ] Source Type vocabulary uses only controlled values.
- [ ] Date fields are semantically correct or explicitly marked `Unknown`.
