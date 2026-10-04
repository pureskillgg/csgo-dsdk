# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/)
and this project adheres to [Semantic Versioning](https://semver.org/).

## 3.2.2

### Fixed

- `scrub_csds_pii` keeps a numeric column's dtype when it replaces it with a number: a narrower `player_status.ping` (int16) stays int16 instead of becoming int64. A number that doesn't fit the column's dtype raises instead of wrapping.

## 3.2.0

### Changed

- Depend only on what the package imports: pandas, python-dateutil and python-rapidjson. `pureskillgg-dsdk` (now a dev dependency, for the tests) and `structlog` are no longer installed with it.
- Allow pandas 3. On pandas 3, the scrubbed string columns are the new `str` dtype; the values are unchanged.

## 3.1.1

### Changed

- Harden the deploy workflows.
- Update GitHub Actions to Node.js 24 runtimes.

### Fixed

- `pop_overtime` keeps rows with a missing `round` instead of dropping them.
- `pop_overtime` no longer drops regulation rows that share an index label with an overtime row.
- Document `max_rounds_csgo` for CS2: pass 24 (MR12); the default 30 is CS:GO MR15.

## 3.1.0 / 2026-07-30

### Added

- Scrub `player_chat.text` and cap `rank_update.win_count`.
- `csds_pii_channel_instructions(manifest)` for per-CSDS PII channels.

## 3.0.1 / 2026-06-14

### Fixed

- Stage uv.lock in the version commit.

## 3.0.0 / 2026-06-14

- Migrate to Python 3.11+ (CI test matrix 3.11-3.14).
- Update to pureskillgg-dsdk 3.0 and the new data stack: pandas 2.3, numpy 2, structlog 26.
- Update dev tooling: black 26, pylint 4, pytest 9, pytest-cov 7; remove pytest-runner.

## 2.0.2 / 2026-06-09

- Normalize the package name automatically. (Tagged but not published to PyPI; superseded by 3.0.0.)

## 2.0.1 / 2026-06-09

- Update GitHub Actions to clear Node 20 deprecations. (Tagged but not published to PyPI; superseded by 3.0.0.)

## 2.0.0 / 2024-04-01

- Update dependencies (pureskillgg-dsdk 2, pandas 2).

## 1.2.1 / 2024-03-31

- Update the pureskillgg-dsdk dependency.

## 1.2.0 / 2024-03-31

- Update the pureskillgg-dsdk and pandas dependencies.

## 1.1.0 / 2023-11-18

- Update the pureskillgg-dsdk dependency.

## 1.0.0 / 2022-07-25

- Initial release.
