# Cameroon Crop Doctor — Tech Stack

**Companion to:** `PROJECT_SPEC.md`, `PARTNERSHIPS.md`
**Owner:** asvaldr04@gmail.com
**Date:** 2026-05-25
**Status:** Draft v1

---

## 1. Guiding Principles

Before any specific tool, the choices below are driven by these principles:

1. **One source of truth for diagnosis logic.** Three frontends (mobile, web, chat) must never duplicate disease logic, advice templates, or model routing. All clients call the same backend API.
2. **Boring over clever.** This is a long-running social-impact project, not a tech demo. Mature, well-documented tools that a small team can operate.
3. **Cheap to operate at MVP, scalable later.** Single VPS today; containerized horizontal scale when the pilot proves traction.
4. **Locally operable.** A Cameroonian developer with a laptop and a free-tier cloud account should be able to spin the whole stack up in an afternoon.
5. **Privacy-respecting by default.** Farmer photo data is sensitive. Encryption at rest, minimum-necessary retention, no third-party analytics that read content.
6. **Reproducible ML.** Every deployed model traceable back to a (dataset version, code commit, training run) triple.
7. **Offline-friendly path.** MVP is cloud-only, but every tool choice keeps the door open for on-device inference and offline-tolerant clients in v2.
8. **Per-crop swappability.** Adding a new crop should not require touching client code — only adding a model file, advice templates, and a config entry.

---

## 2. Architecture Overview

### 2.1 System Diagram

```
┌─────────────────┬────────────────┬───────────────────────────┐
│  Mobile app     │   Web app      │  WhatsApp / Telegram bots │
│  React Native   │   Next.js      │  Python adapters          │
│  (Expo)         │   (Vercel)     │  (FastAPI sub-routes)     │
└────────┬────────┴────────┬───────┴──────────────┬────────────┘
         │                 │                      │
         └─────────────────┴──────────────────────┘
                            │
                            │  HTTPS / REST (OpenAPI-typed)
                            │
                  ┌─────────▼──────────┐
                  │   Backend API      │
                  │   Python FastAPI   │
                  │   (Caddy in front) │
                  └─────────┬──────────┘
                            │
        ┌───────────────────┼─────────────────────┐
        │                   │                     │
┌───────▼───────┐  ┌────────▼────────┐  ┌─────────▼────────┐
│ PostgreSQL    │  │  Redis          │  │  Object storage  │
│ (Supabase /   │  │  (cache, queue, │  │  Cloudflare R2   │
│  self-hosted) │  │   rate limit)   │  │  (photos)        │
└───────────────┘  └─────────────────┘  └──────────────────┘
                            │
                  ┌─────────▼──────────┐
                  │  ML Inference      │
                  │  TensorFlow Serving│
                  │  (per-crop models) │
                  └─────────┬──────────┘
                            │
                  ┌─────────▼──────────┐
                  │  Model registry    │
                  │  (S3-compatible    │
                  │   + manifest)      │
                  └────────────────────┘
```

### 2.2 Request Lifecycle Example

A farmer in Bafoussam sends a cassava leaf photo via WhatsApp:

1. 360dialog (WhatsApp BSP) posts a webhook to `POST /webhooks/whatsapp`.
2. The WhatsApp adapter normalizes the payload into a `DiagnosisRequest{crop, image_ref, user_id, channel}`.
3. The backend uploads the image to Cloudflare R2 and stores a reference in PostgreSQL.
4. The backend calls the cassava inference endpoint on the ML service over gRPC.
5. The ML service returns `{predictions: [...], confidence: 0.84, top_class: "cassava_mosaic"}`.
6. The backend applies confidence calibration, selects the matching advice template (FR or EN), and assembles the reply.
7. The backend logs the interaction (anonymized) in PostgreSQL.
8. The backend returns the reply to the WhatsApp adapter, which posts it back to the farmer via 360dialog.

The same backend endpoint is hit by the React Native app and the Next.js web app — only the adapter layer differs.

