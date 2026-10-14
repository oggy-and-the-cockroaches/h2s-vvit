# CivicPulse AI — FastAPI Backend Service

This directory contains the high-performance Python FastAPI backend for the **CivicPulse AI Operations Platform**.

## 🚀 Features

- **Autonomous AI Incident Triage**: REST API for ranking, filtering, and querying municipal incidents.
- **Multimodal Forensic Intelligence**: Detailed dossier endpoints with EXIF sensor data, vision confidence scores, and citizen report deduplication.
- **Statutory Resolution Verification**: Human-in-the-loop approval deck for officer sign-offs (`APPROVE`, `REQUEST_PROOF`, `SCHEDULE_14D_AUDIT`, `REJECT`) with cryptographic SHA-256 block commitment.
- **Public Transparency Feeds**: Open civic data endpoints with live resolution stream, GeoJSON RFC 7946 export, and CSV download.
- **Real-Time WebSocket Telemetry**: Live stream (`/api/v1/telemetry/ws`) broadcasting heartbeat validator pings and status updates.
- **Integrated Fullstack Mode**: Seamlessly serves the HTML5/CSS/JS frontend directly on `http://localhost:8000/`.

---

## 🛠️ Quickstart

### 1. Install Dependencies
```bash
py -m pip install -r backend/requirements.txt
```

### 2. Run Backend Server
Using the convenience runner:
```bash
py backend/run.py
```

Or using Uvicorn directly:
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📖 Interactive API Documentation

Once the server is running, navigate to:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Schema**: [http://localhost:8000/api/v1/openapi.json](http://localhost:8000/api/v1/openapi.json)

---

## 📡 API Reference Overview

### 1. Incidents & Triage (`/api/v1/incidents`)
- `GET /api/v1/incidents` — List and filter active municipal incidents.  
  *Query params: `category`, `ward`, `status`, `min_priority`, `search`*
- `GET /api/v1/incidents/{incident_id}` — Get full dossier for an incident (e.g., `#CP-8492`).
- `POST /api/v1/incidents` — Ingest new citizen or sensor incident report.
- `PATCH /api/v1/incidents/{incident_id}/checklist/{checklist_id}` — Update field mitigation procedure checklist.

### 2. Resolution Verification (`/api/v1/verification`)
- `GET /api/v1/verification/pending` — List incidents awaiting dual verification.
- `GET /api/v1/verification/{incident_id}` — Get photogrammetry evidence, before/after photos, and LiDAR metrics.
- `POST /api/v1/verification/decision` — Submit officer sign-off decision.  
  *Payload:*
  ```json
  {
    "incident_id": "CP-8461",
    "officer_id": "OP-009",
    "officer_name": "Dir. E. Vance",
    "decision": "APPROVE",
    "notes": "Verified flush road grade and asphalt seam seal."
  }
  ```

### 3. Public Transparency (`/api/v1/transparency`)
- `GET /api/v1/transparency/metrics` — Aggregate trust metrics, SLA speeds, and department compliance.
- `GET /api/v1/transparency/feed` — Public stream of verified resolutions with photos.
- `GET /api/v1/transparency/export/geojson` — Open dataset in RFC 7946 GeoJSON format.
- `GET /api/v1/transparency/export/csv` — Open dataset in CSV format.

### 4. Telemetry (`/api/v1/telemetry`)
- `GET /api/v1/telemetry/status` — Operational status, cluster ping, and hazard counters.
- `GET /api/v1/telemetry/nodes` — List of decentralized validator nodes.
- `WebSocket /api/v1/telemetry/ws` — Real-time telemetry event stream.

---

## 🧪 Example cURL Requests

### List Critical Incidents:
```bash
curl -X GET "http://localhost:8000/api/v1/incidents?min_priority=90"
```

### Inspect Incident #CP-8492:
```bash
curl -X GET "http://localhost:8000/api/v1/incidents/CP-8492"
```

### Approve Resolution for #CP-8461:
```bash
curl -X POST "http://localhost:8000/api/v1/verification/decision" \
     -H "Content-Type: application/json" \
     -d '{"incident_id": "CP-8461", "decision": "APPROVE", "notes": "Statutory sign-off granted."}'
```

### Download GeoJSON:
```bash
curl -X GET "http://localhost:8000/api/v1/transparency/export/geojson" -o incidents.geojson
```
