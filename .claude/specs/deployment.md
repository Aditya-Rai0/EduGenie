# Deployment — EduGenie OS

## CI/CD Pipeline

### GitHub Actions Configuration

**Trigger:** On push to `develop`/`main` branches

**Pipeline Stages:**
1. **Lint** — ruff + black for Python, ESLint + Prettier for TypeScript
2. **Type check** — mypy for Python, tsc for TypeScript
3. **Unit tests** — pytest (backend), Jest (frontend)
4. **Security scan** — Snyk / Trivy
5. **Docker build** → Container Registry
6. **Integration tests**
7. **Deploy** (staging auto, production manual promotion gate)

**Deployment Strategy:** Rolling update strategy
**Post-deploy:** Smoke tests → 1hr monitoring standby

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

## Deployment Guide

### 1. Platform Setup
- Choose a Docker-compatible hosting platform (Render, Railway, Fly.io, or self-hosted VPS)
- Set up Supabase project (PostgreSQL 16 + pgvector + Storage + Auth)
- Configure Redis instance (Upstash, Redis Labs, or self-hosted)

### 2. Infrastructure Provisioning (Terraform)
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

## Environment Variables

### .env.local (development)
All secrets stored in environment variables:

```bash
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
```

---

## Rollback Strategy

| Scenario | Action | Time |
|----------|--------|------|
| **Application** | One-command rollback to previous container image | < 3 min |
| **Database** | `alembic downgrade -1` with verification script | < 5 min |
| **AI Model** | Feature flag toggle to previous model version (no deployment) | < 15 min |
| **Full Environment** | Terraform rollback to previous state | < 10 min |

### Rollback Principles
- DB migrations: additive-only for 2 releases; destructive migrations require dual-write period + explicit rollback script in PR
- Feature flags (PostHog): all new AI features behind flags; rollout: 1% → 5% → 25% → 100% with quality metrics checked at each threshold
- AI model emergency rollback: model version pinned in config; revert via feature flag toggle

---

## Environment Setup

| Environment | Purpose | Configuration |
|-------------|---------|---------------|
| **Development (local)** | Local dev with Docker Compose | All external APIs mocked (VCR.py); local Supabase; Stripe test mode |
| **Staging** | Pre-prod testing; production mirror | Real AI APIs (rate-limited); test Stripe; 100 seeded courses + 500 students; E2E + load tests |
| **Production** | Live platform | Docker containers + Supabase + CDN; 24/7 monitoring; auto-scale active |

---

## Development Workflow (Local)

### Prerequisites
- Python 3.12+ (pyenv or asdf)
- Node.js 20+ (nvm or fnm)
- Docker Desktop (for local Supabase + Redis)
- Expo CLI (`npm install -g expo-cli`)


### Setup
```bash
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

---

## Testing Strategy

### Backend (Python/pytest)
- Coverage: 80% core services, 60% routes
- `pytest tests/unit/` — Agent logic, cost calculations, quiz scoring, certificate generation
- `pytest tests/integration/` — Full pipeline E2E (12 fixed briefs), API contract tests with VCR.py
- `pytest tests/e2e/` — Multi-tenant isolation, payment flow with Stripe test mode

### Frontend Web (Jest + Playwright)
- `npm run test` — Component tests with @testing-library/react
- `npx playwright test` — E2E tests for critical flows (signup → create course → publish)

### Mobile (Jest + Detox)
- `npx jest` — Unit tests for components and services
- `npx detox test` — E2E for enrollment, quiz, certificate flows
- Manual testing via Expo Go on physical devices

### AI Evaluation
- Nightly pipeline tests on 12 fixed briefs; quality scored vs. baseline
- Weekly human review: 25 randomly selected courses rated 1–5
- Bi-weekly hallucination audit: 5% sample by domain experts
- Quarterly red-team: prompt injection, PII leakage, content policy bypass

### Load Testing (k6)
- 300 concurrent pipeline builds + 5,000 concurrent video streams + 1,000 API req/sec
- 48h soak test pre-major release

### Code Quality Tools
- **Python:** ruff (linter + formatter), mypy (type checker), pre-commit hooks
- **TypeScript/JS:** ESLint + Prettier, tsc strict mode
- **Pre-commit:** `.pre-commit-config.yaml` — runs ruff, mypy, ESLint, prettier before commit

---

## Development Phases

### Phase 0: Foundation (Month 1–2)
**Deliverables:**
- Infrastructure provisioning + Terraform
- Supabase schema + auth + RLS policies
- FastAPI project scaffold + Alembic migrations
- Redis + BullMQ job queue
- LangGraph orchestrator skeleton
- Intelligence Agent + Architect Agent
- Creator OS shell (topic brief + curriculum review screens)
- GitHub Actions CI/CD pipeline
- Langfuse AI observability
- SendGrid + Twilio + Stripe base integrations
- Docker Compose local dev environment
- Staging environment deployed

**Success Criteria:**
- Empty course created via API end-to-end
- CI/CD pipeline green on push
- Local dev environment reproducible with one command
- Secrets accessible via secret store in staging

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