### 2.3 Repository Layout

A single monorepo for the MVP, split into per-service packages. We can break it apart later if any one piece outgrows it.

```
crop-doctor/
├── apps/
│   ├── mobile/             # React Native (Expo)
│   ├── web/                # Next.js (admin + landing)
│   └── bots/               # WhatsApp + Telegram adapters
├── services/
│   ├── api/                # FastAPI backend
│   └── ml/                 # Inference service + training pipeline
├── packages/
│   ├── shared-types/       # TypeScript types generated from OpenAPI
│   ├── advice-templates/   # Per-crop FR/EN templates (JSON)
│   └── i18n/               # Shared translation files
├── infra/
│   ├── docker/             # Dockerfiles, docker-compose
│   ├── caddy/              # Reverse proxy config
│   └── github-actions/     # CI workflows
├── data/
│   ├── manifests/          # Dataset version manifests (CSV in git)
│   └── notebooks/          # Exploratory training notebooks
└── docs/                   # PROJECT_SPEC.md, PARTNERSHIPS.md, TECH_STACK.md, etc.
```

---

## 3. Client Stack

### 3.1 Mobile App — React Native + Expo

- **Language:** TypeScript.
- **Framework:** React Native via Expo (managed workflow at MVP; eject only if a native module forces it).
- **State management:** React Query (TanStack Query) for server state; Zustand for local UI state. No Redux at MVP.
- **Camera & image picker:** `expo-camera`, `expo-image-picker`.
- **Offline storage:** `expo-sqlite` for cached diagnoses and pending uploads.
- **On-device inference (v2):** `react-native-fast-tflite` for TFLite model execution.
- **Push notifications:** `expo-notifications` (e.g., for "your diagnosis was reviewed by an extension worker").
- **i18n:** `i18next` with shared translation files.
- **Distribution:** Expo EAS Build for Android APK / AAB; Google Play Store; sideload-friendly APK for areas where the Play Store is not used.

**Why React Native over Flutter:**

- Shares language (TypeScript) and ecosystem with the Next.js web app.
- Larger pool of African developers familiar with JS/React.
- Expo materially reduces native-build complexity for a small team.
- Flutter is technically excellent but doesn't give enough advantage to justify a second language and a second hiring pool.

**Why not native Android only:**

- iOS coverage is nearly free with React Native; closes off zero options.
- Some extension workers, NGOs, and partner staff use iOS.

### 3.2 Web App — Next.js

- **Language:** TypeScript.
- **Framework:** Next.js 14+ (App Router, React Server Components where they help).
- **Styling:** Tailwind CSS.
- **Component library:** shadcn/ui (Radix-based, copy-into-repo so we can adapt freely).
- **Forms:** React Hook Form + Zod for validation.
- **Data fetching:** React Query against the FastAPI OpenAPI client.
- **Auth:** Clerk (extension workers, admins, project team) — see §6.
- **Charts (admin dashboard):** Recharts or Visx.
- **Maps (regional dashboards, v2):** MapLibre GL JS with OpenStreetMap tiles (free, no Google Maps lock-in).
- **i18n:** `next-intl` consuming the same translation JSON files as mobile.
- **Hosting:** Vercel free tier at MVP; self-host on the VPS (Caddy + Node) if cost becomes an issue at scale.

**What the web app does:**

- Public landing / about / partner pages.
- Farmer-facing web diagnosis (upload a photo from a browser).
- **Admin dashboard** for extension workers and project team: interaction logs, escalation queue, advice template management, per-region pilot metrics, dataset upload UI.
- **Labeling UI** (or embedded Label Studio) for partner students to label collected images.

### 3.3 WhatsApp & Telegram Bots — Python Adapters

Both bots are thin Python adapters living inside the FastAPI app (separate routers, shared diagnosis logic). They do not duplicate any disease logic.

- **WhatsApp:** 360dialog (Meta Business Solution Provider). Cheaper than Twilio for African volume; cleaner WhatsApp Business API docs.
  - Fallback option: Twilio if 360dialog onboarding stalls.
  - Direct Meta Cloud API as a v2 option once volume justifies it.
