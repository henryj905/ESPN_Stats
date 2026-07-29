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

    IDENTIFIER_COLUMNS = {"team", "player", "category"}

    # Convert only stat columns to numeric
    for column in df.columns:

        if column in IDENTIFIER_COLUMNS:
            continue

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    aggregation = {}

    for column in df.columns:

        if column in IDENTIFIER_COLUMNS:
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


def aggregate_team_stats(df, category):
    """
    Combines player season stats into team stats.

    Sums counting stats.
    Keeps highest LONG.
    Recalculates averages/percentages.
    """

    # Remove player names if they exist

    DROP_COLUMNS = {
        "QBR",
        "RTG"
    }

    if "player" in df.columns:
        df = df.drop(columns=["player"])


    # Columns that should never be summed
    skip_columns = {
        "team",
        "category"
    }

    for column in DROP_COLUMNS:
        if column in df.columns:
            df = df.drop(columns=[column])

    # Convert stats to numbers
    for column in df.columns:

        if column not in skip_columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )


    aggregation = {}


    for column in df.columns:

        if column in skip_columns:
            continue

        # Longest play/kick/punt
        if column == "LONG":
            aggregation[column] = "max"

        # Everything else gets added
        else:
            aggregation[column] = "sum"


    combined = (
        df.groupby(
            ["team"],
            as_index=False
        )
        .agg(aggregation)
    )


    # Recalculate averages
    if category == "passing":

        if "YDS" in combined and "COMP" in combined:
            combined["AVG"] = (
                combined["YDS"] /
                combined["COMP"]
            ).round(2)

        if "COMP" in combined.columns and "ATT" in combined.columns:
            combined["COMP_PCT"] = (
                    combined["COMP"] /
                    combined["ATT"] *
                    100
            ).round(2)

    elif category == "rushing":

        if "YDS" in combined and "CAR" in combined:
            combined["AVG"] = (
                combined["YDS"] /
                combined["CAR"]
            ).round(2)


    elif category == "receiving":

        if "YDS" in combined and "REC" in combined:
            combined["AVG"] = (
                combined["YDS"] /
                combined["REC"]
            ).round(2)


    elif category == "punting":

        if "YDS" in combined and "PUNTS" in combined:
            combined["AVG"] = (
                combined["YDS"] /
                combined["PUNTS"]
            ).round(2)


    elif category == "kicking":

        if "FG_MADE" in combined and "FG_ATT" in combined:
            combined["PCT"] = (
                combined["FG_MADE"] /
                combined["FG_ATT"] *
                100
            ).round(2)


    return combined
