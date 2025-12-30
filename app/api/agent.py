from fastapi import APIRouter
from app.db.connection import get_db_connection
from app.services.agent_service import decide_ims_action

router = APIRouter(prefix="/agent", tags=["Agent"])

@router.post("/decide")
def run_agent(run_id: str):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM reconciliation_results
        WHERE run_id = ?
    """, (run_id,))

    results = []
    for row in cur.fetchall():
        action, reason = decide_ims_action(row)
        results.append({
            "inum": row["inum"],
            "status": row["match_status"],
            "action": action,
            "reason": reason
        })

    conn.close()
    return results