- **Telegram:** Official Bot API via `python-telegram-bot` library. Free, no provider needed.
- **Message normalization:** Each adapter converts platform-specific webhook payloads into a `DiagnosisRequest` Pydantic model and forwards to the same internal service used by mobile/web.
- **Reply formatting:** Each adapter formats the normalized `DiagnosisReply` for its platform (WhatsApp's markdown, Telegram's MarkdownV2, mobile/web's JSON).

**Why two chat platforms:**

- WhatsApp is the dominant channel in Cameroon for farmers and cooperatives.
- Telegram is useful for tech-savvy users, partner staff, and as a fallback if WhatsApp Business API onboarding takes time.
- Both are trivial to support once the normalization layer exists.

---

## 4. Backend Stack

### 4.1 API Service — FastAPI

- **Language:** Python 3.11+.
- **Framework:** FastAPI.
- **Schemas:** Pydantic v2 for all request/response shapes.
- **OpenAPI:** Auto-generated; consumed by mobile and web via `openapi-typescript` to produce typed clients.
- **DB driver:** SQLAlchemy 2.x + Alembic for migrations.
- **Async:** Async endpoints throughout; sync only where a library forces it (e.g., some image libs).
- **Background jobs:** ARQ (async Redis queue) — fits the async FastAPI codebase; already wired into the boilerplate. RQ was considered but ARQ is a better fit since workers share the same async event loop as the API.
- **Validation:** Pydantic everywhere; centralized error responses.
- **Tests:** `pytest` + `httpx` AsyncClient for integration tests.
- **Linting/formatting:** `ruff` + `black` + `mypy` (strict on new modules, lenient on legacy).

**Why FastAPI over Node/NestJS:**

- ML code is Python. Calling the model from the API without crossing a language boundary keeps the system simple.
- Pydantic + OpenAPI is the cleanest way to expose a typed contract to TS clients.
- The team will be reading ML code anyway — keeping the API in the same language reduces cognitive load.

### 4.2 ML Inference Service — TensorFlow Serving

- **Trained models:** TensorFlow / Keras → exported as SavedModel.
- **Server:** TensorFlow Serving in a separate Docker container.
- **Protocol:** REST from FastAPI at MVP (httpx to TF Serving REST endpoint). gRPC deferred to post-MVP — adds protobuf tooling complexity with no measurable benefit at current scale.
- **Per-crop models:** Loaded as separate model versions in TF Serving; backend routes by crop.
- **Calibration layer:** Temperature scaling applied inside the API before returning confidence to clients (kept out of the model artifact so we can retune without retraining).
- **OOD detection:** Auxiliary "not a leaf / not a pod" classifier per crop where useful; or softmax-entropy threshold for v1 simplicity.
- **Alternative:** BentoML if we want Python-native serving with built-in batching and easier metrics. Decision deferred until we have benchmark numbers.

### 4.3 Database — PostgreSQL

- **Hosted:** Supabase (free tier) at MVP, or Neon. Self-host on the VPS once we know our patterns.
- **Schemas (initial):**
  - `users` — extension workers, admins (farmers identified by phone/chat ID, no row required).
  - `interactions` — every diagnosis call: channel, crop, predicted class, confidence, advice version, expert escalation flag.
  - `farmers` — opt-in record per phone number, consent flags, region.
  - `advice_templates` — versioned, per (crop, class, language).
  - `extension_workers` — directory for escalation routing.
  - `model_versions` — registry of deployed models per crop with metrics.
  - `dataset_manifests` — pointers to dataset versions in object storage.
- **Migrations:** Alembic, every change reviewed.
- **Backups:** Daily automated backups; weekly off-site copy.

### 4.4 Object Storage — Cloudflare R2

- **Why R2:** S3-compatible API, **zero egress fees** (huge as we retrain on accumulated photos), EU/global edge locations with reasonable latency to Cameroon.
- **Alternatives:** Backblaze B2 (similar pricing, slightly less integrated); AWS S3 (expensive egress, rule out for this workload).
- **Buckets:**
  - `cropdoctor-photos-raw` — incoming photos.
  - `cropdoctor-photos-curated` — labeled and accepted into training sets.
  - `cropdoctor-models` — exported SavedModels by version.
  - `cropdoctor-backups` — DB and config backups.
- **Encryption:** Server-side encryption at rest enabled on all buckets.
- **Retention:** Raw photos default 90 days; deletion automated unless farmer opts in.

### 4.5 Cache, Queue, Rate Limiting — Redis

- One Redis instance covers:
  - Rate limiting (per phone number, per IP).
  - Short-term cache (recent diagnoses, dedup).
  - Background job queue via ARQ.
  - Bot conversation state (per channel_id state machine) — initially in-process dict, Redis-backed for multi-instance deployments.
- Hosted: Upstash (free tier) or self-hosted on the VPS.

### 4.6 Reverse Proxy — Caddy

- Automatic HTTPS via Let's Encrypt.
- Simpler config than nginx.
- Fronts FastAPI, the Next.js web app (if self-hosted), and the admin dashboard.

---

## 5. ML Stack

### 5.1 Training

- **Framework:** TensorFlow / Keras (chosen for TF Serving and TFLite compatibility).
- **Notebook environment:** Google Colab Pro for the first models (free GPU, low friction). Migrate to rented GPU (Lambda Labs, RunPod, or Vast.ai) when training runs get longer than a Colab session.
- **Architectures:** MobileNetV3-Large and EfficientNet-Lite-B0 as the two candidate backbones. Per-crop classifier heads on top.
- **Data augmentation:** `albumentations` (richer than Keras built-ins).
- **Confidence calibration:** Temperature scaling on the held-out field-test set.
- **Experiment tracking:** Weights & Biases (free tier covers solo / small team), or MLflow self-hosted if we want everything on-prem.
- **Dataset versioning:** DVC or a manifest CSV in git pointing into R2. v1 starts with the manifest CSV (simpler); upgrade to DVC if it becomes the bottleneck.
- **Reproducibility:** Every training run logs `(dataset_version, code_commit, hyperparams, metrics, model_artifact_path)`.

### 5.2 Labeling

- **Tool:** Label Studio (open source, self-hosted on the VPS or run locally by partner students).
- **Schema per image:** `(crop, class, severity_v2, photographer_id, gps, region, date, notes)`.
- **Multi-labeler workflow:** Each image labeled by ≥2 labelers. Disagreements flagged to the domain expert for adjudication.
- **Web UI alternative:** A custom Next.js labeling page if Label Studio is too heavy for student labelers. Decision deferred.

### 5.3 Evaluation

- Honest **field-test set** per crop — photos collected from fields and photographers not seen in training.
- Metrics: top-1 accuracy, per-class recall, expected calibration error (ECE), confusion matrix.
- Severity-weighted error metric (v2) — missing a severe disease costs more than missing healthy.
- Automated evaluation runs on every model candidate before deployment.

### 5.4 Model Deployment Pipeline

1. Training run produces a SavedModel artifact.
2. CI evaluates against the locked field-test set.
3. If metrics pass thresholds, the model is uploaded to the R2 model bucket.
4. A `model_versions` row is created in Postgres.
5. TF Serving is signaled to load the new model version (canary at first, then promoted).
6. Backend's per-crop routing config is updated to use the new version.
7. Rollback = point routing back to the previous version (zero-downtime).

---

## 6. Identity, Auth, and Access

- **Farmers:** Identified by phone number (WhatsApp / Telegram chat ID) or anonymous web/mobile session. No account required.
- **Extension workers & admins:** Authenticated via the FastAPI backend's own JWT auth — email + password, cookie-based sessions. Role-based access enforced via a `role` column on the `users` table: `admin`, `agronomist`, `extension_worker`, `labeler`. No external auth provider (Clerk was evaluated and rejected — the template's built-in auth covers all internal user needs without the external dependency or US-hosted data concern).
- **API keys:** Per-bot service-to-service auth via signed JWTs; webhook signatures verified for WhatsApp (HMAC-SHA256 on D360-Signature header) and Telegram (X-Telegram-Bot-Api-Secret-Token header).
- **Consent flow:** First-contact message in the bot explains data use; farmer must reply "yes" to opt in for photo retention beyond 90 days. In the mobile app, a `ConsentScreen` is shown on first launch and the decision is stored locally via MMKV.

