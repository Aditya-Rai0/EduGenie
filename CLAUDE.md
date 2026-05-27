# CLAUDE.md — EduGenie OS

## PROJECT OVERVIEW

EduGenie OS is an AI-powered Course Creation & Launch Platform. It takes a topic brief and autonomously builds, packages, launches, and continuously improves a full online course product — content, video, quizzes, sales page, and payment — in a single session.

- **Target Users:** Independent creators (coaches, consultants, educators), corporate L&D teams, digital agencies
- **MVP Scope:** 18 features — 7 AI Pipeline · 6 Creator Tools · 3 Learner Features · 2 Commerce
- **Core Metric:** Full 10-module course built in < 4 hours (vs. 150–300 hours manually)
- **Business Model:** SaaS subscriptions (Starter free, Creator $45/mo, Studio $109/mo, Enterprise custom) + marketplace commission (5–12%)
- **Target:** $6M ARR by Month 18, 15,000 paying creators

### High-Level Architecture

```
┌──────────────────────────────────────────────┐
│                  USERS                        │
│  Creator OS (Next.js)  │  LearnSpace (Next.js) │
│  Mobile App (React Native + Expo)           │
└──────────────────────┬───────────────────────┘
                       │ HTTPS / WSS
┌──────────────────────▼───────────────────────┐
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
                            └────────┬─────────┘
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

### Data Flow — Course Build (End-to-End)

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
  Video Agent  → FFmpeg (PNG frames + MP3) → 1080p MP4 + Whisper SRT (Supabase Storage)
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

## TECHNOLOGY STACK

### Backend
- **Language:** Python 3.12
- **Framework:** FastAPI + Pydantic v2
- **ORM:** SQLAlchemy 2.0 (async) + Alembic (migrations)
- **Auth:** Supabase Auth (magic link, Google/GitHub OAuth, JWT)
- **Task Queue:** Redis (GCP Memorystore) + BullMQ via Python (RQ/arq or Celery)
- **API Style:** REST (all endpoints versioned at `/api/v1/`) + WebSocket for real-time pipeline + analytics
- **Agent Orchestration:** LangGraph supervisor pattern — 7 agents, stateful pipeline, checkpointing

### Frontend Web
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript (strict mode)
- **Styling:** Tailwind CSS
- **UI Components:** Radix UI primitives (accessible, keyboard-navigable)
- **State Management:** Zustand (client state) + TanStack Query (server state)
- **Design:** Clean, professional — blue accent (#2563EB) on white/light-gray, Inter typography

### Mobile Application
- **Framework:** React Native + Expo SDK 52+
- **Development:** Expo Go for testing, EAS Build for production builds
- **Platforms:** iOS and Android
- **Navigation:** React Navigation (stack, tab, drawer)
- **State:** Zustand + TanStack Query
- **Push Notifications:** Expo Push Notifications + Firebase Cloud Messaging

### Database & Storage
- **Primary DB:** Supabase (PostgreSQL 16 + pgvector extension)
- **Object Storage:** Supabase Storage (media files, certificates, slides, scripts)
- **Auth:** Supabase Auth (JWT, magic link, Google/GitHub OAuth, email+password)
- **Cache/Queue:** Redis (sessions, rate limiting, job queue, pipeline checkpoint state)
- **Search Index:** Algolia (marketplace course search)

### AI & Machine Learning
- **Text Generation:** Google Gemini 3.5 Flash (primary for all agentic tasks)
- **Embeddings:** Google Gemini Embedding 2 (1536d) via pgvector
- **Speech-to-Text:** Google Gemini 3.5 Flash (multimodal)
- **Text-to-Speech:** Google Gemini TTS API + ElevenLabs API (voice cloning)
- **Video Rendering:** FFmpeg (background worker, no GPU needed)
- **Plagiarism Check:** Originality.ai
- **PII Detection:** Microsoft Presidio (self-hosted)
- **AI Observability:** Langfuse (self-hosted or cloud-hosted)

### Infrastructure (Container-Based)
- **Compute:** Docker containers (backend APIs, web frontend, workers) hosted on any Docker-compatible platform
- **Video Rendering:** Background worker with FFmpeg (no GPU needed)
- **CI/CD:** GitHub Actions (lint → type check → test → build → deploy)
- **Monitoring:** Prometheus (metrics) + Grafana (dashboards, alerting)
- **Container Registry:** Docker Hub / GitHub Container Registry
- **Secrets:** Environment variables / secret store per platform

### Third-Party APIs
- **Email:** SendGrid (transactional emails, launch sequences, notifications)
- **WhatsApp:** Twilio API for WhatsApp Business
- **Payments:** Stripe (Checkout, Payment Intents, Connect, Tax, Radar, Billing Portal)
- **Product Analytics:** PostHog (self-hosted or Cloud)
- **Search:** Algolia
- **Web Search:** Google Custom Search API + Bing Search API (for Intelligence Agent)

---

## INFRASTRUCTURE ARCHITECTURE

### Compute Layer
- **Docker Containers:** FastAPI backend, Next.js web frontend, BullMQ workers, AI agent services
  - Horizontal auto-scaling based on CPU/memory
  - 2 GB RAM / 2 vCPU per instance (scale with need)
- **Video Rendering:** Background worker with FFmpeg (no GPU needed)
  - Up to 50 parallel renders

### Storage Layer (Supabase Unified)
- **Supabase Storage (Media):**
  - Buckets for video, slides, audio, certificates
  - Signed URLs with 1-hour expiry for video streaming
  - Lifecycle policies configurable per bucket
- **Supabase PostgreSQL 16:**
  - 1 primary + 1 read replica
  - PgBouncer connection pooling
  - Automated backups (hourly), RPO < 1hr, RTO < 3hrs
  - pgvector extension for 1536d embeddings
- **Redis:**
  - Cache, sessions, rate limiting, job queue, pipeline checkpoint state
  - 5GB Standard tier (MVP), scale as needed

### CI/CD Pipeline (GitHub Actions)
- **Trigger:** PR to `development` branch / push to `main` branch
- **Stages:**
  1. Lint (ruff for Python, ESLint + Prettier for TS)
  2. Type check (mypy for Python, tsc for TypeScript)
  3. Unit tests (pytest, Jest)
  4. Security scan (Snyk / Trivy)
  5. Docker build → Container Registry
  6. Integration tests
  7. Deploy (dev auto on PR merge, main with manual approval gate)
- **Deployment:** Rolling update strategy
- **Post-deploy:** Smoke tests → 1hr monitoring standby

### Monitoring & Observability
- **Prometheus:** Metrics collection from all services (API latency, error rates, queue depths, AI cost per course)
- **Grafana:** Dashboards for business and infrastructure metrics
- **Structured JSON Logging:** stdout from all services → log collector
- **Grafana Alerting:** Slack / PagerDuty integration
  - API error rate > 1% for 5 min
  - CPU > 85% sustained
  - Pipeline failure rate > 4% in 24h
  - AI cost per single run > $25
  - Video render queue depth > 200

### Security
- **Secrets:** Environment variables / secret store per platform
- **Container Security:** Regular image scanning
- **API Security:** JWT validation, rate limiting (200 req/min standard, 2000 enterprise)
- **CORS:** Whitelist of allowed origins (edugenie.io, *.edugenie.io)

### IaC
- **Terraform** for all infrastructure provisioning
- Directory: `infra/terraform/`
- Separate state files per environment (dev, staging, prod)

---

## DIRECTORY STRUCTURE

```
edugenie/
├── CLAUDE.md
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
│       ├── api/
│       │   ├── __init__.py
│       │   ├── v1/
│       │   │   ├── __init__.py
│       │   │   ├── router.py          # Aggregates all routers
│       │   │   ├── auth.py
│       │   │   ├── courses.py
│       │   │   ├── creators.py
│       │   │   ├── lessons.py
│       │   │   ├── quizzes.py
│       │   │   ├── enrollments.py
│       │   │   ├── certificates.py
│       │   │   ├── marketplace.py
│       │   │   ├── analytics.py
│       │   │   ├── voice.py
│       │   │   ├── affiliates.py
│       │   │   ├── batch.py
│       │   │   ├── webhooks.py        # Stripe, SendGrid, Twilio
│       │   │   └── health.py
│       │   └── ws/
│       │       ├── pipeline.py         # WS /ws/pipeline/{job_id}/live
│       │       └── analytics.py        # WS /ws/analytics/{course_id}
│       ├── core/
│       │   ├── __init__.py
│       │   ├── security.py            # JWT, hashing, OAuth
│       │   ├── cache.py               # Redis/Memorystore client
│       │   ├── storage.py             # GCP Cloud Storage client
│       │   ├── queue.py               # BullMQ / Redis task queue
│       │   └── webhook_handler.py     # Webhook signature verification
│       ├── models/
│       │   ├── __init__.py
│       │   ├── organization.py
│       │   ├── creator.py
│       │   ├── course.py
│       │   ├── course_version.py
│       │   ├── module.py
│       │   ├── lesson.py
│       │   ├── quiz.py
│       │   ├── student.py
│       │   ├── enrollment.py
│       │   ├── progress.py
│       │   ├── quiz_attempt.py
│       │   ├── sale.py
│       │   ├── affiliate.py
│       │   ├── certificate.py
│       │   ├── discussion.py
│       │   ├── pipeline_run.py
│       │   ├── improvement_report.py
│       │   └── audit_log.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── course.py
│       │   ├── lesson.py
│       │   ├── quiz.py
│       │   ├── analytics.py
│       │   └── ...
│       ├── services/
│       │   ├── __init__.py
│       │   ├── auth_service.py
│       │   ├── course_service.py
│       │   ├── enrollment_service.py
│       │   ├── certificate_service.py
│       │   ├── analytics_service.py
│       │   ├── stripe_service.py
│       │   ├── sendgrid_service.py
│       │   ├── twilio_service.py
│       │   ├── notification_service.py
│       │   ├── search_service.py       # Algolia
│       │   └── storage_service.py      # Cloud Storage
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── base.py                 # Base agent class
│       │   ├── orchestrator.py         # LangGraph supervisor
│       │   ├── intelligence_agent.py   # Market research
│       │   ├── architect_agent.py      # Curriculum design
│       │   ├── scriptwriter_agent.py   # Lesson scripts
│       │   ├── mediaforge_agent.py     # Slides + voice + video
│       │   ├── evaluator_agent.py      # Quizzes + capstone
│       │   ├── launchpad_agent.py      # Sales page + marketing
│       │   ├── optimizer_agent.py      # Post-launch analytics
│       │   └── tools/
│       │       ├── web_search.py       # Google + Bing API
│       │       ├── competitor_scrape.py
│       │       ├── slides.py           # python-pptx
│       │       ├── voice.py            # OpenAI TTS + ElevenLabs
│       │       ├── video.py            # FFmpeg on Cloud Batch
│       │       └── captions.py         # Whisper STT
│       ├── integrations/
│       │   ├── __init__.py
│       │   ├── stripe.py
│       │   ├── sendgrid.py
│       │   ├── twilio.py
│       │   ├── algolia.py
│       │   ├── openai.py
│       │   ├── elevenlabs.py
│       │   ├── originality.py
│       │   ├── presidio.py
│       │   └── posthog.py
│       └── utils/
│           ├── __init__.py
│           ├── pricing.py
│           ├── tax.py
│           └── pdf.py                  # Certificate generation
│
├── frontend-web/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   ├── Dockerfile
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx                    # Landing / Marketplace
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   ├── signup/
│   │   │   └── magic-link/
│   │   ├── (creator)/
│   │   │   ├── dashboard/
│   │   │   ├── studio/                 # Creator Studio (pipeline review)
│   │   │   ├── voice-studio/
│   │   │   ├── analytics/
│   │   │   ├── revenue/
│   │   │   ├── affiliates/
│   │   │   └── settings/
│   │   ├── (learnspace)/
│   │   │   ├── marketplace/
│   │   │   ├── courses/[id]/
│   │   │   ├── learn/[courseId]/
│   │   │   ├── quiz/[attemptId]/
│   │   │   └── certificate/verify/[code]
│   │   ├── (enterprise)/
│   │   │   ├── batch/
│   │   │   └── kanban/
│   │   └── api/                        # Next.js API routes (BFF layer)
│   ├── components/
│   │   ├── ui/                         # Radix UI primitives wrapper
│   │   ├── layout/
│   │   ├── creator/
│   │   ├── learnspace/
│   │   ├── marketplace/
│   │   └── shared/
│   ├── lib/
│   │   ├── supabase.ts                 # Supabase client
│   │   ├── api-client.ts              # Axios/fetch wrapper
│   │   ├── stripe.ts                   # Stripe Elements
│   │   └── utils.ts
│   └── hooks/
│       ├── useAuth.ts
│       ├── useCourses.ts
│       ├── useMarketplace.ts
│       └── useWebSocket.ts
│
├── mobile-app/
│   ├── app.json                        # Expo config
│   ├── app.config.ts
│   ├── package.json
│   ├── tsconfig.json
│   ├── babel.config.js
│   ├── eas.json                        # EAS Build config
│   ├── App.tsx
│   ├── src/
│   │   ├── navigation/
│   │   │   └── RootNavigator.tsx
│   │   ├── screens/
│   │   │   ├── auth/
│   │   │   ├── learnspace/
│   │   │   ├── marketplace/
│   │   │   └── profile/
│   │   ├── components/
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── auth.ts
│   │   │   └── notifications.ts
│   │   ├── hooks/
│   │   ├── store/                      # Zustand stores
│   │   └── utils/
│   └── assets/
│
├── infra/
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── modules/
│   │   │   ├── compute/
│   │   │   ├── network/
│   │   │   ├── storage/
│   │   │   ├── monitoring/
│   │   │   └── cicd/
│   │   └── environments/
│   │       ├── dev/
│   │       ├── staging/
│   │       └── prod/
│   ├── cloudbuild.yaml                 # Cloud Build CI/CD config
│   └── scripts/
│       ├── deploy-backend.sh
│       ├── deploy-frontend.sh
│       └── seed-data.sh
│
├── docs/
│   ├── api/
│   │   └── openapi.json
│   ├── architecture.md
│   ├── development.md
│   └── deployment.md
│
└── tests/
    ├── backend/
    │   ├── conftest.py
    │   ├── unit/
    │   ├── integration/
    │   └── e2e/
    ├── frontend/
    │   ├── unit/
    │   └── e2e/
    └── mobile/
