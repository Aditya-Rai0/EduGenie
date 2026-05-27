# TASKS.md — EduGenie OS

Executable development roadmap organized in dependency-minimized phases. Each row is a mergeable unit of work.

**Branch convention:** `feature/<kebab-case-slug>`  
**Status legend:** ✅ Completed · ▶️ In Progress · ❌ Pending  

---

## Phase 0 · Foundation & Infrastructure

Zero product logic. Everything downstream depends on these being correct.

| Task | Branch | Status |
|------|--------|--------|
| P0-1 · Monorepo scaffold & root config (pyproject.toml, gitignore, prettier, Docker Compose) | `feature/monorepo-scaffold` | ✅ Completed |
| P0-2 · GitHub Actions CI/CD (lint → typecheck → test → Docker build → deploy) | `feature/github-actions` | ✅ Completed |
| P0-3 · Supabase project setup (DB, Storage, Auth providers, RLS templates) | `feature/supabase-config` | ✅ Completed |
| P0-4 · Environment variable templates (`.env.dev.example`, `.env.main.example`) | `feature/env-templates` | ✅ Completed |
| P0-5 · Docker Compose production-grade (PostgreSQL 16 + Redis 7 with healthchecks, volumes, networking) | `feature/docker-compose` | ✅ Completed |
| P0-6 · Terraform module stubs (compute, network, storage, monitoring, CI/CD, env presets) | `feature/terraform-stubs` | ❌ Pending |
| P0-7 · `.pre-commit-config.yaml` (ruff, mypy, ESLint, prettier hooks) | `feature/pre-commit` | ❌ Pending |
| P0-8 · Cloud Build → GitHub Actions migration cleanup (remove `infra/cloudbuild.yaml`) | `feature/cleanup-cloudbuild` | ❌ Pending |

---

## Phase 1 · Backend Data Layer (ORM, Migrations, Auth)

Depends on P0. No API routes yet — pure data layer.

| Task | Branch | Status |
|------|--------|--------|
| P1-1 · FastAPI project baseline, config, DI, Pydantic v2 schemas (all 14 files) | `feature/backend-baseline` | ✅ Completed |
| P1-2 · SQLAlchemy ORM models — Part 1 (organization, creator, course, course_version, module, lesson) | `feature/backend-models-core` | ❌ Pending |
| P1-3 · SQLAlchemy ORM models — Part 2 (quiz, student, enrollment, progress, quiz_attempt, sale, affiliate) | `feature/backend-models-relations` | ❌ Pending |
| P1-4 · SQLAlchemy ORM models — Part 3 (certificate, discussion, pipeline_run, improvement_report, notification, audit_log) | `feature/backend-models-aux` | ❌ Pending |
| P1-5 · Alembic initial migration (all 19 tables + pgvector extension + indexes) | `feature/alembic-init` | ❌ Pending |
| P1-6 · Alembic seed data & factory fixtures (test creators, courses, students) | `feature/alembic-seeds` | ❌ Pending |
| P1-7 · Supabase client wrapper & connection pooling (reuse `app/dependencies.py`) | `feature/supabase-client` | ❌ Pending |
| P1-8 · Auth service layer (signup, login, magic link, JWT validation, refresh tokens, role checking) | `feature/auth-service` | ❌ Pending |
| P1-9 · RBAC middleware & Supabase RLS policy enforcement | `feature/rbac-middleware` | ❌ Pending |
| P1-10 · Core utility modules (cache.py Redis client, queue.py task queue, storage.py Supabase Storage, webhook_handler.py) | `feature/core-utils` | ❌ Pending |

---

## Phase 2 · Backend API Layer (REST Endpoints)

Depends on P1. Implements all API routes from CLAUDE.md spec (~55 endpoints).