---

## 7. Internationalization & Content

- **Library:** `i18next` on mobile (React Native binding). `next-intl` for web is deferred — the admin dashboard is internal and FR/EN switching is not MVP-critical for that audience.
- **Translation file format:** Flat JSON per language, one file per app (`en.json`, `fr.json`), namespaced by key prefix (`diagnosis.*`, `crops.*`, `settings.*`, etc.).
- **Languages at MVP:** French (`fr`), English (`en`).
- **Languages at v2:** Pidgin (`pcm`), Fulfulde (`ff`), Ewondo (`ewo`), Duala (`dua`), Bassa (`bas`).
- **Review workflow:** Every advice template change goes through a native speaker + a pathologist before deployment. PR template enforces this checkbox.

---

## 8. DevOps & Infrastructure

### 8.1 Local Development

- **Containerization:** Docker + Docker Compose. `docker compose up` spins the entire stack (API, ML, Postgres, Redis, Caddy, Label Studio) on a developer laptop.
- **Seed data:** Sample images and a tiny test model in the repo for end-to-end local runs.
- **Pre-commit hooks:** `ruff`, `black`, `mypy`, `eslint`, `prettier`.

### 8.2 CI/CD

- **Provider:** GitHub Actions.
- **Pipelines:**
  - **Lint + typecheck** on every PR.
  - **Unit + integration tests** on every PR.
  - **Build Docker images** on merge to `main`, tagged with commit SHA.
  - **Deploy to staging VPS** automatically.
  - **Deploy to production** on manual approval (button in the GitHub Actions UI).
  - **ML eval pipeline** runs on every model PR — compares new candidate to current production on the locked field-test set.

