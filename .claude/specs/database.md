# Database Design — EduGenie OS

## Platform

- **Primary DB:** Supabase (PostgreSQL 16 + pgvector extension)
- **Cache/Queue:** Redis
- **ORM:** SQLAlchemy 2.0 (async)
- **Migrations:** Alembic

---

## Core Tables

### Organizations (top-level tenant)
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | `gen_random_uuid()` |
| name | VARCHAR(255) | Organization name |
| slug | VARCHAR(100) UNIQUE | URL-friendly identifier |
| settings | JSONB | Brand settings, defaults |
| created_at | TIMESTAMPTZ | `DEFAULT NOW()` |

### Creators
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| organization_id | UUID FK → organizations | Multi-tenant key |
| supabase_user_id | UUID | Supabase Auth reference |
| plan_tier | VARCHAR(50) | starter / creator / studio / enterprise |
| voice_model_id | VARCHAR(255) | ElevenLabs voice ID |
| brand_settings | JSONB | Brand colors, logo, fonts |
| display_name | VARCHAR(200) | |
| bio | TEXT | |
| created_at | TIMESTAMPTZ | |

### Courses
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| organization_id | UUID FK → organizations | |
| creator_id | UUID FK → creators | |
| title | VARCHAR(300) | |
| slug | VARCHAR(200) | URL slug |
| status | VARCHAR(50) | draft / published / archived |
| version | INTEGER | Incremented on publish |
| price | DECIMAL(10,2) | In USD |
| stripe_product_id | VARCHAR(100) | Stripe product reference |
| stripe_price_id | VARCHAR(100) | Stripe price reference |
| topic_brief | JSONB | Original submission |
| language | VARCHAR(10) | Primary language (e.g., 'en') |
| thumbnail_url | TEXT | Supabase Storage URL |
| total_duration_min | INTEGER | Sum of lesson durations |
| difficulty | VARCHAR(20) | beginner / intermediate / advanced |
| created_at | TIMESTAMPTZ | |
| published_at | TIMESTAMPTZ | |

### Course Versions
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| course_id | UUID FK → courses | |
| version_number | INTEGER | |
| changelog | TEXT | Description of changes |
| snapshot | JSONB | Full course state at publish |
| created_at | TIMESTAMPTZ | |

### Modules
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| course_id | UUID FK → courses | |
| position | INTEGER | Ordering (1-based) |
| title | VARCHAR(300) | |
| learning_objective | TEXT | Bloom's taxonomy aligned |
| bloom_level | VARCHAR(50) | remember / understand / apply / analyze / evaluate / create |
| estimated_duration_min | INTEGER | |
| prerequisites | UUID[] | Array of module IDs |

### Lessons
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| module_id | UUID FK → modules | |
| position | INTEGER | Ordering (1-based) |
| title | VARCHAR(300) | |
| script_url | TEXT | Supabase Storage URL for script |
| video_url | TEXT | Supabase Storage signed URL for MP4 |
| slides_url | TEXT | Supabase Storage URL for PPTX |
| captions_url | TEXT | Supabase Storage URL for SRT |
| thumbnail_url | TEXT | |
| duration_min | INTEGER | |
| word_count | INTEGER | Script word count |
| verify_flags | INTEGER | Count of [VERIFY] tags |
| created_at | TIMESTAMPTZ | |

### Quizzes
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| module_id | UUID FK → modules | |
| lesson_id | UUID FK → lessons | Nullable (lesson-level or module-level) |
| pass_threshold | INTEGER | Default 70 (%) |
| max_attempts | INTEGER | Default 3 |
| questions | JSONB | Array of question objects |
| created_at | TIMESTAMPTZ | |

**Question JSON structure:**
```json
{
  "id": "uuid",
  "type": "multiple_choice | true_false | fill_blank | matching",
  "bloom_level": "remember | understand | apply",
  "difficulty": 1.0,
  "question": "What is...?",
  "options": ["A", "B", "C", "D"],
  "correct_answer": "A",
  "explanation": "2–3 sentence explanation",
  "points": 1
}
```

### Students
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| supabase_user_id | UUID | Supabase Auth reference |
| stripe_customer_id | VARCHAR(100) | Stripe customer reference |
| display_name | VARCHAR(200) | |
| email | VARCHAR(255) | |
| locale | VARCHAR(10) | |
| created_at | TIMESTAMPTZ | |

### Enrollments
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| student_id | UUID FK → students | |
| course_id | UUID FK → courses | |
| version | INTEGER | Course version at enrollment |
| status | VARCHAR(50) | active / completed / refunded |
| enrolled_at | TIMESTAMPTZ | |
| completed_at | TIMESTAMPTZ | Nullable |
| certificate_id | UUID FK → certificates | Nullable |

### Progress (per-lesson)
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| enrollment_id | UUID FK → enrollments | |
| lesson_id | UUID FK → lessons | |
| watch_depth_pct | DECIMAL(5,2) | 0.00–100.00 |
| time_spent_sec | INTEGER | |
| completed_at | TIMESTAMPTZ | Nullable |
| updated_at | TIMESTAMPTZ | Updated on each watch event |

### Quiz Attempts
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| enrollment_id | UUID FK → enrollments | |
| quiz_id | UUID FK → quizzes | |
| score | DECIMAL(5,2) | 0.00–100.00 |
| passed | BOOLEAN | |
| answers | JSONB | Student's answers array |
| duration_sec | INTEGER | |
| attempted_at | TIMESTAMPTZ | |
| attempt_number | INTEGER | |

