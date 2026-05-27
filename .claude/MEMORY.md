# MEMORY — EduGenie OS Project Memory

Tracks project context, decisions, architecture references, session state, and historical context for AI-assisted development.

---

## Project Identity

- **Project:** EduGenie OS — AI-Powered Course Creation & Launch Platform
- **PRD Version:** v1.0
- **Repository Root:** `C:\Users\dilsa\Desktop\Edugenio\`
- **Target Users:** Independent creators, corporate L&D teams, digital agencies

## Tech Stack (Decided)

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0 async |
| Frontend Web | Next.js 14+ (App Router), TypeScript strict, Tailwind CSS, Radix UI |
| Mobile | React Native + Expo SDK 52+, React Navigation |
| Database | Supabase (PostgreSQL 16 + pgvector), Redis |
| Storage | Supabase Storage |
| Auth | Supabase Auth (magic link, OAuth, JWT) |
| AI | Gemini 3.5 Flash (Text, Embed, TTS, STT) |
| Agent Framework | LangGraph supervisor pattern (7 agents) |
| Payments | Stripe (Checkout, Connect, Tax, Billing Portal) |
| Email | SendGrid |
| WhatsApp | Twilio |
| Search | Algolia |
| Analytics | PostHog |
| AI Observability | Langfuse |
| Infrastructure | Docker containers (any hosting platform) |
| IaC | Terraform |
| CI/CD | GitHub Actions (lint → type check → test → build → deploy) |
| Monitoring | Prometheus + Grafana |

## Architecture Decisions

| ID | Decision | Rationale | Date |
|----|----------|-----------|------|
| ADR-001 | Docker containers over cloud-specific infra | User requirement; provider-agnostic container-based deployment | Session 1 |
| ADR-002 | Supabase over Cloud SQL | User requirement; PostgreSQL 16 + pgvector + auth out of box | Session 1 |
| ADR-003 | LangGraph over custom agent framework | Mature supervisor pattern, state checkpointing, parallel execution | Session 1 |
| ADR-004 | Gemini 3.5 Flash primary | Gemini 3.5 Flash best quality/cost for course content; ElevenLabs for voice | Session 1 |
| ADR-005 | SendGrid over Resend | Used in original PRD reference architecture; proven at scale | Session 1 |
| ADR-006 | Modular specs/ directory | CLAUDE.md became unwieldy; split into 7 focused files for maintainability | Session 1 |

## File Map

```
C:\Users\dilsa\Desktop\Edugenio\
├── CLAUDE.md            — Top-level authoritative spec (20 sections)
├── SKILL.md             — Required competencies by domain (this file)
├── MEMORY.md            — Project memory & session tracking (this file)
├── PLAN.md              — High-level roadmap & milestones (this file)
├── PLAN_PHASE.md        — Phase-by-phase detailed breakdown (this file)
├── specs/
│   ├── stack.md         — Architecture, stack, features, directory, metrics
│   ├── api-design.md    — REST endpoints, WebSocket, auth, RBAC, rate limits
│   ├── database.md      — 19 core tables, pgvector, migrations, compliance
│   ├── supabase-infrastructure.md — Supabase setup (Storage, Auth, DB)
│   ├── integrations.md  — SendGrid, Twilio, Stripe, Gemini setup + code
│   ├── mobile.md        — Expo config, navigation, push, EAS Build
│   └── deployment.md    — CI/CD pipeline, phases, secrets, domain
└── EduGenie_OS_PRD_Compact_v1.0.pdf — Original source PRD
```

## Session Log

### Session 1 (Current)
- Read PRD PDF and extracted full content
- Created CLAUDE.md (1534 lines, 56,495 chars) with all 20 sections
- Split into 7 modular spec files in specs/ with zero content loss
- Created SKILL.md, MEMORY.md, PLAN.md, PLAN_PHASE.md

### Key Actions Remaining
- Initialize project directories per CLAUDE.md structure
- Scaffold backend (FastAPI + SQLAlchemy + Alembic)
- Scaffold frontend-web (Next.js + Tailwind + Radix)
- Scaffold mobile-app (React Native + Expo)
- Write Terraform for infrastructure
- Implement core models and migrations
- Implement API endpoints
- Implement AI agents (LangGraph)
- Implement third-party integrations
- Set up CI/CD pipeline
- Local development environment (Docker Compose)

## Feature Tracking

| ID | Feature | Status | Agent |
|----|---------|--------|-------|
| F1 | Market Intelligence | Planned | Intelligence Agent |
| F2 | Curriculum Architect | Planned | Architect Agent |
| F3 | Script Engine | Planned | Scriptwriter Agent |
| F4 | Media Production | Planned | MediaForge Agent |
| F5 | Assessment Engine | Planned | Evaluator Agent |
| F6 | Launchpad | Planned | Launchpad Agent |
| F7 | Optimizer | Planned | Optimizer Agent |
| F8 | Creator Studio | Planned | - |
| F9 | Voice Studio | Planned | - |
| F10 | Analytics Dashboard | Planned | - |
| F11 | Course Update & Versioning | Planned | - |
| F12 | Affiliate & Revenue | Planned | - |
| F13 | Multi-Language Generation | Planned | - |
| F14 | Course Player & Progress | Planned | - |
| F15 | Assessment & Certificates | Planned | - |
| F16 | Course Marketplace | Planned | - |
| F17 | Payments & Subscriptions | Planned | - |
| F18 | Enterprise Batch Generation | Planned | - |

## Key Metrics (Targets)

| Metric | Target | Current |
|--------|--------|---------|
| Course build time (10-module) | < 4 hours | N/A |
| AI cost per full course | < $12 blended | N/A |
| API response latency | < 200ms p50, < 800ms p99 | N/A |
| Course completion rate | > 45% | N/A |
| Pipeline success rate | > 98% | N/A |
| AI hallucination rate | < 2% | N/A |
| MRR Month 6 | $35K | N/A |
| MRR Month 12 | $180K | N/A |
| Infrastructure cost (MVP) | ~$200/mo | N/A |

## Common Commands

```bash
# Backend
cd backend && uvicorn app.main:app --reload --port 8000
cd backend && pytest -xvs tests/unit/
cd backend && alembic upgrade head

# Frontend Web
cd frontend-web && npm run dev
cd frontend-web && npm run lint
cd frontend-web && npm run build

# Mobile
cd mobile-app && npx expo start --tunnel
cd mobile-app && npx jest

# Infrastructure
cd infra/terraform && terraform plan
cd infra && docker compose up -d
```
