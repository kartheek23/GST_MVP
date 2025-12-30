import pandas as pd
import numpy as np
import uuid
from datetime import datetime

from app.db.connection import get_db_connection


# -------------------------------
# CORE RECONCILIATION LOGIC
# -------------------------------
def reconcile_gst_invoices(internal_df, portal_df):
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

    return {
        "MATCH": df[df["_merge"] == "both"],
        "MISSING_IN_PORTAL": df[df["_merge"] == "left_only"],
        "MISSING_IN_BOOKS": df[df["_merge"] == "right_only"]
    }


# -------------------------------
# PERSIST RESULTS (SINGLE PATH)
# -------------------------------
def persist_results(run_id, status, action, df):
    if df.empty:
        return

    conn = get_db_connection()

    rows = []
    for _, r in df.iterrows():
        rows.append((
            run_id,
            r.get("stin"),
            r.get("inum"),
            status,
            action,
            r.get("txval_Books"),
            r.get("txval_Portal"),
            r.get("val_Books"),
            r.get("val_Portal"),
            r.get("idt_Books"),
            datetime.utcnow().isoformat()
        ))

    conn.executemany("""
        INSERT INTO reconciliation_results (
            run_id, stin, inum, match_status, reconciliation_action,
            txval_books, txval_portal, val_books, val_portal,
            invoice_date, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)

    conn.commit()
    conn.close()


# -------------------------------
# ORCHESTRATOR (SINGLE ENTRYPOINT)
# -------------------------------
def run_reconciliation(internal_df, portal_df):
    run_id = str(uuid.uuid4())
    results = reconcile_gst_invoices(internal_df, portal_df)

    persist_results(run_id, "MATCH", "Matched (Accept in IMS)", results["MATCH"])
    persist_results(run_id, "MISSING_IN_PORTAL", "Missing in Portal", results["MISSING_IN_PORTAL"])
    persist_results(run_id, "MISSING_IN_BOOKS", "Missing in Books", results["MISSING_IN_BOOKS"])

    return run_id