| Task | Branch | Status |
|------|--------|--------|
| P2-1 · Auth routes (signup, login, magic-link, refresh, me, OAuth callbacks) | `feature/api-auth` | ❌ Pending |
| P2-2 · Course CRUD routes (create, read, update, list, delete, topic brief submit, pipeline status, publish) | `feature/api-courses` | ❌ Pending |
| P2-3 · Creator profile & settings routes (profile CRUD, revenue dashboard) | `feature/api-creators` | ❌ Pending |
| P2-4 · Module & Lesson routes (CRUD, script fetch, video signed URL, slide download) | `feature/api-lessons` | ❌ Pending |
| P2-5 · Quiz routes (list, update, submit attempt, get results) | `feature/api-quizzes` | ❌ Pending |
| P2-6 · Enrollment & Progress routes (enroll, progress update, course complete, list enrollments) | `feature/api-enrollments` | ❌ Pending |
| P2-7 · Certificate routes (auto-generate on completion, verify by code) | `feature/api-certificates` | ❌ Pending |
| P2-8 · Analytics routes (course overview, per-lesson, per-quiz, improvement report) | `feature/api-analytics` | ❌ Pending |
| P2-9 · Marketplace routes (Algolia search proxy, course detail, recommendations) | `feature/api-marketplace` | ❌ Pending |
| P2-10 · Affiliate routes (link generation, stats, payout history) | `feature/api-affiliates` | ❌ Pending |
| P2-11 · Enterprise batch routes (CSV job submission, status, retry) | `feature/api-batch` | ❌ Pending |
| P2-12 · Voice routes (train model, list models, test TTS, delete model) | `feature/api-voice` | ❌ Pending |
| P2-13 · Webhook handlers (Stripe events, SendGrid events, Twilio status callbacks) | `feature/api-webhooks` | ❌ Pending |
| P2-14 · WebSocket endpoints (pipeline live `/ws/pipeline/{job_id}`, analytics live `/ws/analytics/{course_id}`, notifications `/ws/notifications/{user_id}`) | `feature/ws-endpoints` | ❌ Pending |
| P2-15 · Health & monitoring routes (basic health, detailed health, Prometheus metrics scrape) | `feature/api-health` | ❌ Pending |
| P2-16 · Pipeline stage approval/regeneration routes (approve stage, regenerate with feedback) | `feature/api-pipeline` | ❌ Pending |

---

## Phase 3 · AI Agent Pipeline (Gemini + LangGraph)

Depends on P1. Implements the 7-agent orchestrated pipeline.

| Task | Branch | Status |
|------|--------|--------|
| P3-1 · LangGraph state machine (agent state, checkpointing, supervisor, stage transition graph) | `feature/langgraph-core` | ❌ Pending |
| P3-2 · Web search tool (Google Custom Search + Bing Search API integration) | `feature/tool-web-search` | ❌ Pending |
| P3-3 · Competitor scrape tool (market intelligence data extraction) | `feature/tool-scrape` | ❌ Pending |
| P3-4 · Intelligence Agent (F1) — market demand analysis, competitor comparison, angle recommendations | `feature/agent-intelligence` | ❌ Pending |
| P3-5 · Architect Agent (F2) — Bloom's taxonomy curriculum design, module/lesson structure | `feature/agent-architect` | ❌ Pending |
| P3-6 · Scriptwriter Agent (F3) — parallel lesson script generation with [VERIFY] flags, 2K–4K words | `feature/agent-scriptwriter` | ❌ Pending |
| P3-7 · Slide generation tool (python-pptx, JSON → PPTX + PNG frames) | `feature/tool-slides` | ❌ Pending |
| P3-8 · Voice/TTS tool (Gemini TTS + ElevenLabs API, narration caching by script hash) | `feature/tool-voice` | ❌ Pending |
| P3-9 · Video rendering tool (FFmpeg: PNG frames + MP3 → 1080p MP4) | `feature/tool-video` | ❌ Pending |
| P3-10 · Caption generation tool (Gemini STT → SRT captions) | `feature/tool-captions` | ❌ Pending |
| P3-11 · MediaForge Agent (F4) — orchestrates slides + TTS + video + captions per module | `feature/agent-mediaforge` | ❌ Pending |
| P3-12 · Evaluator Agent (F5) — quiz generation (MCQ/T/F/fill-blank 5–12 per module), capstone brief, flashcards | `feature/agent-evaluator` | ❌ Pending |
| P3-13 · Launchpad Agent (F6) — sales page HTML, pricing recommendation, 6-email sequence, 15 social posts | `feature/agent-launchpad` | ❌ Pending |
| P3-14 · Optimizer Agent (F7) — post-launch analytics, drop-off analysis, sentiment NLP, improvement reports | `feature/agent-optimizer` | ❌ Pending |
| P3-15 · Pipeline orchestrator (sequential execution with review gates, parallel agent dispatch, error recovery, cost tracking) | `feature/pipeline-orchestrator` | ❌ Pending |

