# EduGenie OS — System Architecture

> **Version:** 0.1.0  
> **Last Updated:** 2026-05-26  
> **Stack:** FastAPI · Next.js · Expo · LangChain · LangGraph · Supabase · GCP

---

## Table of Contents

1. [High-Level System Architecture](#1-high-level-system-architecture)
2. [Infrastructure & Deployment Pipeline](#2-infrastructure--deployment-pipeline)
3. [Core AI Workflow](#3-core-ai-workflow)
4. [Database Entity Relationship](#4-database-entity-relationship)
5. [Technology Stack Reference](#5-technology-stack-reference)

---

## 1. High-Level System Architecture

This diagram illustrates the complete network topology — from user-facing clients through GCP's edge network, into the application layer, and out to external integrations.

```mermaid
graph LR
    subgraph Clients["Client Layer"]
        WEB[Next.js Web App<br/>Creator OS / LearnSpace]
        MOBILE[Expo Mobile App<br/>React Native]
    end

    subgraph Edge["GCP Edge Network"]
        LB[Cloud Load Balancer<br/>HTTPS / WSS]
        ARMOR[Cloud Armor<br/>WAF · Rate Limiting · DDoS]
        CDN[Cloud CDN<br/>Static Assets · Video Cache]
    end

    subgraph Compute["Application Layer (Cloud Run)"]
        FE[Frontend<br/>Next.js 14+]
        API[Backend API<br/>FastAPI]
        WORKER[Background Workers<br/>RQ / BullMQ]
        PRESIDIO[PII Scanner<br/>Microsoft Presidio]
        LANGFUSE[AI Observability<br/>Langfuse]
    end

    subgraph AI["AI Agent Layer"]
        ORCH[Orchestrator Agent<br/>LangGraph Supervisor]
        INTEL[Intelligence Agent<br/>Market Research]
        ARCH[Architect Agent<br/>Curriculum Design]
        SCRIPT[Scriptwriter Agent<br/>Lesson Scripts]
        MEDIA[MediaForge Agent<br/>Slides · Voice · Video]
        EVAL[Evaluator Agent<br/>Quizzes · Capstone]
        LAUNCH[Launchpad Agent<br/>Sales · Marketing]
        OPT[Optimizer Agent<br/>Post-Launch Analytics]
    end

    subgraph Storage["Data & Storage Layer"]
        DB[(Supabase PostgreSQL 16<br/>+ pgvector)]
        REDIS[(Memorystore Redis<br/>Cache · Queue · Sessions)]
        GCS[(Cloud Storage<br/>Media · Scripts · Certificates)]
    end

    subgraph External["External Integrations"]
        OA[OpenAI<br/>GPT-4o · TTS · Whisper · DALL-E]
        EL[ElevenLabs<br/>Voice Cloning · TTS]
        ST[Stripe<br/>Payments · Connect · Tax]
        SG[SendGrid<br/>Transactional Emails]
        TW[Twilio<br/>WhatsApp Notifications]
        ALG[Algolia<br/>Course Search]
        PH[PostHog<br/>Analytics · Feature Flags]
    end

    %% Client → Edge
    WEB --> LB
    MOBILE --> LB
    LB --> ARMOR

    %% Edge → Compute
    ARMOR -->|Route /app/*| FE
    ARMOR -->|Route /api/*| API
    ARMOR -->|Route /ws/*| API
    CDN -->|Serve cached media| WEB
    CDN -->|Serve cached media| MOBILE

    %% Compute → Compute
    FE -->|BFF API calls| API
    API -->|Enqueue jobs| WORKER

    %% Compute → AI
    API --> ORCH
    WORKER --> ORCH
    ORCH --> INTEL
    ORCH --> ARCH
    ORCH --> SCRIPT
    ORCH --> MEDIA
    ORCH --> EVAL
    ORCH --> LAUNCH
    ORCH --> OPT

    %% AI → Integrations
    INTEL --> OA
    SCRIPT --> OA
    EVAL --> OA
    MEDIA --> OA
    MEDIA --> EL
    LAUNCH --> OA

    %% Compute → Storage
    API --> DB
    API --> REDIS
    API --> GCS
    WORKER --> DB
    WORKER --> REDIS
    WORKER --> GCS

    %% Compute → External
    API --> ST
    API --> SG
    API --> TW
    API --> ALG
    API --> PH
    WORKER --> SG
    WORKER --> TW

    %% AI Observability
    ORCH -.-> LANGFUSE
    INTEL -.-> LANGFUSE
    ARCH -.-> LANGFUSE
    SCRIPT -.-> LANGFUSE
    MEDIA -.-> LANGFUSE
    EVAL -.-> LANGFUSE
    LAUNCH -.-> LANGFUSE
    OPT -.-> LANGFUSE
```

---

## 2. Infrastructure & Deployment Pipeline

This diagram maps the GCP infrastructure topology (provisioned via Terraform) alongside the Cloud Build CI/CD pipeline that deploys each service.

```mermaid
graph TD
    subgraph IaC["Infrastructure as Code (Terraform)"]
        TF_ROOT[root/main.tf]
        TF_COMPUTE[Module: Compute<br/>Cloud Run · Cloud Batch]
        TF_NETWORK[Module: Network<br/>VPC · Load Balancer · CDN · Armor]
        TF_STORAGE[Module: Storage<br/>Cloud Storage · Memorystore]
        TF_MONITORING[Module: Monitoring<br/>Dashboards · Alerts]
        TF_CICD[Module: CI/CD<br/>Cloud Build Triggers · Artifact Registry]

        TF_ROOT --> TF_COMPUTE
        TF_ROOT --> TF_NETWORK
        TF_ROOT --> TF_STORAGE
        TF_ROOT --> TF_MONITORING
        TF_ROOT --> TF_CICD

        subgraph Envs["Terraform Workspaces"]
            DEV[dev/]
            STAGING[staging/]
            PROD[prod/]
        end
    end

    subgraph CICD["CI/CD Pipeline (Cloud Build)"]
        GIT[(Source<br/>GitHub develop/main)]
        LINT[Stage 1: Lint<br/>ruff · ESLint · Prettier]
        TYPE[Stage 2: Type Check<br/>mypy · tsc]
        UNIT[Stage 3: Unit Tests<br/>pytest · Jest]
        SECURITY[Stage 4: Security Scan<br/>Snyk / Trivy]
        BUILD[Stage 5: Docker Build<br/>→ Artifact Registry]
        INTEGRATION[Stage 6: Integration Tests]
        DEPLOY[Stage 7: Deploy to Cloud Run<br/>Blue/Green Traffic Split]
        SMOKE[Post-Deploy: Smoke Tests<br/>→ 100% Traffic → 1h Monitoring]

        GIT --> LINT --> TYPE --> UNIT --> SECURITY --> BUILD --> INTEGRATION --> DEPLOY --> SMOKE
    end

    subgraph GCP["GCP Infrastructure"]
        subgraph Networking["Networking"]
            VPC[Custom VPC<br/>Private Subnet]
            CONNECTOR[Serverless VPC<br/>Connector]
            LB[Cloud Load Balancer<br/>External HTTPS]
            ARMOR[Cloud Armor<br/>OWASP · Rate Limiting]
            CDN[Cloud CDN<br/>Edge Caching]
            DNS[Cloud DNS<br/>edugenie.io]
        end

        subgraph ComputeServices["Cloud Run Services"]
            BE_SVC[edugenie-backend<br/>2 vCPU · 2GB · 1-100 instances]
            FE_SVC[edugenie-frontend<br/>1 vCPU · 1GB · 1-50 instances]
            WORKER_SVC[edugenie-workers<br/>2 vCPU · 2GB · 1-50 instances]
            PRESIDIO_SVC[edugenie-presidio<br/>0-10 instances]
        end

        subgraph Batch["Cloud Batch"]
            RENDER[FFmpeg Video Rendering<br/>Preemptible VMs · 50 parallel]
        end

        subgraph DataLayer["Data Layer"]
            SQL[(Supabase PostgreSQL<br/>Primary + Read Replica)]
            CACHE[(Memorystore Redis<br/>5GB Standard)]
            BUCKET[(Cloud Storage<br/>Multi-region · Versioned)]
        end

        subgraph Security["Security & Secrets"]
            SECRETS[Secret Manager<br/>API Keys · JWT · DB URLs]
            IAM[IAM Service Accounts<br/>Least-Privilege Roles]
        end

        subgraph Monitoring["Monitoring"]
            LOGS[Cloud Logging<br/>Structured JSON]
            METRICS[Cloud Monitoring<br/>Dashboards · Alerts]
            TRACE[Cloud Trace<br/>Distributed Tracing]
            ERRORS[Error Reporting<br/>Exception Aggregation]
        end
    end

    %% CI/CD deploys to GCP
    DEPLOY --> BE_SVC
    DEPLOY --> FE_SVC
    DEPLOY --> WORKER_SVC

    %% Network connections
    LB --> ARMOR
    ARMOR --> VPC
    VPC --> CONNECTOR
    CONNECTOR --> BE_SVC
    CONNECTOR --> FE_SVC
    CONNECTOR --> WORKER_SVC
    CDN --> BUCKET

    %% Service connections
    BE_SVC --> BUCKET
    BE_SVC --> CACHE
    BE_SVC --> SQL
    BE_SVC --> SECRETS
    WORKER_SVC --> BUCKET
    WORKER_SVC --> CACHE
    WORKER_SVC --> RENDER
    WORKER_SVC --> SECRETS

    %% Monitoring
    BE_SVC -.-> LOGS
    FE_SVC -.-> LOGS
    WORKER_SVC -.-> LOGS
    BE_SVC -.-> METRICS
    FE_SVC -.-> METRICS
    WORKER_SVC -.-> METRICS
    BE_SVC -.-> TRACE
    WORKER_SVC -.-> TRACE
    BE_SVC -.-> ERRORS
    FE_SVC -.-> ERRORS
    WORKER_SVC -.-> ERRORS
```

---

## 3. Core AI Workflow

This sequence diagram traces a complete course build request from the moment a creator submits a topic brief through the AI agent pipeline, review gates, and final publication.

```mermaid
sequenceDiagram
    participant C as Creator (Browser/Mobile)
    participant FE as Next.js Frontend
    participant API as FastAPI Backend
    participant Q as Redis Queue
    participant ORCH as Orchestrator Agent
    participant INTEL as Intelligence Agent
    participant ARCH as Architect Agent
    participant SCRIPT as Scriptwriter Agent
    participant MEDIA as MediaForge Agent
    participant EVAL as Evaluator Agent
    participant LAUNCH as Launchpad Agent
    participant OPT as Optimizer Agent
    participant AI as OpenAI / ElevenLabs
    participant DB as Supabase PostgreSQL
    participant STO as Cloud Storage
    participant EXT as Stripe / SendGrid / Algolia

    C->>FE: Submits topic brief<br/>(topic, audience, depth, tone, language)
    FE->>API: POST /courses/build
    API->>DB: Create course record (status: drafting)
    API->>DB: Create pipeline_run record
    API->>Q: Enqueue pipeline job
    API-->>C: Return job_id (202 Accepted)

    Q->>ORCH: Start pipeline

    rect rgb(240, 245, 255)
        Note over ORCH,INTEL: Stage 1 — Market Intelligence
        ORCH->>INTEL: Run with topic brief
        INTEL->>AI: Web search + competitor analysis
        AI-->>INTEL: Market report + angle recommendations
        INTEL->>DB: Save market report
        INTEL-->>ORCH: Completed
        ORCH-->>API: Stage ready for review
        API-->>C: Notify: "Market research ready"
        C->>API: POST /stages/intelligence/approve
    end

    rect rgb(245, 240, 255)
        Note over ORCH,ARCH: Stage 2 — Curriculum Design
        ORCH->>ARCH: Run with approved brief
        ARCH->>AI: Design curriculum (Bloom's taxonomy)
        AI-->>ARCH: Curriculum JSON (modules, lessons, durations)
        ARCH->>DB: Save modules + lessons
        ARCH-->>ORCH: Completed
        ORCH-->>API: Stage ready for review
        API-->>C: Notify: "Curriculum ready"
        C->>API: POST /stages/architect/approve
    end

    rect rgb(255, 245, 240)
        Note over ORCH,SCRIPT: Stage 3 — Script Writing
        ORCH->>SCRIPT: Run with curriculum
        SCRIPT->>AI: Generate lesson scripts (parallel)
        AI-->>SCRIPT: Full lesson scripts with [VERIFY] flags
        SCRIPT->>STO: Upload scripts
        SCRIPT->>DB: Save script metadata + URLs
        SCRIPT-->>ORCH: Completed
        ORCH-->>API: Stage ready for review
        API-->>C: Notify: "Scripts ready for review"
        C->>API: POST /stages/scriptwriter/approve
    end

    rect rgb(240, 255, 245)
        Note over ORCH,MEDIA: Stage 4 — Media Production
        ORCH->>MEDIA: Run with approved scripts
        MEDIA->>AI: Generate slide content + narration
        MEDIA->>AI: Generate voice narration (TTS)
        MEDIA->>STO: Upload slides (PPTX + PNG)
        MEDIA->>STO: Upload narration (MP3)
        MEDIA->>STO: Render video (FFmpeg → MP4)
        MEDIA->>AI: Generate captions (Whisper → SRT)
        MEDIA->>STO: Upload captions + thumbnail
        MEDIA->>DB: Save media URLs
        MEDIA-->>ORCH: Completed
        ORCH-->>API: Stage ready for review
        API-->>C: Notify: "Media ready for review"
        C->>API: POST /stages/mediaforge/approve
    end

    rect rgb(255, 250, 240)
        Note over ORCH,EVAL: Stage 5 — Assessments
        ORCH->>EVAL: Run with course data
        EVAL->>AI: Generate quizzes + capstone brief
        AI-->>EVAL: Quiz questions + capstone project
        EVAL->>DB: Save quizzes
        EVAL-->>ORCH: Completed
        ORCH-->>API: Stage ready for review
        API-->>C: Notify: "Quizzes ready for review"
        C->>API: POST /stages/evaluator/approve
    end

    rect rgb(245, 245, 255)
        Note over ORCH,LAUNCH: Stage 6 — Launch Preparation
        ORCH->>LAUNCH: Run with full course data
        LAUNCH->>AI: Generate sales page + emails + social posts
        AI-->>LAUNCH: Sales HTML + email sequence + social content
        LAUNCH->>EXT: Stage content (not sent yet)
        LAUNCH-->>ORCH: Completed
        ORCH-->>API: Stage ready for final review
        API-->>C: Notify: "Course ready for final review"
    end

    C->>API: POST /courses/{id}/publish
    API->>EXT: Create Stripe product + price
    API->>EXT: Index course in Algolia
    API->>DB: Update course status (published)
    API->>EXT: Send notification emails
    API-->>C: Return published course URL

    rect rgb(240, 240, 250)
        Note over OPT: Post-Launch (Weekly)
        OPT->>DB: Analyze student engagement data
        OPT->>AI: Generate improvement report
        OPT->>DB: Save improvement report
        OPT-->>API: Notify creator of new report
        API-->>C: "Weekly Optimizer report ready"
    end
```

---

## 4. Database Entity Relationship

This diagram presents the core database schema — the primary tables and their relationships within the Supabase PostgreSQL instance.

```mermaid
erDiagram
    organizations ||--o{ creators : "belongs to"
    organizations ||--o{ courses : "owns"
    organizations ||--o{ audit_logs : "tracks"

    creators ||--o{ courses : "authors"
    creators ||--o{ affiliates : "manages"

    courses ||--o{ course_versions : "has versions"
    courses ||--o{ modules : "contains"
    courses ||--o{ enrollments : "receives"
    courses ||--o{ sales : "generates"
    courses ||--o{ pipeline_runs : "tracks builds"
    courses ||--o{ improvement_reports : "has reports"

    modules ||--o{ lessons : "contains"
    modules ||--o{ quizzes : "assesses"

    lessons ||--o{ progress : "tracks"
    lessons ||--o{ discussions : "discusses"

    quizzes ||--o{ quiz_attempts : "records"

    students ||--o{ enrollments : "enrolls in"
    students ||--o{ discussions : "posts"

    enrollments ||--o{ progress : "tracks"
    enrollments ||--o{ quiz_attempts : "records"
    enrollments ||--o| certificates : "awards"

    sales ||--o| enrollments : "creates"
    affiliates ||--o{ sales : "refers"

    organizations {
        uuid id PK
        varchar name
        varchar slug UK
        jsonb settings
        timestamptz created_at
    }

    creators {
        uuid id PK
        uuid organization_id FK
        uuid supabase_user_id
        varchar plan_tier
        varchar voice_model_id
        jsonb brand_settings
        varchar display_name
        text bio
        timestamptz created_at
    }

    courses {
        uuid id PK
        uuid organization_id FK
        uuid creator_id FK
        varchar title
        varchar slug
        varchar status
        int version
        decimal price
        varchar stripe_product_id
        varchar stripe_price_id
        jsonb topic_brief
        varchar language
        text thumbnail_url
        int total_duration_min
        varchar difficulty
        timestamptz created_at
        timestamptz published_at
    }

    course_versions {
        uuid id PK
        uuid course_id FK
        int version_number
        text changelog
        jsonb snapshot
        timestamptz created_at
    }

    modules {
        uuid id PK
        uuid course_id FK
        int position
        varchar title
        text learning_objective
        varchar bloom_level
        int estimated_duration_min
        uuid[] prerequisites
    }

    lessons {
        uuid id PK
        uuid module_id FK
        int position
        varchar title
        text script_url
        text video_url
        text slides_url
        text captions_url
        text thumbnail_url
        int duration_min
        int word_count
        int verify_flags
        timestamptz created_at
    }

    quizzes {
        uuid id PK
        uuid module_id FK
        uuid lesson_id FK
        int pass_threshold
        int max_attempts
        jsonb questions
        timestamptz created_at
    }

    students {
        uuid id PK
        uuid supabase_user_id
        varchar stripe_customer_id
        varchar display_name
        varchar email
        varchar locale
        timestamptz created_at
    }

    enrollments {
        uuid id PK
        uuid student_id FK
        uuid course_id FK
        int version
        varchar status
        timestamptz enrolled_at
        timestamptz completed_at
        uuid certificate_id FK
    }

    progress {
        uuid id PK
        uuid enrollment_id FK
        uuid lesson_id FK
        decimal watch_depth_pct
        int time_spent_sec
        timestamptz completed_at
        timestamptz updated_at
    }

    quiz_attempts {
        uuid id PK
        uuid enrollment_id FK
        uuid quiz_id FK
        decimal score
        boolean passed
        jsonb answers
        int duration_sec
        timestamptz attempted_at
        int attempt_number
    }

    sales {
        uuid id PK
        uuid course_id FK
        uuid enrollment_id FK
        varchar stripe_payment_intent_id
        decimal amount
        decimal platform_fee
        decimal creator_earnings
        varchar channel
        varchar promo_code
        timestamptz refunded_at
        timestamptz created_at
    }

    affiliates {
        uuid id PK
        uuid course_id FK
        uuid creator_id FK
        varchar affiliate_name
        decimal commission_pct
        int cookie_window_days
        text referral_link
        int total_clicks
        int total_conversions
        decimal total_earned
        timestamptz created_at
    }

    certificates {
        uuid id PK
        uuid enrollment_id FK
        varchar verification_code UK
        text pdf_url
        jsonb badge_json
        varchar status
        timestamptz issued_at
        timestamptz revoked_at
        text revoked_reason
    }

    discussions {
        uuid id PK
        uuid lesson_id FK
        uuid student_id FK
        text content
        text ai_response
        decimal ai_confidence
        boolean creator_verified
        int upvotes
        timestamptz created_at
    }

    pipeline_runs {
        uuid id PK
        uuid course_id FK
        varchar stage
        varchar status
        varchar model_used
        int tokens_used
        decimal cost_usd
        timestamptz started_at
        timestamptz completed_at
        text error
    }

    improvement_reports {
        uuid id PK
        uuid course_id FK
        jsonb report_data
        decimal priority_score
        timestamptz viewed_at
        date week_start
        timestamptz created_at
    }

    notifications {
        uuid id PK
        uuid user_id FK
        varchar notification_type
        varchar title
        text body
        jsonb data
        boolean is_read
        timestamptz created_at
        timestamptz read_at
    }

    audit_logs {
        uuid id PK
        uuid organization_id FK
        uuid actor_id
        varchar action
        varchar resource_type
        uuid resource_id
        jsonb details
        inet ip_address
        timestamptz created_at
    }
```

---

## 5. Technology Stack Reference

### Backend Services

| Service | Technology | Deployment | Scaling |
|---------|-----------|------------|---------|
| REST API | FastAPI + Pydantic v2 | Cloud Run (2 vCPU, 2GB) | 1–100 instances |
| Background Workers | RQ / BullMQ | Cloud Run (2 vCPU, 2GB) | 1–50 instances |
| Database ORM | SQLAlchemy 2.0 (async) | Supabase PostgreSQL 16 | Primary + Read Replica |
| Migrations | Alembic | Cloud Build step | — |
| Cache / Queue | Redis via Memorystore | 5GB Standard | Replicated |

### AI & Machine Learning

| Component | Provider | Model / Service |
|-----------|----------|-----------------|
| Text Generation | OpenAI | GPT-4o (primary), GPT-4o-mini (cost-optimized) |
| Text Generation (Fallback) | Anthropic | Claude |
| Embeddings | OpenAI | text-embedding-3-small (1536d) |
| Speech-to-Text | OpenAI | Whisper API |
| Text-to-Speech | OpenAI / ElevenLabs | TTS API / Voice Cloning |
| Image Generation | OpenAI / Ideogram | DALL-E 3 |
| Agent Orchestration | LangChain | LangGraph Supervisor |
| Observability | Langfuse | Self-hosted on Cloud Run |
| PII Detection | Microsoft Presidio | Self-hosted on Cloud Run |
| Plagiarism | Originality.ai | API |

### Frontend & Mobile

| Platform | Framework | State Management | Deployment |
|----------|-----------|-----------------|------------|
| Creator OS (Web) | Next.js 14+ (App Router) | Zustand + TanStack Query | Cloud Run |
| LearnSpace (Web) | Next.js 14+ (App Router) | Zustand + TanStack Query | Cloud Run |
| Mobile App | React Native + Expo SDK 52+ | Zustand + TanStack Query | EAS Build → App Store/Play |

### Third-Party Integrations

| Service | Purpose | Webhook |
|---------|---------|---------|
| Stripe | Payments, Connect, Tax | `POST /webhooks/stripe` |
| SendGrid | Transactional emails | `POST /webhooks/sendgrid` |
| Twilio | WhatsApp notifications | `POST /webhooks/twilio` |
| Algolia | Course search indexing | — |
| PostHog | Product analytics, feature flags | — |

### GCP Infrastructure

| Component | Configuration |
|-----------|---------------|
| Compute | Cloud Run (auto-scale, CPU > 65%) |
| Video Rendering | Cloud Batch (preemptible VMs, 50 parallel) |
| Storage | Cloud Storage (multi-region, versioned) |
| CDN | Cloud CDN (edge caching, signed URLs) |
| Networking | Custom VPC, Serverless VPC Connector |
| Security | Cloud Armor (OWASP, rate limiting) |
| Secrets | Secret Manager (auto-rotation) |
| Monitoring | Cloud Logging + Monitoring + Trace |
| CI/CD | Cloud Build → Artifact Registry → Cloud Run |
| IaC | Terraform (workspaces: dev, staging, prod) |
