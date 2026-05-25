# Deployment — EduGenie OS

## CI/CD Pipeline

### Cloud Build Configuration

**Trigger:** On push to `develop`/`main` branches

**Pipeline Stages:**
1. **Lint** — ruff + black for Python, ESLint + Prettier for TypeScript
2. **Type check** — mypy for Python, tsc for TypeScript
3. **Unit tests** — pytest (backend), Jest (frontend)
4. **Security scan** — Snyk / Trivy
5. **Docker build** → Artifact Registry
6. **Integration tests**
7. **Deploy to Cloud Run** (staging auto, production manual promotion gate)

**Deployment Strategy:** Blue/green via Cloud Run revision traffic splitting
**Post-deploy:** Smoke tests → 100% traffic shift → 1hr monitoring standby

### Cloud Build YAML
```yaml
# cloudbuild.yaml
steps:
  # Backend
  - name: 'python:3.12'
    id: 'backend-lint'
    entrypoint: 'bash'
    args: ['-c', 'pip install ruff mypy && ruff check backend/ && mypy backend/']
  - name: 'python:3.12'
    id: 'backend-test'
    entrypoint: 'bash'
    args: ['-c', 'pip install -r backend/requirements/dev.txt && pytest backend/tests/unit/']
  - name: 'gcr.io/cloud-builders/docker'
    id: 'backend-build'
    args:
      - 'build'
      - '-t'
      - 'us-central1-docker.pkg.dev/$PROJECT_ID/edugenie/backend:$SHORT_SHA'
      - '-f'
      - 'backend/Dockerfile'
      - 'backend/'
    waitFor: ['backend-test']
  - name: 'gcr.io/cloud-builders/docker'
    id: 'backend-push'
    args:
      - 'push'
      - 'us-central1-docker.pkg.dev/$PROJECT_ID/edugenie/backend:$SHORT_SHA'
    waitFor: ['backend-build']
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    id: 'backend-deploy'
    entrypoint: 'gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'edugenie-backend'
      - '--image=us-central1-docker.pkg.dev/$PROJECT_ID/edugenie/backend:$SHORT_SHA'
      - '--region=us-central1'
      - '--platform=managed'
      - '--allow-unauthenticated'
      - '--memory=2Gi'
      - '--cpu=2'
      - '--min-instances=1'
      - '--max-instances=100'
      - '--concurrency=80'
      - '--set-secrets=OPENAI_API_KEY=openai-api-key:latest,...'
    waitFor: ['backend-push']

  # Frontend Web
  - name: 'node:20'
    id: 'frontend-lint'
    entrypoint: 'bash'
    args: ['-c', 'cd frontend-web && npm ci && npm run lint']
  - name: 'node:20'
    id: 'frontend-build'
    entrypoint: 'bash'
    args: ['-c', 'cd frontend-web && npm ci && npm run build']
    waitFor: ['frontend-lint']
  - name: 'gcr.io/cloud-builders/docker'
    id: 'frontend-image'
    args:
      - 'build'
      - '-t'
      - 'us-central1-docker.pkg.dev/$PROJECT_ID/edugenie/frontend:$SHORT_SHA'
      - '-f'
      - 'frontend-web/Dockerfile'
      - 'frontend-web/'
    waitFor: ['frontend-build']
  - name: 'gcr.io/cloud-builders/docker'
    id: 'frontend-push'
    args:
      - 'push'
      - 'us-central1-docker.pkg.dev/$PROJECT_ID/edugenie/frontend:$SHORT_SHA'
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    id: 'frontend-deploy'
    entrypoint: 'gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'edugenie-frontend'
      - '--image=us-central1-docker.pkg.dev/$PROJECT_ID/edugenie/frontend:$SHORT_SHA'
      - '--region=us-central1'
      - '--platform=managed'
      - '--allow-unauthenticated'
    waitFor: ['frontend-push']

  # Database Migrations
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    id: 'db-migrate'
    entrypoint: 'bash'
    args: ['-c', 'alembic upgrade head']
    env:
      - 'SUPABASE_URL=$_SUPABASE_URL'
      - 'SUPABASE_SERVICE_ROLE_KEY=$_SUPABASE_SERVICE_ROLE_KEY'
    waitFor: ['backend-test']

timeout: 1800s
substitutions:
  _SUPABASE_URL: ''
  _SUPABASE_SERVICE_ROLE_KEY: ''
options:
  machineType: 'E2_HIGHCPU_8'
```

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

