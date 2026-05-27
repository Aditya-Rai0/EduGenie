# TASKS.md — EduGenie OS

Development plan in dependency-minimized phases. Each row is one mergeable unit of work; implement on the listed branch.
Branch convention: `feature/<repo-name>` — use a short kebab-case slug.
Status: ✅ Completed or ❌ Pending
References: CLAUDE.md, EduGenie_OS_PRD_Compact_v1.0.pdf.

---

## Phase P0 · Foundation (Month 1–2)

No cloud or product logic. Everything downstream assumes this exists.

| Task | Description | Branch | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- |
| P0-1 · Infrastructure setup & IAM | Infrastructure setup & IAM | `feature/infra-setup` | — | ❌ Pending |
| P0-2 · Supabase DB + Auth | PostgreSQL 16 schema + pgvector extension, Auth bootstrap (magic link, OAuth), RLS policies, Alembic migrations scaffold | `feature/db-auth-bootstrap` | P0-1 | ❌ Pending |
| P0-3 · Backend + Frontend skeleton | FastAPI app scaffold (config, DI, health endpoint) + Next.js 14 App Router shell (layout, routing, Tailwind, Radix UI) | `feature/app-skeleton` | P0-2 | ❌ Pending |
| P0-4 · Redis + Job Queue | Redis setup, BullMQ task queue for async course builds + video renders | `feature/queue-redis` | P0-1 | ❌ Pending |
| P0-5 · LangGraph orchestrator | Supervisor agent skeleton, pipeline state machine, checkpointing, stage transition logic | `feature/langgraph-base` | P0-3 | ❌ Pending |
| P0-6 · Intelligence + Architect agents (F1, F2) | Market research agent (web search, competitor scrape, demand scoring) + Curriculum architect agent (Bloom's taxonomy, module/lesson structure) | `feature/agents-intel-arch` | P0-4, P0-5 | ❌ Pending |
| P0-7 · Creator OS shell (F8) | Topic brief input UI + Curriculum review & reorder interface | `feature/ui-creator-shell` | P0-3, P0-6 | ❌ Pending |
| P0-8 · CI/CD pipeline | GitHub Actions triggers, Docker builds, Container Registry, staging deploy to Container, blue/green traffic split | `feature/ci-cd-pipeline` | P0-1 | ❌ Pending |

---

## Phase P1 · Alpha Pipeline (Month 3–4)

Depends on P0. AI agents, Creator Studio, LearnSpace, Stripe payments, and mobile scaffold.

| Task | Description | Branch | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- |
| P1-1 · Scriptwriter + MediaForge agents (F3, F4) | Lesson script writing (parallel, 2K–4K words each) + Slide generation (python-pptx, Gemini), ElevenLabs TTS narration, FFmpeg video render with Gemini captions | `feature/agents-media` | P0-5 | ❌ Pending |
| P1-2 · Evaluator + Launchpad agents (F5, F6) | Quiz generator (MCQ/T/F/fill-blank, 5–12 per module), capstone + rubric + flashcards + Sales page HTML, pricing rec, 6-email sequence, 15 social posts | `feature/agents-eval-launch` | P0-5 | ❌ Pending |
| P1-3 · Creator Studio full review (F8) | 6-stage review flow: Market → Curriculum → Scripts → Slides/Video → Quizzes → Launch. Inline editing, regeneration-with-note, approval gates, progress tracking | `feature/ui-creator-review` | P0-7, P1-1, P1-2 | ❌ Pending |
| P1-4 · LearnSpace player + assessments (F14, F15) | Video player (captions, speed, chapters, auto-resume), note-taking, quiz interface, certificate auto-generation (PDF/PNG), LinkedIn deeplink, public verification page | `feature/ui-learnspace` | P0-3, P1-1, P1-2 | ❌ Pending |
| P1-5 · Stripe payments + Connect (F17) | Stripe Checkout, subscriptions (Starter/Creator/Studio/Enterprise), Connect Express payouts, webhook handling, promo codes, Stripe Tax | `feature/stripe-payments` | P0-3 | ❌ Pending |
| P1-6 · Voice Studio (F9) | Audio upload (10–30 min), ElevenLabs voice model training, quality scoring, pronunciation dictionary, test & deploy UI | `feature/voice-studio` | P0-3, P1-1 | ❌ Pending |
| P1-7 · Mobile scaffold (Expo) | React Native + Expo SDK 52 setup, navigation (auth/learn/marketplace/profile), Supabase auth, basic course player screen | `feature/mobile-scaffold` | P0-3 | ❌ Pending |
| P1-8 · Notifications + SendGrid/Twilio | WebSocket notification system, in-app notifications table, SendGrid transactional emails (welcome, enrollment, certificate, weekly digest), Twilio WhatsApp (enrollment, reminders, receipts) | `feature/notifications-setup` | P0-3, P0-4 | ❌ Pending |

---

## Phase P2 · Public Beta (Month 5–6)

Depends on P1. Marketplace, affiliates, analytics, multi-language, and white-label.

| Task | Description | Branch | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- |
| P2-1 · Optimizer agent (F7) | Weekly post-launch analysis: drop-off heatmap, quiz failure patterns, discussion mining, sentiment NLP, prioritized improvement report with one-click fix links | `feature/agent-optimizer` | P1-1, P1-2 | ❌ Pending |
| P2-2 · Marketplace + Algolia (F16) | Public course catalog with Algolia search (faceted filters, autocomplete, personalized ranking), AI recommendations, free preview lessons, trending collections | `feature/marketplace-algolia` | P1-5 | ❌ Pending |
| P2-3 · Affiliates + Revenue (F12, F10) | Affiliate link generation, real-time conversion tracking, Stripe Connect payouts, fraud detection. Revenue dashboard: earnings by course/channel/period, refund rate, MoM growth, tax docs | `feature/affiliate-revenue` | P1-5 | ❌ Pending |
| P2-4 · Multi-language (F13) | 6 languages (EN/ES/PT/FR/DE/JA) via Gemini + ElevenLabs, cultural localization, language-native voice models, localized sales pages with hreflang SEO, PPP pricing | `feature/multi-language` | P1-1, P1-2 | ❌ Pending |
| P2-5 · White-label + Promo codes | White-label storefront with custom domain CNAME, brand customization (colors, logo, fonts), promo code engine (Stripe Coupon API, %/fixed, max uses, validity window) | `feature/whitelabel-promo` | P1-5 | ❌ Pending |
| P2-6 · Course versioning (F11) | Selective regeneration per module/lesson, version history, student change notifications, content staleness scanner, 3 active versions per course | `feature/course-versioning` | P1-1, P1-3 | ❌ Pending |
| P2-7 · Mobile EAS builds | EAS Build config for iOS TestFlight + Android internal track, push notifications (Expo + FCM), deep linking, Stripe SDK integration for mobile payments | `feature/mobile-eas-builds` | P1-7 | ❌ Pending |

---

## Phase P3 · Growth & Enterprise (Month 7–12)

Depends on P2. Enterprise batch generation, advanced analytics, and compliance.

| Task | Description | Branch | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- |
| P3-1 · Enterprise batch (F18) | CSV upload (5–30 parallel builds), SME routing + review links, Kanban dashboard for batch tracking, cost estimation before confirmation | `feature/enterprise-batch` | P1-3, P1-1 | ❌ Pending |
| P3-2 · Advanced analytics | Cohort analysis, lesson completion heatmaps, per-question failure analysis, cross-course comparison dashboards, automated PDF/CSV exports, weekly AI narrative | `feature/advanced-analytics` | P2-1, P2-3 | ❌ Pending |
| P3-3 · Adaptive learning paths | Branching curriculum with conditional module unlocks, AI-recommended remedial content for struggling students, personalized pace adjustment | `feature/adaptive-learning` | P1-4, P2-1 | ❌ Pending |
| P3-4 · SSO/SAML + SCORM/xAPI | Enterprise SSO (SAML/OIDC), SCORM 1.2/2004 export, xAPI statement generation for LMS integration, role provisioning via SCIM | `feature/enterprise-sso-scorm` | P0-2 | ❌ Pending |
| P3-5 · Public API + rate limits | Public REST API release with API key auth (multi-model, scoped per endpoint), rate limiting tiers (200/2000 req/min), developer docs with OpenAPI | `feature/public-api` | P0-3 | ❌ Pending |
| P3-6 · Compliance + SOC 2 | Compliance course templates (medical/legal/financial), mandatory disclaimer injection, PII scan (Presidio), SOC 2 Type II audit preparation, GDPR/CCPA data export & deletion flows | `feature/compliance-templates` | P1-3 | ❌ Pending |
| P3-7 · PWA + native features | PWA wrapper with offline support, service worker caching for video segments, push notifications via FCM, Apple Pay / Google Pay integration | `feature/pwa-mobile` | P1-7, P2-7 | ❌ Pending |

---

## Phase P4 · Ecosystem & Scale

Depends on P3. Optimization, security hardening, and GA launch.

| Task | Description | Branch | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- |
| P4-1 · Cost optimization | AI model routing (Gemini 3.5 Flash for low-complexity tasks), narration caching by script hash, preemptible VMs for FFmpeg, CDN edge caching, Container min-instances=0 for non-critical services | `feature/scale-optimization` | P1-1, P1-2 | ❌ Pending |
| P4-2 · Security hardening | Penetration testing (third-party), bug bounty program launch, prompt injection audit, OWASP Top 10 scan, WAF tuning, secret rotation automation | `feature/security-hardening` | P3-6 | ❌ Pending |
| P4-3 · Load testing (k6) | 300 concurrent pipeline builds, 5,000 concurrent video streams, 1,000 API req/sec sustained, 48-hour soak test pre-major release | `feature/load-testing` | P3-1, P3-5 | ❌ Pending |
| P4-4 · DR & runbooks | Disaster recovery drills, RPO < 1hr / RTO < 3hrs validation, runbook documentation, automated failover testing, backup restoration drills | `feature/dr-runbooks` | P0-1, P0-8 | ❌ Pending |
| P4-5 · GA launch | Marketing assets (demo video, case studies, landing page), partner program launch, public pricing page, self-serve onboarding flow, first customer onboarding program | `feature/ga-launch` | All P0–P3 | ❌ Pending |

---

## Dependency graph (summary)

```text
P0 (Foundation) ──────────────────────────────────────────────────────────┐
  │                                                                        │
  ├─ P0-1 (Infra)  ← P0-2 (DB) ← P0-3 (Skeleton) ← P0-5 (LangGraph) ─────┐│
  │                P0-1 ← P0-4 (Queue) ← P0-6 (Intel+Arch)               ││
  │                P0-3 + P0-6 ← P0-7 (UI Shell)                        ││
  │                P0-1 ← P0-8 (CI/CD)                                   ││
  │                                                                       ▼▼
P1 (Alpha Pipeline) ──────────────────────────────────────────────────────┘│
  │                                                                         │
  ├─ P1-1 (Script+Media) · P1-2 (Eval+Launch) ← P0-5                     │
  ├─ P1-3 (Creator Studio) ← P0-7 + P1-1 + P1-2                           │
  ├─ P1-4 (LearnSpace) ← P0-3 + P1-1 + P1-2                               │
  ├─ P1-5 (Stripe) ← P0-3                                                  │
  ├─ P1-6 (Voice) ← P0-3 + P1-1                                           │
  ├─ P1-7 (Mobile) ← P0-3                                                  │
  └─ P1-8 (Notifications) ← P0-3 + P0-4                                   │
                                                                           ▼
P2 (Public Beta) ─────────────────────────────────────────────────────────┘
  │
  ├─ P2-1 (Optimizer) ← P1-1 + P1-2
  ├─ P2-2 (Marketplace) ← P1-5
  ├─ P2-3 (Affiliate+Revenue) ← P1-5
  ├─ P2-4 (Multi-language) ← P1-1 + P1-2
  ├─ P2-5 (White-label) ← P1-5
  ├─ P2-6 (Versioning) ← P1-1 + P1-3
  └─ P2-7 (Mobile EAS) ← P1-7
                                                                           
P3 (Growth & Enterprise) ────────────────────────────────────────────────┘
  │
  ├─ P3-1 (Enterprise Batch) ← P1-3 + P1-1
  ├─ P3-2 (Advanced Analytics) ← P2-1 + P2-3
  ├─ P3-3 (Adaptive Learning) ← P1-4 + P2-1
  ├─ P3-4 (SSO/SCORM) ← P0-2
  ├─ P3-5 (Public API) ← P0-3
  ├─ P3-6 (Compliance) ← P1-3
  └─ P3-7 (PWA) ← P1-7 + P2-7

P4 (Ecosystem & Scale) ──────────────────────────────────────────────────┘
  └─ All P4 tasks ← P0–P3 complete
```

## Feature-to-phase mapping

| Feature | Description | Phase | Agent / Component |
| :--- | :--- | :--- | :--- |
| F1 | Market Intelligence & Validation | P0-6 | Intelligence Agent |
| F2 | Curriculum Architect | P0-6 | Architect Agent |
| F3 | Lesson Script Engine | P1-1 | Scriptwriter Agent |
| F4 | Slide Deck & Media Production | P1-1 | MediaForge Agent |
| F5 | Assessment & Evaluator Engine | P1-2 | Evaluator Agent |
| F6 | Launchpad — Sales Page, Pricing & Launch | P1-2 | Launchpad Agent |
| F7 | Optimizer — Post-Launch Improvement | P2-1 | Optimizer Agent |
| F8 | Creator Studio — Review & Edit Interface | P0-7, P1-3 | Creator OS |
| F9 | Voice Studio — Voice Model Training | P1-6 | Creator OS |
| F10 | Analytics Dashboard | P2-3 | Creator OS |
| F11 | Course Update & Version Management | P2-6 | Creator OS |
| F12 | Affiliate & Revenue System | P2-3 | Creator OS |
| F13 | Multi-Language Course Generation | P2-4 | Pipeline |
| F14 | Course Player & Progress Tracking | P1-4 | LearnSpace |
| F15 | Assessment Interface & Certificates | P1-4 | LearnSpace |
| F16 | Course Marketplace & Discovery | P2-2 | LearnSpace |
| F17 | Payments & Subscriptions | P1-5 | Commerce |
| F18 | Enterprise Batch Generation | P3-1 | Commerce |
