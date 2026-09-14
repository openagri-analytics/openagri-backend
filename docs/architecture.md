# Architecture — OpenAgri Analytics

## Repository Layout

The platform is split into three independent repositories:

| Repo | Language | Purpose |
|---|---|---|
| `openagri-backend` | Rust / Axum | REST API, PostgreSQL, analytics engine |
| `openagri-frontend` | HTML / CSS / JS | Analytics dashboard |
| `openagri-contract` | Rust | Smart contract — contribution & reward tracking |

## Design Principle

**Agricultural analytics first → backend second → blockchain third.**

The platform is fully usable without the smart contract. The contract adds a
transparent contribution/reward layer on top.

## System Diagram

```text
┌─────────────────────────────────────────────────┐
│              openagri-frontend                  │
│          (HTML / CSS / JS Dashboard)            │
└────────────────────┬────────────────────────────┘
                     │ REST API (fetch)
┌────────────────────▼────────────────────────────┐
│              openagri-backend                   │
│                (Rust / Axum)                    │
├─────────────────────────────────────────────────┤
│  Routes       /health /datasets /analytics      │
│  Services     dataset_service analytics_service │
│  Models       Dataset AgricultureRecord         │
│  DB           SQLx → PostgreSQL                 │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│                  PostgreSQL                     │
│   datasets   agriculture_records                │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│              openagri-contract                  │
│               (Rust — WASM)                     │
├─────────────────────────────────────────────────┤
│  register_project   register_contributor        │
│  record_contribution  allocate_reward           │
│  claim_rewards                                  │
└─────────────────────────────────────────────────┘
```

## Data Flow

```
Raw CSV
  │
  ▼ analytics/python/cleaning.py
Cleaned CSV
  │
  ▼ analytics/python/analysis.py
Summary tables + analytics/python/visualization.py → PNG charts
  │
  ▼ POST /datasets (API)
PostgreSQL (datasets + agriculture_records)
  │
  ▼ GET /analytics/* (API)
Frontend dashboard
```

## What Goes On-Chain

The contract stores only small, verifiable records:

| Stored on-chain | NOT stored on-chain |
|---|---|
| Dataset SHA-256 hash | Dataset file content |
| Contributor address | Farmer personal data |
| Contribution reference (PR URL) | Agricultural records |
| Points | SQL query results |
| Reward allocation amount | |

## Security Considerations

- Never commit `.env` files or private keys.
- All user input is validated before database insertion.
- Smart contract authorization checks owner before reward allocation.
- CORS is configured — restrict `allow_origin` for production deployments.
