from fastapi import APIRouter
from app.services.sandbox_gst import SandboxGSTClient

router = APIRouter(prefix='/portal', tags=['portal'])
@router.post('/fetch')
def fetch_portal(api_key: str, api_secret: str):
    client = SandboxGSTClient(api_key, api_secret):
    client.authenticate()
    df = client.fetch_b2b_invoices()

    df.to_excel('Purchase_Register_2025.xlsx', index=False)

    return {
        "status": "success",
        "invoices_fetched": len(df)
    }