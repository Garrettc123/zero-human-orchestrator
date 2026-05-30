# Zero-Human Enterprise Orchestrator — Architecture

## Overview

The Zero-Human Enterprise Orchestrator (ZHEO) is the central control plane for the Garcar Enterprise autonomous platform. It exposes a FastAPI web API hosted on Vercel that can deploy, monitor, and orchestrate all systems in the portfolio via GitHub Actions workflow dispatches.

## System Map

```
                  +---------------------------+
                  |  ZHEO FastAPI (Vercel)    |
                  |  zero-human-orchestrator  |
                  +---------------------------+
                           |
          +----------------+----------------+
          |                |                |
   +------+------+  +------+------+  +------+------+
   | zero-human  |  | zero-human  |  | ueep-ha-    |
   | cicd-found  |  | billing-    |  | system      |
   | -ation      |  | stripe      |  +-------------+
   +-------------+  +-------------+
          |                |
   +------+------+  +------+------+
   | enterprise  |  | revenue-    |
   | mlops-plat  |  | agent-sys   |
   | form        |  | tem         |
   +-------------+  +-------------+
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check + GENESIS score |
| GET | `/systems` | List all registered systems |
| POST | `/orchestrations/launch-business` | Trigger selected systems |
| POST | `/orchestrations/launch-all` | Trigger all systems |
| GET | `/metrics/revenue` | Stripe MRR/ARR dashboard |
| GET | `/genesis/score` | Current GENESIS benchmark score |
| GET | `/genesis/breakthroughs` | All 10 MAUT-ranked breakthroughs |
| GET | `/genesis/roadmap` | Priority roadmap to GENESIS 90.0 |

## System Tiers

- **core**: CICD, Platform Core
- **revenue**: Data Monetization, Billing/Stripe, Revenue Agent
- **infrastructure**: HA System
- **ai**: MLOps Platform, RHNS Core

## Environment Variables

| Variable | Source | Purpose |
|----------|--------|---------|
| `GITHUB_TOKEN` | GitHub PAT | Dispatch workflows across repos |
| `GITHUB_USER` | Default: Garrettc123 | Repo owner namespace |
| `STRIPE_SECRET_KEY` | Stripe Dashboard | Pull MRR/ARR from Stripe |

## Deployment

1. Push to `main` branch
2. GitHub Actions runs `deploy.yml`
3. Vercel builds and deploys `api/main.py` as serverless function
4. Smoke tests run hourly via `smoke-test.yml` schedule

## GENESIS Benchmark

The platform architecture is governed by the GENESIS MAUT framework:
- **Baseline Score**: 85.7 (mean of B1=87.7, B3=84.8, B4=84.6)
- **Target Score**: 90.0 in 18 months
- **Top Priority**: B1 — Persistent World Model Integration into RHNS
