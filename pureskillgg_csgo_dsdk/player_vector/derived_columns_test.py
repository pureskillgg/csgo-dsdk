# pylint: disable=missing-docstring

import os

import numpy as np
import pandas as pd
import pytest
from pureskillgg_dsdk import GameDsLoader, DsReaderFs

from .derived_columns import (
    add_player_vector_derived_columns,
    player_vector_source_columns,
    PLAYER_VECTOR_DERIVED_COLUMNS,
    calc_velocity,
    calc_angular_velocity,
    calc_speed_2d,
    calc_movement_angle,
    calc_movement_angle_diff,
)
from ..errors import MissingColumns


def _samples(*rows, player_id=1):
    """rows: (round, tick, x_pos) for one player; theta_ang follows x_pos."""
    return pd.DataFrame(
        [
            {
                "round": rnd,
                "tick": tick,
                "player_id": player_id,
                "x_pos": x,
                "y_pos": 0.0,
                "z_pos": 0.0,
                "phi_ang": 90.0,
                "theta_ang": x,
            }
            for rnd, tick, x in rows
        ]
    )


def _second(df):
    return df["tick"] / 64


def test_adds_every_derived_column_in_order():
    df = _samples((1, 100, 0.0), (1, 101, 2.0))
    out = add_player_vector_derived_columns(df)

    assert out is df
    assert list(df.columns[-10:]) == list(PLAYER_VECTOR_DERIVED_COLUMNS)
    assert all(
        df[column].dtype == "float64" for column in PLAYER_VECTOR_DERIVED_COLUMNS
    )


def test_second_is_the_tick_over_the_tick_rate():
    df = _samples((1, 64, 0.0), (1, 96, 0.0))
    add_player_vector_derived_columns(df)
    assert list(df["second"]) == [1.0, 1.5]

    add_player_vector_derived_columns(df, tick_rate=128)
    assert list(df["second"]) == [0.5, 0.75]


def test_moving_along_x_while_looking_along_it():
    df = _samples((1, 100, 0.0), (1, 101, 2.0))
    add_player_vector_derived_columns(df)
    moving = df.iloc[1]

    assert moving["x_vel"] == 128.0
    assert moving["y_vel"] == 0.0
    assert moving["z_vel"] == 0.0
    assert moving["speed_2d"] == 128.0
    assert moving["movement_angle"] == 0.0
    assert moving["theta_vel"] == 128.0
    assert moving["phi_vel"] == 0.0
    assert moving["ang_vel"] == 128.0
    # looking at theta_ang 2, moving at 0
    assert moving["movement_angle_diff"] == 2.0


def test_velocity_restarts_at_a_new_round():
    # a respawn between rounds is not one tick of movement
    df = _samples((1, 100, 0.0), (1, 101, 2.0), (2, 500, 1500.0))
    velocity = calc_velocity(df, _second(df))

    assert list(velocity.columns) == ["x_vel", "y_vel", "z_vel"]
    assert list(velocity["x_vel"]) == [0.0, 128.0, 0.0]


def test_velocity_is_per_player():
    df = pd.concat(
        [
            _samples((1, 100, 0.0), (1, 101, 1.0), player_id=1),
            _samples((1, 100, 500.0), (1, 101, 502.0), player_id=2),
        ]
    ).sort_values("tick", kind="stable", ignore_index=True)
    velocity = calc_velocity(df, _second(df))

    assert list(velocity["x_vel"]) == [0.0, 0.0, 64.0, 128.0]


def test_a_teleport_inside_a_round_reads_as_standing_still():
    # 1,000 units in one tick is past the engine's 3,500 a second cap
    df = _samples((1, 100, 0.0), (1, 101, 1000.0), (1, 102, 1001.0))
    df["y_pos"] = [0.0, 1.0, 2.0]
    velocity = calc_velocity(df, _second(df))

    assert list(velocity["x_vel"]) == [0.0, 0.0, 64.0]
    # every axis reads 0 on the teleport, not only the one over the cap
    assert list(velocity["y_vel"]) == [0.0, 0.0, 64.0]


def test_angular_velocity_restarts_at_a_new_round():
    df = _samples((1, 100, 10.0), (1, 101, 11.0), (2, 500, 90.0))
    angular = calc_angular_velocity(df, _second(df))

    assert list(angular.columns) == ["phi_vel", "theta_vel", "ang_vel"]
    assert list(angular["theta_vel"]) == [0.0, 64.0, 0.0]
    assert list(angular["ang_vel"]) == [0.0, 64.0, 0.0]