```

---

## CORE FEATURES & MODULES

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

## THIRD-PARTY INTEGRATIONS

### A. SendGrid Email Integration

**Purpose:** Transactional emails, launch sequences, affiliate notifications, weekly digests

**Setup:**
1. Create SendGrid account, verify sender identity (SPF/DKIM)
2. Store API key in GCP Secret Manager as `SENDGRID_API_KEY`
3. Implement `backend/app/integrations/sendgrid.py`

**Email Templates:**
- Welcome / Onboarding sequence
- Course published notification (to creator)
- New enrollment confirmation (to student)
- Course purchase receipt
- Certificate awarded
- Launch email sequence (6 emails, auto-generated by Launchpad Agent)
- Weekly digest (creator analytics)
- Affiliate commission notification
- Course update notification (to enrolled students)

**Transactional Workflows:**
- On signup → welcome email + getting started guide
- On first course publish → congratulations + marketplace tips
- On first student enrollment → notification + dashboard link
- On weekly Optimizer report → digest with action items
- On affiliate conversion → commission earned notification

**Integration Code Pattern:**

```python
# backend/app/integrations/sendgrid.py
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

async def send_email(to: str, subject: str, html_content: str) -> None:
    message = Mail(
        from_email=Email("noreply@edugenie.io", "EduGenie"),
        to_emails=To(to),
        subject=subject,
        html_content=Content("text/html", html_content)
    )
    response = await sg.async_send(message)
    # Log response.status_code, response.body, response.headers
