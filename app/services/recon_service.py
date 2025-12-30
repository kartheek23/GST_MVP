from api.reconciliation import run_reconciliation
def run_recon(internal_df, portal_df):
    run_id = run_reconciliation(internal_df, portal_df)
    return run_id