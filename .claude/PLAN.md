# PLAN — EduGenie OS Project Plan

High-level roadmap, milestones, dependencies, and delivery timeline.

---

## Timeline Overview

```
Phase 0: Foundation     Month 1–2    ████████░░░░░░░░░░░░  16%
Phase 1: Alpha Pipeline Month 3–4    ░░░░░░░░████░░░░░░░░  16%
Phase 2: Public Beta    Month 5–6    ░░░░░░░░░░░░████░░░░  16%
Phase 3: Growth         Month 7–12   ░░░░░░░░░░░░░░░░████  52%
                                                             100%
                              Launch
                                │
                         Month 4 (Alpha)
                         Month 6 (Public Beta)
                        Month 12 (Full GA)
```

## Milestones

| Milestone | Target | Deliverable | Gate Criteria |
|-----------|--------|-------------|---------------|
| M0 - Foundation Complete | Month 2 | GCP infra provisioned, DB schema, auth, CI/CD, dev env | Empty course created via API E2E; CI/CD green |
| M1 - Alpha Launch | Month 4 | Full 7-agent pipeline, Creator Studio, LearnSpace, Stripe | 10-module course built < 4hrs; first paying student |
| M2 - Beta Launch | Month 6 | Marketplace, affiliates, analytics, multi-language, mobile | 800 creators; $35K MRR; 5K courses |
| M3 - GA Launch | Month 12 | Enterprise batch, adaptive paths, public API, SOC 2 start | 5K creators; $180K MRR; 30K courses |

## Release Strategy

```
Phase 0 ──► Phase 1 ──► Phase 2 ──► Phase 3
  │             │            │            │
  ▼             ▼            ▼            ▼
  Dev           Alpha        Beta         GA
  (internal)    (30 users)   (800 users)  (public)
```

## Dependency Map

```
Phase 0 (Foundation)
├── GCP Infrastructure (Terraform)
├── Supabase Schema + Auth
├── FastAPI Scaffold
├── Next.js Scaffold
├── LangGraph Orchestrator Skeleton
├── CI/CD Pipeline
├── Local Dev Environment (Docker Compose)
└── SendGrid + Twilio + Stripe Base
│
├── Depends on: Nothing (foundation layer)
└── Required by: Phase 1, Phase 2, Phase 3

Phase 1 (Alpha Pipeline)
├── Intelligence Agent
├── Architect Agent
├── Scriptwriter Agent
├── MediaForge Agent (Slides, Voice, Video)
├── Evaluator Agent
├── Launchpad Agent
├── Creator Studio (6-stage Review)
├── LearnSpace Course Player + Quizzes + Certificates
├── Stripe Payments + Connect
├── Voice Studio
├── Mobile App Scaffold
├── In-App Notifications (WebSocket + Push)
└── Invite-Only Alpha (30 creators)
│
├── Depends on: Phase 0
└── Required by: Phase 2

Phase 2 (Public Beta)
├── Optimizer Agent
├── Algolia Marketplace Search + AI Recommendations
├── Affiliate System + Stripe Connect Payouts
├── Analytics Dashboard (Real-time + AI Narrative)
├── Multi-Language (6 languages)
├── White-Label Storefront (Beta)
├── Promo Code Engine
├── Course Version Management
├── Revenue Dashboard
├── EAS Build (iOS TestFlight, Android Internal)
└── Open Beta (800 creators)
│
├── Depends on: Phase 1
└── Required by: Phase 3

Phase 3 (Growth & Enterprise)
├── Enterprise Batch Generation (CSV + Kanban)
├── Advanced Analytics (Cohort, Heatmap, Per-Question)
├── Course Repurposing Engine
├── Adaptive Learner Paths
├── PWA → Full Native (Expo)
├── SSO/SAML + SCORM/xAPI Export
├── Public API + Rate Limiting
├── Compliance Course Templates
├── Enterprise SLA Tiers
├── Native Learner App (iOS + Android)
├── SOC 2 Type II Audit (Month 9 start)
└── 5,000 Creators; $180K MRR
│
└── Depends on: Phase 2
```

## Resource Plan

### Phase 0 (Months 1-2)
- 1 Backend Engineer (Full-time)
- 1 Frontend Engineer (Full-time)
- 1 DevOps Engineer (Part-time)

### Phase 1 (Months 3-4)
- 2 Backend Engineers (Full-time)
- 1 Frontend Engineer (Full-time)
- 1 Mobile Engineer (Part-time)
- 1 AI/ML Engineer (Full-time)

### Phase 2 (Months 5-6)
- 2 Backend Engineers (Full-time)
- 2 Frontend Engineers (Full-time)
- 1 Mobile Engineer (Full-time)
- 1 AI/ML Engineer (Full-time)
- 1 QA Engineer (Part-time)

### Phase 3 (Months 7-12)
- 3 Backend Engineers (Full-time)
- 2 Frontend Engineers (Full-time)
- 2 Mobile Engineers (Full-time)
- 2 AI/ML Engineers (Full-time)
- 1 QA Engineer (Full-time)
- 1 DevOps Engineer (Full-time)

## Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| AI cost per course exceeds $12 | Financial | Medium | Model routing (GPT-4o-mini for simple tasks); narration caching by hash |
| Pipeline hallucinations > 2% | Quality | Medium | [VERIFY] flags on uncertain claims; human review gates before video |
| Cloud Run cold start latency | Performance | Low | Min instances = 1; CPU always-on for workers; connection pooling |
| Supabase pgvector performance | Performance | Medium | Index tuning; hybrid search (0.65 vector + 0.35 BM25); read replica |
| ElevenLabs voice training quality | Quality | Low | Minimum 10-30 min audio required; test-before-deploy flow |
| Stripe Connect onboarding friction | Adoption | Medium | Express dashboard; guided onboarding flow; test mode for creators |
| Course completion rate < 45% | Product | High | Weekly Optimizer reports; AI-powered discussion Q&A; adaptive paths (Phase 3) |
| Prompt injection / PII leakage | Security | Medium | Microsoft Presidio scanning; content sandboxing; audit logging |

## Success Criteria Summary

| Phase | Key Metric | Target |
|-------|------------|--------|
| Phase 0 | E2E empty course via API | Complete |
| Phase 1 | Full course build time | < 4 hours |
| Phase 1 | First paying student | Complete |
| Phase 2 | Paying creators | 800 |
| Phase 2 | MRR | $35K |
| Phase 2 | Published courses | 5,000 |
| Phase 2 | Course completion rate | > 35% |
| Phase 3 | Paying creators | 5,000 |
| Phase 3 | MRR | $180K |
| Phase 3 | Published courses | 30,000 |
| Phase 3 | Enterprise accounts | 10 |
| Phase 3 | Platform completion rate | > 45% |
