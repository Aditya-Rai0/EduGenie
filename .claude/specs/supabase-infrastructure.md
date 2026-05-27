# Supabase Infrastructure — EduGenie OS

## Overview

Supabase serves as our unified backend — replacing separate database, object storage, authentication, and queue services with a single integrated platform. All infrastructure is managed via Terraform.

---

## Compute Layer

### Docker Containers (Primary Compute)
All services run as Docker containers with the following configuration:

| Service | Purpose | RAM | vCPU |
|---------|---------|-----|------|
| `edugenie-backend` | FastAPI REST + WebSocket API | 2GB | 2 |
| `edugenie-frontend` | Next.js web frontend | 1GB | 1 |
| `edugenie-workers` | BullMQ job queue workers | 2GB | 2 |

- **Scaling:** Horizontal auto-scaling based on CPU/memory
- **Hosting:** Any Docker-compatible platform (Render, Railway, Fly.io, or self-hosted VPS)

### Video Rendering Worker
- **Purpose:** FFmpeg video rendering (PNG frames + MP3 narration → 1080p MP4)
- **Type:** Background worker (no GPU needed)
- **Max Parallel Renders:** Up to 50 simultaneous jobs
- **Job Dispatch:** Per lesson via BullMQ job queue
- **Output:** 1080p MP4 + SRT captions → Supabase Storage

---

## Storage Layer (Supabase Unified)

### Supabase Storage (Media)
| Attribute | Value |
|-----------|-------|
| Buckets | video, slides, audio, certificates |
| Signed URL Duration | 1 hour (video streaming) |
| Encryption | AES-256 (server-side) |
| Lifecycle | Configurable per bucket |

**Stored Assets:**
- Video files (MP4)
- Slide decks (PPTX, PDF, PNG frames)
- Audio narrations (MP3)
- Caption files (SRT)
- Certificates (PDF, PNG)
- Course thumbnails
- Script files

### Supabase PostgreSQL 16
- **Version:** PostgreSQL 16
- **Extension:** pgvector for 1536d embeddings
- **Architecture:** 1 primary + 1 read replica
- **Connection Pooling:** PgBouncer
- **Backups:** Automated hourly snapshots
- **RPO:** < 1hr
- **RTO:** < 3hrs

### Supabase Auth
- **Methods:** Magic link, Google OAuth, GitHub OAuth, email+password
- **Multi-factor:** Optional TOTP 2FA
- **Tokens:** JWTs (1hr expiry) + rotating refresh tokens (30-day window)
- **RLS:** Row-level security on all tables for tenant isolation

### Redis
- **Purpose:** Cache, sessions, rate limiting, BullMQ job queue, LangGraph pipeline checkpoint state
- **Initial Size:** 5GB Standard tier (MVP), scale as needed
- **High Availability:** Replication enabled

---

## Security

### Secrets Management
All secrets stored as environment variables / per-platform secret store:

| Secret | Description |
|--------|-------------|
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key |
| `GEMINI_API_KEY` | Gemini 3.5 Flash API key |
| `STRIPE_SECRET_KEY` | Stripe secret key |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret |
| `SENDGRID_API_KEY` | SendGrid API key |
| `TWILIO_ACCOUNT_SID` | Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token |
| `TWILIO_WHATSAPP_NUMBER` | Twilio WhatsApp sender |
| `ALGOLIA_APP_ID` | Algolia application ID |
| `ALGOLIA_API_KEY` | Algolia admin API key |
| `ELEVENLABS_API_KEY` | ElevenLabs API key (optional) |
| `POSTHOG_API_KEY` | PostHog API key |
| `LANGFUSE_SECRET_KEY` | Langfuse secret key |

### API Security
- **Authentication:** JWT (1hr expiry) + refresh tokens (30-day rotation)
- **Authorization:** Supabase RLS + FastAPI dependency injection for role checks
- **Input Validation:** Pydantic v2 on all endpoints
- **CORS:** Whitelist of allowed origins (edugenie.io, *.edugenie.io)
- **Rate Limiting:** 200 req/min standard, 2000 req/min enterprise
- **Webhook Verification:** Stripe HMAC-SHA256, Twilio signature validation, SendGrid webhook signature

---

## Monitoring & Observability

### Prometheus Metrics
- Metrics exported from all services (API latency, error rates, queue depths, AI cost per course)
- AI cost tracking per agent call (Langfuse)

### Grafana Dashboards
| Dashboard | Metrics |
|-----------|---------|
| **API Performance** | Latency p50/p95/p99 per endpoint, error rate, throughput |
| **AI Pipeline** | Per-stage latency, cost per build, model usage breakdown |
| **Business** | Active creators, course builds, enrollments, revenue, completion rate |
| **Infrastructure** | Container CPU/memory, Redis memory, Storage metrics |

### Alerting Rules
| Alert | Condition | Notification |
|-------|-----------|-------------|
| API Error Rate | > 1% for 5 min | PagerDuty (critical) |
| P95 Latency | > 800ms for 5 min | Slack (high) |
| AI Cost/ Build | > $25 single run | Slack (finance) |
| Pipeline Failure | > 4% in 24h | PagerDuty (critical) |
| Video Render Queue | Depth > 200 | Slack (auto-scale) |
| Database Replication Lag | > 30s | PagerDuty (critical) |
| SMS/Email Failure | > 2% delivery fail | Slack (high) |

---

## IaC (Terraform)

### Directory Structure
```
infra/terraform/
├── main.tf                    # Root module
├── variables.tf               # Global variables
├── outputs.tf                 # Global outputs
├── modules/
│   ├── compute/               # Container services
│   ├── network/               # Networking, load balancer
│   ├── storage/               # Storage configuration
│   ├── monitoring/            # Dashboards, alerts, logging
│   └── cicd/                  # CI/CD configuration
└── environments/
    ├── dev/                   # Dev.tfvars
    ├── staging/               # Staging.tfvars
    └── prod/                  # Prod.tfvars
```

### Provisioning Workflow
```bash
cd infra/terraform
terraform init
terraform workspace new staging
terraform plan -var-file="environments/staging.tfvars"
terraform apply -var-file="environments/staging.tfvars"
```

---

## Cost Optimization Strategies

| Strategy | Savings | Detail |
|----------|---------|--------|
| AI Model Routing | Variable | Gemini 3.5 Flash for all agentic tasks |
| Narration Caching | ~35% | Cache ElevenLabs TTS by `(script_hash + voice_id)` |
| Video Rendering | Variable | Background worker with FFmpeg (no GPU needed) |
| Storage Lifecycle | Variable | Archive to cold storage after 90+ days |
| Container Scaling | Variable | Auto-scale based on CPU/memory, scale to zero for non-critical |

### Estimated Monthly Cost (MVP)

| Service | Cost |
|---------|------|
| Hosting (compute) | ~$80 |
| Storage + CDN | ~$40 |
| Redis | ~$25 |
| FFmpeg rendering | ~$20 |
| Supabase (Pro) | ~$25 |
| Gemini API | ~$500 (variable) |
| ElevenLabs | ~$100 |
| SendGrid | ~$15 |
| Twilio | ~$10 |
| Algolia | ~$25 |
| **Total Base** | **~$200/mo + AI costs** |
