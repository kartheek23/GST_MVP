def decide_ims_action(row: dict):
    """
    Stateless agent decision logic.
    Input: dict with match_status, val_books, val_portal
    """

    status = row["match_status"]

    if status == "MATCH":
        return "ACCEPT", "Exact match between Books and Portal."

    if status == "MISSING_IN_PORTAL":
        return "WAIT", "Invoice not present in GSTR-2B / IMS."

    if status == "MISSING_IN_BOOKS":
        return "RECORD", "Invoice missing in books."

    if status == "VALUE_MISMATCH":
        val_books = row["val_books"] or 0
        val_portal = row["val_portal"] or 0
        diff = abs(val_books - val_portal)
        return "REJECT", f"Value mismatch of {diff}"

    return "REVIEW", "Manual review required."