---

## Phase 4 · External Integrations

Depends on P1. Plugs into third-party services.

| Task | Branch | Status |
|------|--------|--------|
| P4-1 · Stripe integration (Checkout sessions, Connect payouts, webhook parsing, subscription management, promo codes) | `feature/integration-stripe` | ❌ Pending |
| P4-2 · SendGrid integration (email templates, transactional workflows, template engine) | `feature/integration-sendgrid` | ❌ Pending |
| P4-3 · Twilio integration (WhatsApp message sending, webhook handling, opt-out management) | `feature/integration-twilio` | ❌ Pending |
| P4-4 · Algolia integration (index management, search proxy endpoint, recommendation engine, sync on publish) | `feature/integration-algolia` | ❌ Pending |
| P4-5 · ElevenLabs integration (voice cloning, pronunciation dictionary, voice model management) | `feature/integration-elevenlabs` | ❌ Pending |
| P4-6 · Langfuse AI observability (LLM call tracing, cost tracking, latency monitoring) | `feature/integration-langfuse` | ❌ Pending |
| P4-7 · PostHog product analytics (event tracking, user properties, feature flags) | `feature/integration-posthog` | ❌ Pending |
| P4-8 · Originality.ai plagiarism check (script scanning pre-publish gate) | `feature/integration-originality` | ❌ Pending |
| P4-9 · Microsoft Presidio PII detection (creator upload scanning, content sanitization) | `feature/integration-presidio` | ❌ Pending |

---

## Phase 5 · Frontend Web — Creator OS

Depends on P1 (API layer). The creator-facing application.

| Task | Branch | Status |
|------|--------|--------|
| P5-1 · Next.js project scaffold (package.json, App Router layout, Tailwind theme, Radix UI primitives, Inter font, Zustand + TanStack Query setup) | `feature/web-scaffold` | ❌ Pending |
| P5-2 · Auth UI (login page, signup page, magic-link flow, OAuth buttons, session persistence, route guards) | `feature/web-auth` | ❌ Pending |
| P5-3 · Shared UI library (button, input, card, modal, toast, table, badge, spinner, skeleton) | `feature/web-ui-library` | ❌ Pending |
| P5-4 · Layout components (sidebar nav, top header, breadcrumbs, mobile drawer) | `feature/web-layout` | ❌ Pending |
| P5-5 · API client & hooks (Supabase client, Axios wrapper, useAuth, useCourses, useWebSocket, TanStack Query hooks) | `feature/web-api-layer` | ❌ Pending |
| P5-6 · Creator Dashboard (course list with status badges, pipeline progress bars, quick action buttons) | `feature/web-dashboard` | ❌ Pending |
| P5-7 · Topic Brief submission form (topic, audience, depth, tone, language — validates + submits to pipeline) | `feature/web-topic-brief` | ❌ Pending |
| P5-8 · Creator Studio — 6-stage review flow (Market → Curriculum → Scripts → Slides/Video → Quizzes → Launch) with approve/regenerate gates | `feature/web-creator-studio` | ❌ Pending |
| P5-9 · Course creation/edit form (title, description, price, thumbnail, version management) | `feature/web-course-edit` | ❌ Pending |
| P5-10 · Voice Studio (audio upload widget, model training status, test playback, voice selection dropdown) | `feature/web-voice-studio` | ❌ Pending |
| P5-11 · Analytics Dashboard (charts: enrollments, completion rate, drop-off, quiz scores; AI narrative summaries) | `feature/web-analytics` | ❌ Pending |
| P5-12 · Revenue Dashboard (sales chart, payout history, subscription tier, MoM comparison) | `feature/web-revenue` | ❌ Pending |
| P5-13 · Affiliate Dashboard (link creation, click/conversion stats, commission history) | `feature/web-affiliates` | ❌ Pending |
| P5-14 · Settings page (profile edit, notification prefs, payment methods, brand settings) | `feature/web-settings` | ❌ Pending |

