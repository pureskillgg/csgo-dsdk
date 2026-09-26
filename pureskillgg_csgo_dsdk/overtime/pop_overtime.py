"""
Remove overtime from your data
"""

import pandas as pd
from ..errors import MissingColumns


def pop_overtime(
    df: pd.DataFrame,
    /,
    *,
    max_rounds_csgo: int = 30,
) -> pd.DataFrame:
    """Remove events in overtime rounds

    The overtime rows are removed from df in place and returned. A row whose
    round is missing is not overtime and stays in df.

    Keywords:
        df (dataframe): Any individual channel with a "round" column.
        max_rounds_csgo (int): Default value: 30
            The number of regulation rounds; any later round is overtime.
            The default 30 is CS:GO MR15 (a short CS:GO match is 16).
            CS2 regulation is MR12, 24 rounds, so CS2 callers should pass 24.

    Returns:
        data (dataframe): The removed events, with their original index labels.

    Examples:
        >>> pop_overtime(df)

        >>> df_ot = pop_overtime(df)

        >>> df_ot = pop_overtime(df, max_rounds_csgo=24)  # CS2

    """
    if "round" not in df.columns:
        raise MissingColumns("Cannot pop overtime", columns=["round"])
    is_overtime = (df["round"] > max_rounds_csgo).to_numpy(dtype=bool, na_value=False)
    overtime = df[is_overtime]
    if is_overtime.any():
        # drop() is label-based, so it would also remove rows that share a
        # label with an overtime row. Drop by position, then restore labels.
        kept_index = df.index[~is_overtime]
        df.index = pd.RangeIndex(len(df))
        df.drop(df.index[is_overtime], inplace=True)
        df.index = kept_index
    return overtime
