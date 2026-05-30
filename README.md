# Zero-Human Enterprise Orchestrator (ZHEO)

> **Central control plane for the Garcar Enterprise autonomous platform.**
> Deploys, monitors, and scales all systems autonomously via a single FastAPI web API.

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Garrettc123/zero-human-orchestrator)
![GENESIS Score](https://img.shields.io/badge/GENESIS_Score-85.7-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.12-blue)

---

## What This Is

ZHEO is the command center for the Zero-Human Enterprise platform. It exposes a REST API that can:

- **Trigger deployments** across all your GitHub repos via workflow dispatch
- **Monitor system health** across the entire portfolio
- **Pull live Stripe revenue metrics** (MRR, ARR, subscriptions)
- **Query the GENESIS benchmark** — the MAUT-scored architectural roadmap for RHNS

Instead of logging into eight different dashboards, you call one endpoint.

---

## Quick Start

```bash
# Clone and run locally
git clone https://github.com/Garrettc123/zero-human-orchestrator
cd zero-human-orchestrator
pip install -r requirements.txt

export GITHUB_TOKEN=ghp_your_token
export STRIPE_SECRET_KEY=sk_live_your_key

uvicorn api.main:app --reload
# Open http://localhost:8000/docs
```

---

## API Reference

### Health
```
GET /          → Status + GENESIS score
```

### Systems
```
GET /systems   → List all 8 registered systems with tier and config
```

### Orchestration
```
POST /orchestrations/launch-business
  Body: {"systems": ["cicd", "billing", "ha"], "ref": "main"}
  → Triggers workflow_dispatch on each system's repo

POST /orchestrations/launch-all
  → Triggers all 8 systems at once
```

### Revenue
```
GET /metrics/revenue
  → {"mrr": 12500.00, "arr": 150000.00, "active_subscriptions": 42}
```

### GENESIS Benchmark
```
GET /genesis/score         → Current score: 85.7
GET /genesis/breakthroughs → All 10 MAUT-ranked breakthroughs
GET /genesis/roadmap       → Priority roadmap to score 90.0
```

---

## Systems Registry

| System Key | Repo | Tier |
|-----------|------|------|
| `cicd` | zero-human-cicd-foundation | core |
| `platform_core` | zero-human-platform-core | core |
| `data_monetization` | zero-human-data-monetization | revenue |
| `billing` | zero-human-billing-stripe | revenue |
| `revenue_agent` | revenue-agent-system | revenue |
| `ha` | ueep-ha-system | infrastructure |
| `mlops` | enterprise-mlops-platform | ai |
| `rhns` | rhns-core | ai |

---

## Deployment

### Vercel (Recommended)
1. Fork this repo
2. Connect to Vercel
3. Add environment variables (see below)
4. Push to `main` → auto-deploys

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | Yes | PAT with `repo` + `workflow` scopes |
| `GITHUB_USER` | No | Defaults to `Garrettc123` |
| `STRIPE_SECRET_KEY` | No | For revenue metrics |
| `ORCHESTRATOR_URL` | For smoke tests | Your deployed URL |

### GitHub Secrets Needed

```
VERCEL_TOKEN
VERCEL_ORG_ID
VERCEL_PROJECT_ID
GITHUB_TOKEN
STRIPE_SECRET_KEY
ORCHESTRATOR_URL
```

---

## GENESIS Score: 85.7

The platform architecture is governed by the GENESIS MAUT benchmark. The top 4 breakthroughs:

| Rank | Breakthrough | Score |
|------|-------------|-------|
| B1 | Persistent World Model Integration into RHNS | 87.7 |
| B2 | Recursive Self-Improvement Loop (RSI) | 84.9 |
| B3 | Manifold-Constrained Hyper-Connection Architecture | 84.8 |
| B4 | Neural ODE Continual Learning | 84.6 |

**Target**: 90.0 in 18 months. See [docs/genesis-maut.md](docs/genesis-maut.md) for the full roadmap.

---

## Pricing Tiers

| Tier | Price | Systems Included |
|------|-------|------------------|
| Starter | $299/mo | cicd, platform_core |
| Professional | $799/mo | + billing, data_monetization |
| Enterprise | $1,999+/mo | All 8 systems + RHNS + dedicated support |

---

## License

MIT © Garrettc123 / Garcar Enterprise
