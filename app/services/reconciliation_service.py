import pandas as pd


def reconcile_gst_invoices(internal_df: pd.DataFrame, portal_df: pd.DataFrame):
    """
    Core reconciliation logic.
    Returns categorized DataFrames.
    """

    internal_df = internal_df.copy()
    portal_df = portal_df.copy()

    internal_df["inum"] = internal_df["inum"].astype(str)
    portal_df["inum"] = portal_df["inum"].astype(str)

    df = pd.merge(
        internal_df,
        portal_df,
        on=["stin", "inum"],
        how="outer",
        suffixes=("_Books", "_Portal"),
        indicator=True
    )

    missing_in_portal = df[df["_merge"] == "left_only"]
    missing_in_books = df[df["_merge"] == "right_only"]

    matched = df[df["_merge"] == "both"].copy()

    matched["value_diff"] = (
        (matched["val_Books"].fillna(0) - matched["val_Portal"].fillna(0))
        .abs()
    )

    value_mismatch = matched[matched["value_diff"] > 0]
    exact_match = matched[matched["value_diff"] == 0]

    return {
        "MATCH": exact_match,
        "VALUE_MISMATCH": value_mismatch,
        "MISSING_IN_PORTAL": missing_in_portal,
        "MISSING_IN_BOOKS": missing_in_books
    }