```

### B. Twilio WhatsApp Integration

**Purpose:** WhatsApp Business notifications for course updates, enrollment confirmations, engagement reminders

**Setup:**
1. Twilio account with WhatsApp Business API enabled
2. Register WhatsApp Business sender number
3. Store Twilio Account SID and Auth Token in GCP Secret Manager
4. Configure webhook URL at Twilio Console: `https://api.edugenie.io/api/v1/webhooks/twilio`

**Message Templates (pre-approved by WhatsApp):**
- Enrollment confirmation: "You're enrolled in {course_name}! Start learning: {link}"
- Certificate earned: "🎉 You earned a certificate for {course_name}! View: {link}"
- Course update: "{course_name} has been updated — check out what's new: {link}"
- Payment receipt: "Payment confirmed for {course_name}. Amount: ${amount}"
- Reminder: "You haven't visited {course_name} in 3 days. Continue: {link}"

**Webhook Handling:**
- Incoming messages → log + route to support ticket or AI response
- Delivery status callbacks → update notification status in DB
- Opt-out handling → update preferences, stop further messages

**Integration Code Pattern:**

```python
# backend/app/integrations/twilio.py
from twilio.rest import Client

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

async def send_whatsapp(to: str, body: str) -> None:
    message = client.messages.create(
        from_=f"whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}",
        body=body,
        to=f"whatsapp:{to}"
    )
    # Log message.sid, message.status

# Webhook handler (FastAPI endpoint)
@router.post("/webhooks/twilio")
async def twilio_webhook(request: Request):
    form = await request.form()
    # Validate Twilio signature
    # Process incoming message or status callback
```

