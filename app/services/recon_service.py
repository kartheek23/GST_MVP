import uuid
from datetime import datetime
import pandas as pd

from app.db.connection import get_db_connection
from app.services.reconciliation_service import reconcile_gst_invoices
from app.services.agent_service import decide_ims_action


def run_recon(internal_df: pd.DataFrame, portal_df: pd.DataFrame) -> str:
    """
    Orchestrates reconciliation + agent decisions + persistence.
    """

    run_id = str(uuid.uuid4())
    conn = get_db_connection()

    results = reconcile_gst_invoices(internal_df, portal_df)

    rows_to_insert = []

    for status, df in results.items():
        for _, row in df.iterrows():

            action, reason = decide_ims_action({
                "match_status": status,
                "val_books": row.get("val_Books"),
                "val_portal": row.get("val_Portal")
            })

            rows_to_insert.append((
                run_id,
                row.get("stin"),
                row.get("inum"),
                status,
                action,
                reason,
                row.get("txval_Books"),
                row.get("txval_Portal"),
                row.get("val_Books"),
                row.get("val_Portal"),
                row.get("idt_Books"),
                datetime.utcnow().isoformat()
            ))

    conn.executemany("""
        INSERT INTO reconciliation_results (
            run_id,
            stin,
            inum,
            match_status,
            reconciliation_action,
            agent_reason,
            txval_books,
            txval_portal,
            val_books,
            val_portal,
            invoice_date,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rows_to_insert)

    conn.commit()
    conn.close()

    return run_id
