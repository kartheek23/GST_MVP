def decide_ims_action(row):
    status = row["match_status"]

    if status == "MATCH":
        return "ACCEPT", "Exact match between Books and Portal."
    elif status == "MISSING_IN_PORTAL":
        return "WAIT", "Invoice not present in GSTR-2B / IMS"
    elif status == "MISSING_IN_BOOKS":
        return "RECORD", "Invoice missing in books"
    elif status == "VALUE_MISMATCH":
        diff = abs((row["val_books"] or 0) - (row["val_portal"] or 0))
        return "REJECT", f"Value Mismatch of {diff}"
    else:
        return "REVIEW", "Manual review required"
