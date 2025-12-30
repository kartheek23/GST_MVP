import pandas as pd
from app.services.sandbox_gst import SandboxGSTClient


def fetch_portal_invoices(api_key, api_secret):
    client = SandboxGSTClient(api_key, api_secret)
    client.authenticate()

    df = client.fetch_b2b_invoices()

    output_file = "data/portal/portal_invoices.xlsx"
    df.to_excel(output_file, index=False)

    return {
        "rows_fetched": len(df),
        "file_saved_as": output_file
    }
