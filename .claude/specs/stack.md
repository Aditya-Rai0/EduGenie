# Stack — EduGenie OS

## Project Overview

EduGenie OS is an AI-powered Course Creation & Launch Platform. It takes a topic brief and autonomously builds, packages, launches, and continuously improves a full online course product — content, video, quizzes, sales page, and payment — in a single session.

- **Target Users:** Independent creators (coaches, consultants, educators), corporate L&D teams, digital agencies
- **MVP Scope:** 18 features — 7 AI Pipeline · 6 Creator Tools · 3 Learner Features · 2 Commerce
- **Core Metric:** Full 10-module course built in < 4 hours (vs. 150–300 hours manually)
- **Business Model:** SaaS subscriptions (Starter free, Creator $45/mo, Studio $109/mo, Enterprise custom) + marketplace commission (5–12%)
- **Target:** $6M ARR by Month 18, 15,000 paying creators

---

## High-Level Architecture

```
┌──────────────────────────────────────────────┐
│                  USERS                        │
│  Creator OS (Next.js)  │  LearnSpace (Next.js) │
│  Mobile App (React Native + Expo)           │
└──────────────┬───────────────────────────────┘
               │ HTTPS / WSS
┌──────────────▼───────────────────────────────┐
│           Compute Layer (Docker)              │
│  ┌─────────┐  ┌──────────────┐  ┌──────────┐ │
│  │ Next.js │  │ FastAPI      │  │ Redis +  │ │
│  │ Frontend│  │ Backend      │  │ BullMQ   │ │
│  └─────────┘  └──────┬───────┘  └──────────┘ │
└──────────────────────┼────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
   ┌─────────────┐          ┌──────────────────┐
   │  Services   │          │  AI Agent Layer   │
   │ - Courses   │          │  Intelligence     │
   │ - Creator   │          │  Architect        │
   │ - Student   │          │  Scriptwriter     │
   │ - Commerce  │          │  MediaForge       │
   └─────────────┘          │  Evaluator        │
                            │  Launchpad        │
                            │  Optimizer        │
                            └────────┬──────────┘
                                     │
             ┌───────────────────────┼──────────────────┐
             ▼                       ▼                  ▼
┌─────────────────────┐  ┌──────────────────┐  ┌──────────────┐
│  Supabase (Unified) │  │  Gemini 3.5 Flash │  │ FFmpeg       │
│  ┌───────────────┐  │  │  (Text + Embed +   │  │ (Video       │
│  │ PostgreSQL 16 │  │  │   TTS + STT)      │  │  Rendering)  │
│  │ + pgvector    │  │  └──────────────────┘  └──────────────┘
│  │ Supabase Auth │  │
│  │ Supabase      │  │
│  │  Storage      │  │
│  └───────────────┘  │
└─────────────────────┘
```

## Data Flow — Course Build (End-to-End)

```
Creator submits topic brief (topic + audience + depth + tone + language)
  ↓
Intelligence Agent → web search + competitor scrape → market report
  ↓ [REVIEW GATE: creator approves topic angle]
Architect Agent → curriculum JSON (modules, lessons, objectives, durations)
  ↓ [REVIEW GATE: creator reorders / approves outline]
Scriptwriter Agent → parallel script writing → lesson scripts (Supabase Storage)
  ↓
MediaForge Agent → parallel per module:
  Slide Agent  → slide JSON → python-pptx render → PPTX + PNG frames (Supabase Storage)
  Voice Agent  → Gemini TTS / ElevenLabs → MP3 narration (Supabase Storage, cached by hash)
  Video Agent  → FFmpeg (PNG frames + MP3) → 1080p MP4 + Gemini SRT (Supabase Storage)
  ↓
Evaluator Agent → quiz JSON + capstone brief + flashcards
  ↓
Launchpad Agent → sales page HTML + pricing rec + email sequence + social posts
  ↓ [FINAL REVIEW: creator reviews → edits → approves]
Publish → DB record + Storage URLs locked + Algolia indexed + Stripe product created → live URL
  ↓ (post-launch, weekly)
Optimizer Agent → student analytics → improvement report → creator action items
```

---

## Technology Stack

### Backend
- **Language:** Python 3.12
- **Framework:** FastAPI + Pydantic v2
- **ORM:** SQLAlchemy 2.0 (async) + Alembic (migrations)
- **Auth:** Supabase Auth (magic link, Google/GitHub OAuth, JWT)
- **Task Queue:** Redis + BullMQ via Python (RQ/arq or Celery)
- **API Style:** REST (all endpoints versioned at `/api/v1/`) + WebSocket for real-time pipeline + analytics
- **Agent Orchestration:** LangGraph supervisor pattern — 7 agents, stateful pipeline, checkpointing

