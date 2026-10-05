# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/)
and this project adheres to [Semantic Versioning](https://semver.org/).

## 3.3.2

### Changed

- Pin workflow runners to `ubuntu-24.04`.

## 3.3.1

### Changed

- `movement_angle` is missing while standing still, from `calc_movement_angle` and so from `add_player_vector_derived_columns`. It read 0, the same as moving along +x. csgo-ppp writes it the same way from [csgo-ppp#189](https://github.com/pureskillgg/csgo-ppp/pull/189) on; files written before store 0 there.

## 3.3.0

### Added

- `add_player_vector_derived_columns` adds the ten `player_vector` columns that csgo-ppp computes from the columns read from the demo: `second`, `x_vel`, `y_vel`, `z_vel`, `speed_2d`, `movement_angle`, `movement_angle_diff`, `phi_vel`, `theta_vel` and `ang_vel`. csgo-ppp will stop storing them, and readers compute them on load with this function. It gives the values csgo-ppp writes: motion restarts at every round, a teleport reads as standing still, and `movement_angle_diff` is the look-minus-move angle from -180 to 180, missing when standing still. A file that still stores the columns comes out the same, since they are replaced, not read. `columns` adds only some of them, and `group_by` keeps the matches of a tome apart.
- `player_vector_source_columns` lists the columns to load for them, and `PLAYER_VECTOR_DERIVED_COLUMNS` names the ten.
- `pureskillgg_csgo_dsdk.player_vector` also has each step on its own (`calc_velocity`, `calc_angular_velocity`, `calc_speed_2d`, `calc_movement_angle`, `calc_movement_angle_diff`), which csgo-ppp calls.

### Changed

- numpy is a direct dependency. It was already installed with pandas.

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