### C. Stripe Payment Integration

**Setup:**
1. Stripe account, API keys (pk_*, sk_*) in GCP Secret Manager
2. Webhook signing secret in Secret Manager
3. Configure webhook endpoint: `https://api.edugenie.io/api/v1/webhooks/stripe`

**Products & Prices:**
- SaaS Subscriptions: Starter (free), Creator ($45/mo), Studio ($109/mo), Enterprise (custom)
- Course products: Created dynamically per course via Stripe API on publish
- Promo codes: Stripe Coupon API (% or fixed, max uses, validity window)

**Stripe Connect (Creator Payouts):**
- Creators onboard via Stripe Connect Express
- Bi-weekly payouts (minimum $25 threshold)
- Platform fee: 5–12% of course sales
- Stripe Tax: Automatic VAT/GST calculation for EU transactions

**Webhook Events Handled:**
- `checkout.session.completed` → enroll student, send confirmation
- `payment_intent.succeeded` → update enrollment status
- `payment_intent.payment_failed` → notify student, retry logic
- `customer.subscription.created/updated/deleted` → sync plan tier
- `charge.refunded` → reverse enrollment, revoke access
- `payout.paid` → notify creator
- `account.updated` → sync Connect account status

**Integration Code Pattern:**

```python
# backend/app/integrations/stripe.py
import stripe
from stripe import webhook

stripe.api_key = settings.STRIPE_SECRET_KEY

async def create_checkout_session(course, student_email: str) -> str:
    session = stripe.checkout.Session.create(
        customer_email=student_email,
        line_items=[{"price": course.stripe_price_id, "quantity": 1}],
        mode="payment",
        success_url="https://learn.edugenie.io/courses/{course.id}/success",
        cancel_url="https://learn.edugenie.io/courses/{course.id}",
        metadata={"course_id": str(course.id), "creator_id": str(course.creator_id)}
    )
    return session.url

@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    event = webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    handler = STRIPE_EVENT_HANDLERS.get(event["type"])
    if handler:
        await handler(event["data"]["object"])
```

### D. In-App Notification System

**Architecture:**
- **Real-time:** WebSocket connections via `WS /ws/notifications/{user_id}`
- **Push:** Expo Push Notifications (mobile) + Firebase Cloud Messaging (FCM)
- **Storage:** PostgreSQL `notifications` table with read/unread status
- **Queue:** Notifications dispatched via Redis pub/sub to WebSocket handlers

**Notification Types:**
- Pipeline stage complete / ready for review
- New enrollment / sale
- New discussion question
- Certificate earned
- New affiliate conversion
- Weekly Optimizer report ready
- Course published
- Payout processed
- Refund processed

**Schema:**

```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    notification_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    body TEXT,
    data JSONB,                    -- contextual payload
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    read_at TIMESTAMPTZ,
    INDEX idx_notifications_user_unread (user_id, is_read) WHERE NOT is_read
);
```

---

## MOBILE APPLICATION (React Native + Expo)

### Expo Configuration
```json
// app.json
{
  "expo": {
    "name": "EduGenie",
    "slug": "edugenie",
    "version": "1.0.0",
    "orientation": "portrait",
    "scheme": "edugenie",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "light",
    "splash": { "backgroundColor": "#2563EB" },
    "assetBundlePatterns": ["**/*"],
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "io.edugenie.learnspace",
      "associatedDomains": ["applinks:learn.edugenie.io"],
      "infoPlist": {
        "NSCameraUsageDescription": "Upload profile photo",
        "NSPhotoLibraryUsageDescription": "Save certificate to gallery"
      }
    },
    "android": {
      "package": "io.edugenie.learnspace",
      "intentFilters": [
        { "action": "VIEW", "autoVerify": true,
          "data": [{ "scheme": "https", "host": "*.edugenie.io" }],
          "category": ["BROWSABLE", "DEFAULT"] }
      ]
    },
    "plugins": [
      "expo-router",
      "expo-secure-store",
      "@stripe/stripe-react-native",
      "expo-notifications",
      "expo-linking"
    ],
    "extra": {
      "apiUrl": "https://api.edugenie.io",
      "supabaseUrl": "https://xxx.supabase.co",
      "stripePublishableKey": "pk_live_..."
    }
  }
}
```

### Navigation Structure
```
RootNavigator (Stack)
├── AuthStack
│   ├── Login
│   ├── Signup
│   └── MagicLink
├── MainTabs (Tab Navigator)
│   ├── LearnStack
│   │   ├── MyCourses
│   │   ├── CoursePlayer
│   │   └── QuizScreen
│   ├── MarketplaceStack
│   │   ├── Browse
│   │   ├── Search
│   │   └── CourseDetail
│   └── ProfileStack
│       ├── Profile
│       ├── Certificates
│       └── Settings
└── NotificationStack
    └── NotificationCenter
```

### Stripe SDK Integration
- **Web:** Stripe Elements via `@stripe/react-stripe-js`
- **Mobile:** `@stripe/stripe-react-native` for Apple Pay / Google Pay
- **Backend:** Stripe Checkout via redirect (web) or PaymentSheet (mobile)

### Push Notifications (Expo + FCM)
```typescript
// mobile-app/src/services/notifications.ts
import * as Notifications from 'expo-notifications';

export async function registerForPushNotifications() {
  const { status } = await Notifications.requestPermissionsAsync();
  if (status !== 'granted') return null;
  const token = await Notifications.getExpoPushTokenAsync();
  // POST /api/v1/notifications/register-push-token { token, platform }
  return token;
}

// Handle notification tap → deep link
Notifications.addNotificationResponseReceivedListener((response) => {
  const { courseId, screen } = response.notification.request.content.data;
  // Navigate: router.push(`/learn/${courseId}`)
});
```