---

## Phase 6 · Frontend Web — LearnSpace

Depends on P1. The student-facing application.

| Task | Branch | Status |
|------|--------|--------|
| P6-1 · Marketplace landing page (course cards, category filters, search bar, trending section) | `feature/web-marketplace` | ❌ Pending |
| P6-2 · Course detail page (description, curriculum accordion, preview video, enrollment CTA, pricing) | `feature/web-course-detail` | ❌ Pending |
| P6-3 · Course player (video player with captions/speed/chapters/auto-resume, side panel with lesson list, notes textarea) | `feature/web-course-player` | ❌ Pending |
| P6-4 · Quiz interface (question timer, option selection, submit confirmation, results overlay with explanations) | `feature/web-quiz` | ❌ Pending |
| P6-5 · Certificate view & download (animated badge, LinkedIn share, PDF download, public verify URL) | `feature/web-certificate` | ❌ Pending |
| P6-6 · Discussion Q&A per lesson (question form, AI-generated answer, creator verify badge, threaded replies) | `feature/web-discussions` | ❌ Pending |
| P6-7 · Enterprise batch dashboard (Kanban board, CSV upload wizard, bulk progress tracking, SME assignment) | `feature/web-enterprise-batch` | ❌ Pending |
| P6-8 · Notifications center (in-app notification list, real-time WebSocket updates, mark-read, bell badge) | `feature/web-notifications` | ❌ Pending |
| P6-9 · Search & discovery (Algolia autocomplete, faceted filters by category/level/price, personalized recommendations) | `feature/web-search` | ❌ Pending |

---

## Phase 7 · Mobile App (React Native + Expo)

Depends on P1. Cross-platform learner experience.

| Task | Branch | Status |
|------|--------|--------|
| P7-1 · Expo project scaffold (package.json, app.json, navigation structure, theme, providers) | `feature/mobile-scaffold` | ❌ Pending |
| P7-2 · Auth screens (login, signup, magic link, token persistence with expo-secure-store) | `feature/mobile-auth` | ❌ Pending |
| P7-3 · API service layer (Axios/fetch wrapper, Supabase client, endpoint hooks with TanStack Query) | `feature/mobile-api-layer` | ❌ Pending |
| P7-4 · LearnSpace screens (My Courses list, course detail, video player with expo-av) | `feature/mobile-learnspace` | ❌ Pending |
| P7-5 · Quiz screens (question card swipe, answer selection, results summary) | `feature/mobile-quiz` | ❌ Pending |
| P7-6 · Marketplace screens (browse grid, search with Algolia, course detail with enrollment) | `feature/mobile-marketplace` | ❌ Pending |
| P7-7 · Profile & Certificate screens (user profile, certificate gallery, download/ share, settings) | `feature/mobile-profile` | ❌ Pending |
| P7-8 · Push notifications (Expo Push Tokens, FCM config, deep link handling, notification preferences) | `feature/mobile-notifications` | ❌ Pending |
| P7-9 · EAS Build profiles (development, preview, production) + TestFlight + Google Play submission config | `feature/mobile-eas` | ❌ Pending |

