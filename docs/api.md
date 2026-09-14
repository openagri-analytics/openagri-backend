# API Reference — openagri-backend

Base URL: `http://localhost:3000`

---

## Health

### GET /health

Returns API liveness status.

**Response**

```json
{
  "status": "ok",
  "service": "openagri-backend",
  "version": "0.1.0"
}
```

---

## Datasets

### GET /datasets

Returns all registered datasets.

**Response** — array of dataset objects:

```json
[
  {
    "id": "uuid",
    "name": "Nigeria Agricultural Survey 2025",
    "description": "...",
    "record_count": 30,
    "file_hash": "sha256:abc...",
    "source": "https://...",
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z"
  }
]
```

---

### POST /datasets

Register a new dataset.

**Request body**

```json
{
  "name": "Nigeria Agricultural Survey 2025",
  "description": "Annual crop yield data for 30 states",
  "source": "https://example.com",
  "file_hash": "sha256:abc..."
}
```

**Response** — the created dataset object.

---

### GET /datasets/:id

Returns a single dataset by UUID. Returns `404` if not found.

---

### DELETE /datasets/:id

Delete a dataset. Returns `404` if not found.

**Response**

```json
{ "deleted": "uuid" }
```

---

## Analytics

### GET /analytics/yield

Average yield per crop across all records.

**Response**

```json
[
  { "crop": "Cassava", "average_yield_tons": 6.82, "total_records": 4 },
  { "crop": "Rice",    "average_yield_tons": 4.26, "total_records": 6 }
]
```

---

### GET /analytics/profit

Total revenue, cost, and profit per crop.

**Response**

```json
[
  {
    "crop": "Groundnut",
    "total_revenue": 748000.0,
    "total_cost": 330000.0,
    "total_profit": 418000.0,
    "average_profit_per_record": 104500.0
  }
]
```

---

### GET /analytics/revenue

Total revenue per state/region.

**Response**

```json
[
  { "state": "Borno", "total_revenue": 220000.0, "total_records": 1 }
]
```

---

### GET /analytics/crops

List of distinct crop names.

**Response**

```json
["Cassava", "Groundnut", "Maize", "Rice", "Sorghum", "Soybean", "Yam"]
```

---

### GET /analytics/quality/:dataset_id

Data quality report for a dataset.

**Response**

```json
{
  "dataset_id": "uuid",
  "total_records": 30,
  "missing_yield": 0,
  "missing_rainfall": 0,
  "negative_profit": 0,
  "duplicate_farmer_ids": 0,
  "quality_score": 100.0
}
```

---

## Error Responses

All errors return a JSON body:

```json
{
  "error": "Dataset abc123 not found",
  "status": 404
}
```

| Status | Meaning |
|---|---|
| 400 | Bad request — invalid input |
| 404 | Resource not found |
| 422 | Validation error |
| 500 | Internal server error |
