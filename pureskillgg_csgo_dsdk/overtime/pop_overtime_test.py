# pylint: disable=missing-docstring
# pylint: disable=unused-import

import os
import pytest
from pureskillgg_dsdk import GameDsLoader, DsReaderFs
import pandas as pd

from .pop_overtime import pop_overtime
from ..errors import MissingColumns, UnsupportedChannelStructure


def load_data(match_id):
    csds_reader = DsReaderFs(
        root_path=os.path.join("fixtures"),
        manifest_key=os.path.join("csds", "2022", "05", "15", match_id, "csds"),
        log=None,
    )
    csds_loader = GameDsLoader(reader=csds_reader, log=None)
    return csds_loader.get_channels([{"channel": "round_state"}, {"channel": "header"}])


def test_match_with_overtime():
    data = load_data("80e8dd2f-b876-4136-bfe5-6985bf2db179")
    original_length = data["round_state"].shape[0]
    data_overtime = {}
    data_overtime["round_state"] = pop_overtime(data["round_state"])
    assert isinstance(data["round_state"], pd.DataFrame)
    assert isinstance(data_overtime["round_state"], pd.DataFrame)
    assert data["round_state"].shape[0] < original_length
    assert data["round_state"].shape[0] > 0
    assert data_overtime["round_state"].shape[0] > 0
    assert (
        data_overtime["round_state"].shape[0] + data["round_state"].shape[0]
        == original_length
    )


def test_unsupported_channel_structure_error_usage():
    with pytest.raises(UnsupportedChannelStructure) as e_info:
        data = load_data("994a9fed-d4a5-4096-8088-93b422be5025")
        data_overtime = {}
        data_overtime["header"] = pop_overtime(data["header"])

    assert str(e_info.value) == "Cannot pop overtime: missing columns round"


def test_missing_columns_error_usage():
    with pytest.raises(MissingColumns) as e_info:
        data = load_data("994a9fed-d4a5-4096-8088-93b422be5025")
        data_overtime = {}
        data_overtime["header"] = pop_overtime(data["header"])

    assert e_info.value.columns == ["round"]
    assert str(e_info.value) == "Cannot pop overtime: missing columns round"


def test_short_match():
    data = load_data("9c9c6333-0eff-445f-9f18-6cb5138f944c")
    original_length = data["round_state"].shape[0]

    data_overtime = {}
    data_overtime["round_state"] = pop_overtime(data["round_state"])
    assert isinstance(data["round_state"], pd.DataFrame)
    assert isinstance(data["round_state"], pd.DataFrame)
    assert data["round_state"].shape[0] == original_length
    assert data_overtime["round_state"].shape[0] == 0


def test_regular_match():
    data = load_data("994a9fed-d4a5-4096-8088-93b422be5025")

    data_overtime = {}
    data_overtime["round_state"] = pop_overtime(data["round_state"])
    assert isinstance(data["round_state"], pd.DataFrame)
    assert isinstance(data_overtime["round_state"], pd.DataFrame)


@pytest.mark.parametrize(
    "rounds",
    [
        pd.array([1.0, float("nan"), 31.0, 30.0], dtype="float64"),
        pd.array([1, None, 31, 30], dtype="Int64"),
    ],
)
def test_missing_round_is_not_overtime(rounds):
    df = pd.DataFrame({"round": rounds, "x": ["a", "b", "c", "d"]})

    overtime = pop_overtime(df)

    assert list(overtime["x"]) == ["c"]
    assert list(overtime.index) == [2]
    assert list(df["x"]) == ["a", "b", "d"]
    assert list(df.index) == [0, 1, 3]
    assert df["round"].isna().sum() == 1


def test_duplicate_index_labels():
    regulation = pd.DataFrame({"round": [29, 30], "x": ["a", "b"]})
    extra_time = pd.DataFrame({"round": [31, 32], "x": ["c", "d"]})
    df = pd.concat([regulation, extra_time])

    overtime = pop_overtime(df)

    pd.testing.assert_frame_equal(df, regulation)
    pd.testing.assert_frame_equal(overtime, extra_time)


def test_removes_rows_in_place_and_keeps_order():
    df = pd.DataFrame(
        {"round": [1, 31, 2, 32, 3], "x": ["a", "b", "c", "d", "e"]},
        index=[10, 11, 12, 13, 14],
    )
    callers_df = df

    pop_overtime(df)

    assert list(callers_df["x"]) == ["a", "c", "e"]
    assert list(callers_df.index) == [10, 12, 14]
