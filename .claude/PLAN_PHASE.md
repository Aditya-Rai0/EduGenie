# PLAN_PHASE — EduGenie OS Phase-by-Phase Breakdown

Detailed phase-by-phase breakdown with tasks, timelines, dependencies, and deliverables.

---

## Phase 0: Foundation (Month 1–2)

### Goal
Stand up infrastructure, database, auth, CI/CD, and local dev environment. Deliver a working skeleton that can create an empty course end-to-end via API.

### Week 1-2: Infrastructure

#### Tasks
- [ ] Create Infrastructure project, enable APIs (Run, Build, Storage, secret store, Docker worker, monitoring)
- [ ] Set up Terraform backend (Supabase Storage bucket for state)
- [ ] Terraform modules: `compute/` (Container services), `network/` (VPC, LB, CDN, WAF), `storage/` (Supabase Storage, Redis), `monitoring/` (dashboards, alerts), `cicd/` (GitHub Actions triggers)
- [ ] Provision: Container (backend, frontend, workers), Redis (Redis 5GB), Supabase Storage (media bucket with lifecycle), CDN, Load balancer, WAF
- [ ] Create service accounts with least-privilege IAM
- [ ] Store all secrets in secret store (Gemini, Stripe, SendGrid, Twilio, Algolia, Supabase)
- [ ] Configure VPC, firewall rules

#### Deliverables
- `infra/terraform/` — Modules, environments (dev/staging/prod)
- Infrastructure project with all services provisioned
- Secret store populated with all API keys

### Week 2-3: Database & Auth

#### Tasks
- [ ] Set up Supabase project (PostgreSQL 16 + pgvector)
- [ ] Create all 19 core tables via Alembic migrations
- [ ] Implement RLS policies for all tables
- [ ] Configure Supabase Auth (magic link, Google OAuth, GitHub OAuth, email+password)
- [ ] Create auth helper utilities in FastAPI (JWT validation, refresh, role checks)
- [ ] Set up pgvector extension and indexes
- [ ] Create initial seed data scripts
- [ ] Configure PgBouncer connection pooling

#### Deliverables
- `backend/app/models/` — All 19 SQLAlchemy models
- `backend/alembic/versions/` — Initial migration
- `backend/app/core/security.py` — JWT + OAuth + RBAC middleware
- Supabase project configured with auth providers

### Week 3-4: Backend Scaffold

#### Tasks
- [ ] FastAPI project scaffold with dependency injection
- [ ] Settings (pydantic-settings) with env override + secret store integration
- [ ] Core utilities: `security.py`, `cache.py` (Redis), `storage.py` (Supabase), `queue.py` (BullMQ/arq)
- [ ] API v1 router structure with all endpoint stubs
- [ ] Health check endpoints (`/health`, `/health/detailed`)
- [ ] Base agent class (`agents/base.py`) and orchestrator skeleton
- [ ] WebSocket manager for pipeline + notifications
- [ ] Logging setup (structured JSON)
- [ ] Error handling middleware (custom exceptions, validation errors, 500 handler)

#### Deliverables
- `backend/app/main.py` — Working FastAPI app with all routes registered
- `backend/app/api/v1/` — All endpoint modules (auth, courses, creators, lessons, quizzes, enrollments, certificates, marketplace, analytics, voice, affiliates, batch, webhooks, health)
- `backend/app/api/ws/` — WebSocket endpoints (pipeline, analytics, notifications)
- `backend/app/core/` — All core utilities

### Week 4-5: Frontend Scaffold

