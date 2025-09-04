# YouTube Shorts Auto-Generator 🎬 (Seeking Contributors!)

[![status](https://img.shields.io/badge/status-MVP-blue)](#) [![license](https://img.shields.io/badge/license-MIT-green)](#) [![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#)

A production-ready starter that **generates YouTube Shorts automatically** and can **upload/schedule** them via the YouTube Data API. It mines trends, writes a script, synthesizes a voiceover, assembles a 9:16 video with captions, and publishes to YouTube — all automated.

> This project is early but functional. We’re actively looking for feedback and improvements across performance, quality, safety, and DX. **PRs welcome!**

---

## ✨ What it does (today)

- Trend mining (Google Trends) → topic candidates  
- Script generation (OpenAI optional, deterministic fallback included)  
- TTS (Azure Neural TTS)  
- Stock footage (Pexels) + license ledger  
- 9:16 vertical composition (FFmpeg) with burned captions + loudness normalization  
- SEO metadata generation (title, description, tags, hashtags)  
- YouTube upload (resumable) + optional scheduling + captions upload  
- API (FastAPI) + minimal worker + Postgres + Redis  
- Dockerized dev environment

---

## 🧱 Architecture (high-level)

FastAPI (services/api) Worker (services/worker)
└─ creates jobs └─ consumes jobs from Redis
└─ writes to DB └─ runs app/pipeline:
trends → script → assets → TTS
→ captions → FFmpeg compose
→ SEO → YouTube upload → captions
Infra: Postgres (jobs/state) + Redis (queue) + Docker


---

## 🚀 Quick start

```bash
# 1) clone
git clone https://github.com/<you>/yt-shorts-autogen.git
cd yt-shorts-autogen

# 2) env
cp .env.example .env
# fill: PEXELS_API_KEY, AZURE_TTS_KEY/REGION, YOUTUBE_TOKEN_JSON paths, etc.

# 3) secrets (OAuth creds + refresh token)
mkdir -p secrets data
# put client_secret.json and token.json in ./secrets

# 4) run
docker compose up --build

# 5) create a job
curl -X POST http://localhost:8080/jobs -H "Content-Type: application/json" -d '{
  "locale": "US",
  "topicHint": "productivity hacks",
  "approveToPublish": false,
  "scheduleAt": null
}'

# 6) check status
curl http://localhost:8080/jobs/1

⚠️ YouTube: uploads via API may initially be private until your project is verified by Google. Plan for that in your workflow.

🧪 Local development
# optional: run API locally (without Docker) after installing requirements
uvicorn services.api.main:app --reload --port 8080
# run worker in another shell:
python services/worker/worker.py

🛡️ Security & Compliance

Least-privilege OAuth scopes; tokens stored outside images (/secrets).

No PII in logs; structured logging via loguru.

Every downloaded asset is logged in LICENSE_LEDGER.

Guardrails in scriptgen.safety_filter() — contributions welcome to improve filters.

Please report security issues privately via Issues → “Security” or email (see repo security policy if present).

📌 Roadmap / Help Wanted

We’d love help with any of the following. If you’re interested, comment on the issue or open a draft PR:

Trend Miner 2.0: add niche-aware topic scoring, multi-source signals (YouTube search, Reddit, X).

Caption alignment: replace naive line timing with TTS alignment or ASR forced alignment (e.g., gentle/whisper-timestamp).

Visual polish: progress bars, kinetic text, templates, transitions; optional MoviePy overlays w/ safe defaults.

Music: licensed background music module with waveform-aware ducking + per-track license audit.

YouTube retries & quotas: smarter backoff, failure classification, and observability (Sentry/OTel).

Approval workflow: “generate → human approve → upload” flag with override UI.

Analytics: YouTube Analytics ingestion + retention/CTR reports; topic loopback to prioritise what works.

Internationalization: multi-language scripts/voices and locale-aware SEO.

CI/CD: GitHub Actions for lint/test/build; add basic unit tests (see below).

Docs: deepen operator runbook & troubleshooting guide.

If you have other ideas, open a Discussion or Issue!

🧰 Contributing

Fork → create a feature branch → commit with clear messages.

Add/adjust tests when you change behavior.

Ensure type safety/linters pass:

pip install ruff mypy
ruff check .
mypy app services

Code style & security

Keep functions small and testable.

Validate and sanitize all external inputs (URLs, file paths, metadata).

Never log secrets or raw OAuth tokens.

Use prepared/parameterized DB queries (SQLAlchemy ORM already).

Prefer pure FFmpeg filters for performance, with MoviePy only when needed.

🧪 Testing ideas (starter)

Unit: seo.build_seo, captions.write_srt, trends.get_trending_topics (mock network).

Integration: pipeline smoke test with mocked Pexels/Azure/YouTube clients.

Contract: verify YouTube payload structure and scheduling logic.

🐛 Issues & Discussions

Bug report: include steps, logs (api & worker), and env details.

Feature request: explain the use case and potential API changes.

Q&A / Ideas: use Discussions tab to brainstorm.