def test_a_turn_across_the_theta_boundary_is_a_small_turn():
    df = _samples((1, 100, 179.0), (1, 101, -179.0), (1, 102, 179.0))
    angular = calc_angular_velocity(df, _second(df))

    assert list(angular["theta_vel"]) == [0.0, 128.0, -128.0]


def test_a_missing_player_id_has_no_motion():
    df = _samples((1, 100, 0.0), (1, 101, 2.0))
    df["player_id"] = pd.array([1, None], dtype="Int32")
    velocity = calc_velocity(df, _second(df))

    assert velocity["x_vel"].isna().tolist() == [False, True]


def test_speed_2d():
    speed = calc_speed_2d(pd.Series([3.0, 0.0]), pd.Series([4.0, 0.0]))
    assert list(speed) == [5.0, 0.0]


def test_movement_angle_is_from_0_to_360():
    x_vel = pd.Series([1.0, 0.0, -1.0, 0.0, 0.0])
    y_vel = pd.Series([0.0, 1.0, 0.0, -1.0, 0.0])
    angle = calc_movement_angle(x_vel, y_vel)

    # standing still reads 0, like moving along +x
    assert angle.round(6).tolist() == [0.0, 90.0, 180.0, 270.0, 0.0]


def test_standing_still_reads_0_whatever_the_sign_of_zero():
    # arctan2(0.0, -0.0) is 180 degrees
    x_vel = pd.Series([-0.0, -0.0, 0.0, 0.0])
    y_vel = pd.Series([0.0, -0.0, -0.0, 0.0])
    angle = calc_movement_angle(x_vel, y_vel)

    assert angle.tolist() == [0.0, 0.0, 0.0, 0.0]
    assert not np.signbit(angle).any()


def _looking_and_moving(*rows):
    """rows: (theta_ang the player looks at, direction they move in, speed)."""
    move = np.radians([direction for _, direction, _ in rows])
    speed = pd.Series([s for _, _, s in rows], dtype=float)
    theta_ang = pd.Series([look for look, _, _ in rows])
    return theta_ang, speed * np.cos(move), speed * np.sin(move), speed


def test_the_look_minus_move_angle_is_within_plus_or_minus_180():
    # looking at -170 and moving at 170 is 20, not 340
    theta_ang, x_vel, y_vel, speed = _looking_and_moving(
        (170.0, 190.0, 250.0),
        (-170.0, 170.0, 250.0),
        (0.0, 0.0, 250.0),
        (90.0, 0.0, 250.0),
        (0.0, 180.0, 250.0),
    )
    diff = calc_movement_angle_diff(theta_ang, calc_movement_angle(x_vel, y_vel), speed)

    assert diff.round(6).tolist() == [-20.0, 20.0, 0.0, 90.0, -180.0]


def test_standing_still_has_no_look_minus_move_angle():
    theta_ang, x_vel, y_vel, speed = _looking_and_moving(
        (45.0, 0.0, 0.0), (45.0, 0.0, 250.0)
    )
    diff = calc_movement_angle_diff(theta_ang, calc_movement_angle(x_vel, y_vel), speed)

    assert diff.isna().tolist() == [True, False]


def test_the_narrow_types_csgo_ppp_writes_give_the_same_values():
    wide = _samples((1, 100, 0.5), (1, 101, 2.25), (2, 500, -1500.125))
    narrow = wide.astype(
        {
            "tick": "int32",
            "round": "Int16",
            "player_id": "Int32",
            "x_pos": "float32",
            "y_pos": "float32",
            "z_pos": "float32",
            "phi_ang": "float32",
            "theta_ang": "float32",
        }
    )
    add_player_vector_derived_columns(wide)
    add_player_vector_derived_columns(narrow)

    for column in PLAYER_VECTOR_DERIVED_COLUMNS:
        assert narrow[column].dtype == "float64"
        pd.testing.assert_series_equal(narrow[column], wide[column])


def test_stored_derived_columns_are_replaced_not_read():
    # files written before csgo-ppp 8.5.4 store velocities with respawn spikes
    df = _samples((1, 100, 0.0), (1, 101, 2.0))
    df["x_vel"] = [365000.0, 365000.0]
    df["second"] = np.array([0.0, 0.0], dtype="float32")
    add_player_vector_derived_columns(df)

    assert list(df["x_vel"]) == [0.0, 128.0]
    assert list(df["speed_2d"]) == [0.0, 128.0]
    assert list(df["second"]) == [100 / 64, 101 / 64]
    # a replaced column keeps its place
    assert list(df.columns[-10:-8]) == ["x_vel", "second"]