### EAS Build Configuration
```json
// eas.json
{
  "cli": { "version": ">= 3.0" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "channel": "development",
      "env": {
        "API_URL": "https://api-staging.edugenie.io",
        "SUPABASE_URL": "https://xxx.supabase.co"
      }
    },
    "preview": {
      "distribution": "internal",
      "channel": "staging",
      "android": { "buildType": "apk" },
      "ios": { "simulator": true }
    },
    "production": {
      "channel": "production",
      "env": {
        "API_URL": "https://api.edugenie.io",
        "SUPABASE_URL": "https://xxx.supabase.co"
      }
    }
  },
  "submit": {
    "production": {
      "ios": { "appleId": "...", "ascAppId": "..." },
      "android": { "track": "production", "releaseStatus": "completed" }
    }
  }
}
```

### Testing Strategy (Mobile)
- **Expo Go:** Daily development testing on physical devices
- **Jest + React Native Testing Library:** Unit tests for components, hooks, services
- **EAS Build + TestFlight (iOS):** Beta distribution for QA team
- **EAS Build + Google Play Console (Android):** Internal track testing
- **Detox / Maestro:** E2E UI tests for critical flows (enrollment, quiz, certificate)

---

## AUTHENTICATION & AUTHORIZATION

### Auth Strategy — Supabase Auth
- **Methods:** Magic link (primary), Google OAuth, GitHub OAuth, email+password fallback
- **Multi-factor:** Optional TOTP 2FA
- **Tokens:** JWTs (1hr expiry) + rotating refresh tokens (30-day window)

### Role-Based Access Control (RBAC)
```
Roles: admin | creator | student | enterprise_admin | affiliate
```

- **Supabase RLS policies** on all tables enforce tenant isolation via `organization_id`
- **Backend middleware** validates JWT and checks permissions per endpoint
- **Creator scoping:** creators access only their own data via `creator_id` filter
- **Student scoping:** students access only courses they're enrolled in

### API Authentication
- **Public:** Marketplace search, course detail, certificate verification
- **Authenticated:** Enrollment, progress, profile
- **Creator-Only:** Studio, analytics, revenue, affiliates
- **Admin:** Enterprise batch, platform settings
- **Webhook:** Signature verification (Stripe: HMAC-SHA256, SendGrid: API key header, Twilio: Twilio signature)

---

## DATABASE DESIGN

### Supabase PostgreSQL Schema

**Core Tables:**
- `organizations` — Top-level tenant
- `creators` — Creator profile, plan tier, brand settings (JSONB)
- `courses` — Course metadata, status, version, price, Stripe product ID
- `course_versions` — Version history with changelog
- `modules` — Module definition, position, learning objective, Bloom's level
- `lessons` — Lesson metadata + Cloud Storage URLs (script, video, slides, captions)
- `quizzes` — Quiz definition, questions JSONB, pass threshold
- `students` — Student identity, Stripe customer ID, locale
- `enrollments` — Student ↔ Course mapping, progress, certificate ID
- `progress` — Per-lesson: watch depth %, time spent, completed_at
- `quiz_attempts` — Per attempt: score, answers JSONB, passed
- `sales` — Stripe payment intent → course mapping, channel, promo
- `affiliates` — Affiliate link, commission %, clicks, conversions
- `certificates` — Verification code, PDF URL, issued_at, revoked_at
- `discussions` — Per-lesson Q&A: content, AI response, creator verified
- `pipeline_runs` — Pipeline stage tracking: model, tokens, cost
- `improvement_reports` — Weekly Optimizer report JSON
- `notifications` — User notifications
- `audit_logs` — Immutable append-only: AI decisions, creator actions, system events

### Vector Database (pgvector)
- **Embeddings Model:** OpenAI `text-embedding-3-small` (1536d)
- **Use Cases:**
  - Research cache (Intelligence Agent) — dedup by `(topic_hash, date)`
  - Curriculum pattern matching — suggest adjustments from high-completion courses
  - Content similarity (plagiarism baseline)
  - Learner confusion signal clustering
- **Hybrid Search:** 0.65 vector + 0.35 BM25

### Migration Strategy
- **Tool:** Alembic with async SQLAlchemy
- **Pattern:** Additive-only migrations for 2 releases; destructive migrations require dual-write period + rollback script
- **CI/CD:** Migrations run as part of Cloud Build deploy step
- **Rollback:** `alembic downgrade -1` with verification script

---

## API SPECIFICATIONS

### Base URL: `https://api.edugenie.io/api/v1/`

### Endpoints