### 8.3 Hosting Topology

- **MVP:**
  - One Hetzner CX22 or OVH equivalent VPS (~€5–10/month) hosting FastAPI, TF Serving, Postgres (if not Supabase), Redis (if not Upstash), Caddy, Label Studio.
  - Web app on Vercel free tier.
  - Object storage on Cloudflare R2.
- **Scale-up (post-pilot):**
  - Separate VPS or managed Postgres (Supabase Pro / Neon paid tier).
  - Dedicated VPS for TF Serving with more CPU (and a GPU if inference latency demands it).
  - Optional: managed Kubernetes (DigitalOcean Kubernetes — cheapest reasonable option) once we run more than 3 services.

### 8.4 Domains & Networking

- One root domain (e.g., `cropdoctor.cm` if available, or a `.org` equivalent).
- Subdomains: `api.`, `admin.`, `bot.`, `labeling.`, `staging.`.
- All HTTPS via Caddy + Let's Encrypt.

---

## 9. Observability

- **Errors:** Sentry across mobile, web, and backend. Free tier covers MVP.
- **Product analytics:** PostHog (self-hosted option available, privacy-respecting). Tracks anonymized funnel: photo sent → diagnosis returned → advice viewed → escalation requested.
- **Backend metrics:** Prometheus + Grafana on the VPS once traffic justifies it (not at MVP). Initially just structured logs.
- **Uptime monitoring:** UptimeRobot free tier on the public endpoints.
- **Log storage:** Application logs to stdout, collected by a Loki instance or shipped to a hosted service (Better Stack, Grafana Cloud free tier).

---

## 10. Security & Privacy

