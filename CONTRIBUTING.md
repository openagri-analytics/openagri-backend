# Contributing to openagri-backend

Contributions are welcome. See the main [OpenAgri Analytics CONTRIBUTING guide](https://github.com/OpenAgriAnalytics/openagri-analytics/blob/main/CONTRIBUTING.md) for
the full process, points system, and code of conduct.

## Backend-specific notes

- Run `cargo fmt` before opening a PR.
- Run `cargo clippy -- -D warnings` and fix all warnings.
- Add tests for new service logic in `src/services/`.
- New endpoints need a matching service function and model struct.
- Database schema changes go in a new `migrations/NNNN_description.sql` file.

## Local setup

```bash
cp .env.example .env
# Set DATABASE_URL in .env
cargo run
cargo test
```