| Area | Method | Endpoint | Auth | Description |
|------|--------|----------|------|-------------|
| **Auth** | POST | `/auth/signup` | Public | Create account |
| | POST | `/auth/login` | Public | Email+password login |
| | POST | `/auth/magic-link` | Public | Request magic link |
| | POST | `/auth/refresh` | Public | Refresh JWT |
| | GET | `/auth/me` | JWT | Current user profile |
| **Creators** | GET | `/creators/{id}` | JWT | Creator profile |
| | PATCH | `/creators/{id}` | Creator | Update profile |
| | GET | `/creators/{id}/courses` | Creator | Creator's courses |
| | GET | `/creators/{id}/revenue` | Creator | Revenue dashboard data |
| **Courses** | GET | `/courses` | Public | List courses |
| | POST | `/courses` | Creator | Create course |
| | PATCH | `/courses/{id}` | Creator | Update course |
| | POST | `/courses/build` | Creator | Submit topic brief → start pipeline |
| | GET | `/courses/{id}/pipeline` | Creator | Pipeline status |
| | POST | `/courses/{id}/publish` | Creator | Publish course |
| **Pipeline** | POST | `/courses/{id}/stages/{stage}/approve` | Creator | Approve pipeline stage |
| | POST | `/courses/{id}/stages/{stage}/regenerate` | Creator | Regenerate stage with instructions |
| **Voice** | POST | `/voice/train` | Creator | Upload audio → train voice model |
| | GET | `/voice/models` | Creator | List voice models |
| | POST | `/voice/test` | Creator | Test voice model with text |
| | DELETE | `/voice/{id}` | Creator | Delete voice model |
| **Lessons** | GET | `/courses/{id}/lessons` | JWT | List lessons |
| | GET | `/lessons/{id}/script` | JWT | Get lesson script |
| | GET | `/lessons/{id}/video` | JWT | Get video signed URL |
| | GET | `/lessons/{id}/slides` | JWT | Get slide download URL |
| **Quizzes** | GET | `/courses/{id}/quizzes` | JWT | List quizzes |
| | PATCH | `/courses/{id}/quizzes` | Creator | Update quiz questions |
| | POST | `/quizzes/{id}/attempt` | Student | Submit quiz attempt |
| | GET | `/quizzes/{id}/results` | Student | Get attempt results |
| **Students** | GET | `/students/{id}` | JWT | Student profile |
| | GET | `/students/{id}/enrollments` | Student | Enrolled courses |
| | GET | `/students/{id}/progress` | Student | Course progress |
| **Enrollments** | POST | `/enrollments` | System | Create enrollment (Stripe webhook) |
| | GET | `/enrollments/{id}/progress` | Student | Per-course progress |
| | POST | `/enrollments/{id}/complete` | Student | Mark course complete |
| **Certificates** | POST | `/certificates/generate` | System | Auto-generate on completion |
| | GET | `/certificates/verify/{code}` | Public | Verification page |
| **Analytics** | GET | `/analytics/courses/{id}/overview` | Creator | Course analytics overview |
| | GET | `/analytics/courses/{id}/lessons` | Creator | Per-lesson analytics |
| | GET | `/analytics/courses/{id}/quizzes` | Creator | Quiz performance |
| | GET | `/analytics/courses/{id}/improvement-report` | Creator | Optimizer report |
| **Marketplace** | GET | `/marketplace/search` | Public | Algolia proxy search |
| | GET | `/marketplace/courses/{id}` | Public | Course detail page data |
| | GET | `/marketplace/recommendations` | Public | AI recommendations |
| **Affiliates** | POST | `/affiliates` | Creator | Generate affiliate link |
| | GET | `/affiliates/{id}/stats` | Creator | Affiliate performance |
| | GET | `/affiliates/{id}/payouts` | Creator | Affiliate payout history |
| **Enterprise** | POST | `/batch/jobs` | Admin | Submit batch CSV |
| | GET | `/batch/jobs/{id}` | Admin | Batch status |
| | POST | `/batch/jobs/{id}/retry` | Admin | Retry failed job |
| **Webhooks** | POST | `/webhooks/stripe` | Public | Stripe event webhook |
| | POST | `/webhooks/sendgrid` | Public | SendGrid event webhook |
| | POST | `/webhooks/twilio` | Public | Twilio status callback |
| **Health** | GET | `/health` | Public | Basic health check |
| | GET | `/health/detailed` | Internal | Detailed service status |

### WebSocket Endpoints
- `WS /ws/pipeline/{job_id}/live` — Real-time pipeline stage progress (stage name, % complete, ETA)
- `WS /ws/analytics/{course_id}` — Live student enrollment + completion events
- `WS /ws/notifications/{user_id}` — Real-time in-app notifications

### Rate Limiting
| Tier | Limit |
|------|-------|
| Starter (Free) | 3 course builds/month, max 5 modules, 5 listings |
| Creator ($45/mo) | Unlimited builds, unlimited modules, priority queue |
| Studio ($109/mo) | Everything in Creator + 8 parallel builds |
| Enterprise | Unlimited everything, 30 parallel builds, custom rate limits |
| API (Public) | Standard: 200 req/min, Enterprise: 2,000 req/min |

---

## DEVELOPMENT WORKFLOW

### Local Development Setup
```bash
# Prerequisites
- Python 3.12+ (pyenv or asdf)
- Node.js 20+ (nvm or fnm)
- Docker Desktop (for local Supabase + Redis)
- Expo CLI (`npm install -g expo-cli`)

# Clone and setup
git clone <repo-url> && cd edugenie
cp .env.example .env.local

# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements/dev.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# Frontend Web
cd frontend-web
npm install
npm run dev

# Mobile App
cd mobile-app
npm install
npx expo start --tunnel

# Infrastructure
cd infra
docker compose up -d  # Local Supabase + Redis
```

### Environment Variables
```bash
# .env.local (all stored securely per platform)
ENVIRONMENT=development

# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
SUPABASE_ANON_KEY=eyJ...

# Gemini
GEMINI_API_KEY=AIza...

# Stripe
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_CONNECT_CLIENT_ID=ca_...

# SendGrid
SENDGRID_API_KEY=SG....

# Twilio
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_NUMBER=+14155551234

# Algolia
ALGOLIA_APP_ID=...
ALGOLIA_API_KEY=...
ALGOLIA_INDEX_NAME=edugenie_courses

# ElevenLabs (voice cloning, optional)
ELEVENLABS_API_KEY=...

# PostHog
POSTHOG_API_KEY=phc_...

# Langfuse (AI observability, optional)
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...

# Redis
REDIS_URL=redis://localhost:6379/0

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/edugenie

# Confluent Kafka (optional)
KAFKA_BOOTSTRAP_SERVERS=...
KAFKA_API_KEY=...
KAFKA_API_SECRET=...
```

### Testing Strategy

**Backend (Python/pytest):**
- Coverage: 80% core services, 60% routes
- `pytest tests/unit/` — Agent logic, cost calculations, quiz scoring, certificate generation
- `pytest tests/integration/` — Full pipeline E2E (12 fixed briefs), API contract tests with VCR.py
- `pytest tests/e2e/` — Multi-tenant isolation, payment flow with Stripe test mode

**Frontend Web (Jest + Playwright):**
- `npm run test` — Component tests with @testing-library/react
- `npx playwright test` — E2E tests for critical flows (signup → create course → publish)

