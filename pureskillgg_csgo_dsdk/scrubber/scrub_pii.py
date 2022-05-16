"""
Scrub PII from your data
"""
# pylint: disable=invalid-name
# pylint: disable=c-extension-no-member

from typing import Dict, Union
from numbers import Number
import dateutil.parser
import rapidjson

REDACTED = "redacted"

SCRUB_CSDS_PII_CHANNEL_INSTRUCTIONS = [
    {"channel": "player_name"},
    {"channel": "header"},
    {"channel": "player_personal"},
    {"channel": "player_info"},
    {"channel": "player_status"},
]


def scrub_csds_pii(manifest: Dict, data: Dict):
    """Remove events in overtime rounds

    Inputs:
        manifest (dict): CSDS manifest.
        data (dict): CSDS data dictionary.

    Returns:
        manifest (dict): CSDS manifest.
        The data is changed in place and not returned.
    """
    manifest = replace_job_id(manifest)
    manifest["sharecode"] = REDACTED
    manifest["demoId"] = REDACTED
    manifest["metadata"]["bucket"] = REDACTED
    manifest["matchDate"] = fix_date_precision(manifest["matchDate"])

    for i in range(len(manifest["channels"])):
        manifest["channels"][i]["redacted"] = False

    replace_if_exists(data, manifest, "header", "sharecode")
    replace_if_exists(data, manifest, "header", "demo_id")

    replace_if_exists(data, manifest, "player_name", "name_new")
    replace_if_exists(data, manifest, "player_name", "name_old")

    replace_if_exists(data, manifest, "player_personal", "name")
    replace_if_exists(data, manifest, "player_personal", "clan_tag")

    fix_steam_ids(data, manifest)

    fix_commends_and_wins(data, manifest)

    replace_if_exists(data, manifest, "player_status", "ping", replacement=0)

    return manifest


def data_exists(data, channel, column):
    """Check for a channel/column existing"""
    if channel in data:
        if column in data[channel].columns:
            return True
    return False


def replace_if_exists(
    data, manifest, channel, column, /, replacement: Union[str, bool, Number] = REDACTED
):
    """Replace a column with a certain value if it exists"""
    if data_exists(data, channel, column):
        data[channel][column] = replacement
        channel_index, column_index = get_manifest_indexes(manifest, channel, column)
        manifest["channels"][channel_index]["columns"][column_index][
            "origin"
        ] += "-redacted"
        manifest["channels"][channel_index]["redacted"] = True


def get_manifest_indexes(manifest, channel, column):
    """Get the indices for channel and column in the manifest"""
    channel_index = -1
    for x in range(len(manifest["channels"])):
        if manifest["channels"][x]["channel"] == channel:
            channel_index = x
            break
    if channel_index == -1:
        raise Exception(f"Channel does not exist: {channel}")
    column_index = -1
    for x in range(len(manifest["channels"][channel_index]["columns"])):
        if manifest["channels"][channel_index]["columns"][x]["name"] == column:
            column_index = x
    if column_index == -1:
        raise Exception(f"Column does not exist in channel {channel}: {column}")
    return channel_index, column_index


def fix_steam_ids(data, manifest):
    """Replace steam ids with A, B, C..."""
    if "player_personal" not in data:
        return
    pp = data["player_personal"]
    if "steam_id" not in pp.columns:
        return
    unique_ids = {}
    alphabet = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
    for i, steam_id in enumerate(pp["steam_id"].unique()):
        unique_ids[steam_id] = alphabet[i]
    pp["steam_id"] = pp["steam_id"].apply(lambda x: unique_ids[x])
    data["player_personal"] = pp
    channel_index, column_index = get_manifest_indexes(
        manifest, "player_personal", "steam_id"
    )
    manifest["channels"][channel_index]["columns"][column_index][
        "origin"
    ] += "-redacted"
    manifest["channels"][channel_index]["redacted"] = True


def fix_commends_and_wins(data, manifest):
    """Clear out too many commends and wins"""

    def cap_manifest_to_value(column, value=101):
        channel_index, column_index = get_manifest_indexes(
            manifest, "player_info", column
        )
        manifest["channels"][channel_index]["columns"][column_index][
            "origin"
        ] += "-capped"
        manifest["channels"][channel_index]["columns"][column_index][
            "comment"
        ] += f" Capped to {value}."
        manifest["channels"][channel_index]["redacted"] = True

    if "player_info" not in data:
        return
    pi = data["player_info"]
    columns = pi.columns
    if "wins" in columns:
        index = pi["wins"] > 2500
        pi.loc[index, "wins"] = 2501
        cap_manifest_to_value("wins", value=2501)
    if "commends_friendly" in columns:
        index = pi["commends_friendly"] > 100
        pi.loc[index, "commends_friendly"] = 101
        cap_manifest_to_value("commends_friendly")
    if "commends_leader" in columns:
        index = pi["commends_leader"] > 100
        pi.loc[index, "commends_leader"] = 101
        cap_manifest_to_value("commends_leader")
    if "commends_teacher" in columns:
        index = pi["commends_teacher"] > 100
        pi.loc[index, "commends_teacher"] = 101
        cap_manifest_to_value("commends_teacher")
    data["player_info"] = pi


def replace_job_id(manifest):
    """Replace job id in manifest with id"""
    job_id = manifest["jobId"]
    anon_id = manifest["id"]
    manifest_str = rapidjson.dumps(manifest)
    manifest_str = manifest_str.replace(job_id, anon_id)
    manifest = rapidjson.loads(manifest_str)
    manifest["redacted"] = True
    return manifest


def fix_date_precision(date, timespec="minutes"):
    """Set date to time precision"""
    dt = dateutil.parser.isoparse(date)
    return dt.isoformat(timespec=timespec)
