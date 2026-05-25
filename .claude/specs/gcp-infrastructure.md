# GCP Infrastructure — EduGenie OS

## Overview

All infrastructure is deployed on Google Cloud Platform (GCP). Infrastructure-as-code is managed with Terraform. All AWS references from the original PRD have been replaced with GCP equivalents.

---

## Compute Layer

### Cloud Run (Primary Compute)
All services run on Cloud Run with the following configuration:

| Service | Purpose | Min Instances | Max Instances | RAM | vCPU |
|---------|---------|---------------|---------------|-----|------|
| `edugenie-backend` | FastAPI REST + WebSocket API | 1 | 100 | 2GB | 2 |
| `edugenie-frontend` | Next.js web frontend | 1 | 50 | 1GB | 1 |
| `edugenie-workers` | BullMQ job queue workers | 1 | 50 | 2GB | 2 |
| `edugenie-presidio` | PII detection service | 0 | 10 | 1GB | 1 |
| `edugenie-langfuse` | AI observability | 0 | 5 | 1GB | 1 |

- **Scaling:** Auto-scale on CPU > 65%
- **CPU Allocation:** Request-based for API, always-on for workers
- **Concurrency:** 80 concurrent requests per instance (backend)

### Cloud Batch (Video Rendering)
- **Purpose:** FFmpeg video rendering (PNG frames + MP3 narration → 1080p MP4)
- **Instance Type:** Preemptible VMs for cost savings (~60% cost reduction)
- **Max Parallel Renders:** Up to 50 simultaneous jobs
- **Job Dispatch:** Per lesson via BullMQ job queue
- **Output:** 1080p MP4 + Whisper SRT captions → Cloud Storage

---

## Storage Layer

### Cloud Storage (Media)
| Attribute | Value |
|-----------|-------|
| Bucket Name | `edugenie-media` |
| Location | Multi-region |
| Object Versioning | Enabled |
| Default Encryption | AES-256 (server-side) |
| Signed URL Duration | 1 hour (video streaming) |
| Lifecycle — Nearline | After 90 days |
| Lifecycle — Coldline | After 365 days |

**Stored Assets:**
- Video files (MP4)
- Slide decks (PPTX, PDF, PNG frames)
- Audio narrations (MP3)
- Caption files (SRT)
- Certificates (PDF, PNG)
- Course thumbnails
- Script files

### Cloud CDN
- **Origin:** Cloud Storage bucket
- **Caching:** Static assets, video segments at edge
- **Signed URLs:** For private content access
- **SSL:** Managed certificates

### Memorystore for Redis
- **Purpose:** Cache, sessions, rate limiting, BullMQ job queue, LangGraph pipeline checkpoint state
- **Tier:** Standard (MVP), scale as needed
- **Initial Size:** 5GB
- **High Availability:** Replication enabled

### Supabase (PostgreSQL)
- **Version:** PostgreSQL 16
- **Extension:** pgvector for embeddings
- **Architecture:** 1 primary + 1 read replica
- **Connection Pooling:** PgBouncer
- **Backups:** Automated hourly snapshots
- **RPO:** < 1hr
- **RTO:** < 3hrs

---

## Networking

| Component | Configuration |
|-----------|---------------|
| **VPC** | Custom VPC with private subnet |
| **Serverless VPC Connector** | Bridge Cloud Run to VPC resources (Cloud SQL, Memorystore) |
| **Cloud Load Balancer** | External HTTPS for frontend, internal for service-to-service |
| **Cloud CDN** | Static asset caching, course media edge delivery |
| **Cloud Armor** | WAF rules, DDoS protection, IP allow/deny lists, rate limiting (200 req/min standard, 2000 enterprise) |
| **Cloud DNS** | Domain management with DNSSEC |
| **VPC Firewall** | Ingress restricted to Load Balancer; egress restricted to specific external APIs |

---

## Security

### Secret Manager
All secrets stored in GCP Secret Manager with auto-rotation:

