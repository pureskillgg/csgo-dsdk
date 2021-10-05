"""
Remove overtime from your data
"""

from typing import Dict, Union
import pandas as pd
from ..errors import MissingColumns


def pop_overtime(
    df: pd.DataFrame,
    /,
    *,
    max_rounds_csgo: int = 30,
) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """Remove events in overtime rounds

    Keywords:
        df (dataframe): Any individual channel with a "round" column.
        max_rounds_csgo (int): Default value: 30
            Max rounds of CS:GO for regular-time. This is 30 for normal
            matches and 16 for short matches.

    Returns:
        data (dataframe): The removed events.

    Examples:
        >>> pop_overtime(df)

        >>> df_ot = pop_overtime(df)

    """
    if "round" not in df.columns:
        raise MissingColumns("Cannot pop overtime", columns=["round"])
    overtime = df[df["round"] > max_rounds_csgo]
    index = df.index[~(df["round"] <= max_rounds_csgo)]
    df.drop(index, inplace=True)
    return overtime
