# Deep dive: `scrub_csds_pii`

`scrub_csds_pii(manifest, data)` anonymizes a single CSDS ("Counter-Strike Data
Standard") match in place. It is the privacy-critical path for any data leaving
the platform (for example Data Exchange / academic datasets), so this document
spells out exactly which fields are **redacted** (overwritten with a constant)
vs. **capped** (clamped to a ceiling), and how the manifest bookkeeping works.

Source: `pureskillgg_csgo_dsdk/scrubber/scrub_pii.py`.

## Inputs and return value

- `manifest` (dict): the CSDS manifest. The function returns a **rewritten**
  manifest (because of the `jobId` round-trip described below), so callers must
  use the return value.
- `data` (dict): a mapping of channel name to a pandas DataFrame. This is
  mutated **in place** and is not returned.

Before calling, load the PII channels. **Filter the instruction list against
the manifest first** — `get_channels` raises on a channel missing from the
manifest, and a CSDS written before a channel existed does not carry it:

```python
from pureskillgg_csgo_dsdk import csds_pii_channel_instructions, scrub_csds_pii

data = loader.get_channels(csds_pii_channel_instructions(loader.manifest))
manifest = scrub_csds_pii(loader.manifest, data)
```

Passing `SCRUB_CSDS_PII_CHANNEL_INSTRUCTIONS` to `get_channels` unfiltered works
only while every listed channel happens to be present, and breaks whenever a
channel is added to the list. The list is `player_name`, `header`,
`player_personal`, `player_info`, `player_status`, `player_chat`,
`rank_update`.

## What happens to the manifest

1. **`jobId` -> `id` round-trip.** `replace_job_id` reads `manifest["jobId"]`
   and `manifest["id"]` (the anonymous id), serializes the whole manifest with
   `rapidjson.dumps`, does a plain string `.replace(job_id, anon_id)`, then
   `rapidjson.loads` it back. This removes the job id *everywhere it appears* in
   the manifest, not just the top-level key. It also sets
   `manifest["redacted"] = True`.
2. **Constant redactions.** `manifest["sharecode"]`, `manifest["demoId"]`, and
   `manifest["metadata"]["bucket"]` are overwritten with the literal string
   `"redacted"`. (The `bucket` here is a manifest field, not a live S3 bucket.)
3. **Date precision.** `manifest["matchDate"]` is reparsed and re-emitted at
   minute precision (`fix_date_precision`, `timespec="minutes"`, hardcoded at the
   call site — there is no public way to change the precision).
4. **Channel `redacted` flags initialized.** Every channel's `redacted` flag is
   first set to `False`; per-column edits below then flip the applicable ones
   back to `True`.

## What happens to the channel DataFrames

Columns are redacted only **if they exist** (`replace_if_exists`), so a match
missing a channel/column is skipped rather than erroring.

| Channel | Column(s) | Action |
| --- | --- | --- |
| `header` | `sharecode`, `demo_id` | overwritten with `"redacted"` |
| `player_name` | `name_new`, `name_old` | overwritten with `"redacted"` |
| `player_personal` | `name`, `clan_tag` | overwritten with `"redacted"` |
| `player_personal` | `steam_id` | mapped to letters `A`, `B`, `C` ... |
| `player_status` | `ping` | set to `0` |
| `player_chat` | `text` | overwritten with `"redacted"` |
| `player_info` | `wins` | values over 2500 clamped to 2501 (capped) |
| `rank_update` | `win_count` | values over 2500 clamped to 2501 (capped) |
| `player_info` | `commends_friendly`, `commends_leader`, `commends_teacher` | values over 100 clamped to 101 (capped) |

Note that player names live under `name_new` / `name_old` in the `player_name`
channel and under `name` in `player_personal` — there is no single `name`
column covering all of them.

`player_info.wins` and `rank_update.win_count` are the same quantity, so they
share one cap (`WINS_CAP_THRESHOLD` / `WINS_CAP_VALUE`). Capping one without the
other would leak around the rule. Only `text` is removed from `player_chat`:
who spoke and when is kept.

### `steam_id` letter mapping

`fix_steam_ids` builds a dict from each unique `steam_id` in `player_personal`
to a 26-letter alphabet (`A` .. `Z`) and applies it. A match with more than 26
unique steam ids would raise `IndexError` — a theoretical edge, not an observed
issue.

## Manifest origin/comment bookkeeping

Every mutation also records what it did in the manifest:

- **Redacted columns** have `"-redacted"` appended to their `origin` string, and
  their channel's `redacted` flag set to `True`.
- **Capped columns** (`wins` and the three `commends_*`) have `"-capped"`
  appended to `origin`, get `" Capped to <value>."` appended to their `comment`,
  and their channel's `redacted` flag set to `True`.

The channel/column positions are resolved by `get_manifest_indexes`, which
raises a `RuntimeError` if a referenced channel or column is not present in the
manifest.

## Errors

- `RuntimeError` — a channel or column referenced during scrubbing is missing
  from the manifest structure.
- The library's own `MissingColumns` / `UnsupportedChannelStructure` are raised
  by the sibling `pop_overtime` helper, not by `scrub_csds_pii`.