---

## Phase 8 · Testing & QA

Depends on relevant implementation phases.

| Task | Branch | Status |
|------|--------|--------|
| P8-1 · Backend unit tests — models & services (pytest, factory-boy fixtures, coverage > 80%) | `feature/test-backend-unit` | ❌ Pending |
| P8-2 · Backend unit tests — agents & pipeline (mock Gemini, verify agent outputs, cost tracking) | `feature/test-backend-agents` | ❌ Pending |
| P8-3 · Backend integration tests — API endpoints (httpx AsyncClient, VCR.py for external API cassettes) | `feature/test-backend-integration` | ❌ Pending |
| P8-4 · Backend E2E tests — full pipeline (12 fixed topic briefs, verify course output artifacts) | `feature/test-backend-e2e` | ❌ Pending |
| P8-5 · Frontend component tests (Jest + @testing-library/react, all 14 page modules) | `feature/test-frontend-unit` | ❌ Pending |
| P8-6 · Frontend E2E tests (Playwright: signup → create course → publish flow) | `feature/test-frontend-e2e` | ❌ Pending |
| P8-7 · Mobile unit tests (Jest + React Native Testing Library, screens & hooks) | `feature/test-mobile-unit` | ❌ Pending |
| P8-8 · Mobile E2E tests (Detox / Maestro: enrollment, quiz, certificate flows) | `feature/test-mobile-e2e` | ❌ Pending |
| P8-9 · Load tests (k6: 300 concurrent builds, 5,000 video streams, 1,000 req/s, 48h soak) | `feature/test-load` | ❌ Pending |
| P8-10 · AI evaluation suite (nightly pipeline tests on 12 briefs, weekly human review, quarterly red-team) | `feature/test-ai-eval` | ❌ Pending |

---

## Phase 9 · Production & Monitoring

Depends on P0 and deployment readiness.

| Task | Branch | Status |
|------|--------|--------|
| P9-1 · Prometheus metrics instrumentation (request count, latency, AI cost, pipeline failures, queue depth) | `feature/monitoring-metrics` | ❌ Pending |
| P9-2 · Grafana dashboards (API performance, AI pipeline, business KPIs, infrastructure) | `feature/monitoring-dashboards` | ❌ Pending |
| P9-3 · Alerting rules & notification channels (Grafana alerts → Slack/PagerDuty, 7 alert conditions) | `feature/monitoring-alerts` | ❌ Pending |
| P9-4 · Sentry error tracking (backend + frontend, source maps, performance tracing) | `feature/monitoring-sentry` | ❌ Pending |
| P9-5 · Terraform production environment (infra state, secrets, DNS, SSL) | `feature/terraform-prod` | ❌ Pending |
| P9-6 · Production Docker images & Supabase RLS policies (hardening, migration automation) | `feature/prod-deploy` | ❌ Pending |
| P9-7 · Backup & disaster recovery (hourly DB backup, RPO < 1hr / RTO < 3hrs, runbook) | `feature/prod-dr` | ❌ Pending |
| P9-8 · Security hardening (CORS whitelist, rate limiting, WAF, secret rotation, penetration test) | `feature/prod-security` | ❌ Pending |

---

## Dependency Graph