| Secret Name | Description |
|-------------|-------------|
| `openai-api-key` | OpenAI API key |
| `sendgrid-api-key` | SendGrid API key |
| `twilio-auth` | Twilio Account SID + Auth Token |
| `stripe-secret-key` | Stripe secret key |
| `stripe-webhook-secret` | Stripe webhook signing secret |
| `elevenlabs-api-key` | ElevenLabs API key |
| `algolia-api-key` | Algolia admin API key |
| `supabase-service-role-key` | Supabase service role key |
| `posthog-api-key` | PostHog API key |
| `langfuse-secret-key` | Langfuse secret key |
| `jwt-secret` | JWT signing secret |

### IAM Service Accounts

| Service Account | Roles |
|----------------|-------|
| `edugenie-backend` | `roles/run.invoker`, `roles/storage.objectAdmin`, `roles/secretmanager.secretAccessor` |
| `edugenie-frontend` | `roles/run.invoker` |
| `edugenie-workers` | `roles/run.invoker`, `roles/storage.objectAdmin`, `roles/batch.jobsEditor` |
| `edugenie-terraform` | `roles/editor` (scoped to project) |

### Cloud Armor WAF Rules
- OWASP Top 10 rules enabled
- Rate limiting: 200 req/min (standard), 2,000 req/min (enterprise)
- Geo-based access controls (if needed)
- HTTP header validation
- SQL injection and XSS prevention

---

## Monitoring & Observability

### Cloud Logging
```python
# backend/app/main.py
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler

client = google.cloud.logging.Client()
handler = CloudLoggingHandler(client, name="edugenie-backend")
root_logger = logging.getLogger()
root_logger.addHandler(handler)
root_logger.setLevel(logging.INFO)
```

### Cloud Monitoring Dashboards
| Dashboard | Metrics |
|-----------|---------|
| **API Performance** | Latency p50/p95/p99 per endpoint, error rate, throughput |
| **AI Pipeline** | Per-stage latency, cost per build, model usage breakdown |
| **Business** | Active creators, course builds, enrollments, revenue, completion rate |
| **Infrastructure** | Cloud Run CPU/memory, Redis memory, Storage metrics |

### Cloud Trace
- Distributed tracing across FastAPI + AI agent calls
- Trace context propagated through BullMQ job queue

### Error Reporting
- Real-time exception aggregation from all services
- Stack traces captured with release version tags

### Alerting Rules (Cloud Monitoring)

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
│   ├── compute/               # Cloud Run, Cloud Batch
│   ├── network/               # VPC, Load Balancer, CDN, Armor
│   ├── storage/               # Cloud Storage, Memorystore
│   ├── monitoring/            # Dashboards, alerts, logging
│   └── cicd/                  # Cloud Build triggers, Artifact Registry
└── environments/
    ├── dev/                   # Dev.tfvars
    ├── staging/               # Staging.tfvars
    └── prod/                  # Prod.tfvars
```

### Provisioning Workflow
```bash
cd infra/terraform
terraform init -backend-config="bucket=edugenie-tfstate"
terraform workspace new staging
terraform plan -var-file="environments/staging.tfvars"
terraform apply -var-file="environments/staging.tfvars"
```

---

## Cost Optimization Strategies

| Strategy | Savings | Detail |
|----------|---------|--------|
| AI Model Routing | Variable | GPT-4o-mini for quizzes/short tasks, GPT-4o for curriculum/scripts |
| Narration Caching | ~35% | Cache ElevenLabs TTS by `(script_hash + voice_id)` |
| Cloud Batch Preemptible VMs | ~60% | Preemptible VMs for FFmpeg rendering |
| Cloud CDN | Variable | Cache static assets, video segments at edge |
| Cloud Storage Lifecycle | Variable | Archive to Nearline after 90 days, Coldline after 365 days |
| Cloud Run min-instances=0 | Variable | Non-critical services scale to zero when idle |

### Estimated Monthly Cost (MVP)

| Service | Cost |
|---------|------|
| Cloud Run (backend + workers) | ~$80 |
| Cloud Storage + CDN | ~$40 |
| Memorystore (Redis) | ~$25 |
| Cloud Batch (FFmpeg) | ~$20 |
| Supabase (Pro) | ~$25 |
| OpenAI API | ~$500 (variable) |
| ElevenLabs | ~$100 |
| SendGrid | ~$15 |
| Twilio | ~$10 |
| Algolia | ~$25 |
| **Total Base** | **~$200/mo + AI costs** |