**Mobile (Jest + Detox):**
- `npx jest` — Unit tests for components and services
- `npx detox test` — E2E for enrollment, quiz, certificate flows
- Manual testing via Expo Go on physical devices

**AI Evaluation:**
- Nightly pipeline tests on 12 fixed briefs; quality scored vs. baseline
- Weekly human review: 25 randomly selected courses rated 1–5
- Bi-weekly hallucination audit: 5% sample by domain experts
- Quarterly red-team: prompt injection, PII leakage, content policy bypass

**Load Testing (k6):**
- 300 concurrent pipeline builds + 5,000 concurrent video streams + 1,000 API req/sec
- 48h soak test pre-major release

### Code Quality Tools
- **Python:** ruff (linter + formatter), mypy (type checker), pre-commit hooks
- **TypeScript/JS:** ESLint + Prettier, tsc strict mode
- **Pre-commit:** `.pre-commit-config.yaml` — runs ruff, mypy, ESLint, prettier before commit

---

## CI/CD PIPELINE

### GitHub Actions Configuration

The CI/CD pipeline is defined in `.github/workflows/main.yml`. Two workflows handle dev and main branches:

**Workflow triggers:**
- **Pull request to `development` branch** → runs lint, type check, unit tests, build
- **Push to `main` branch** → runs full pipeline + deployment (manual approval gate)

**Pipeline stages:**
1. Lint (ruff for Python, ESLint + Prettier for TypeScript)
2. Type check (mypy for Python, tsc for TypeScript)
3. Unit tests (pytest for Python, Jest for TypeScript)
4. Security scan (Snyk / Trivy)
5. Docker build → Container Registry
6. Integration tests
7. Deploy (dev: auto on PR merge; main: manual approval)

### EAS Build for Mobile
```bash
# Development build (internal testing)
eas build --platform all --profile development

# Preview build (QA)
eas build --platform all --profile preview

# Production
eas build --platform all --profile production
eas submit --platform ios --profile production
eas submit --platform android --profile production
```

---

## DEPLOYMENT GUIDE

### 1. Platform Setup
- Choose a Docker-compatible hosting platform (Render, Railway, Fly.io, or self-hosted VPS)
- Set up Supabase project (PostgreSQL 16 + pgvector + Storage + Auth)
- Configure Redis instance (Upstash, Redis Labs, or self-hosted)

### 2. Infrastructure Provisioning
```bash
cd infra/terraform
terraform init
terraform workspace new staging
terraform apply -var-file="environments/staging.tfvars"
```

### 3. Secrets Management
```bash
# Store secrets in your platform's secret store or .env
# Required secrets:
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_ANON_KEY=
GEMINI_API_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_CONNECT_CLIENT_ID=
SENDGRID_API_KEY=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_NUMBER=
ALGOLIA_APP_ID=
ALGOLIA_API_KEY=
```

### 4. Custom Domain & SSL
- Configure DNS A/CNAME records pointing to your hosting provider
- SSL/TLS is handled automatically by the hosting platform
- TLS 1.3 enforced, HSTS header recommended

---

## MONITORING & OPERATIONS

### Prometheus Metrics Export (example)
```python
# backend/app/main.py
from prometheus_client import Counter, Histogram, start_http_server
import time

REQUEST_COUNT = Counter("api_requests_total", "Total API requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("api_request_duration_seconds", "API request latency", ["method", "endpoint"])
AI_COST = Counter("ai_cost_usd_total", "Total AI cost in USD", ["agent", "model"])
PIPELINE_FAILURES = Counter("pipeline_failures_total", "Pipeline stage failures", ["stage"])
```

### Grafana Dashboards
- **API Performance:** Latency p50/p95/p99 per endpoint, error rate, throughput
- **AI Pipeline:** Per-stage latency, cost per build, model usage breakdown
- **Business:** Active creators, course builds, enrollments, revenue, completion rate
- **Infrastructure:** CPU/memory per container, Redis memory, Storage metrics

### Alerting Rules (Grafana)
| Alert | Condition | Notification |
|-------|-----------|-------------|
| API Error Rate | > 1% for 5 min | PagerDuty (critical) |
| P95 Latency | > 800ms for 5 min | Slack (high) |
| AI Cost/ Build | > $25 single run | Slack (finance) |
| Pipeline Failure | > 4% in 24h | PagerDuty (critical) |
| Video Render Queue | Depth > 200 | Slack (auto-scale) |
| Database Replication Lag | > 30s | PagerDuty (critical) |
| SMS/Email Failure | > 2% delivery fail | Slack (high) |

### Cost Optimization Strategies
- **AI Model Routing:** GPT-4o-mini for low-complexity tasks (quizzes, short tasks), GPT-4o for curriculum + scripts
- **Narration Caching:** Cache ElevenLabs TTS by `(script_hash + voice_id)` — ~35% cost reduction
- **Cloud Batch:** Preemptible VMs for FFmpeg video rendering (~60% cost savings)
- **Cloud CDN:** Cache static assets, video segments at edge
- **Cloud Storage Lifecycle:** Archive to Nearline after 90 days, Coldline after 365 days
- **Scaling:** Cloud Run min-instances=0 for non-critical services (auto-scale down to zero)

---

## SECURITY CONSIDERATIONS

### Data Encryption
- **At Rest:** AES-256 for PII (student names/emails) at application level; Cloud Storage server-side encryption (AES-256); Supabase encryption at rest
- **In Transit:** TLS 1.3 enforced for all external traffic; VPC internal traffic encrypted by default

### API Security
- **Authentication:** JWT (1hr expiry) + refresh tokens (30-day rotation)
- **Authorization:** Supabase RLS + FastAPI dependency injection for role checks
- **Input Validation:** Pydantic v2 on all endpoints
- **CORS:** Whitelist of allowed origins (edugenie.io, *.edugenie.io)
- **Rate Limiting:** 200 req/min standard, 2000 req/min enterprise
- **Webhook Verification:** Stripe HMAC-SHA256, Twilio signature validation, SendGrid webhook signature