### 1. GCP Project Setup
```bash
gcloud projects create edugenie-prod --name="EduGenie Production"
gcloud config set project edugenie-prod

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  storage.googleapis.com \
  cloudcdn.googleapis.com \
  compute.googleapis.com \
  secretmanager.googleapis.com \
  cloudresourcemanager.googleapis.com \
  iam.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com \
  cloudbatch.googleapis.com
```

### 2. Service Accounts & IAM

Create dedicated service accounts with least-privilege roles:

```bash
# Backend service account
gcloud iam service-accounts create edugenie-backend \
  --display-name="EduGenie Backend SA"

# Grant storage admin
gcloud projects add-iam-policy-binding edugenie-prod \
  --member="serviceAccount:edugenie-backend@edugenie-prod.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"

# Grant secret accessor
gcloud projects add-iam-policy-binding edugenie-prod \
  --member="serviceAccount:edugenie-backend@edugenie-prod.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Grant run invoker
gcloud projects add-iam-policy-binding edugenie-prod \
  --member="serviceAccount:edugenie-backend@edugenie-prod.iam.gserviceaccount.com" \
  --role="roles/run.invoker"

# Worker service account (adds batch job editor)
gcloud iam service-accounts create edugenie-workers \
  --display-name="EduGenie Workers SA"
gcloud projects add-iam-policy-binding edugenie-prod \
  --member="serviceAccount:edugenie-workers@edugenie-prod.iam.gserviceaccount.com" \
  --role="roles/batch.jobsEditor"
```

### 3. Infrastructure Provisioning (Terraform)
```bash
cd infra/terraform
terraform init -backend-config="bucket=edugenie-tfstate"
terraform workspace new staging
terraform plan -var-file="environments/staging.tfvars"
terraform apply -var-file="environments/staging.tfvars"
```

### 4. Secrets Management (Secret Manager)
```bash
# Store all secrets — one-time setup
echo -n "sk-proj-..." | gcloud secrets create openai-api-key --data-file=-
echo -n "SG.xxxxx" | gcloud secrets create sendgrid-api-key --data-file=-
echo -n "ACxxxxx:xxxxx" | gcloud secrets create twilio-auth --data-file=-
echo -n "sk_live_..." | gcloud secrets create stripe-secret-key --data-file=-
echo -n "whsec_..." | gcloud secrets create stripe-webhook-secret --data-file=-
echo -n "..." | gcloud secrets create elevenlabs-api-key --data-file=-
echo -n "..." | gcloud secrets create algolia-api-key --data-file=-
echo -n "..." | gcloud secrets create supabase-service-role-key --data-file=-
echo -n "..." | gcloud secrets create jwt-secret --data-file=-
```

### 5. Custom Domain Setup
```bash
# Verify domain ownership
gcloud domains verify edugenie.io

# Create managed DNS zone
gcloud dns managed-zones create edugenie-zone \
  --dns-name="edugenie.io." \
  --visibility=public

# Point API subdomain to load balancer
gcloud dns record-sets create api.edugenie.io \
  --zone=edugenie-zone \
  --type=A \
  --ttl=300 \
  --rrdatas="$(gcloud compute addresses describe edugenie-lb-ip --global --format='value(address)')"
```

### 6. SSL/TLS
- Cloud Load Balancer: Managed SSL certificate (Google Trust Services / Let's Encrypt)
- Automatic renewal
- TLS 1.3 enforced
- HSTS header configured on Load Balancer

---

## Environment Variables

### .env.local (development)
All secrets stored in GCP Secret Manager in production:

```bash
ENVIRONMENT=development

# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# GCP
GCP_PROJECT_ID=edugenie-prod
GCP_REGION=us-central1
GCP_STORAGE_BUCKET=edugenie-media

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_ORG_ID=org-...

# ElevenLabs
ELEVENLABS_API_KEY=...

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

# PostHog
POSTHOG_API_KEY=phc_...

# Langfuse
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...
```

---

## Rollback Strategy

| Scenario | Action | Time |
|----------|--------|------|
| **Application** | One-command Cloud Run service rollback to previous revision | < 3 min |
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
| **Production** | Live platform | GCP Cloud Run + Supabase + Cloud Storage + Cloud CDN; 24/7 monitoring; auto-scale active |

---

## Development Workflow (Local)

### Prerequisites
- Python 3.12+ (pyenv or asdf)
- Node.js 20+ (nvm or fnm)
- Docker Desktop (for local Supabase + Redis)
- Expo CLI (`npm install -g expo-cli`)
- GCP Cloud SDK (gcloud CLI)

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
- Multi-language (6 languages via OpenAI + ElevenLabs)
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
