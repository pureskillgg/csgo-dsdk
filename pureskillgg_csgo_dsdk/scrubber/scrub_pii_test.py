# pylint: disable=missing-docstring

import copy
import os
import pandas as pd
import pytest
import dateutil.parser
from pureskillgg_dsdk import GameDsLoader, DsReaderFs

from .scrub_pii import (
    scrub_csds_pii,
    csds_pii_channel_instructions,
    replace_if_exists,
    WINS_CAP_VALUE,
)


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
    instructions = csds_pii_channel_instructions(csds_loader.manifest)
    data = csds_loader.get_channels(instructions)
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

    scrubbed_channels = [k["channel"] for k in instructions]
    for channel in manifest["channels"]:
        if channel["channel"] in scrubbed_channels:
            assert channel["redacted"] is True
        else:
            assert channel["redacted"] is False
    assert manifest["redacted"] is True


def _manifest(*channels):
    return {
        "jobId": "job-1",
        "id": "anon-1",
        "sharecode": "CSGO-abc",
        "demoId": "demo-1",
        "matchDate": "2026-07-30T12:34:56.789Z",
        "metadata": {"bucket": "a-bucket"},
        "channels": [
            {
                "channel": name,
                "columns": [
                    {"name": col, "origin": "replay", "comment": ""} for col in cols
                ],
            }
            for name, cols in channels
        ],
    }


def test_redacts_chat_text():
    manifest = _manifest(("player_chat", ["round", "tick", "player_id", "text"]))
    data = {
        "player_chat": pd.DataFrame(
            {"round": [1], "tick": [10], "player_id": [3], "text": ["gg wp add me"]}
        )
    }

    manifest = scrub_csds_pii(manifest, data)

    assert list(data["player_chat"]["text"]) == ["redacted"]
    # who talked and when survives; only the content goes
    assert list(data["player_chat"]["player_id"]) == [3]
    chat = manifest["channels"][0]
    assert chat["redacted"] is True
    text_col = [c for c in chat["columns"] if c["name"] == "text"][0]
    assert text_col["origin"].endswith("-redacted")


def test_redacts_the_server_session_convar():
    manifest = _manifest(("convar", ["round", "tick", "name", "value"]))
    data = {
        "convar": pd.DataFrame(
            {
                "round": [0, 1],
                "tick": [0, 84],
                "name": ["mp_maxrounds", "steamworks_sessionid_server"],
                "value": ["24", "8947377548882"],
            }
        )
    }

    manifest = scrub_csds_pii(manifest, data)

    # the setting and its tick stay; only the session id goes
    assert list(data["convar"]["value"]) == ["24", "redacted"]
    assert list(data["convar"]["name"]) == [
        "mp_maxrounds",
        "steamworks_sessionid_server",
    ]
    convar = manifest["channels"][0]
    assert convar["redacted"] is True
    value_col = [c for c in convar["columns"] if c["name"] == "value"][0]
    assert value_col["origin"].endswith("-redacted")
    assert value_col["comment"].endswith(
        "Redacted for mp_guardian_bomb_plant_custom_x_mark_location,"
        " steamworks_sessionid_server."
    )


def test_redacts_the_faceit_match_id_convar():
    # FACEIT servers put their match id in this Guardian-mode setting
    manifest = _manifest(("convar", ["round", "tick", "name", "value"]))
    data = {
        "convar": pd.DataFrame(
            {
                "round": [0, 0, 0],
                "tick": [0, 0, 0],
                "name": [
                    "mp_guardian_bomb_plant_custom_x_mark_location",
                    "mp_freezetime",
                    # names are case-insensitive in the engine
                    "MP_Guardian_Bomb_Plant_Custom_X_Mark_Location",
                ],
                "value": [
                    "1-00000000-0000-0000-0000-000000000000-1-1",
                    "15",
                    "1-00000000-0000-0000-0000-000000000000-1-1",
                ],
            }
        )
    }

    scrub_csds_pii(manifest, data)

    assert list(data["convar"]["value"]) == ["redacted", "15", "redacted"]
    assert list(data["convar"]["name"]) == [
        "mp_guardian_bomb_plant_custom_x_mark_location",
        "mp_freezetime",
        "MP_Guardian_Bomb_Plant_Custom_X_Mark_Location",
    ]


def test_redacts_the_team_names_that_are_set():
    manifest = _manifest(
        ("team_info", ["round", "tick", "team_code", "clan_name", "flag"])
    )
    data = {
        "team_info": pd.DataFrame(
            {
                "round": [0, 0, 1, 1],
                "tick": [0, 0, 10, 10],
                "team_code": pd.Series([2, 3, 2, 3], dtype="int32"),
                "clan_name": ["team_somebody", "team_other", "", None],
                "flag": ["", "", "", ""],
            }
        )
    }

    manifest = scrub_csds_pii(manifest, data)

    ti = data["team_info"]
    # FACEIT names a team after a player; an empty name (Valve) stays as sent
    assert list(ti["clan_name"][:3]) == ["redacted", "redacted", ""]
    assert pd.isna(ti["clan_name"].iat[3])
    assert list(ti["team_code"]) == [2, 3, 2, 3]
    team_info = manifest["channels"][0]
    assert team_info["redacted"] is True
    name_col = [c for c in team_info["columns"] if c["name"] == "clan_name"][0]
    assert name_col["origin"].endswith("-redacted")
    assert name_col["comment"].endswith("Redacted where set; empty stays empty.")
    flag_col = [c for c in team_info["columns"] if c["name"] == "flag"][0]
    assert flag_col["origin"] == "replay"