def test_adds_only_the_columns_asked_for():
    df = _samples((1, 100, 0.0), (1, 101, 2.0))
    before = list(df.columns)
    add_player_vector_derived_columns(df, columns=["speed_2d", "second"])

    assert list(df.columns) == before + ["second", "speed_2d"]
    assert list(df["speed_2d"]) == [0.0, 128.0]


def test_needs_only_the_source_columns_of_what_is_asked_for():
    df = _samples((1, 100, 0.0), (1, 101, 2.0))

    for columns in (["second"], ["speed_2d"], ["ang_vel"], ["movement_angle_diff"]):
        sources = player_vector_source_columns(columns)
        out = add_player_vector_derived_columns(df[sources].copy(), columns=columns)
        assert list(out.columns) == sources + columns


def test_source_columns():
    assert player_vector_source_columns(["second"]) == ["tick"]
    assert player_vector_source_columns(["z_vel"]) == [
        "tick",
        "player_id",
        "round",
        "x_pos",
        "y_pos",
        "z_pos",
    ]
    assert player_vector_source_columns(["theta_vel"]) == [
        "tick",
        "player_id",
        "round",
        "phi_ang",
        "theta_ang",
    ]
    assert player_vector_source_columns() == [
        "tick",
        "player_id",
        "round",
        "x_pos",
        "y_pos",
        "z_pos",
        "phi_ang",
        "theta_ang",
    ]
    assert player_vector_source_columns(
        ["movement_angle_diff"], group_by=["match_key", "player_id", "round"]
    ) == [
        "tick",
        "match_key",
        "player_id",
        "round",
        "x_pos",
        "y_pos",
        "z_pos",
        "theta_ang",
    ]


def test_missing_source_columns_error_usage():
    df = _samples((1, 100, 0.0), (1, 101, 2.0)).drop(columns=["x_pos", "theta_ang"])
    with pytest.raises(MissingColumns) as e_info:
        add_player_vector_derived_columns(df)

    assert e_info.value.columns == ["x_pos", "theta_ang"]
    assert (
        str(e_info.value)
        == "Cannot add derived player_vector columns: missing columns x_pos, theta_ang"
    )


def test_rejects_a_column_that_is_not_derived():
    df = _samples((1, 100, 0.0))
    with pytest.raises(ValueError, match="Not derived player_vector columns: x_pos"):
        add_player_vector_derived_columns(df, columns=["x_pos"])


def test_group_by_keeps_matches_apart():
    # the same player and round in two matches, as in a tome
    tome = pd.concat(
        [
            _samples((1, 100, 0.0), (1, 101, 2.0)).assign(match_key="a"),
            _samples((1, 100, 800.0), (1, 101, 801.0)).assign(match_key="b"),
        ],
        ignore_index=True,
    )
    add_player_vector_derived_columns(
        tome, group_by=["match_key", "player_id", "round"]
    )

    assert list(tome["x_vel"]) == [0.0, 128.0, 0.0, 64.0]


def load_player_vector(match_id):
    manifest_key = os.path.join("csds", "2022", "05", "15", match_id, "csds")
    reader = DsReaderFs(root_path="fixtures", manifest_key=manifest_key, log=None)
    loader = GameDsLoader(reader=reader, log=None)
    return loader.get_channels([{"channel": "player_vector"}, {"channel": "header"}])


def test_a_real_match():
    data = load_player_vector("994a9fed-d4a5-4096-8088-93b422be5025")
    stored = data["player_vector"]
    df = stored.drop(
        columns=[c for c in PLAYER_VECTOR_DERIVED_COLUMNS if c in stored.columns]
    )
    add_player_vector_derived_columns(df, tick_rate=data["header"]["tick_rate"][0])

    assert len(df) == len(stored)
    np.testing.assert_array_equal(df["second"].to_numpy(), stored["second"].to_numpy())
    velocity = df[["x_vel", "y_vel", "z_vel"]]
    assert velocity.notna().all().all()
    assert (velocity.abs() <= 3500).all().all()
    first = ~df.duplicated(subset=["player_id", "round"])
    assert (df.loc[first, ["x_vel", "y_vel", "z_vel", "ang_vel"]] == 0).all().all()
    moving = df["speed_2d"] != 0
    assert df.loc[~moving, "movement_angle_diff"].isna().all()
    assert df.loc[moving, "movement_angle_diff"].between(-180, 180).all()
