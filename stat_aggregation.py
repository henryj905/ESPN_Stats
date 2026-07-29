import pandas as pd


AVERAGE_COLUMNS = {
    "passing": ["AVG", "QBR", "RTG"],
    "rushing": ["AVG"],
    "receiving": ["AVG"],
    "punting": ["AVG"],
    "kicking": ["PCT"]
}


MAX_COLUMNS = {
    "passing": ["LONG"],
    "rushing": ["LONG"],
    "receiving": ["LONG"],
    "punting": ["LONG"],
    "kicking": ["LONG"]
}


def aggregate_stats(df, category, group_columns):
    """
    Aggregates statistics.

    Parameters
    ----------
    df : DataFrame
        Data to aggregate.

    category : str
        passing, rushing, receiving, etc.

    group_columns : list
        Columns to group by.
        Example:
            ["team", "player", "category"]
        or
            ["team"]
    """

    # Convert every stat column to numeric
    for column in df.columns:

        if column not in group_columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    aggregation = {}

    for column in df.columns:

        if column in group_columns:
            continue

        if column in AVERAGE_COLUMNS.get(category, []):
            aggregation[column] = "mean"

        elif column in MAX_COLUMNS.get(category, []):
            aggregation[column] = "max"

        else:
            aggregation[column] = "sum"

    combined = (
        df.groupby(
            group_columns,
            as_index=False
        )
        .agg(aggregation)
    )

    # Round averages
    for column in AVERAGE_COLUMNS.get(category, []):

        if column in combined.columns:
            combined[column] = combined[column].round(2)

    return combined