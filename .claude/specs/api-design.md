# API Design — EduGenie OS

## Base URL

All API endpoints are versioned:

```
https://api.edugenie.io/api/v1/
```

## Authentication & Authorization

### Auth Strategy — Supabase Auth
- **Methods:** Magic link (primary), Google OAuth, GitHub OAuth, email+password fallback
- **Multi-factor:** Optional TOTP 2FA
- **Tokens:** JWTs (1hr expiry) + rotating refresh tokens (30-day window)

### Role-Based Access Control (RBAC)
```
Roles: admin | creator | student | enterprise_admin | affiliate
```

- **Supabase RLS policies** on all tables enforce tenant isolation via `organization_id`
- **Backend middleware** validates JWT and checks permissions per endpoint
- **Creator scoping:** creators access only their own data via `creator_id` filter
- **Student scoping:** students access only courses they're enrolled in

### API Authentication Levels
- **Public:** No auth required — marketplace search, course detail, certificate verification
- **JWT Authenticated:** User must be logged in — enrollment, progress, profile
- **Creator-Only:** Studio, analytics, revenue, affiliates
- **Admin:** Enterprise batch, platform settings
- **Webhook:** Signature verification (Stripe: HMAC-SHA256, SendGrid: API key header, Twilio: Twilio signature)

### API Security
- **Authentication:** JWT (1hr expiry) + refresh tokens (30-day rotation)
- **Authorization:** Supabase RLS + FastAPI dependency injection for role checks
- **Input Validation:** Pydantic v2 on all endpoints
- **CORS:** Whitelist of allowed origins (edugenie.io, *.edugenie.io)
- **Rate Limiting:** 200 req/min standard, 2000 req/min enterprise
- **Webhook Verification:** Stripe HMAC-SHA256, Twilio signature validation, SendGrid webhook signature

---

## REST Endpoints

### Auth

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/signup` | Public | Create account |
| POST | `/auth/login` | Public | Email+password login |
| POST | `/auth/magic-link` | Public | Request magic link |
| POST | `/auth/refresh` | Public | Refresh JWT |
| GET | `/auth/me` | JWT | Current user profile |

### Creators

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/creators/{id}` | JWT | Creator profile |
| PATCH | `/creators/{id}` | Creator | Update profile |
| GET | `/creators/{id}/courses` | Creator | Creator's courses |
| GET | `/creators/{id}/revenue` | Creator | Revenue dashboard data |

### Courses

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/courses` | Public | List courses |
| POST | `/courses` | Creator | Create course |
| PATCH | `/courses/{id}` | Creator | Update course |
| POST | `/courses/build` | Creator | Submit topic brief → start pipeline |
| GET | `/courses/{id}/pipeline` | Creator | Pipeline status |
| POST | `/courses/{id}/publish` | Creator | Publish course |

### Pipeline Stages

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/courses/{id}/stages/{stage}/approve` | Creator | Approve pipeline stage |
| POST | `/courses/{id}/stages/{stage}/regenerate` | Creator | Regenerate stage with instructions |

### Voice Models

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/voice/train` | Creator | Upload audio → train voice model |
| GET | `/voice/models` | Creator | List voice models |
| POST | `/voice/test` | Creator | Test voice model with text |
| DELETE | `/voice/{id}` | Creator | Delete voice model |

### Lessons

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/courses/{id}/lessons` | JWT | List lessons |
| GET | `/lessons/{id}/script` | JWT | Get lesson script |
| GET | `/lessons/{id}/video` | JWT | Get video signed URL |
| GET | `/lessons/{id}/slides` | JWT | Get slide download URL |

### Quizzes

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/courses/{id}/quizzes` | JWT | List quizzes |
| PATCH | `/courses/{id}/quizzes` | Creator | Update quiz questions |
| POST | `/quizzes/{id}/attempt` | Student | Submit quiz attempt |
| GET | `/quizzes/{id}/results` | Student | Get attempt results |

### Students

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/students/{id}` | JWT | Student profile |
| GET | `/students/{id}/enrollments` | Student | Enrolled courses |
| GET | `/students/{id}/progress` | Student | Course progress |

### Enrollments

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/enrollments` | System | Create enrollment (Stripe webhook) |
| GET | `/enrollments/{id}/progress` | Student | Per-course progress |
| POST | `/enrollments/{id}/complete` | Student | Mark course complete |

### Certificates

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/certificates/generate` | System | Auto-generate on completion |
| GET | `/certificates/verify/{code}` | Public | Verification page |

### Analytics

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/analytics/courses/{id}/overview` | Creator | Course analytics overview |
| GET | `/analytics/courses/{id}/lessons` | Creator | Per-lesson analytics |
| GET | `/analytics/courses/{id}/quizzes` | Creator | Quiz performance |
| GET | `/analytics/courses/{id}/improvement-report` | Creator | Optimizer report |

### Marketplace

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/marketplace/search` | Public | Algolia proxy search |
| GET | `/marketplace/courses/{id}` | Public | Course detail page data |
| GET | `/marketplace/recommendations` | Public | AI recommendations |

### Affiliates

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/affiliates` | Creator | Generate affiliate link |
| GET | `/affiliates/{id}/stats` | Creator | Affiliate performance |
| GET | `/affiliates/{id}/payouts` | Creator | Affiliate payout history |

### Enterprise Batch

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/batch/jobs` | Admin | Submit batch CSV |
| GET | `/batch/jobs/{id}` | Admin | Batch status |
| POST | `/batch/jobs/{id}/retry` | Admin | Retry failed job |

### Webhooks

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/webhooks/stripe` | Public | Stripe event webhook |
| POST | `/webhooks/sendgrid` | Public | SendGrid event webhook |
| POST | `/webhooks/twilio` | Public | Twilio status callback |

### Health

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/health` | Public | Basic health check |
| GET | `/health/detailed` | Internal | Detailed service status |

---

## WebSocket Endpoints

| Endpoint | Description |
|----------|-------------|
| `WS /ws/pipeline/{job_id}/live` | Real-time pipeline stage progress (stage name, % complete, ETA) |
| `WS /ws/analytics/{course_id}` | Live student enrollment + completion events |
| `WS /ws/notifications/{user_id}` | Real-time in-app notifications |

---

## Rate Limiting

| Tier | Limit |
|------|-------|
| Starter (Free) | 3 course builds/month, max 5 modules, 5 listings |
| Creator ($45/mo) | Unlimited builds, unlimited modules, priority queue |
| Studio ($109/mo) | Everything in Creator + 8 parallel builds |
| Enterprise | Unlimited everything, 30 parallel builds, custom rate limits |
| API (Public) | Standard: 200 req/min, Enterprise: 2,000 req/min |

---

## Data Encryption & Security

- **At Rest:** AES-256 for PII (student names/emails) at application level; Supabase Storage server-side encryption (AES-256); Supabase encryption at rest
- **In Transit:** TLS 1.3 enforced for all external traffic; internal traffic encrypted by default
- **API Security:** JWT (1hr expiry) + refresh tokens (30-day rotation), Pydantic v2 input validation, CORS whitelist
- **Rate Limiting:** OWASP Top 10 rules, rate limiting, DDoS protection