- **Transport:** HTTPS-only. HSTS enabled.
- **At rest:** Postgres encryption (managed providers handle this); R2 server-side encryption enabled.
- **Secrets:** `.env` files in dev; GitHub Actions secrets in CI; `doppler` or `sops` if secret sprawl gets bad.
- **PII minimization:** No farmer names stored; phone numbers hashed where used as identifiers in analytics tables.
- **Data retention:** Photos default-deleted at 90 days. Farmer can revoke consent at any time via a `STOP` command in the bot.
- **Access control:** Admin dashboard locked behind own JWT auth + role check (`admin`, `agronomist`, `extension_worker`, `labeler`). All admin actions audit-logged.
- **Cameroon data protection:** Compliance with ANTIC guidelines reviewed before scale.
- **Penetration / dependency scanning:** GitHub Dependabot enabled; `pip-audit` and `npm audit` in CI.

---

## 11. Cost Estimate (MVP, Monthly)

Rough order-of-magnitude, USD. Real costs depend heavily on usage.

| Item                                                   | Cost                        |
| ------------------------------------------------------ | --------------------------- |
| VPS (Hetzner CX22)                                     | ~$5                         |
| Cloudflare R2 (first ~10 GB free)                      | $0–5                        |
| PostgreSQL (Supabase free)                             | $0                          |
| Redis (Upstash free)                                   | $0                          |
| Vercel (web, free tier)                                | $0                          |
| Sentry (free tier)                                     | $0                          |
| Twilio / 360dialog WhatsApp (per-conversation pricing) | $20–100 depending on volume |
| Telegram                                               | $0                          |
| Domain                                                 | $1–2                        |
| Colab Pro (training, intermittent)                     | ~$10                        |
| **Total**                                              | **~$40–125 / month**        |

This is realistic for a self-funded MVP. Scale to thousands of farmers and the WhatsApp line dominates.

---

## 12. Technology Decision Log

A short log of the key choices and what we'd reconsider:

| Decision                        | Choice                        | What would change our mind                                                                                         |
| ------------------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Mobile framework                | React Native (Expo)           | If we need deep native camera/ML integration before v2 and Flutter's tooling proves materially better              |
| Web framework                   | Next.js                       | If we want to avoid Vercel lock-in entirely from day one (then SvelteKit or Remix)                                 |
| Backend language                | Python (FastAPI)              | Never — ML is Python; co-locating is the right call                                                                |
| WhatsApp provider               | 360dialog                     | If onboarding stalls, switch to Twilio                                                                             |
| ML framework                    | TensorFlow                    | If a critical SOTA paper we want to use is PyTorch-only and conversion is painful — switch to PyTorch + TorchServe |
| Inference server                | TF Serving                    | If batching, observability, or Python custom logic in serving becomes important — BentoML                          |
| Database                        | PostgreSQL                    | Never for the MVP. Maybe add a vector DB in v2 if we add RAG to advice generation                                  |
| Object storage                  | Cloudflare R2                 | Only if R2 has reliability issues — fall back to Backblaze B2                                                      |
| Auth                            | Own JWT (FastAPI boilerplate) | If we need social login or SSO for external partners — add Supabase Auth or self-hosted Authentik                  |
| Bot background jobs             | ARQ                           | If job patterns become complex and Celery's retry/scheduling features are needed                                   |
| ML serving protocol             | REST (TF Serving)             | Switch to gRPC when inference latency becomes measurable at scale                                                  |
| Advice template source of truth | DB (canonical)                | JSON files in packages/ are reference/seed only; edits go through the admin UI                                     |
| Bot deployment                  | Separate `apps/bots/` package | Merge back into FastAPI sub-routers if ops complexity outweighs independence benefit                               |
| Hosting                         | Single VPS (Hetzner)          | Move to managed K8s once >3 services or >1 region                                                                  |
| Monorepo                        | Single repo with packages     | Split out the mobile or ML repo if build times become painful                                                      |

---

## 13. What We Are Explicitly _Not_ Building (Yet)

