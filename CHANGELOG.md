# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/)
and this project adheres to [Semantic Versioning](https://semver.org/).

## 3.1.0 / 2026-07-30

### Added

- Scrub `player_chat.text` and cap `rank_update.win_count`, the two new rushb
  channels carrying PII. `win_count` is the same quantity as `player_info.wins`,
  already capped at 2501; both now read one shared constant.
- `csds_pii_channel_instructions(manifest)` returns only the PII channels a CSDS
  actually has. `get_channels` raises on a channel missing from the manifest, so
  callers must filter or adding a channel breaks every older CSDS.

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
