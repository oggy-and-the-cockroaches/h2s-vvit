# CivicPulse AI — Municipal Operations & Civic Trust Platform

> **"Every report deserves a response."**  
> An autonomous, real-time civic operations intelligence platform for municipal incident detection, multimodal AI triage dispatch, tamper-evident resolution verification, and citizen transparency.

Live Production URL: **[https://ajayhemanth.online](https://ajayhemanth.online)**  
Repository: **[https://github.com/oggy-and-the-cockroaches/h2s-vvit](https://github.com/oggy-and-the-cockroaches/h2s-vvit)**

---

## 🏛️ Platform Architecture

```
                    ┌───────────────────────────────────────────────┐
                    │               CIVICPULSE AI                   │
                    │   Next-Generation Municipal Operations Hub   │
                    └───────────────────────┬───────────────────────┘
                                            │
        ┌───────────────────┬───────────────┴───────────────┬───────────────────┐
        ▼                   ▼                               ▼                   ▼
┌───────────────┐   ┌───────────────┐               ┌───────────────┐   ┌───────────────┐
│  Command      │   │   Incident    │               │  Resolution   │   │    Public     │
│  Center       │   │ Intelligence  │               │ Verification  │   │ Transparency  │
│  (index.html) │   │  (Dossiers)   │               │  (Forensics)  │   │   (Portal)    │
└───────┬───────┘   └───────┬───────┘               └───────┬───────┘   └───────┬───────┘
        │                   │                               │                   │
        └───────────────────┴───────────────┬───────────────┴───────────────────┘
                                            │
                        ┌───────────────────┴───────────────────┐
                        │      FastAPI High-Performance Engine │
                        │  REST API • WebSocket Telemetry • DB  │
                        └───────────────────────────────────────┘
```

---

## 🚀 Key Modules & Connected Views

### 1. 🎛️ Operational Command Center (`index.html`)
- **Real-Time Telemetry Cockpit**: Live incident metrics, open case distribution, critical hazard countdowns, median SLA calculations.
- **Geospatial Tactical Map**: Interactive vector map with multi-hazard layers, cluster radiuses, unit trajectories, and clickable incident coordinates.
- **Autonomous AI Triage Engine**: Priority composite ranking (1–100), automated multi-report deduplication, and single-click dispatch recommendations.
- **Priority Triage Queue**: Sortable, filterable dynamic incident table with live status badges and direct inspect actions.

### 2. 🧠 Incident Intelligence Dossier (`incident-intelligence.html`)
- **Multimodal Visual Forensics**: High-resolution photogrammetry viewport with thermal hazard HUD overlays, EXIF geo-anchors, and SHA-256 cryptographic verification.
- **Explainability Scoring Matrix**: Composite priority breakdown across Safety Urgency, Community Impact, Waiting Duration, and Corroboration Concordance.
- **Spatio-Temporal Citizen Clustering**: Merges corroborating citizen reports within proximity threshold into a single deduplicated actionable incident record.
- **Field Unit Dispatch & Checklist**: Live unit tracking, crew ETA countdown, and interactive mitigation procedure checklist.
- **Immutable Audit Trail**: Chronological event logs synced to cryptographic ledger blocks.

### 3. 🔍 Resolution Verification Workspace (`resolution-verification.html`)
- **Dual Visual Inspection**: Side-by-Side viewport and interactive **Overlay Comparison Slider** with smooth mouse and touch drag controls.
- **Photogrammetry & Elevation Heatmap**: Toggleable metric LiDAR grid and subsurface depression elevation heatmap.
- **Synchronized Pan-and-Zoom**: Real-time wheel zoom inspection across both before & after forensic captures.
- **Officer Decision Action Deck**: Human-in-the-loop statutory sign-off actions:
  - *Approve Resolution* (Signs off and unlocks contractor payout)
  - *Request More Proof* (Orders crew re-submission)
  - *Schedule 14-Day Audit* (Queues automated mobile LiDAR re-scan)
  - *Reject & Reissue* (Flags non-conformance and resets SLA)
- **Citizen Transparency SMS/Push Notification Preview**: Live preview of automated citizen alerts with before/after visual proof.

### 4. 🌐 Civic Transparency & Public Trust Portal (`public-transparency.html`)
- **Open Ledger Verification**: Public cryptographic audit ID and Merkle root synchronization status.
- **Universal Civic Search & Category Filtering**: Search by incident ID, cross-street, or hazard category.
- **30-Day Historical Resolution Velocity**: Interactive SVG performance compliance trend line against municipal SLA targets.
- **Live Resolution Stream**: Real-time feed of approved municipal repairs with before/after evidence photos.
- **Community Trust Scorecard**: Public satisfaction benchmarks and resident feedback.
- **Open Civic Datasets**: Export GeoJSON, download CSV logs, or subscribe to webhooks.

---

## ⚡ Global Platform Features & Shortcuts

- **Command Palette (`⌘K` / `Ctrl+K`)**: Instant search and navigation modal accessible from anywhere on the platform.
- **Operational Alerts Drawer**: Real-time notification panel triggered from header bell icon with direct navigation to incidents.
- **Keyboard Navigation**:
  - `Alt + 1` &rarr; Command Center
  - `Alt + 2` &rarr; Incident Intelligence
  - `Alt + 3` &rarr; Resolution Verification
  - `Alt + 4` &rarr; Public Transparency
- **Real-Time Telemetry Clock**: Synchronized heartbeat timers simulating live validator node pings.
- **Custom Design System**: Consistent Tailwind dark mode theme, Geist and JetBrains Mono typography, custom scrollbars, and toast alerts.

---

## 📁 Repository Structure

```
├── CNAME                              # GitHub Pages custom domain (ajayhemanth.online)
├── DESIGN.md                          # Design system specification and color tokens
├── README.md                          # Platform documentation
├── index.html                         # Command Center (Homepage)
├── incident-intelligence.html         # Incident Intelligence & Multimodal Forensics
├── resolution-verification.html       # Resolution Verification Workspace
├── public-transparency.html           # Public Transparency & Impact Portal
├── css/
│   └── style.css                      # Platform stylesheet, animations, and modals
├── js/
│   ├── app.js                         # Core router, command palette, toasts, and telemetry
│   └── verification.js                # Comparison slider, zoom controls, and audit deck
├── assets/
│   └── screenshots/                   # High-resolution platform preview captures
│       ├── command-center.png
│       ├── incident-intelligence.png
│       ├── resolution-verification.png
│       └── public-transparency.png
└── backend/                           # FastAPI backend service (Python)
    ├── run.py                         # One-click backend server runner
    ├── requirements.txt               # Python dependencies
    ├── README.md                      # Backend API documentation
    └── app/
        ├── main.py                    # FastAPI application entrypoint & static mount
        ├── core/config.py             # Application settings & CORS
        ├── models/schemas.py          # Pydantic schemas for incidents & verifications
        ├── data/database.py           # In-memory realistic civic database
        └── api/v1/
            ├── router.py              # Central v1 route aggregator
            └── endpoints/             # Triage, verification, transparency, and telemetry
```

---

## 💻 Running the Frontend

The frontend is built using **clean, standards-compliant HTML5, CSS3, and JavaScript**. No build step or bundler is required.

### Option 1: Direct Browser Access
Simply open `index.html` in any modern web browser.

### Option 2: Local Static Server
Using Python:
```bash
python -m http.server 8000
```
Then visit `http://localhost:8000`.

Using Node.js:
```bash
npx serve .
```

---

## ⚙️ Running the FastAPI Backend

A high-performance Python FastAPI backend provides REST endpoints for incident data, triage dispatch, cryptographic audit verification, WebSocket telemetry, and open datasets. When started, it also serves the frontend directly at `http://localhost:8000/`.

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run server with runner script
python backend/run.py

# Or run with uvicorn directly
uvicorn backend.app.main:app --reload --port 8000
```

Interactive API documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🛡️ License & Open Government Standards

Published under the MIT License in compliance with the **Open Civic Telemetry Standard & Freedom of Information Framework**.
