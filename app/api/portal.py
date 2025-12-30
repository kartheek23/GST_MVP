from fastapi import APIRouter
from app.services.portal_service import fetch_portal_invoices

router = APIRouter(prefix="/portal", tags=["Portal"])

@router.post("/fetch")
def fetch_portal(api_key: str, api_secret: str):
    df = fetch_portal_invoices(api_key, api_secret)

    return {
        "status": "success",
        "invoices_fetched": len(df)
    }
