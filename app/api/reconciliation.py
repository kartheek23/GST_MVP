from fastapi import APIRouter
import pandas as pd
from app.services.recon_service import run_recon

router = APIRouter(prefix="/reconciliation", tags=["Reconciliation"])

@router.post("/run")
def run_reconciliation_api():
    internal_df = pd.read_excel("Purchase_Regsiter_2025_test.xlsx")
    portal_df = pd.read_excel("Purchase_Register_2025.xlsx")

    run_id = run_recon(internal_df, portal_df)

    return {
        "run_id": run_id,
        "status": "completed"
    }