```
P0 (Foundation & Infra)
  ├── P0-1 through P0-8 — parallelizable, no cross-deps
  │
P1 (Backend Data Layer) ← P0 (all)
  ├── P1-1 ✅ baseline → P1-2/3/4 models → P1-5 migration → P1-6 seeds
  ├── P1-7 client → P1-8 auth → P1-9 RBAC
  └── P1-10 utilities (parallel with P1-8)
  │
P2 (API Routes) ← P1 (all)
  ├── P2-1 auth routes ← P1-8/9
  ├── P2-2 through P2-16 — mostly parallel after P1
  │
P3 (AI Agents) ← P1 (models/migrations)
  ├── P3-1 LangGraph core
  ├── P3-2/3 tools → P3-4/5 agents → P3-6 through P3-14 agents → P3-15 orchestrator
  │
P4 (Integrations) ← P1 (all) — parallelizable with P2/P3
  ├── P4-1 through P4-9 — independent of each other
  │
P5 (Creator OS) ← P1 (all) + P2 (API)
  ├── P5-1 scaffold → P5-2/3/4/5 → P5-6 through P5-14
  │
P6 (LearnSpace) ← P1 (all) + P2 (API)
  ├── P6-1 through P6-9 — mostly parallel after P5-1
  │
P7 (Mobile) ← P1 (all) + P2 (API)
  ├── P7-1 scaffold → P7-2 through P7-9
  │
P8 (Testing) ← respective implementation phases
  ├── P8-1/2 ← P1 · P8-3/4 ← P2 · P8-5/6 ← P5/6 · P8-7/8 ← P7 · P8-9/10 ← all
  │
P9 (Production) ← P0 + P2 (deployable API)
  ├── P9-1/2/3/4 — parallel · P9-5/6/7/8 — sequential
```

## Phase Summary

| Phase | Tasks | Completed | Pending | Est. Duration |
|-------|-------|-----------|---------|---------------|
| P0 · Foundation & Infrastructure | 8 | 5 | 3 | Week 1–2 |
| P1 · Backend Data Layer | 10 | 1 | 9 | Week 2–4 |
| P2 · Backend API Routes | 16 | 0 | 16 | Week 4–7 |
| P3 · AI Agent Pipeline | 15 | 0 | 15 | Week 6–10 |
| P4 · External Integrations | 9 | 0 | 9 | Week 5–8 |
| P5 · Frontend Web — Creator OS | 14 | 0 | 14 | Week 7–11 |
| P6 · Frontend Web — LearnSpace | 9 | 0 | 9 | Week 9–12 |
| P7 · Mobile App | 9 | 0 | 9 | Week 10–14 |
| P8 · Testing & QA | 10 | 0 | 10 | Week 7–15 |
| P9 · Production & Monitoring | 8 | 0 | 8 | Week 13–16 |
| **Total** | **108** | **6** | **102** | **~16 weeks** |

## Feature-to-Phase Mapping

| Feature | Description | Phase | Primary Component |
|---------|-------------|-------|-------------------|
| F1 | Market Intelligence | P3-4 | Intelligence Agent |
| F2 | Curriculum Architect | P3-5 | Architect Agent |
| F3 | Lesson Script Engine | P3-6 | Scriptwriter Agent |
| F4 | Media Production | P3-7–P3-11 | MediaForge Agent |
| F5 | Assessment Engine | P3-12 | Evaluator Agent |
| F6 | Launchpad | P3-13 | Launchpad Agent |
| F7 | Optimizer | P3-14 | Optimizer Agent |
| F8 | Creator Studio | P5-8 | Creator OS |
| F9 | Voice Studio | P5-10 | Creator OS |
| F10 | Analytics Dashboard | P5-11 | Creator OS |
| F11 | Course Versioning | P5-9 | Creator OS |
| F12 | Affiliate & Revenue | P4-1, P5-12, P5-13 | Creator OS + Stripe |
| F13 | Multi-Language | P3-15 | Pipeline Config |
| F14 | Course Player & Progress | P6-3 | LearnSpace |
| F15 | Assessments & Certificates | P6-4, P6-5 | LearnSpace |
| F16 | Course Marketplace | P6-1, P6-2, P6-9 | LearnSpace |
| F17 | Payments & Subscriptions | P4-1 | Commerce (Stripe) |
| F18 | Enterprise Batch | P6-7 | Commerce |
