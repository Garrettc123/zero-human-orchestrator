# api/main.py — Zero-Human Enterprise Orchestrator
import os
import json
from pathlib import Path
from typing import Dict, List, Optional

import httpx
import stripe
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── env ──────────────────────────────────────────────────────────────────────
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_USER  = os.getenv("GITHUB_USER", "Garrettc123")
STRIPE_KEY   = os.getenv("STRIPE_SECRET_KEY", "")

if STRIPE_KEY:
    stripe.api_key = STRIPE_KEY

# ── app ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Zero-Human Enterprise Orchestrator",
    description="Central control plane for the Garcar Enterprise autonomous platform.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── systems registry ─────────────────────────────────────────────────────────
SYSTEMS: Dict[str, Dict] = {
    "cicd": {
        "repo": "zero-human-cicd-foundation",
        "workflow": "deploy.yml",
        "health_url": "",
        "tier": "core",
    },
    "data_monetization": {
        "repo": "zero-human-data-monetization",
        "workflow": "deploy.yml",
        "health_url": "",
        "tier": "revenue",
    },
    "platform_core": {
        "repo": "zero-human-platform-core",
        "workflow": "deploy.yml",
        "health_url": "",
        "tier": "core",
    },
    "billing": {
        "repo": "zero-human-billing-stripe",
        "workflow": "deploy.yml",
        "health_url": "",
        "tier": "revenue",
    },
    "ha": {
        "repo": "ueep-ha-system",
        "workflow": "deploy.yml",
        "health_url": "",
        "tier": "infrastructure",
    },
    "mlops": {
        "repo": "enterprise-mlops-platform",
        "workflow": "deploy.yml",
        "health_url": "",
        "tier": "ai",
    },
    "revenue_agent": {
        "repo": "revenue-agent-system",
        "workflow": "deploy.yml",
        "health_url": "",
        "tier": "revenue",
    },
    "rhns": {
        "repo": "rhns-core",
        "workflow": "deploy.yml",
        "health_url": "",
        "tier": "ai",
    },
}

# ── GENESIS scores ───────────────────────────────────────────────────────────
GENESIS_DATA = {
    "attributes": [
        {"name": "RHNS Integration",          "weight": 0.30},
        {"name": "Architectural Novelty",      "weight": 0.25},
        {"name": "Zero-Human Operability",     "weight": 0.20},
        {"name": "Implementation Feasibility", "weight": 0.15},
        {"name": "Commercial Leverage",        "weight": 0.10},
    ],
    "breakthroughs": [
        {"id": "B1",  "name": "Persistent World Model Integration into RHNS",      "maut_score": 87.7},
        {"id": "B2",  "name": "Recursive Self-Improvement Loop (RSI)",              "maut_score": 84.9},
        {"id": "B3",  "name": "Manifold-Constrained Hyper-Connection Architecture", "maut_score": 84.8},
        {"id": "B4",  "name": "Neural ODE Continual Learning",                      "maut_score": 84.6},
        {"id": "B5",  "name": "Agentic Mesh Network Protocol Layer",                "maut_score": 83.4},
        {"id": "B6",  "name": "Hyperdimensional Computing (VSA) Working Memory",   "maut_score": 80.7},
        {"id": "B7",  "name": "Metacognitive Confidence Calibration Engine",        "maut_score": 80.6},
        {"id": "B8",  "name": "Neuro-Symbolic AI Hardware Co-Design",               "maut_score": 77.4},
        {"id": "B9",  "name": "Emotion-Aligned Decision Weighting",                 "maut_score": 78.3},
        {"id": "B10", "name": "Formal Verification Layer for Symbolic Reasoning",   "maut_score": 79.4},
    ],
    "genesis_score": {"baseline": 85.7, "components": ["B1", "B3", "B4"]},
}

# ── models ───────────────────────────────────────────────────────────────────
class LaunchRequest(BaseModel):
    systems: List[str]
    ref: str = "main"

class OrchestrationResult(BaseModel):
    systems: Dict[str, str]
    triggered: int
    failed: int

# ── helpers ──────────────────────────────────────────────────────────────────
async def dispatch_workflow(repo: str, workflow: str, ref: str = "main") -> bool:
    if not GITHUB_TOKEN:
        return False
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/actions/workflows/{workflow}/dispatches"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(url, json={"ref": ref}, headers=headers)
        return 200 <= r.status_code < 300

# ── routes ───────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "service": "Zero-Human Enterprise Orchestrator",
        "version": "1.0.0",
        "status": "operational",
        "systems_registered": len(SYSTEMS),
        "genesis_score": GENESIS_DATA["genesis_score"]["baseline"],
    }

@app.get("/systems", tags=["Systems"])
async def list_systems():
    return {"systems": SYSTEMS, "total": len(SYSTEMS)}

@app.post("/orchestrations/launch-business", response_model=OrchestrationResult, tags=["Orchestration"])
async def launch_business(payload: LaunchRequest):
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=500, detail="GITHUB_TOKEN not configured")
    results: Dict[str, str] = {}
    for system in payload.systems:
        config = SYSTEMS.get(system)
        if not config:
            results[system] = "unknown-system"
            continue
        ok = await dispatch_workflow(config["repo"], config["workflow"], payload.ref)
        results[system] = "triggered" if ok else "failed"
    triggered = sum(1 for v in results.values() if v == "triggered")
    failed    = sum(1 for v in results.values() if v == "failed")
    return OrchestrationResult(systems=results, triggered=triggered, failed=failed)

@app.post("/orchestrations/launch-all", response_model=OrchestrationResult, tags=["Orchestration"])
async def launch_all(ref: str = "main"):
    payload = LaunchRequest(systems=list(SYSTEMS.keys()), ref=ref)
    return await launch_business(payload)

@app.get("/metrics/revenue", tags=["Revenue"])
async def revenue_metrics():
    if not STRIPE_KEY:
        return {"error": "STRIPE_SECRET_KEY not configured", "mrr": 0, "arr": 0, "customers": 0}
    try:
        subs = stripe.Subscription.list(status="active", limit=100)
        mrr = sum(
            (item.price.unit_amount or 0) / 100
            for sub in subs.auto_paging_iter()
            for item in sub["items"]["data"]
        )
        customers = stripe.Customer.list(limit=1)
        return {
            "mrr": round(mrr, 2),
            "arr": round(mrr * 12, 2),
            "active_subscriptions": subs.total_count if hasattr(subs, 'total_count') else len(subs.data),
            "currency": "usd",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/genesis/score", tags=["GENESIS"])
async def genesis_score():
    return GENESIS_DATA["genesis_score"]

@app.get("/genesis/breakthroughs", tags=["GENESIS"])
async def genesis_breakthroughs():
    return {"breakthroughs": GENESIS_DATA["breakthroughs"], "attributes": GENESIS_DATA["attributes"]}

@app.get("/genesis/roadmap", tags=["GENESIS"])
async def genesis_roadmap():
    top4 = sorted(GENESIS_DATA["breakthroughs"], key=lambda x: x["maut_score"], reverse=True)[:4]
    return {
        "priority_order": top4,
        "target_genesis_score": 90.0,
        "timeline_months": 18,
        "current_baseline": GENESIS_DATA["genesis_score"]["baseline"],
    }
