from fastapi import APIRouter
from app.services.recon_service import run_recon

router = APIRouter(prefix="/reconciliation", tags=["Reconciliation"])

@router.post("/run")
def run_reconciliation():
    # For MVP, files are assumed present
    import pandas as pd

    internal_df = pd.read_excel("data/portal/portal_invoices.xlsx")
    portal_df = pd.read_excel("data/portal/portal_invoices_test.xlsx")

    run_id = run_recon(internal_df, portal_df)

    return {
        "status": "success",
        "run_id": run_id
    }
