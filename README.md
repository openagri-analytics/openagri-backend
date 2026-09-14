# openagri-backend

Rust/Axum REST API backend for the [OpenAgri Analytics](https://github.com/OpenAgriAnalytics) platform.

[![Rust CI](https://github.com/OpenAgriAnalytics/openagri-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/OpenAgriAnalytics/openagri-backend/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

The backend exposes a REST API for:

- Agricultural dataset management
- Crop yield, profit, and revenue analytics
- Data-quality reports
- Database-backed persistence via PostgreSQL

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Rust (stable) |
| Web framework | Axum 0.7 |
| Database | PostgreSQL 15+ |
| ORM / queries | SQLx 0.7 |
| Async runtime | Tokio |

---

## API Endpoints

```
GET    /health
GET    /datasets
POST   /datasets
GET    /datasets/:id
DELETE /datasets/:id

GET    /analytics/yield
GET    /analytics/profit
GET    /analytics/revenue
GET    /analytics/crops
GET    /analytics/quality/:dataset_id
```

---

## Quick Start

### Requirements

- [Rust](https://rustup.rs) stable toolchain
- PostgreSQL 15+

### Setup

```bash
git clone https://github.com/OpenAgriAnalytics/openagri-backend.git
cd openagri-backend

cp .env.example .env
# Edit .env — set DATABASE_URL to your PostgreSQL connection string

cargo run
```

API available at `http://localhost:3000`

```bash
curl http://localhost:3000/health
# {"status":"ok","service":"openagri-backend","version":"0.1.0"}
```

### Run tests

```bash
cargo test
```

---

## Project Structure

```
openagri-backend/
├── migrations/           # SQLx database migrations
├── src/
│   ├── main.rs           # Entry point — server setup
│   ├── config.rs         # Environment config
│   ├── error.rs          # AppError → HTTP response mapping
│   ├── db/
│   │   └── postgres.rs   # Connection pool + migrations
│   ├── models/
│   │   ├── dataset.rs    # Dataset and AgricultureRecord structs
│   │   └── analytics.rs  # Analytics response structs
│   ├── routes/
│   │   ├── health.rs
│   │   ├── datasets.rs
│   │   └── analytics.rs
│   └── services/
│       ├── dataset_service.rs
│       └── analytics_service.rs
├── .env.example
├── Cargo.toml
└── README.md
```

---

## Related Repos

| Repo | Description |
|---|---|
| [openagri-frontend](https://github.com/OpenAgriAnalytics/openagri-frontend) | Analytics dashboard (HTML/JS) |
| [openagri-contract](https://github.com/OpenAgriAnalytics/openagri-contract) | Rust smart contract for contribution tracking |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All contributions earn points tracked on-chain.

## License

[MIT](LICENSE)