### AI Safety & Governance
- **Content Policy:** Topic screened at intake (hate, misinformation, fraud, dangerous DIY) — hard reject before any resources consumed
- **Hallucination Handling:** [VERIFY] tags on uncertain claims; creator must dismiss each flag before video generation
- **Regulated Domains:** Medical/legal/financial topics trigger mandatory disclaimer injection
- **Voice Consent:** Mandatory consent confirmation with audit log before training
- **Originality Check:** All scripts through Originality.ai; > 12% similarity triggers regeneration
- **PII Detection:** Microsoft Presidio scans creator-uploaded reference content before LLM context injection
- **Prompt Injection:** User content sandboxed; system prompt integrity validated per request
- **Audit Logging:** Immutable append-only log of all AI decisions, creator actions, system events (7-year retention)

### Compliance Roadmap
- **GDPR:** Right to access (30-day export), right to deletion (90-day processing), Data Processing Agreement with sub-processors
- **CCPA:** No data sale, quarterly privacy review
- **COPPA:** Age gate at registration
- **PCI-DSS:** Handled by Stripe (Stripe is PCI-DSS Level 1 certified)
- **SOC 2 Type II:** Target within 18 months of launch; audit preparation begins Month 9

---

## DEVELOPMENT PHASES

### Phase 0: Foundation (Month 1–2)
**Deliverables:**
- GCP infrastructure + Terraform
- Supabase schema + auth + RLS policies
- FastAPI project scaffold + Alembic migrations
- Redis/Memorystore + BullMQ job queue
- LangGraph orchestrator skeleton
- Intelligence Agent + Architect Agent
- Creator OS shell (topic brief + curriculum review screens)
- Cloud Build CI/CD pipeline
- Langfuse AI observability
- SendGrid + Twilio + Stripe base integrations
- Docker Compose local dev environment
- Staging environment deployed

**Success Criteria:**
- Empty course created via API end-to-end
- CI/CD pipeline green on push
- Local dev environment reproducible with one command
- Secrets accessible via Secret Manager in staging

### Phase 1: Alpha Pipeline (Month 3–4)
**Deliverables:**
- Scriptwriter Agent + MediaForge Agent (slides, voice, video)
- Evaluator Agent + Launchpad Agent
- Creator Studio full review workflow (6 stages)
- LearnSpace course player + quizzes + certificates
- Stripe payments + creator payouts (Connect)
- Voice Studio (ElevenLabs integration)
- Mobile app scaffold (Expo, navigation, auth)
- In-app notification system (WebSocket + push)
- Certificate generation (PDF/PNG + verification page)
- Invite-only alpha (30 creators)

**Success Criteria:**
- Full 10-module course built end-to-end in < 4 hours
- First paying student enrolled via Stripe
- Creator publishes course → live URL with checkout
- Certificate auto-generated on completion
- 30 alpha creators active, feedback collected

### Phase 2: Public Beta (Month 5–6)
**Deliverables:**
- Optimizer Agent (weekly improvement reports)
- Marketplace with Algolia search + AI recommendations
- Affiliate system with Stripe Connect payouts
- Analytics dashboard (real-time + weekly AI narrative)
- Multi-language (6 languages via Gemini + ElevenLabs)
- White-label storefront (beta)
- Promo code engine
- Course version management
- Revenue dashboard
- EAS Build for mobile (iOS TestFlight, Android internal track)

**Success Criteria:**
- 800 paying creators
- $35K MRR
- 5,000 published courses
- $800K GMV
- Course completion rate > 35%

### Phase 3: Growth & Enterprise (Month 7–12)
**Deliverables:**
- Enterprise batch course generation (CSV upload, Kanban dashboard)
- Advanced analytics (cohort, heatmap, per-question analysis)
- Course repurposing engine
- Adaptive learner paths
- PWA mobile wrapper → full native features
- SSO/SAML + SCORM/xAPI export
- API public release with rate limiting
- Compliance course templates
- Enterprise SLA tiers
- SOC 2 Type II audit begins (Month 9)
- Native learner app (iOS + Android) via Expo

**Success Criteria:**
- 5,000 paying creators
- $180K MRR
- 30,000 courses
- $12M GMV
- 10 enterprise accounts
- Platform-wide completion rate > 45%

---

## DOCUMENTATION REQUIREMENTS

- **API Documentation:** OpenAPI/Swagger auto-generated at `/docs` (FastAPI built-in)
- **Architecture Decision Records:** `docs/adr/` — key technical decisions with rationale
- **Developer Onboarding:** `docs/development.md` — setup, conventions, workflow
- **Deployment Guide:** `docs/deployment.md` — provisioning, CI/CD, rollback
- **API Integration Guide:** For third-party developers consuming the public API

---

## KEY SUCCESS METRICS

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

## COST ESTIMATION (MVP)

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

---

## QUICK REFERENCE — COMMON COMMANDS

```bash
# Backend
cd backend && uvicorn app.main:app --reload --port 8000
cd backend && pytest -xvs tests/unit/
cd backend && alembic upgrade head

# Frontend Web
cd frontend-web && npm run dev
cd frontend-web && npm run lint
cd frontend-web && npm run test

# Mobile
cd mobile-app && npx expo start --tunnel
cd mobile-app && npx expo start --ios
cd mobile-app && npx jest

# Infrastructure
cd infra/terraform && terraform plan -var-file="environments/staging.tfvars"
cd infra && docker compose up -d
```

---

*Generated from PRD v1.0 — EduGenie OS. This CLAUDE.md serves as the authoritative specification for code generation. Stack: FastAPI · Next.js · Expo · LangGraph · Gemini 3.5 Flash · Supabase. Third-party integrations (SendGrid, Twilio, Stripe) remain consistent with documented PRD feature workflows.*
