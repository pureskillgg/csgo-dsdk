# pylint: disable=missing-docstring
# pylint: disable=unused-import

import copy
import os
import pytest
import dateutil.parser
from pureskillgg_dsdk import GameDsLoader, DsReaderFs

from .scrub_pii import scrub_csds_pii, SCRUB_CSDS_PII_CHANNEL_INSTRUCTIONS


def test_remove_pii():
    redacted = "redacted"
    csds_reader = DsReaderFs(
        root_path=os.path.join("fixtures"),
        manifest_key=os.path.join(
            "csds", "2022", "05", "15", "9c9c6333-0eff-445f-9f18-6cb5138f944c", "csds"
        ),
        log=None,
    )
    csds_loader = GameDsLoader(reader=csds_reader, log=None)
    data = csds_loader.get_channels(SCRUB_CSDS_PII_CHANNEL_INSTRUCTIONS)
    data["player_info"]["commends_teacher"] = 12345
    manifest = copy.deepcopy(csds_loader.manifest)

    manifest = scrub_csds_pii(manifest, data)
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
    assert manifest["sharecode"] == redacted
    assert manifest["demoId"] == redacted
    assert manifest["metadata"]["bucket"] == redacted
    date = dateutil.parser.isoparse(manifest["matchDate"])
    assert date.second == 0

    scrubbed_channels = [k["channel"] for k in SCRUB_CSDS_PII_CHANNEL_INSTRUCTIONS]
    for channel in manifest["channels"]:
        if channel["channel"] in scrubbed_channels:
            assert channel["redacted"] is True
        else:
            assert channel["redacted"] is False
    assert manifest["redacted"] is True
