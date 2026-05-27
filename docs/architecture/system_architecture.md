# EduGenie OS — System Architecture

> **Version:** 0.2.0  
> **Last Updated:** 2026-05-27  
> **Stack:** FastAPI · Next.js · Expo · LangGraph · Gemini 3.5 Flash · Supabase

---

## Table of Contents

1. [High-Level System Architecture](#1-high-level-system-architecture)
2. [Infrastructure & Deployment Pipeline](#2-infrastructure--deployment-pipeline)
3. [Core AI Workflow](#3-core-ai-workflow)
4. [Database Entity Relationship](#4-database-entity-relationship)
5. [Technology Stack Reference](#5-technology-stack-reference)

---

## 1. High-Level System Architecture

This diagram illustrates the complete network topology — from user-facing clients through the application layer, into the unified Supabase backend, and out to external integrations.

```mermaid
graph LR
    subgraph Clients["Client Layer"]
        WEB[Next.js Web App<br/>Creator OS / LearnSpace]
        MOBILE[Expo Mobile App<br/>React Native]
    end

    subgraph Compute["Application Layer"]
        FE[Frontend<br/>Next.js 14+]
        API[Backend API<br/>FastAPI]
        WORKER[Background Workers<br/>RQ / BullMQ]
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

    subgraph Supabase["Unified Backend (Supabase)"]
        DB[(PostgreSQL 16<br/>+ pgvector)]
        STORAGE[(Supabase Storage<br/>Media · Scripts · Certificates)]
        AUTH[Supabase Auth<br/>JWT · Magic Link · OAuth]
    end

    subgraph Cache["Cache & Queue"]
        REDIS[(Redis<br/>Cache · Queue · Sessions)]
        KAFKA["Confluent Kafka<br/>(optional streaming)"]
    end

    subgraph External["External Integrations"]
        GM[Gemini 3.5 Flash<br/>Text · Code · Reasoning]
        EMB[Gemini Embedding 2<br/>1536d embeddings]
        ST[Stripe<br/>Payments · Connect · Tax]
        SG[SendGrid<br/>Transactional Emails]
        TW[Twilio<br/>WhatsApp Notifications]
        ALG[Algolia<br/>Course Search]
        PH[PostHog<br/>Analytics · Feature Flags]
    end

    subgraph Monitoring["Observability"]
        PROM[Prometheus<br/>Metrics Collection]
        GRAF[Grafana<br/>Dashboards · Alerts]
    end

    %% Client → Compute
    WEB --> FE
    WEB --> API
    MOBILE --> API

    %% Compute → Compute
    FE --> API
    API --> WORKER

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

    %% AI → Gemini
    INTEL --> GM
    SCRIPT --> GM
    EVAL --> GM
    MEDIA --> GM
    LAUNCH --> GM

    %% AI → Embeddings
    INTEL --> EMB
    ARCH --> EMB

    %% Compute → Supabase
    API --> DB
    API --> STORAGE
    API --> AUTH
    WORKER --> DB
    WORKER --> STORAGE

    %% Compute → Cache
    API --> REDIS
    WORKER --> REDIS
    WORKER --> KAFKA

    %% Compute → External
    API --> ST
    API --> SG
    API --> TW
    API --> ALG
    API --> PH
    WORKER --> SG
    WORKER --> TW

    %% Monitoring
    API -.-> PROM
    WORKER -.-> PROM
    PROM -.-> GRAF
```

---

## 2. Infrastructure & Deployment Pipeline

This diagram maps the deployment topology alongside the GitHub Actions CI/CD pipeline.

```mermaid
graph TD
    subgraph CICD["CI/CD Pipeline (GitHub Actions)"]
        GIT[(Source<br/>GitHub dev/main)]
        LINT[Job 1: Lint<br/>ruff · ESLint · Prettier]
        TYPE[Job 2: Type Check<br/>mypy · tsc]
        UNIT[Job 3: Unit Tests<br/>pytest · Jest]
        BUILD[Job 4: Build & Push<br/>Docker → Container Registry]
        DEPLOY[Job 5: Deploy<br/>dev: auto on PR merge<br/>main: manual approval gate]

        GIT -->|PR to development| LINT --> TYPE --> UNIT --> BUILD
        BUILD -->|merge to main| DEPLOY
    end

    subgraph ComputeServices["Compute (Hosted)"]
        BE_SVC[Backend API<br/>FastAPI · 2 vCPU · 2GB]
        FE_SVC[Frontend Web<br/>Next.js · 1 vCPU · 1GB]
        WORKER_SVC[Background Workers<br/>BullMQ · 2 vCPU · 2GB]
    end

    subgraph DataLayer["Unified Data Layer (Supabase)"]
        SQL[(PostgreSQL 16<br/>Primary + Read Replica<br/>+ pgvector)]
        BUCKET[(Supabase Storage<br/>Media · Certificates)]
        AUTH_PROV[Supabase Auth<br/>JWT · OAuth · Magic Link]
    end

    subgraph CacheLayer["Cache & Queue"]
        CACHE[(Redis<br/>Sessions · Queue · Cache)]
        STREAM["Confluent Kafka<br/>(optional event stream)"]
    end

    subgraph MonitoringStack["Observability"]
        PROMETHEUS[Prometheus<br/>Metrics Exporters]
        GRAFANA[Grafana<br/>Dashboards · Alerting]
    end

    %% CI/CD deploys
    DEPLOY --> BE_SVC
    DEPLOY --> FE_SVC
    DEPLOY --> WORKER_SVC

    %% Service connections
    BE_SVC --> SQL
    BE_SVC --> BUCKET
    BE_SVC --> AUTH_PROV
    BE_SVC --> CACHE
    WORKER_SVC --> SQL
    WORKER_SVC --> BUCKET
    WORKER_SVC --> CACHE
    WORKER_SVC --> STREAM

    %% Monitoring
    BE_SVC -.-> PROMETHEUS
    FE_SVC -.-> PROMETHEUS
    WORKER_SVC -.-> PROMETHEUS
    PROMETHEUS -.-> GRAFANA
```

---

## 3. Core AI Workflow

This sequence diagram traces a complete course build request from the moment a creator submits a topic brief through the AI agent pipeline, review gates, and final publication.

```mermaid
sequenceDiagram
    participant C as "Creator (Browser/Mobile)"
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
    participant OPTIMIZER as Optimizer Agent
    participant GM as Gemini 3.5 Flash
    participant SUPABASE as "Supabase<br/>(DB + Storage + Auth)"
    participant EXT as Stripe / SendGrid / Algolia

    C->>FE: "Submits topic brief<br/>(topic, audience, depth, tone, language)"
    FE->>API: POST /courses/build
    API->>SUPABASE: "Create course record (status: drafting)"
    API->>SUPABASE: Create pipeline_run record
    API->>Q: Enqueue pipeline job
    API-->>C: Return job_id (202 Accepted)

    Q->>ORCH: Start pipeline

    rect rgb(240, 245, 255)
        Note over ORCH,INTEL: Stage 1 — Market Intelligence
        ORCH->>INTEL: Run with topic brief
        INTEL->>GM: Web search + competitor analysis
        GM-->>INTEL: Market report + angle recommendations
        INTEL->>SUPABASE: Save market report
        INTEL-->>ORCH: Completed
        ORCH-->>API: Stage ready for review
        API-->>C: Notify: "Market research ready"
        C->>API: POST /stages/intelligence/approve
    end

    rect rgb(245, 240, 255)
        Note over ORCH,ARCH: Stage 2 — Curriculum Design
        ORCH->>ARCH: Run with approved brief
        ARCH->>GM: "Design curriculum (Bloom's taxonomy)"
        GM-->>ARCH: Curriculum JSON (modules, lessons, durations)
        ARCH->>SUPABASE: Save modules + lessons
        ARCH-->>ORCH: Completed
        ORCH-->>API: Stage ready for review
        API-->>C: Notify: "Curriculum ready"
        C->>API: POST /stages/architect/approve
    end

    rect rgb(255, 245, 240)
        Note over ORCH,SCRIPT: Stage 3 — Script Writing
        ORCH->>SCRIPT: Run with curriculum
        SCRIPT->>GM: Generate lesson scripts (parallel)
        GM-->>SCRIPT: Full lesson scripts with [VERIFY] flags
        SCRIPT->>SUPABASE: Upload scripts to Storage
        SCRIPT->>SUPABASE: Save script metadata + URLs
        SCRIPT-->>ORCH: Completed
        ORCH-->>API: Stage ready for review
        API-->>C: Notify: "Scripts ready for review"
        C->>API: POST /stages/scriptwriter/approve
    end

    rect rgb(240, 255, 245)
        Note over ORCH,MEDIA: Stage 4 — Media Production
        ORCH->>MEDIA: Run with approved scripts
        MEDIA->>GM: Generate slide content
        MEDIA->>GM: "Generate voice narration (TTS)"
        MEDIA->>SUPABASE: "Upload slides (PPTX + PNG)"
        MEDIA->>SUPABASE: "Upload narration (MP3)"
        MEDIA->>SUPABASE: "Render video (FFmpeg → MP4)"
        MEDIA->>SUPABASE: Upload captions + thumbnail
        MEDIA->>SUPABASE: Save media URLs
        MEDIA-->>ORCH: Completed
        ORCH-->>API: Stage ready for review
        API-->>C: Notify: "Media ready for review"
        C->>API: POST /stages/mediaforge/approve
    end

    rect rgb(255, 250, 240)
        Note over ORCH,EVAL: Stage 5 — Assessments
        ORCH->>EVAL: Run with course data
        EVAL->>GM: Generate quizzes + capstone brief
        GM-->>EVAL: Quiz questions + capstone project
        EVAL->>SUPABASE: Save quizzes
        EVAL-->>ORCH: Completed
        ORCH-->>API: Stage ready for review
        API-->>C: Notify: "Quizzes ready for review"
        C->>API: POST /stages/evaluator/approve
    end

    rect rgb(245, 245, 255)
        Note over ORCH,LAUNCH: Stage 6 — Launch Preparation
        ORCH->>LAUNCH: Run with full course data
        LAUNCH->>GM: Generate sales page + emails + social posts
        GM-->>LAUNCH: Sales HTML + email sequence + social content
        LAUNCH-->>ORCH: Completed
        ORCH-->>API: Stage ready for final review
        API-->>C: Notify: "Course ready for final review"
    end

    C->>API: POST /courses/{id}/publish
    API->>EXT: Create Stripe product + price
    API->>EXT: Index course in Algolia
    API->>SUPABASE: "Update course status (published)"
    API->>EXT: Send notification emails
    API-->>C: Return published course URL

    rect rgb(240, 240, 250)
        Note over OPTIMIZER: Post-Launch (Weekly)
        OPTIMIZER->>SUPABASE: Analyze student engagement data
        OPTIMIZER->>GM: Generate improvement report
        OPTIMIZER->>SUPABASE: Save improvement report
        OPTIMIZER-->>API: Notify creator of new report
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
| REST API | FastAPI + Pydantic v2 | Docker container (2 vCPU, 2GB) | Horizontal auto-scale |
| Background Workers | RQ / BullMQ | Docker container (2 vCPU, 2GB) | Horizontal auto-scale |
| Database ORM | SQLAlchemy 2.0 (async) | Supabase PostgreSQL 16 | Primary + Read Replica |
| Migrations | Alembic | GitHub Actions step | — |
| Cache / Queue | Redis | 5GB Standard | Replicated |
| Event Stream | Confluent Kafka (optional) | Managed cluster | Partition-based |

### AI & Machine Learning

| Component | Provider | Model / Service |
|-----------|----------|-----------------|
| Text Generation | Google | Gemini 3.5 Flash (primary, all agentic tasks) |
| Embeddings | Google | Gemini Embedding 2 (1536d) via pgvector |
| Speech-to-Text | Google | Gemini 3.5 Flash (multimodal) |
| Text-to-Speech | Google / ElevenLabs | Gemini TTS / Voice Cloning |
| Agent Orchestration | LangChain | LangGraph Supervisor |
| AI Observability | Langfuse | Self-hosted |
| PII Detection | Microsoft Presidio | Self-hosted |
| Plagiarism | Originality.ai | API |
| Video Rendering | FFmpeg | Background worker (no GPU needed) |

### Frontend & Mobile

| Platform | Framework | State Management | Deployment |
|----------|-----------|-----------------|------------|
| Creator OS (Web) | Next.js 14+ (App Router) | Zustand + TanStack Query | Docker container |
| LearnSpace (Web) | Next.js 14+ (App Router) | Zustand + TanStack Query | Docker container |
| Mobile App | React Native + Expo SDK 52+ | Zustand + TanStack Query | EAS Build → App Store/Play |

### Third-Party Integrations

| Service | Purpose | Webhook |
|---------|---------|---------|
| Stripe | Payments, Connect, Tax | `POST /webhooks/stripe` |
| SendGrid | Transactional emails | `POST /webhooks/sendgrid` |
| Twilio | WhatsApp notifications | `POST /webhooks/twilio` |
| Algolia | Course search indexing | — |
| PostHog | Product analytics, feature flags | — |

### Data Layer (Supabase — Unified)

| Component | Implementation | Configuration |
|-----------|---------------|---------------|
| Relational DB | PostgreSQL 16 | Primary + Read Replica, PgBouncer pooling |
| Vector DB | pgvector extension | 1536d embeddings, hybrid search (0.65 vector + 0.35 BM25) |
| Object Storage | Supabase Storage | Media files, certificates, scripts, slides |
| Authentication | Supabase Auth | JWT, magic link, Google/GitHub OAuth, email+password |

### Observability

| Component | Implementation |
|-----------|---------------|
| Metrics | Prometheus (exporters on all services) |
| Dashboards | Grafana (API latency, error rates, queue depths, AI cost per course) |
| Logging | Structured JSON stdout → log collector |
| Alerting | Grafana Alerting (Slack/PagerDuty) |
| AI Observability | Langfuse (per-agent cost, latency, quality tracing) |

### CI/CD

| Pipeline | Implementation |
|----------|---------------|
| CI | GitHub Actions (lint → type check → test → build) |
| CD | GitHub Actions (deploy dev on PR merge, main with manual approval) |
| Container Registry | Docker Hub / GitHub Container Registry |
| IaC | Terraform (workspaces: dev, staging, prod) |
