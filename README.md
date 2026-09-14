# openagri-backend

Rust REST API backend for the OpenAgri Analytics platform. Built with [Axum](https://github.com/tokio-rs/axum) and [SQLx](https://github.com/launchbadge/sqlx), backed by PostgreSQL.

## Tech stack

| Layer | Crate |
|---|---|
| HTTP framework | `axum 0.7` |
| Async runtime | `tokio 1` |
| Database | `sqlx 0.7` + PostgreSQL |
| Serialization | `serde` + `serde_json` |
| Error handling | `thiserror` + `anyhow` |
| Logging | `tracing` + `tracing-subscriber` |
| Validation | `validator 0.18` |

## Project structure

```
openagri-backend/
├── src/
│   ├── main.rs                    # Server setup, CORS, router assembly
│   ├── config.rs                  # Config from environment variables
│   ├── error.rs                   # AppError → HTTP response mapping
│   ├── db/
│   │   └── postgres.rs            # PgPool connection + SQLx migrations
│   ├── models/
│   │   ├── dataset.rs             # Dataset, AgricultureRecord structs
│   │   └── analytics.rs           # Analytics summary structs
│   ├── routes/
│   │   ├── health.rs              # GET /health
│   │   ├── datasets.rs            # CRUD /datasets
│   │   └── analytics.rs           # GET /analytics/*
│   └── services/
│       ├── dataset_service.rs     # Dataset business logic
│       └── analytics_service.rs   # Analytics query logic
├── migrations/
│   └── 0001_initial_schema.sql    # datasets + agriculture_records tables
├── analytics/
│   ├── python/                    # Data cleaning and visualization scripts
│   └── sql/                       # Standalone SQL analysis queries
├── data/
│   ├── sample/agriculture.csv     # Sample dataset
│   ├── raw/                       # Raw data drop folder
│   └── cleaned/                   # Cleaned data output folder
├── docs/
│   ├── api.md                     # API endpoint reference
│   └── architecture.md            # System architecture overview
├── .env.example                   # Environment variable template
└── Cargo.toml
```

## Prerequisites

- [Rust](https://rustup.rs/) 1.75+
- PostgreSQL 14+
- [`sqlx-cli`](https://github.com/launchbadge/sqlx/tree/main/sqlx-cli) (optional, for manual migrations)

## Getting started

### 1. Clone and configure

```bash
git clone https://github.com/openagri-analytics/openagri-backend.git
cd openagri-backend
cp .env.example .env
```

Edit `.env`:

```env
HOST=0.0.0.0
PORT=3000
DATABASE_URL=postgres://postgres:postgres@localhost:5432/openagri
```

### 2. Create the database

```bash
psql -U postgres -c "CREATE DATABASE openagri;"
```

### 3. Run the server

```bash
cargo run
```

SQLx will automatically apply migrations from `migrations/` on startup. The server starts at `http://0.0.0.0:3000`.

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check — returns service name and version |
| `GET` | `/datasets` | List all datasets |
| `POST` | `/datasets` | Create a dataset |
| `GET` | `/datasets/:id` | Get a dataset by UUID |
| `DELETE` | `/datasets/:id` | Delete a dataset by UUID |
| `GET` | `/analytics/yield` | Average yield grouped by crop |
| `GET` | `/analytics/profit` | Profit summary grouped by crop |
| `GET` | `/analytics/revenue` | Revenue summary grouped by region/state |
| `GET` | `/analytics/crops` | List of distinct crop types |
| `GET` | `/analytics/quality/:dataset_id` | Data quality report for a dataset |

### Example requests

```bash
# Health check
curl http://localhost:3000/health

# List datasets
curl http://localhost:3000/datasets

# Create a dataset
curl -X POST http://localhost:3000/datasets \
  -H "Content-Type: application/json" \
  -d '{"name": "Nigeria 2024", "description": "National crop data", "source": "FMARD"}'

# Yield analytics
curl http://localhost:3000/analytics/yield
```

## Database schema

Two tables are created by `migrations/0001_initial_schema.sql`:

**`datasets`** — metadata for each uploaded dataset (name, description, source, record count, file hash).

**`agriculture_records`** — individual farming records linked to a dataset (farmer ID, state, crop, farm size, yield, irrigation, rainfall, market price, production cost, revenue, profit, harvest date).

## Running tests

```bash
cargo test
```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Bind address |
| `PORT` | `3000` | Bind port |
| `DATABASE_URL` | `postgres://postgres:postgres@localhost:5432/openagri` | PostgreSQL connection string |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
