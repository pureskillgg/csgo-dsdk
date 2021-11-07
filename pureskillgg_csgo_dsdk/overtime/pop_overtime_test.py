# pylint: disable=missing-docstring
# pylint: disable=unused-import

import os
import pytest
from pureskillgg_dsdk import GameDsLoader, DsReaderFs
import pandas as pd
import structlog

from .pop_overtime import pop_overtime
from ..errors import MissingColumns, UnsupportedChannelStructure


def load_data(job_id):
    csds_reader = DsReaderFs(
        root_path=os.path.join("fixtures"),
        manifest_key=os.path.join(job_id, "csds"),
        log=None,
    )
    csds_loader = GameDsLoader(reader=csds_reader, log=None)
    return csds_loader.get_channels([{"channel": "round_state"}, {"channel": "header"}])


def test_match_with_overtime():
    data = load_data("Y0C7ADW4AZEHSMxKlrFs")
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
        data = load_data("Y0C7ADW4AZEHSMxKlrFs")
        data_overtime = {}
        data_overtime["header"] = pop_overtime(data["header"])

    assert str(e_info.value) == "Cannot pop overtime: missing columns round"


def test_missing_columns_error_usage():
    with pytest.raises(MissingColumns) as e_info:
        data = load_data("Y0C7ADW4AZEHSMxKlrFs")
        data_overtime = {}
        data_overtime["header"] = pop_overtime(data["header"])

    assert e_info.value.columns == ["round"]
    assert str(e_info.value) == "Cannot pop overtime: missing columns round"


def test_short_match():
    data = load_data("xgcHI9wjH5aKCf5hF578")
    original_length = data["round_state"].shape[0]

    data_overtime = {}
    data_overtime["round_state"] = pop_overtime(data["round_state"])
    assert isinstance(data["round_state"], pd.DataFrame)
    assert isinstance(data["round_state"], pd.DataFrame)
    assert data["round_state"].shape[0] == original_length
    assert data_overtime["round_state"].shape[0] == 0


def test_regular_match():
    data = load_data("Z2ZVbsBleCmXZVZ9bFuL")

    data_overtime = {}
    data_overtime["round_state"] = pop_overtime(data["round_state"])
    assert isinstance(data["round_state"], pd.DataFrame)
    assert isinstance(data_overtime["round_state"], pd.DataFrame)


test_unsupported_channel_structure_error_usage()
test_missing_columns_error_usage()