def test_team_info_is_read_only_when_the_csds_has_it():
    with_it = _manifest(("team_info", ["clan_name"]), ("header", ["demo_id"]))
    without = _manifest(("header", ["demo_id"]))

    assert {"channel": "team_info"} in csds_pii_channel_instructions(with_it)
    assert {"channel": "team_info"} not in csds_pii_channel_instructions(without)


def test_redacts_the_client_settings():
    settings = [
        "viewmodel_offset_x",
        "viewmodel_offset_y",
        "viewmodel_offset_z",
        "viewmodel_fov",
    ]
    manifest = _manifest(
        (
            "player_personal",
            ["round", "player_id", "steam_id", "crosshair_code"] + settings,
        )
    )
    data = {
        "player_personal": pd.DataFrame(
            {
                "round": [1, 1],
                "player_id": [3, 4],
                "steam_id": ["76561190000000001", "76561190000000002"],
                "crosshair_code": ["CSGO-aaaaa-bbbbb-ccccc-ddddd-eeeee", None],
                "viewmodel_offset_x": pd.Series([1.0, 2.5], dtype="float32"),
                "viewmodel_offset_y": pd.Series([1.0, 0.0], dtype="float32"),
                "viewmodel_offset_z": pd.Series([-1.0, -1.5], dtype="float32"),
                "viewmodel_fov": pd.Series([60.0, 68.0], dtype="float32"),
            }
        )
    }

    manifest = scrub_csds_pii(manifest, data)

    pp = data["player_personal"]
    # the rows stay; the crosshair code and the viewmodel settings go
    assert list(pp["player_id"]) == [3, 4]
    assert list(pp["crosshair_code"]) == ["redacted", "redacted"]
    for column in settings:
        assert pp[column].dtype == "float32", column
        assert pp[column].isna().all(), column
    personal = manifest["channels"][0]
    assert personal["redacted"] is True
    for col in personal["columns"]:
        if col["name"] in ["crosshair_code"] + settings:
            assert col["origin"].endswith("-redacted"), col["name"]


def test_convar_is_read_only_when_the_csds_has_it():
    with_it = _manifest(("convar", ["name", "value"]), ("header", ["demo_id"]))
    without = _manifest(("header", ["demo_id"]))

    assert {"channel": "convar"} in csds_pii_channel_instructions(with_it)
    assert {"channel": "convar"} not in csds_pii_channel_instructions(without)


@pytest.mark.parametrize("dtype", ["int16", "Int16", "int64", "Int64"])
def test_redacted_ping_keeps_its_dtype(dtype):
    # narrower csds store ping as int16; the zero that replaces it stays int16
    manifest = _manifest(("player_status", ["tick", "ping"]))
    data = {
        "player_status": pd.DataFrame(
            {"tick": [10, 11], "ping": pd.Series([35, 40], dtype=dtype)}
        )
    }

    manifest = scrub_csds_pii(manifest, data)

    assert data["player_status"]["ping"].dtype == dtype
    assert list(data["player_status"]["ping"]) == [0, 0]
    assert manifest["channels"][0]["redacted"] is True


def test_a_number_that_does_not_fit_the_column_raises():
    manifest = _manifest(("player_status", ["ping"]))
    data = {"player_status": pd.DataFrame({"ping": pd.Series([1, 2], dtype="int8")})}

    with pytest.raises((OverflowError, TypeError, ValueError)):
        replace_if_exists(data, manifest, "player_status", "ping", replacement=1000)


def test_caps_rank_update_win_count_like_player_info_wins():
    # rank_update.win_count is the same quantity as player_info.wins, which is
    # already capped -- an uncapped copy in a new channel would leak around it
    manifest = _manifest(("rank_update", ["round", "tick", "player_id", "win_count"]))
    data = {
        "rank_update": pd.DataFrame(
            {
                "round": [1, 1],
                "tick": [10, 11],
                "player_id": [3, 4],
                "win_count": [99999, 12],
            }
        )
    }

    manifest = scrub_csds_pii(manifest, data)

    assert list(data["rank_update"]["win_count"]) == [WINS_CAP_VALUE, 12]
    assert manifest["channels"][0]["redacted"] is True


def test_leaves_a_csds_without_the_new_channels_alone():
    # pre-overhaul CSDS in S3 carry neither channel
    manifest = _manifest(("header", ["sharecode", "demo_id"]))
    data = {}

    manifest = scrub_csds_pii(manifest, data)

    assert manifest["redacted"] is True


def test_instructions_are_filtered_to_what_the_csds_has():
    # a CSDS written before player_chat existed must not ask for it: the loader
    # raises on a channel missing from the manifest
    old = _manifest(("header", ["sharecode"]), ("player_status", ["ping"]))
    names = [i["channel"] for i in csds_pii_channel_instructions(old)]
    assert names == ["header", "player_status"]

    new = _manifest(("player_chat", ["text"]), ("rank_update", ["win_count"]))
    names = [i["channel"] for i in csds_pii_channel_instructions(new)]
    assert sorted(names) == ["player_chat", "rank_update"]
