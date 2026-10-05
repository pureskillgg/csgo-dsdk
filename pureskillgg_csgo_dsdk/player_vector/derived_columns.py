"""
Compute player_vector's derived columns
"""

from typing import Iterable, List, Optional, Sequence

import numpy as np
import pandas as pd

from ..errors import MissingColumns

CS2_TICK_RATE = 64

# Motion is differenced per player per round: a player respawns between
# rounds, and a step across the respawn is not movement.
MOTION_GROUP = ("player_id", "round")

# The engine clamps each velocity component to sv_maxvelocity, 3,500 units a
# second, so a bigger step between two samples is a teleport, not movement.
MAX_AXIS_VELOCITY = 3500.0

# In the order add_player_vector_derived_columns adds them.
PLAYER_VECTOR_DERIVED_COLUMNS = (
    "second",
    "phi_vel",
    "theta_vel",
    "ang_vel",
    "x_vel",
    "y_vel",
    "z_vel",
    "speed_2d",
    "movement_angle",
    "movement_angle_diff",
)

_POSITIONS = ("x_pos", "y_pos", "z_pos")
_ANGLES = ("phi_ang", "theta_ang")
_ANGULAR = ("phi_vel", "theta_vel", "ang_vel")
_LINEAR = (
    "x_vel",
    "y_vel",
    "z_vel",
    "speed_2d",
    "movement_angle",
    "movement_angle_diff",
)


def add_player_vector_derived_columns(
    df: pd.DataFrame,
    /,
    *,
    columns: Optional[Iterable[str]] = None,
    tick_rate: float = CS2_TICK_RATE,
    group_by: Sequence[str] = MOTION_GROUP,
) -> pd.DataFrame:
    """Add the columns csgo-ppp computes from player_vector's other columns

    The columns are added to df in place, as float64, and df is returned.
    They are always computed from the columns read from the demo. A derived
    column df already has is replaced, never read, so an older file that
    stores them comes out the same as a file that doesn't.

    Rows must be in tick order within each player and round, as csgo-ppp
    writes them.

    Keywords:
        df (dataframe): The player_vector channel.
        columns (list): Default value: every derived column
            Which of PLAYER_VECTOR_DERIVED_COLUMNS to add.
            player_vector_source_columns lists what df needs for them.
        tick_rate (number): Default value: 64
            Ticks a second. CS2 is 64. A CS:GO match's is in its header.
        group_by (list): Default value: ("player_id", "round")
            The columns that tell one player's round from another's. Motion
            restarts at each. Put the match's key first when df holds more
            than one match, as a tome does.

    Returns:
        data (dataframe): df

    Examples:
        >>> add_player_vector_derived_columns(player_vector)

        >>> add_player_vector_derived_columns(player_vector, columns=["speed_2d"])

        >>> add_player_vector_derived_columns(
        ...     tome, group_by=["match_key", "player_id", "round"]
        ... )

    """
    wanted = _wanted(columns)
    missing = [
        column
        for column in player_vector_source_columns(wanted, group_by=group_by)
        if column not in df.columns
    ]
    if missing:
        raise MissingColumns(
            "Cannot add derived player_vector columns", columns=missing
        )

    second = df["tick"].astype("float64") / tick_rate
    derived = {"second": second}

    linear = any(column in _LINEAR for column in wanted)
    angular = any(column in _ANGULAR for column in wanted)
    if linear or angular:
        sources = (*(_POSITIONS if linear else ()), *(_ANGLES if angular else ()))
        steps = _steps(df, second, sources, group_by)
        if angular:
            derived.update(_angular_velocity(steps))
        if linear:
            derived.update(_velocity(steps))
            derived["speed_2d"] = calc_speed_2d(derived["x_vel"], derived["y_vel"])
            derived["movement_angle"] = calc_movement_angle(
                derived["x_vel"], derived["y_vel"]
            )
    if "movement_angle_diff" in wanted:
        derived["movement_angle_diff"] = calc_movement_angle_diff(
            df["theta_ang"].astype("float64"),
            derived["movement_angle"],
            derived["speed_2d"],
        )

    for column in PLAYER_VECTOR_DERIVED_COLUMNS:
        if column in wanted:
            df[column] = derived[column]
    return df


def player_vector_source_columns(
    columns: Optional[Iterable[str]] = None,
    /,
    *,
    group_by: Sequence[str] = MOTION_GROUP,
) -> List[str]:
    """The player_vector columns the derived columns are computed from

    Load these to call add_player_vector_derived_columns with the same
    arguments.

    Keywords:
        columns (list): Default value: every derived column
            Which of PLAYER_VECTOR_DERIVED_COLUMNS will be added.
        group_by (list): Default value: ("player_id", "round")
            As for add_player_vector_derived_columns.

    Returns:
        data (list): Column names.

    Examples:
        >>> player_vector_source_columns(["second"])
        ['tick']

        >>> player_vector_source_columns(["speed_2d"])
        ['tick', 'player_id', 'round', 'x_pos', 'y_pos', 'z_pos']

    """
    wanted = _wanted(columns)
    linear = any(column in _LINEAR for column in wanted)
    angular = any(column in _ANGULAR for column in wanted)
    sources = ["tick"]
    if linear or angular:
        sources.extend(group_by)
    if linear:
        sources.extend(_POSITIONS)
    if angular:
        sources.extend(_ANGLES)
    if "movement_angle_diff" in wanted and not angular:
        sources.append("theta_ang")
    return sources