To keep the MVP achievable, the stack deliberately omits:

- Microservices beyond `api` + `ml`. No service mesh, no event bus.
- GraphQL — REST + OpenAPI is enough.
- Kubernetes at MVP — a single VPS is cheaper and simpler.
- Firebase / Firestore — vendor lock-in, expensive at scale.
- A custom ML serving framework — TF Serving or BentoML suffices.
- An LLM in the inference path at MVP — templated advice only.
- A vector database — no RAG until we have a curated knowledge base worth retrieving against.
- Native Android-only or iOS-only apps — React Native covers both.
- A custom admin UI from scratch — shadcn/ui + Retool fill the gap until volume justifies more.

These are deferred to v2 and revisited only when concrete pressure justifies the added complexity.

---

## 14. Open Questions

**Decided during scaffolding (no longer open):**

- ~~Auth for web/mobile~~ → Own JWT, no Clerk.
- ~~Background job queue~~ → ARQ.
- ~~Advice template source of truth~~ → DB canonical; JSON files are seed/reference only.
- ~~ML serving protocol~~ → REST at MVP; gRPC post-MVP.
- ~~Bot deployment model~~ → Separate `apps/bots/` package.

**Still open:**

1. **WhatsApp BSP** — 360dialog or Twilio? Pricing scales differently; need real volume estimate before locking in.
2. **Self-hosted vs. managed Postgres** — Supabase free tier is great for MVP, but for sovereignty/data-residency reasons should we self-host from day one?
3. **Hosting region** — EU (Hetzner) vs. closer-to-Africa (AWS Cape Town, OVH Senegal)? Latency vs. cost vs. data-sovereignty tradeoff.
4. **Labeling UI** — Label Studio (powerful, heavy) vs. custom Next.js page (lightweight, more dev work)?
5. **Experiment tracking** — Weights & Biases hosted vs. self-hosted MLflow?
6. **Telegram parity** — full feature parity with WhatsApp from day one, or Telegram as a "lite" channel?
7. **Mobile-first vs. WhatsApp-first launch** — both are in scope, but which gets the first 100 users? Probably WhatsApp; confirm.
8. **Open-source license** — when (not if) we open-source the codebase and dataset, which license? Apache 2.0 for code, CC-BY-NC for dataset are reasonable starting points.

---

## 15. Stack Summary (One-Page Cheat Sheet)

| Layer          | Choice                                                                              |
| -------------- | ----------------------------------------------------------------------------------- |
| Mobile         | React Native + Expo, TypeScript                                                     |
| Web            | Next.js 14 (App Router), TypeScript, Tailwind, shadcn/ui                            |
| Chat bots      | Python adapters for WhatsApp (360dialog) and Telegram (Bot API)                     |
| Backend API    | FastAPI, Pydantic, SQLAlchemy, Alembic                                              |
| ML serving     | TensorFlow Serving (REST at MVP, gRPC post-MVP), separate container                 |
| ML training    | TensorFlow / Keras, Colab Pro → Lambda Labs, Weights & Biases                       |
| Labeling       | Label Studio (self-hosted)                                                          |
| Database       | PostgreSQL (Supabase free → self-hosted)                                            |
| Cache / queue  | Redis (Upstash → self-hosted) + ARQ                                                 |
| Object storage | Cloudflare R2                                                                       |
| Auth           | Own JWT (FastAPI boilerplate) — roles: admin, agronomist, extension_worker, labeler |
| Reverse proxy  | Caddy (auto HTTPS)                                                                  |
| Containers     | Docker + Docker Compose; Kubernetes only post-MVP                                   |
| CI/CD          | GitHub Actions                                                                      |
| Hosting        | Hetzner VPS + Vercel + Cloudflare R2                                                |
| Observability  | Sentry + PostHog + UptimeRobot; Prometheus/Grafana later                            |
| i18n           | i18next + next-intl, shared JSON files                                              |
| Repo           | Monorepo (apps/, services/, packages/, infra/, data/, docs/)                        |
