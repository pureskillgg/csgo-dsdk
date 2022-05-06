# pylint: disable=missing-docstring
# pylint: disable=unused-import

import copy
import os
import pytest
from pureskillgg_dsdk import GameDsLoader, DsReaderFs

from .scrub_pii import scrub_csds_pii


def test_remove_pii():
    redacted = "redacted"
    csds_reader = DsReaderFs(
        root_path=os.path.join("fixtures"),
        manifest_key=os.path.join("Y0C7ADW4AZEHSMxKlrFs", "csds"),
        log=None,
    )
    csds_loader = GameDsLoader(reader=csds_reader, log=None)
    data = csds_loader.get_channels(
        [
            {"channel": "player_name"},
            {"channel": "header"},
            {"channel": "player_personal"},
            {"channel": "player_info"},
            {"channel": "player_status", "columns": ["ping"]},
        ]
    )
    data["player_info"]["commends_teacher"] = 12345
    manifest = copy.deepcopy(csds_loader.manifest)

    manifest = scrub_csds_pii(data, manifest)
    assert data["header"]["sharecode"].iat[0] == redacted
    assert data["header"]["demo_id"].iat[0] == redacted
    assert data["player_personal"]["clan_tag"].iat[0] == redacted
    assert data["player_personal"]["name"].iat[0] == redacted
    steam_ids = data["player_personal"]["steam_id"]
    for steam_id in steam_ids:
        assert len(steam_id) == 1
    assert data["player_status"]["ping"].iat[100] == 0
    assert data["player_info"]["commends_teacher"].iat[0] == 101
    assert manifest["jobId"] == manifest["id"]