def calc_velocity(
    df: pd.DataFrame,
    second: pd.Series,
    /,
    *,
    group_by: Sequence[str] = MOTION_GROUP,
) -> pd.DataFrame:
    """x_vel, y_vel and z_vel, in units a second

    Each player's first sample in a round reads 0. So does a teleport: a
    sample where any axis moved faster than the engine allows.

    Keywords:
        df (dataframe): The player_vector channel.
        second (series): Each row's time in seconds.
        group_by (list): Default value: ("player_id", "round")
            As for add_player_vector_derived_columns.

    Returns:
        data (dataframe): The three columns, on df's index.

    """
    return pd.DataFrame(_velocity(_steps(df, second, _POSITIONS, group_by)))


def calc_angular_velocity(
    df: pd.DataFrame,
    second: pd.Series,
    /,
    *,
    group_by: Sequence[str] = MOTION_GROUP,
) -> pd.DataFrame:
    """phi_vel, theta_vel and ang_vel, in degrees a second

    Each player's first sample in a round reads 0. A theta step across the
    -180 / 180 boundary is the small turn it really was.

    Keywords:
        df (dataframe): The player_vector channel.
        second (series): Each row's time in seconds.
        group_by (list): Default value: ("player_id", "round")
            As for add_player_vector_derived_columns.

    Returns:
        data (dataframe): The three columns, on df's index.

    """
    return pd.DataFrame(_angular_velocity(_steps(df, second, _ANGLES, group_by)))


def calc_speed_2d(x_vel: pd.Series, y_vel: pd.Series, /) -> pd.Series:
    """The speed over the ground, in units a second"""
    return np.sqrt(x_vel * x_vel + y_vel * y_vel)


def calc_movement_angle(x_vel: pd.Series, y_vel: pd.Series, /) -> pd.Series:
    """The direction of movement over the ground, in degrees from 0 to 360

    Standing still reads 0, the same as moving along +x.
    """
    angle = np.arctan2(y_vel, x_vel) * 360.0 / (2 * np.pi)
    angle = angle.mask(angle < 0, angle + 360)
    # arctan2 tells -0.0 from 0.0, so a stationary -0.0 would read 180.
    return angle.mask((x_vel == 0) & (y_vel == 0), 0.0)


def calc_movement_angle_diff(
    theta_ang: pd.Series, movement_angle: pd.Series, speed_2d: pd.Series, /
) -> pd.Series:
    """Where the player looks minus where they move, in degrees

    From -180 to 180: 0 moving the way they look, 90 or -90 sideways, 180 or
    -180 backwards. Standing still has no direction of movement, so it is
    missing.
    """
    diff = (theta_ang - movement_angle + 180) % 360 - 180
    return diff.mask(speed_2d == 0)


def _wanted(columns):
    if columns is None:
        return PLAYER_VECTOR_DERIVED_COLUMNS
    wanted = tuple(columns)
    unknown = [
        column for column in wanted if column not in PLAYER_VECTOR_DERIVED_COLUMNS
    ]
    if unknown:
        raise ValueError(f"Not derived player_vector columns: {', '.join(unknown)}")
    return wanted


def _steps(df, second, columns, group_by):
    """How far `second` and each column moved since the group's previous row

    A group's first row gets 1 for `second` and 0 for the columns, so every
    rate there is 0. A row with a missing key has no group and stays missing.
    A missing value inside a group reads as a group start too, for its own row
    and the next: csgo-ppp does the same, and its positions and angles are
    never missing.
    """
    keys = list(group_by)
    work = df[keys].copy()
    work["second"] = second.astype("float64")
    for column in columns:
        work[column] = df[column].astype("float64")
    values = ["second", *columns]
    steps = work.groupby(keys, sort=False)[values].diff()
    in_group = work[keys].notna().all(axis=1)
    for name in values:
        first_fill = 1.0 if name == "second" else 0.0
        steps[name] = steps[name].mask(in_group & steps[name].isna(), first_fill)
    return steps


def _velocity(steps):
    velocity = pd.DataFrame(
        {f"{axis}_vel": steps[f"{axis}_pos"] / steps["second"] for axis in "xyz"}
    )
    # A teleport inside a round starts a new segment, as a round does.
    teleport = (velocity.abs() > MAX_AXIS_VELOCITY).any(axis=1)
    velocity.loc[teleport, :] = 0.0
    return {name: velocity[name] for name in velocity.columns}


def _angular_velocity(steps):
    phi_vel = steps["phi_ang"] / steps["second"]
    theta_step = steps["theta_ang"]
    # wrap-around: a step across the -180 / 180 boundary is really a small turn
    theta_step = theta_step.mask(theta_step > 180, theta_step - 360)
    theta_step = theta_step.mask(theta_step < -180, theta_step + 360)
    theta_vel = theta_step / steps["second"]
    ang_vel = np.sqrt(theta_vel * theta_vel + phi_vel * phi_vel)
    return {"phi_vel": phi_vel, "theta_vel": theta_vel, "ang_vel": ang_vel}
