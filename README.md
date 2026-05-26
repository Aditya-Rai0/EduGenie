# EduGenie OS

**AI-Powered Course Creation & Launch Platform**

EduGenie is an advanced educational platform that takes a topic brief and autonomously builds, packages, launches, and continuously improves a full online course — content, video, quizzes, sales page, and payment — in a single session.

---

## Monorepo Architecture

```
edugenie/
├── backend/            # FastAPI server (Python 3.12)
│   ├── app/
│   │   ├── api/        # REST + WebSocket endpoints
│   │   ├── agents/     # LangGraph AI agent pipeline
│   │   ├── core/       # Security, cache, storage, queue
│   │   ├── models/     # SQLAlchemy ORM models
│   │   ├── schemas/    # Pydantic request/response schemas
│   │   ├── services/   # Business logic layer
│   │   └── integrations/ # OpenAI, Stripe, SendGrid, etc.
│   ├── alembic/        # Database migrations
│   └── requirements/   # Dependency manifests
├── frontend-web/       # Next.js 14+ Creator OS & LearnSpace
├── mobile-app/         # React Native + Expo
├── infra/              # Terraform, Cloud Build, deployment scripts
├── docs/               # Architecture, PRD, deployment guides
└── tests/              # Backend, frontend, and mobile test suites
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **API** | FastAPI + Pydantic v2 (Python 3.12) |
| **AI / Agents** | LangChain, LangGraph, OpenAI GPT-4o |
| **Database** | PostgreSQL 16 + pgvector (Supabase) |
| **ORM** | SQLAlchemy 2.0 (async) + Alembic |
| **Auth** | Supabase Auth (JWT, magic link, OAuth) |
| **Queue** | Redis + RQ |
| **Web Frontend** | Next.js 14+ (App Router), TypeScript, Tailwind CSS |
| **Mobile** | React Native + Expo SDK 52+ |
| **Infrastructure** | GCP (Cloud Run, Cloud Storage, Cloud SQL) |
| **CI/CD** | Cloud Build, Artifact Registry, Cloud Deploy |
| **IaC** | Terraform |
| **Payments** | Stripe (Checkout, Connect, Tax) |
| **Email** | SendGrid |
| **Notifications** | Twilio WhatsApp, Expo Push, WebSocket |

---

## Git Workflow

This repository follows a structured branch-and-PR workflow:

### Branch Hierarchy

```
main ────── production-ready (protected, 2 approvals required)
  │
testing ─── QA environment (protected, 1 approval required)
  │
development ── integration branch (protected, 1 approval required)
  │
  └── feature/* ── short-lived feature branches
```

### Workflow Rules

| Rule | Description |
|------|-------------|
| **No direct commits** | All branches are protected — direct pushes are blocked |
| **PRs required** | Every change must go through a Pull Request |
| **Code reviews** | `main` requires 2 approvals; `development` and `testing` require 1 |
| **Feature branches** | Create from `development`: `git checkout -b feature/my-feature development` |
| **Merge direction** | Feature → Development → Testing → Main |

### Getting Started

```bash
git clone https://github.com/Aditya-Rai0/EduGenie.git
git checkout development
git pull
git checkout -b feature/your-feature-name
```

After completing work on your feature branch, push it and open a PR against `development`.

---

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements/dev.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend-web
npm install
npm run dev
```

### Mobile

```bash
cd mobile-app
npm install
npx expo start --tunnel
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the required values:

```bash
cp .env.example .env
```

See `.env.example` for the full list of required variables (API keys for OpenAI, Stripe, SendGrid, Twilio, GCP, etc.).

---

## Related Documents

- [Architecture & Design](./docs/architecture.md)
- [API Documentation](./docs/api/openapi.json)
- [Deployment Guide](./docs/deployment.md)
- [PRD](./docs/prd/EduGenie_OS_PRD_Compact_v1.0.pdf)