#### Tasks
- [ ] Next.js 14+ project with App Router
- [ ] Tailwind CSS configuration with brand design system (blue #2563EB accent, Inter typography)
- [ ] Radix UI primitive wrappers in `components/ui/`
- [ ] Layout components (header, sidebar, footer)
- [ ] Auth pages (login, signup, magic-link)
- [ ] Supabase client setup (`lib/supabase.ts`)
- [ ] API client wrapper (`lib/api-client.ts`) with auth token injection
- [ ] Zustand stores (auth, course builder, notifications)
- [ ] TanStack Query setup for server state
- [ ] Stripe Elements configuration
- [ ] Landing / Marketplace page shell

#### Deliverables
- `frontend-web/` — Working Next.js app
- All layouts, auth screens, and shared UI components
- State management and API client

### Week 5-6: CI/CD & Local Dev

#### Tasks
- [ ] GitHub Actions pipeline: lint (ruff, eslint) -> type check (mypy, tsc) -> test (pytest, jest) -> build (Docker) -> push (Container Registry) -> deploy (Container)
- [ ] Blue/green deployment with traffic splitting
- [ ] Post-deploy smoke tests
- [ ] Docker Compose local dev environment (FastAPI, Next.js, Supabase local, Redis, MailHog)
- [ ] Pre-commit hooks (ruff, mypy, eslint, prettier)
- [ ] README and development docs

#### Deliverables
- `.github/workflows/main.yml` — Full CI/CD pipeline
- `docker-compose.yml` — Local dev environment
- `.pre-commit-config.yaml`
- `docs/development.md`

### Week 6-8: Base Integrations & Staging

#### Tasks
- [ ] SendGrid base setup: API client, welcome email template, webhook handler
- [ ] Twilio base setup: WhatsApp client, message template registration, webhook handler
- [ ] Stripe base setup: Checkout session creation, webhook verification, Connect onboarding
- [ ] Deploy staging environment
- [ ] E2E test: create empty course via API
- [ ] E2E test: auth flow (signup -> magic link -> JWT)
- [ ] Staging monitoring dashboards
- [ ] Load test baseline (k6)

#### Deliverables
- `backend/app/integrations/sendgrid.py`
- `backend/app/integrations/twilio.py`
- `backend/app/integrations/stripe.py`
- Staging environment live
- All Phase 0 acceptance tests passing

### Phase 0 Acceptance Criteria
- [ ] CI/CD pipeline green on push to `develop`
- [ ] Local dev environment reproducible with `docker compose up`
- [ ] Supabase schema migrated with all 19 tables + RLS
- [ ] Auth working (signup, magic link, JWT)
- [ ] Empty course created via API E2E
- [ ] Stripe Checkout session creates successfully (test mode)
- [ ] SendGrid email sends (test mode)
- [ ] Twilio WhatsApp message sends (test mode)
- [ ] Secrets accessible via secret store in staging
- [ ] Load test: 50 concurrent requests, p95 < 500ms

---

## Phase 1: Alpha Pipeline (Month 3–4)

### Goal
Build the full 7-agent AI pipeline, Creator Studio review workflow, LearnSpace course player, Stripe payments, and mobile scaffold. Launch invite-only alpha with 30 creators.

### Week 1-2: AI Agents (Intelligence + Architect)

#### Tasks
- [ ] LangGraph supervisor orchestrator (`agents/orchestrator.py`)
  - State machine with checkpointing (Redis)
  - Per-stage progress reporting via WebSocket
  - Error handling + retry + timeout per stage
  - Cost tracking per agent call (Langfuse)
- [ ] Intelligence Agent
  - Web search tools (Google Custom Search API + Bing Search API)
  - Competitor scrape tool
  - Market report generation (demand score, 5+ competitor courses, 3 angle options)
  - Research cache by `(topic_hash, date)` with pgvector dedup
- [ ] Architect Agent
  - Bloom's taxonomy curriculum design
  - JSON output: modules (8-16), lessons (3-8 each), objectives, prerequisites, durations
  - Curriculum validation rules (module count, lesson depth, time estimates)
- [ ] REVIEW GATE 1: Creator approves topic angle
- [ ] REVIEW GATE 2: Creator reorders / approves outline

#### Deliverables
- `backend/app/agents/orchestrator.py`
- `backend/app/agents/intelligence_agent.py`
- `backend/app/agents/architect_agent.py`
- `backend/app/agents/tools/web_search.py`
- `backend/app/agents/tools/competitor_scrape.py`

### Week 2-3: AI Agents (Scriptwriter + MediaForge)

#### Tasks
- [ ] Scriptwriter Agent
  - Parallel lesson script writing (2,000-4,000 words per lesson)
  - Structured sections: hook, concept, example, code (if applicable), summary
  - [VERIFY] flags on uncertain claims
  - Plagiarism check via Originality.ai (> 12% triggers regeneration)
  - PII scan via Microsoft Presidio before storing
  - Script storage in Supabase Storage (JSON + markdown)
- [ ] MediaForge Agent — Slides
  - Slide generation: JSON outline per lesson (10-20 slides)
  - `python-pptx` render to PPTX
  - PNG frame extraction for video compositing
  - Storage: PPTX + PNG frames in Supabase Storage
- [ ] MediaForge Agent — Voice
  - Gemini TTS (primary) or ElevenLabs (if voice model trained)
  - MP3 narration generation per lesson
  - Caching by `(script_hash + voice_id)` — ~35% cost reduction
  - Storage: MP3 in Supabase Storage
- [ ] MediaForge Agent — Video
  - FFmpeg rendering (PNG frames + MP3 narration)
  - 1080p MP4 output
  - Gemini STT caption generation
  - Docker worker job submission
  - Storage: MP4 + SRT in Supabase Storage

#### Deliverables
- `backend/app/agents/scriptwriter_agent.py`
- `backend/app/agents/mediaforge_agent.py`
- `backend/app/agents/tools/slides.py`
- `backend/app/agents/tools/voice.py`
- `backend/app/agents/tools/video.py`
- `backend/app/agents/tools/captions.py`

### Week 3-4: AI Agents (Evaluator + Launchpad + Optimizer)

#### Tasks
- [ ] Evaluator Agent
  - Per-module quiz generation (5-12 questions)
  - Question types: multiple choice, true/false, fill-in-blank, coding
  - Capstone project brief + rubric
  - Flashcards generation
  - Quiz validation (correct answer coverage, difficulty curve)
- [ ] Launchpad Agent
  - Sales page HTML generation (hero, features, testimonials, pricing, FAQ)
  - Email launch sequence (6 emails: welcome, module 1, mid-point, final, certificate, upsell)
  - Social media posts (15 posts: Twitter/X, LinkedIn, Instagram)
  - Pricing recommendation (based on module count + market data)
- [ ] Optimizer Agent (Post-Launch)
  - Student analytics ingestion (completions, drop-off, quiz scores)
  - Improvement report generation (weekly)
  - Prioritized fix recommendations
  - Email digest to creator

#### Deliverables
- `backend/app/agents/evaluator_agent.py`
- `backend/app/agents/launchpad_agent.py`
- `backend/app/agents/optimizer_agent.py`
- All agent tools modules

### Week 4-5: Creator Studio (Full 6-Stage Review)

#### Tasks
- [ ] Stage 1: Market Review — display market report, approve angle
- [ ] Stage 2: Curriculum Review — display outline, reorder/approve
- [ ] Stage 3: Script Review — display scripts, edit, approve
- [ ] Stage 4: Media Review — preview slides + voice + video
- [ ] Stage 5: Quiz Review — preview quizzes, capstone, flashcards
- [ ] Stage 6: Launch Review — preview sales page, pricing, emails, social
- [ ] Pipeline progress tracking (real-time via WebSocket)
- [ ] Regenerate single stage with custom instructions
- [ ] Publish flow (DB record, Stripe product, Algolia index, live URL)

#### Deliverables
- `frontend-web/app/(creator)/studio/` — All 6 review stage screens
- `frontend-web/components/creator/` — Stage-specific components
- `backend/app/api/v1/courses.py` — Pipeline + publish endpoints
- WebSocket handler for live pipeline progress

### Week 5-6: LearnSpace (Course Player + Quizzes + Certificates)

#### Tasks
- [ ] Course player: video player (signed URLs), script display, progress tracking
- [ ] Quiz interface: per-module quiz, timer, auto-grading
- [ ] Capstone submission: file upload, description, rubric display
- [ ] Discussion Q&A: per-lesson, AI-powered answer suggestions, creator verification
- [ ] Progress tracking: per-lesson watch depth %, time spent, completion
- [ ] Certificate generation: PDF/PNG with verification code
- [ ] Certificate verification page (public)
- [ ] Enrollment management

#### Deliverables
- `frontend-web/app/(learnspace)/learn/[courseId]/` — Course player
- `frontend-web/app/(learnspace)/quiz/[attemptId]/` — Quiz screen
- `frontend-web/app/(learnspace)/certificate/verify/[code]` — Verification
- `backend/app/api/v1/lessons.py` — Signed URLs, progress update
- `backend/app/api/v1/quizzes.py` — Attempt submission, grading
- `backend/app/api/v1/certificates.py` — Generate, verify
- `backend/app/utils/pdf.py` — Certificate generation

### Week 6-7: Payments & Mobile Scaffold

#### Tasks
- [ ] Stripe Checkout integration (course purchase flow)
- [ ] Stripe webhooks: `checkout.session.completed` -> enroll student
- [ ] Stripe Connect Express: creator onboarding, bi-weekly payouts
- [ ] Payment receipt emails (SendGrid)
- [ ] Stripe Tax for EU transactions
- [ ] Promo code support (Stripe Coupons)
- [ ] Voice Studio: upload audio (10-30 min), train ElevenLabs model, test + deploy
- [ ] Mobile app scaffold: Expo project, navigation, auth flow
- [ ] Mobile marketplace browse + course detail screens
- [ ] Mobile course player (basic)

#### Deliverables
- Stripe payments fully integrated (web, mobile)
- Voice Studio MVP
- Mobile app scaffold with auth + browse + play

### Week 7-8: Notifications, Alpha Launch

#### Tasks
- [ ] WebSocket notification system (pipeline, enrollment, certificate)
- [ ] Push notifications (Expo Push + FCM)
- [ ] In-app notification center (read/unread, list, badge)
- [ ] Onboarding email sequence (signup -> welcome -> getting started)
- [ ] Load test: full pipeline build for 10-module course
- [ ] Alpha invite system (30 creators)
- [ ] Monitoring alerts configured (API error rate, pipeline failure, AI cost)
- [ ] Alpha feedback collection system
- [ ] Bug bash + stabilization

#### Deliverables
- Notification system (WebSocket + push + in-app)
- Email onboarding sequence
- Alpha program live (30 creators)
- Monitoring dashboards + alerts

### Phase 1 Acceptance Criteria
- [ ] Full 10-module course built end-to-end in < 4 hours
- [ ] All 7 agents functional in pipeline
- [ ] AI cost per course < $12 blended
- [ ] Creator Studio with 6-stage review flow
- [ ] First paying student enrolled via Stripe Checkout
- [ ] Creator publishes course -> live URL with checkout
- [ ] Certificate auto-generated on course completion
- [ ] Mobile app: browse, course detail, login
- [ ] 30 alpha creators active
- [ ] Pipeline success rate > 95%

---

## Phase 2: Public Beta (Month 5–6)

### Goal
Launch public beta with marketplace, affiliates, analytics, multi-language, mobile app, and all commerce features. Onboard 800 creators, reach $35K MRR.

### Week 1-2: Marketplace & Search

#### Tasks
- [ ] Algolia index setup: course attributes, searchable fields, faceting
- [ ] Marketplace backend: search proxy, filtering (category, price, language, rating), sorting
- [ ] AI recommendations: personalized course suggestions (pgvector similarity)
- [ ] Free previews: first lesson video + script preview
- [ ] Course detail page: description, curriculum, reviews, instructor
- [ ] Rating and review system
- [ ] Enroll / purchase CTA

#### Deliverables
- `backend/app/api/v1/marketplace.py` — Search, recommendations, detail
- `backend/app/integrations/algolia.py` — Index management
- `frontend-web/app/(learnspace)/marketplace/` — Browse, search, detail
- `mobile-app/src/screens/marketplace/` — Mobile equivalents

### Week 2-3: Affiliates & Revenue

#### Tasks
- [ ] Affiliate link generation (creator referral links)
- [ ] Commission tracking (clicks, conversions, earned)
- [ ] Stripe Connect payouts (bi-weekly, min $25 threshold)
- [ ] Affiliate dashboard: stats, links, payouts
- [ ] Affiliate commission notifications
- [ ] Revenue dashboard: course sales, subscription, payout history, projections
- [ ] Promo code management (create, activate, deactivate, analytics)

#### Deliverables
- `backend/app/api/v1/affiliates.py`
- `backend/app/api/v1/creators.py` — Revenue endpoints
- `frontend-web/app/(creator)/revenue/` — Revenue dashboard
- `frontend-web/app/(creator)/affiliates/` — Affiliate dashboard
- Stripe Connect payout integration

### Week 3-4: Analytics Dashboard

#### Tasks
- [ ] Real-time analytics: enrollments, completions, drop-off per lesson
- [ ] Quiz performance: per-question pass rate, difficulty analysis
- [ ] Cohort analytics: enrollment trends, retention by week
- [ ] AI narrative: natural language summary of course performance
- [ ] Optimizer agent integration: weekly improvement report display
- [ ] Export analytics (CSV download)

#### Deliverables
- `backend/app/api/v1/analytics.py`
- `frontend-web/app/(creator)/analytics/` — Full analytics dashboard
- `backend/app/services/analytics_service.py`
- WebSocket for live analytics events

### Week 4-5: Multi-Language

#### Tasks
- [ ] 6 target languages: Spanish, French, German, Portuguese, Hindi, Japanese
- [ ] Gemini translation pipeline (course content, scripts, quizzes)
- [ ] ElevenLabs multilingual TTS (per-language voice models)
- [ ] Subtitle generation per language
- [ ] Language selector (student preference)
- [ ] Language-specific marketplace filtering
- [ ] Cultural localization notes (idioms, examples, references)

#### Deliverables
- Multi-language agent updates (Scriptwriter, MediaForge)
- Language preference management
- Translated subtitles + voice tracks

### Week 5-6: Mobile App Completion

#### Tasks
- [ ] Full mobile marketplace (browse, search, filter, detail)
- [ ] Full course player (video, progress, notes)
- [ ] Quiz interface (mobile-optimized)
- [ ] Certificate download / share
- [ ] Push notifications (course updates, reminders)
- [ ] Stripe SDK for Apple Pay / Google Pay
- [ ] Offline support (downloaded videos, cached scripts)
- [ ] EAS Build: iOS TestFlight + Android Internal Track

#### Deliverables
- `mobile-app/` — Complete learner app
- EAS Build profiles for dev/preview/production
- Stripe mobile payments

### Week 6-7: White-Label & Versioning

#### Tasks
- [ ] White-label storefront: custom domain, brand colors, logo
- [ ] Course version management: version history, changelog
- [ ] Selective regeneration: update single lesson/module, regenerate
- [ ] Student notifications on course updates
- [ ] Rollback to previous version

#### Deliverables
- `frontend-web/app/(creator)/studio/` — Version management UI
- `backend/app/models/course_version.py` — Version model
- White-label storefront settings

### Week 7-8: Beta Launch

#### Tasks
- [ ] Load test: 1,000 concurrent learners, 100 parallel builds
- [ ] Security audit: penetration test, dependency scan
- [ ] Performance optimization: bundle size, image optimization, CDN tuning
- [ ] Onboarding flow optimization
- [ ] Beta waitlist management -> open access
- [ ] Marketing site readiness
- [ ] Launch day runbook
- [ ] Post-launch monitoring (48h)

#### Deliverables
- Public beta live
- Load test report
- Security audit report
- Launch runbook

### Phase 2 Acceptance Criteria
- [ ] 800 paying creators onboarded
- [ ] $35K MRR achieved
- [ ] 5,000 published courses on marketplace
- [ ] $800K GMV
- [ ] Course completion rate > 35%
- [ ] Marketplace search < 500ms p95
- [ ] Mobile app available on TestFlight + Internal Track
- [ ] Multi-language support live (6 languages)
- [ ] Affiliate system operational

---

## Phase 3: Growth & Enterprise (Month 7–12)

### Goal
Scale to 5,000 creators, 30,000 courses, $180K MRR. Launch enterprise features, public API, and native mobile apps. Begin SOC 2 Type II audit.

### Month 7: Enterprise Batch Generation

#### Tasks
- [ ] CSV upload interface (topic, audience, depth, tone, language per row)
- [ ] Batch job management: 5-30 parallel course builds
- [ ] Kanban dashboard: pending, running, completed, failed
- [ ] SME routing: assign subject matter expert per course
- [ ] Batch progress tracking (per-course, aggregate)
- [ ] Retry failed jobs individually
- [ ] Enterprise usage analytics

#### Deliverables
- `backend/app/api/v1/batch.py`
- `frontend-web/app/(enterprise)/batch/` — Upload + Kanban
- `frontend-web/app/(enterprise)/kanban/` — Dashboard
- Batch queue management (BullMQ)

### Month 7-8: Advanced Analytics

#### Tasks
- [ ] Cohort analysis: enrollment, retention, completion by cohort
- [ ] Heatmap: per-second video engagement (seek, pause, drop)
- [ ] Per-question analysis: difficulty index, discrimination index
- [ ] Funnel analysis: browse -> enroll -> first lesson -> complete
- [ ] Export reports (PDF, CSV, automated weekly email)
- [ ] API for custom analytics queries

#### Deliverables
- Advanced analytics modules
- Report export system
- Analytics API

### Month 8-9: Course Repurposing & Adaptive Paths

#### Tasks
- [ ] Course repurposing: course -> blog post, social thread, email course, ebook
- [ ] Adaptive learner paths: skip known content, recommend remedial lessons
- [ ] Prerequisite-based pathing
- [ ] AI tutor: per-student Q&A with course context
- [ ] Personalized review sessions (spaced repetition)

#### Deliverables
- Repurposing engine
- Adaptive path engine
- AI tutor integration

### Month 9-10: Enterprise Features

#### Tasks
- [ ] SSO/SAML integration (Okta, Azure AD, Google Workspace)
- [ ] SCORM/xAPI export for LMS compatibility
- [ ] Compliance course templates (HIPAA, GDPR, SOC 2, PCI)
- [ ] Enterprise SLA tiers (99.95%, 99.99%)
- [ ] Audit trail export for enterprise customers
- [ ] Custom branding at enterprise level
- [ ] Role management (admin, manager, learner)
- [ ] SOC 2 Type II audit kickoff

#### Deliverables
- SSO/SAML integration
- SCORM/xAPI API
- Compliance templates
- Enterprise admin dashboard
- SOC 2 audit preparation

### Month 10: Public API

#### Tasks
- [ ] API documentation (OpenAPI, developer portal)
- [ ] Rate limiting tiers (standard 200/min, enterprise 2,000/min)
- [ ] API key management (create, revoke, usage stats)
- [ ] Webhook system for third-party integrations
- [ ] SDK generation (Python, JavaScript)
- [ ] Developer onboarding guide
- [ ] API usage dashboard
- [ ] API monetization (pay-per-request)

#### Deliverables
- Public API with documentation
- Developer portal
- SDK packages
- API key management system

### Month 10-11: Native Mobile Apps

#### Tasks
- [ ] Full native iOS app (Swift/SwiftUI) or via Expo dev client
- [ ] Full native Android app (Kotlin/Jetpack Compose) or via Expo dev client
- [ ] Offline-first architecture (downloaded courses, sync queue)
- [ ] Background audio playback
- [ ] Picture-in-picture video
- [ ] Native push notification optimization
- [ ] App Store + Play Store submission
- [ ] Mobile-specific analytics

#### Deliverables
- iOS app on App Store
- Android app on Play Store
- Mobile analytics

### Month 11-12: Scale & Optimization

#### Tasks
- [ ] Infrastructure cost optimization (right-sizing, reserved instances)
- [ ] AI cost optimization (model distillation, batch processing)
- [ ] Database optimization (query tuning, index optimization, partitioning)
- [ ] CDN tuning (cache hit ratio, edge optimization)
- [ ] Performance optimization (Lighthouse score > 90)
- [ ] Security hardening (penetration test, bug bounty program)
- [ ] 48-hour soak test (production scale)
- [ ] Disaster recovery drill
- [ ] SOC 2 evidence collection

#### Deliverables
- Performance optimization report
- Infrastructure cost report
- Security audit
- Disaster recovery plan

### Month 12: GA Launch

#### Tasks
- [ ] Marketing campaign (blog, social, PR, webinars)
- [ ] Case studies from top creators
- [ ] Pricing page optimization
- [ ] Enterprise sales enablement
- [ ] Partner program launch
- [ ] 24/7 support rotation
- [ ] GA announcement + press release

#### Deliverables
- General availability launch
- 5,000 creators, $180K MRR
- 30,000 courses published
- 10 enterprise accounts
- SOC 2 Type II underway

### Phase 3 Acceptance Criteria
- [ ] 5,000 paying creators
- [ ] $180K MRR
- [ ] 30,000 published courses
- [ ] $12M GMV
- [ ] 10 enterprise accounts
- [ ] Platform-wide completion rate > 45%
- [ ] Enterprise batch: 30 parallel builds
- [ ] API: 200 req/min standard, 2K enterprise
- [ ] Mobile: iOS + Android native apps
- [ ] SOC 2 Type II audit commenced
- [ ] API latency < 200ms p50, < 800ms p99
- [ ] Uptime 99.9%
