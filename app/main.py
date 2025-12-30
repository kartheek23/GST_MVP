from fastapi import FastAPI

from app.api import portal, reconciliation, agent
from app.db.schema import init_db

def create_app():
    app = FastAPI(title="GST Agentic AI")

    # Initialize DB schema ONCE
    init_db()

    # Register routers
    app.include_router(portal.router)
    app.include_router(reconciliation.router)
    app.include_router(agent.router)

    return app

app = create_app()
