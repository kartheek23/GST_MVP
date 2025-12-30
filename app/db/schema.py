import sqlite3
import os,sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_code TEXT UNIQUE,
            legal_name TEXT,
            created_at TEXT
        );

        CREATE TABLE  IF NOT EXISTS gstins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            gstin TEXT,
            state_code TEXT,
            created_at TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        );


        CREATE TABLE IF NOT EXISTS periods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gstin_id INTEGER,
            period TEXT, -- e.g. 2024-11
            return_type TEXT, -- GSTR-2B
            created_at TEXT,
            FOREIGN KEY (gstin_id) REFERENCES gstins(id)
        );


        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT UNIQUE,
            client_id INTEGER,
            period_id INTEGER,
            source_books TEXT, -- Excel, Tally, API
            source_portal TEXT, -- GST API
            created_at TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (period_id) REFERENCES periods(id)
        );

        CREATE TABLE IF NOT EXISTS reconciliation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id TEXT,

            gstin TEXT,
            stin TEXT,
            inum TEXT,
            invoice_date TEXT,

            match_status TEXT,
            -- MATCH | MISSING_IN_PORTAL | MISSING_IN_BOOKS | VALUE_MISMATCH

            reconciliation_action TEXT,
            -- ACCEPT | WAIT | RECORD | REJECT | REVIEW

            agent_reason TEXT,

            txval_books REAL,
            txval_portal REAL,
            val_books REAL,
            val_portal REAL,

            created_at TEXT,

            FOREIGN KEY (run_id) REFERENCES runs(run_id)
        );


        CREATE TABLE IF NOT EXISTS agent_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT,
            recon_id INTEGER,

            agent_decision TEXT,
            -- ACCEPT | REJECT | WAIT | REVIEW

            explanation TEXT,
            confidence REAL,

            next_retry_at TEXT,
            human_override INTEGER DEFAULT 0,

            created_at TEXT,
            FOREIGN KEY (recon_id) REFERENCES reconciliation_results(id)
        );

        CREATE TABLE IF NOT EXISTS ims_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_action_id INTEGER,
            ims_action TEXT, -- ACCEPT / REJECT
            ims_reference TEXT,
            status TEXT, -- SUCCESS / FAILED
            error_message TEXT,
            submitted_at TEXT,
            FOREIGN KEY (agent_action_id) REFERENCES agent_actions(id)
        );

        CREATE TABLE IF NOT EXISTS supplier_scores (
            stin TEXT,
            period TEXT,
            total_invoices INTEGER,
            mismatches INTEGER,
            compliance_score REAL,
            created_at TEXT
        );

    """)
    conn.commit()
    conn.close()