### Sales
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| course_id | UUID FK → courses | |
| enrollment_id | UUID FK → enrollments | |
| stripe_payment_intent_id | VARCHAR(100) | Stripe reference |
| amount | DECIMAL(10,2) | Transaction amount |
| platform_fee | DECIMAL(10,2) | |
| creator_earnings | DECIMAL(10,2) | |
| channel | VARCHAR(50) | direct / marketplace / affiliate / promo |
| promo_code | VARCHAR(50) | Nullable |
| refunded_at | TIMESTAMPTZ | Nullable |
| created_at | TIMESTAMPTZ | |

### Affiliates
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| course_id | UUID FK → courses | |
| creator_id | UUID FK → creators | |
| affiliate_name | VARCHAR(200) | |
| commission_pct | DECIMAL(5,2) | 10.00–70.00 |
| cookie_window_days | INTEGER | 7 / 14 / 30 / 60 |
| referral_link | TEXT | Unique tracking URL |
| total_clicks | INTEGER | |
| total_conversions | INTEGER | |
| total_earned | DECIMAL(10,2) | |
| created_at | TIMESTAMPTZ | |

### Certificates
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| enrollment_id | UUID FK → enrollments | |
| verification_code | VARCHAR(16) UNIQUE | Alphanumeric, 16 chars |
| pdf_url | TEXT | Supabase Storage URL |
| badge_json | JSONB | Open Badge format |
| status | VARCHAR(20) | active / revoked / revised |
| issued_at | TIMESTAMPTZ | |
| revoked_at | TIMESTAMPTZ | Nullable |
| revoked_reason | TEXT | Nullable |

### Discussions (per-lesson Q&A)
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| lesson_id | UUID FK → lessons | |
| student_id | UUID FK → students | |
| content | TEXT | Question content |
| ai_response | TEXT | AI-generated answer |
| ai_confidence | DECIMAL(5,2) | |
| creator_verified | BOOLEAN | |
| upvotes | INTEGER | |
| created_at | TIMESTAMPTZ | |

### Pipeline Runs
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| course_id | UUID FK → courses | |
| stage | VARCHAR(50) | intelligence / architect / scriptwriter / mediaforge / evaluator / launchpad / optimizer |
| status | VARCHAR(50) | running / completed / failed / approved |
| model_used | VARCHAR(100) | e.g., 'gemini-3.5-flash' |
| tokens_used | INTEGER | |
| cost_usd | DECIMAL(10,6) | |
| started_at | TIMESTAMPTZ | |
| completed_at | TIMESTAMPTZ | Nullable |
| error | TEXT | Nullable |

### Improvement Reports (Optimizer)
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| course_id | UUID FK → courses | |
| report_data | JSONB | Full Optimizer report |
| priority_score | DECIMAL(5,2) | |
| viewed_at | TIMESTAMPTZ | Nullable |
| week_start | DATE | |
| created_at | TIMESTAMPTZ | |

### Notifications
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| user_id | UUID FK → users | |
| notification_type | VARCHAR(50) | |
| title | VARCHAR(200) | |
| body | TEXT | |
| data | JSONB | Contextual payload |
| is_read | BOOLEAN | DEFAULT FALSE |
| created_at | TIMESTAMPTZ | |
| read_at | TIMESTAMPTZ | Nullable |

**Index:** `CREATE INDEX idx_notifications_user_unread ON notifications(user_id, is_read) WHERE NOT is_read;`

### Audit Logs (immutable, append-only)
| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| organization_id | UUID FK → organizations | |
| actor_id | UUID | User or system |
| action | VARCHAR(100) | e.g., 'pipeline.stage.approved' |
| resource_type | VARCHAR(50) | 'course', 'lesson', etc. |
| resource_id | UUID | |
| details | JSONB | |
| ip_address | INET | |
| created_at | TIMESTAMPTZ | |

---

## Vector Database (pgvector)

- **Embeddings Model:** Gemini Embedding 2 (1536 dimensions)
- **Extension:** `pgvector` on Supabase PostgreSQL

### Use Cases
1. **Research cache** (Intelligence Agent) — deduplicate web search results by `(topic_hash, date)`
2. **Curriculum pattern matching** — suggest adjustments from high-completion courses via similarity search
3. **Content similarity** — establish plagiarism baseline for Originality.ai comparison
4. **Learner confusion signal clustering** — group unresolved discussion questions by concept

### Hybrid Search Strategy
```
Score = 0.65 × vector_similarity + 0.35 × BM25_text_score
```

---

## Migration Strategy

- **Tool:** Alembic with async SQLAlchemy
- **Pattern:** Additive-only migrations for 2 releases; destructive migrations require dual-write period + explicit rollback script in PR
- **CI/CD:** Migrations run as part of CI/CD deploy step
- **Rollback:** `alembic downgrade -1` with verification script
- **Multi-tenant isolation:** `organization_id` on every table; Supabase RLS policies enforce tenant isolation

### Backup & Recovery
- Hourly Supabase snapshots
- Supabase Storage object versioning enabled
- RPO < 1hr, RTO < 3hrs
- Supabase PostgreSQL with 1 primary + 1 read replica
- PgBouncer connection pooling

---

## Data Privacy

- **Multi-tenant:** `organization_id` + `creator_id` on every table; Supabase RLS policies enforce tenant isolation
- **PII Encryption:** AES-256 at application level for student names/emails; TLS 1.3 in transit
- **Creator Content:** Creator owns all AI-generated content — EduGenie claims no IP or training rights
- **Voice Model Audio:** Encrypted in Supabase Storage; accessible only by creator's account and ElevenLabs
- **Compliance:** GDPR right-to-access (30-day export), right-to-deletion (90-day processing), DPA with sub-processors
- **Student PII:** Stored in isolated tables; never passed to LLM prompts; behavioral data uses anonymous student IDs