### Frontend Web
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript (strict mode)
- **Styling:** Tailwind CSS
- **UI Components:** Radix UI primitives (accessible, keyboard-navigable)
- **State Management:** Zustand (client state) + TanStack Query (server state)
- **Design:** Clean, professional — blue accent (#2563EB) on white/light-gray, Inter typography
- **Deployment:** Docker container on any Docker-compatible platform

### Mobile Application
- **Framework:** React Native + Expo SDK 52+
- **Development:** Expo Go for testing, EAS Build for production builds
- **Platforms:** iOS and Android
- **Navigation:** React Navigation (stack, tab, drawer)
- **State:** Zustand + TanStack Query
- **Push Notifications:** Expo Push Notifications + Firebase Cloud Messaging

### Database & Storage
- **Primary DB:** Supabase (PostgreSQL 16 + pgvector extension)
- **Cache/Queue:** Redis (sessions, rate limiting, job queue, pipeline checkpoint state)
- **Object Storage:** Supabase Storage (media files, certificates, slides)
- **Search Index:** Algolia (marketplace course search)

### AI & Machine Learning
- **Text Generation:** Gemini 3.5 Flash (primary, all agentic tasks)
- **Embeddings:** Gemini Embedding 2 (1536d) via pgvector
- **Speech-to-Text:** Gemini 3.5 Flash (multimodal)
- **Text-to-Speech:** Gemini TTS + ElevenLabs API (voice cloning)
- **Video Rendering:** FFmpeg (background worker, no GPU needed)
- **Plagiarism Check:** Originality.ai
- **PII Detection:** Microsoft Presidio (self-hosted)
- **AI Observability:** Langfuse (self-hosted or cloud-hosted)

### Infrastructure (Container-Based)
- **Compute:** Docker containers (backend APIs, web frontend, workers) on any hosting platform
- **Video Rendering:** Background worker with FFmpeg (no GPU needed)
- **CI/CD:** GitHub Actions (lint → type check → test → build → deploy)
- **Monitoring:** Prometheus + Grafana (dashboards, alerting)
- **Secrets:** Environment variables / secret store per platform

### Third-Party APIs
- **Email:** SendGrid (transactional emails, launch sequences, notifications)
- **WhatsApp:** Twilio API for WhatsApp Business
- **Payments:** Stripe (Checkout, Payment Intents, Connect, Tax, Radar, Billing Portal)
- **Product Analytics:** PostHog (self-hosted or Cloud)
- **Search:** Algolia
- **Web Search:** Google Custom Search API + Bing Search API (for Intelligence Agent)

---

## Core Features & Modules

### AI Pipeline Features (7)

| Feature | Agent | Description | Key Output |
|---------|-------|-------------|------------|
| F1 — Market Intelligence | Intelligence Agent | Market demand, competitor analysis, angle recommendations | Market report with demand score, 5+ competitor courses, 3 angle options |
| F2 — Curriculum Architect | Architect Agent | Bloom's taxonomy-aligned curriculum design | 8–16 modules, 3–8 lessons each, prerequisites, durations |
| F3 — Script Engine | Scriptwriter Agent | Complete lesson scripts with examples, code, [VERIFY] flags | 2,000–4,000 words per lesson, structured sections |
| F4 — Media Production | MediaForge Agent | Slides, voice narration, video rendering, captions | PPTX, MP4, SRT, thumbnail — per lesson |
| F5 — Assessment Engine | Evaluator Agent | Quizzes, capstone project, flashcards | Module quizzes (5–12 Q), capstone brief, rubric |
| F6 — Launchpad | Launchpad Agent | Sales page, pricing, email sequence, social posts | HTML sales page, 6 emails, 15 social posts |
| F7 — Optimizer | Optimizer Agent | Post-launch analytics, drop-off analysis, improvement report | Weekly report with prioritized fixes |

### Creator Tool Features (6)

| Feature | Description |
|---------|-------------|
| F8 — Creator Studio | 6-stage review flow: Market → Curriculum → Scripts → Slides/Video → Quizzes → Launch |
| F9 — Voice Studio | Voice model training from 10–30 min audio, test + deploy |
| F10 — Analytics Dashboard | Real-time metrics: enrollments, completion, drop-off, quiz performance, AI narrative |
| F11 — Course Update & Versioning | Selective regeneration, version history, student notifications |
| F12 — Affiliate & Revenue System | Referral links, commission tracking, Stripe Connect payouts |
| F13 — Multi-Language Generation | 6 languages simultaneously with cultural localization |

### Learner Features (3)

| Feature | Description |
|---------|-------------|
| F14 — Course Player & Progress | Video player, notes, progress tracking, AI-powered discussion Q&A |
| F15 — Assessment & Certificates | Quiz interface, capstone submission, auto-generated PDF/PNG certificate |
| F16 — Course Marketplace | Algolia-powered search, filters, AI recommendations, free previews |

### Commerce Features (2)

| Feature | Description |
|---------|-------------|
| F17 — Payments & Subscriptions | Stripe Checkout, 4 pricing tiers, creator payouts via Connect, promo codes |
| F18 — Enterprise Batch Generation | CSV upload, 5–30 parallel course builds, SME routing, Kanban dashboard |

---

## Directory Structure

```
edugenie/
├── CLAUDE.md
├── specs/                        # Modular specification files
│   ├── stack.md
│   ├── api-design.md
│   ├── database.md
│   ├── supabase-infrastructure.md
│   ├── integrations.md
│   ├── mobile.md
│   └── deployment.md
├── docker-compose.yml
├── .env.example
├── .env.local
├── .gitignore
│
├── backend/
│   ├── pyproject.toml
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── dev.txt
│   │   └── prod.txt
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   └── app/
│       ├── __init__.py
│       ├── main.py                    # FastAPI app entry
│       ├── config.py                  # Settings (pydantic-settings)
│       ├── dependencies.py            # DI (get_db, get_current_user)
│       ├── api/v1/                    # Route handlers
│       │   ├── router.py
│       │   ├── auth.py, courses.py, creators.py, lessons.py
│       │   ├── quizzes.py, enrollments.py, certificates.py
│       │   ├── marketplace.py, analytics.py, voice.py
│       │   ├── affiliates.py, batch.py, webhooks.py, health.py
│       │   └── ws/                    # WebSocket handlers
│       ├── core/                      # Core utilities
│       │   ├── security.py, cache.py, storage.py, queue.py
│       │   └── webhook_handler.py
│       ├── models/                    # SQLAlchemy models
│       ├── schemas/                   # Pydantic schemas
│       ├── services/                  # Business logic layer
│       ├── agents/                    # AI agent implementations
│       │   ├── base.py, orchestrator.py
│       │   ├── intelligence_agent.py through optimizer_agent.py
│       │   └── tools/                 # Agent tool functions
│       ├── integrations/             # Third-party API clients
│       │   ├── stripe.py, sendgrid.py, twilio.py
│       │   ├── algolia.py, openai.py, elevenlabs.py
│       │   ├── originality.py, presidio.py, posthog.py
│       └── utils/                    # Utilities
│           ├── pricing.py, tax.py, pdf.py
│
├── frontend-web/
│   ├── package.json, tsconfig.json, tailwind.config.ts
│   ├── next.config.js, Dockerfile
│   ├── app/                          # Next.js App Router pages
│   │   ├── layout.tsx, page.tsx
│   │   ├── (auth)/, (creator)/, (learnspace)/, (enterprise)/
│   │   └── api/                      # BFF API routes
│   ├── components/                   # UI components
│   │   ├── ui/, layout/, creator/
│   │   ├── learnspace/, marketplace/, shared/
│   ├── lib/                          # Client libraries
│   │   ├── supabase.ts, api-client.ts, stripe.ts, utils.ts
│   └── hooks/                        # React hooks
│
├── mobile-app/
│   ├── app.json, app.config.ts, package.json
│   ├── tsconfig.json, babel.config.js, eas.json
│   ├── App.tsx
│   └── src/
│       ├── navigation/, screens/, components/
│       ├── services/, hooks/, store/, utils/
│
├── infra/
│   ├── terraform/                    # Infrastructure IaC
│   │   ├── main.tf, variables.tf, outputs.tf
│   │   ├── modules/ (compute, network, storage, monitoring, cicd)
│   │   └── environments/ (dev, staging, prod)
│   ├── cloudbuild.yaml
│   └── scripts/
│
├── docs/                             # Documentation
│   ├── api/openapi.json
│   ├── architecture.md, development.md, deployment.md
│
└── tests/                            # Test suites
    ├── backend/ (unit, integration, e2e)
    ├── frontend/ (unit, e2e)
    └── mobile/
```

---

## Key Success Metrics

| Metric | Target |
|--------|--------|
| Course build time (10-module) | < 4 hours |
| AI cost per full course | < $12 blended |
| API response latency | < 200ms p50, < 800ms p99 |
| Marketplace search | < 500ms p95 |
| Course completion rate | > 45% |
| Creator retention (Year 1) | > 65% for second course |
| Pipeline success rate | > 98% |
| AI hallucination rate | < 2% |
| Uptime (API + Creator OS) | 99.9% |
| MRR (Month 6) | $35K |
| Infrastructure cost at MVP | ~$200/mo |

---

## Cost Estimation (MVP)

| Service | Estimated Monthly Cost |
|---------|----------------------|
| Hosting (compute) | ~$80 |
| Storage + CDN | ~$40 |
| Redis | ~$25 |
| FFmpeg rendering | ~$20 |
| Supabase (Pro) | ~$25 |
| Gemini API (AI pipeline) | ~$500 (variable) |
| ElevenLabs API (voice) | ~$100 |
| SendGrid (email) | ~$15 |
| Twilio (WhatsApp) | ~$10 |
| Algolia | ~$25 |
| Stripe fees | % of transactions |
| **Total Base** | **~$200/mo + AI costs** |

At 500 creators/3 courses per month: ~$2,000/mo total (AI-heavy)
At 15K creators at scale: ~$3K/mo infrastructure + variable AI costs
