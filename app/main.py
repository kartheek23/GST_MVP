from fastapi import FastAPI
from app.api import portal, reconciliation, agent

app = FastAPI(title="GST Agentic AI")

app.include_router(portal.router)
app.include_router(reconciliation.router)
app.include_router(agent.router)
