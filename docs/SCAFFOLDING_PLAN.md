# Crop Doctor — Scaffolding Plan

**Status:** Monorepo scaffold complete. Templates copied and cleaned. Ready for domain modifications.
**Last updated:** 2026-05-31

---

## What is done

### Monorepo root (`crop-doctor/`)
- [x] Git initialized, `main` branch set
- [x] `package.json` (pnpm workspaces: apps/web, apps/mobile, packages/*)
- [x] `.gitignore` (Node, Python, Expo, ML artifacts)
- [x] `.env.example` (all env vars for all services)
- [x] `CLAUDE.md` (monorepo orientation for future sessions)

### `apps/web` — Next.js 14 (bulletproof-react base)
- [x] Template copied, `.git` and README/LICENSE removed
- [x] All template branding replaced (Bulletproof React → Crop Doctor)
- [x] Package name: `@crop-doctor/web`
- [x] Cookie name: `crop_doctor_auth_token`
- [x] App metadata, titles, homepage updated

### `apps/mobile` — Expo React Native (obytes base)
- [x] Template copied (including `.npmrc`, `.github/` workflows), `.git`/README/LICENSE/claude.md removed
- [x] All template branding replaced (obytes/ObytesApp → Crop Doctor)
- [x] Package name: `@crop-doctor/mobile`
- [x] Bundle IDs: `cm.cropdoctor.*`
- [x] App scheme: `cropDoctor`
- [x] EAS account owner + project ID cleared (placeholders — set before first build)
- [x] Expo slug: `crop-doctor`
- [x] Translations: `en.json` onboarding message updated; `ar.json` onboarding message updated
- [x] Onboarding screen: Crop Doctor copy
- [x] Maestro YAML e2e tests: assertions updated

### `services/api` — FastAPI (FastAPI-boilerplate base)
- [x] Template copied, `.git`/README/LICENSE/CONTRIBUTING/docs removed
- [x] All template branding replaced (fastapi-boilerplate/Benav Labs → Crop Doctor)
- [x] `pyproject.toml`: name `crop-doctor-api`, author Crop Doctor Team
- [x] `config.py`: default `APP_NAME = "Cameroon Crop Doctor"`
- [x] All 3 `.env.example` files updated
- [x] Demo files deleted: posts, tasks, tiers, rate_limits (endpoints + models + schemas + crud)
- [x] Router `__init__.py`: only health/login/logout/users remain; placeholder stubs added
- [x] Worker `functions.py`: sample task removed, placeholder comments added
- [x] Worker `settings.py`: `functions = []` with comment

### `packages/`
- [x] `advice-templates/cassava/en.json` — all 5 classes (healthy, CMD, CBSD, pest, unknown)
- [x] `advice-templates/cassava/fr.json` — same in French
- [x] `i18n/en.json` — shared UI strings (common, diagnosis, nav)
- [x] `i18n/fr.json` — same in French
- [x] `shared-types/index.ts` — TypeScript types: Crop, CropClass, ConfidenceLevel, DiagnosisRequest, DiagnosisReply

### `infra/`
- [x] `docker/docker-compose.yml` — db, redis, api, worker, ml (TF Serving), web, labelstudio
- [x] `caddy/Caddyfile` — reverse proxy for api, admin, labeling, staging subdomains
- [x] `github-actions/ci.yml` — lint + test + typecheck for all three services

### `docs/`
- [x] `PROJECT_SPEC.md` copied in
- [x] `TECH_STACK.md` copied in
- [x] `PARTNERSHIPS.md` copied in
- [x] `SCAFFOLDING_PLAN.md` (this file)

---

## What is NOT yet done — domain modifications needed

### Repo structure constraint
Each service is self-contained: its own `package.json`/`pyproject.toml`, lockfile, and Dockerfile.
Shared packages (`advice-templates`, `i18n`, `shared-types`) will become publishable npm packages
when/if the monorepo is split into separate repos.

---

### `services/api` — domain layer

**Why:** The template has the engine (async DB, JWT, Redis, ARQ) but no Crop Doctor domain.
Every other service calls this API — it must be built first.

#### Models (SQLAlchemy 2.x async)
- [ ] `Crop` enum: cassava | maize | plantain | tomato | cocoa
- [ ] `CropClass` enum: all 25 classes across 5 crops (5 per crop)
- [ ] `Channel` enum: whatsapp | telegram | mobile | web
- [ ] `Language` enum: fr | en
- [ ] `ConfidenceLevel` enum: low | medium | high
- [ ] `Interaction` model — every diagnosis call logged:
  - `id`, `created_at`, `channel`, `crop`, `predicted_class`, `confidence_raw` (float, private),
    `confidence_level` (low/med/high, public), `advice_template_version`, `image_ref`,
    `farmer_id` (FK, nullable), `region`, `escalated` (bool), `model_version_id` (FK)
- [ ] `Farmer` model — opt-in record per phone/chat ID:
  - `id`, `channel_id` (hashed phone/chat ID), `channel`, `region`, `language`,
    `consent_given_at`, `retain_photos` (bool), `created_at`
- [ ] `AdviceTemplate` model — versioned per (crop, class, language):
  - `id`, `crop`, `crop_class`, `language`, `version`, `label`, `opening`,
    `steps` (JSON array), `consult_message`, `reviewed_by`, `reviewed_at`, `is_active`
- [ ] `ExtensionWorker` model — escalation directory:
  - `id`, `name`, `region`, `phone`, `whatsapp_available` (bool), `crops` (array), `active`
- [ ] `ModelVersion` model — ML model registry:
  - `id`, `crop`, `version`, `dataset_version`, `code_commit`, `accuracy`, `ece`,
    `artifact_path` (R2 key), `deployed_at`, `is_active`

#### Schemas (Pydantic v2)
- [ ] `DiagnosisRequest` — crop, image_ref, user_id, channel, language
- [ ] `DiagnosisReply` — crop, predicted_class, confidence (low/med/high), label, opening,
      steps, consult_message, escalate, advice_template_version
- [ ] `InteractionCreate` / `InteractionRead`
- [ ] `FarmerCreate` / `FarmerRead`
- [ ] `AdviceTemplateRead` / `AdviceTemplateUpdate`
- [ ] `ExtensionWorkerRead`
- [ ] `ModelVersionRead`

#### Services / business logic
- [ ] `DiagnosisService` — orchestrates the full flow:
  1. Upload image to Cloudflare R2
  2. Call ML inference service (gRPC to TF Serving)
  3. Apply confidence calibration (raw softmax → low/med/high)
  4. Load matching `AdviceTemplate` from DB
  5. Log `Interaction` to DB
  6. Return `DiagnosisReply`
- [ ] `R2Client` — boto3/httpx wrapper for Cloudflare R2:
  - `upload_photo(image_bytes, farmer_id, crop)` → key
  - `delete_photo(key)`
  - `schedule_deletion(key, days=90)` (via ARQ job)
- [ ] `MLClient` — gRPC client to TF Serving:
  - `predict(crop, image_bytes)` → `{class, raw_confidence}`
- [ ] `ConfidenceCalibrator` — temperature scaling:
  - `calibrate(raw_softmax, crop)` → `ConfidenceLevel`
- [ ] `ConsentService` — first-contact consent flow, STOP command handler

#### Endpoints (routers)
- [ ] `POST /api/v1/diagnosis` — main diagnosis endpoint (mobile + web)
- [ ] `POST /api/v1/webhooks/whatsapp` — 360dialog webhook handler
- [ ] `POST /api/v1/webhooks/telegram` — Telegram Bot API webhook
- [ ] `GET  /api/v1/interactions` — admin: paginated interaction log
- [ ] `GET  /api/v1/advice-templates` — list active templates
- [ ] `PUT  /api/v1/advice-templates/{id}` — update template (agronomist role)
- [ ] `GET  /api/v1/extension-workers` — list by region
- [ ] `GET  /api/v1/model-versions` — list deployed models

#### Background jobs (ARQ)
- [ ] `process_diagnosis_image` — async image upload + inference
- [ ] `delete_expired_photos` — cron: delete R2 photos past 90-day retention

#### Alembic migrations
- [ ] Initial migration for all new models

---

### `apps/web` — Next.js domain layer

**Why:** Custom cookie auth must be replaced with Clerk; i18n must be added;
admin dashboard needs real Crop Doctor pages; API client must point at FastAPI.

#### Auth
- [ ] Install `@clerk/nextjs`
- [ ] Replace custom `lib/auth.tsx` + cookie auth with Clerk `<ClerkProvider>` + `useUser()`
- [ ] Protect admin routes with Clerk `auth()` middleware
- [ ] Role-based access: `admin`, `agronomist`, `extension_worker`, `labeler`

#### i18n
- [ ] Install `next-intl`
- [ ] Wire shared `packages/i18n/en.json` + `fr.json` into Next.js
- [ ] Language switcher component (FR / EN)
- [ ] All user-facing strings use translation keys

#### API client
- [ ] Point `NEXT_PUBLIC_API_URL` at FastAPI
- [ ] Generate typed client from FastAPI OpenAPI spec via `openapi-typescript`
- [ ] Import `DiagnosisRequest`, `DiagnosisReply` from `@crop-doctor/shared-types`

#### Pages / features
- [ ] Replace demo `discussions` feature with `diagnosis` feature
- [ ] `/app/diagnose` — web diagnosis page: crop select + photo upload + result display
- [ ] `/app/interactions` — admin: interaction log table (channel, crop, class, confidence, date)
- [ ] `/app/escalations` — admin: flagged low-confidence cases pending expert review
- [ ] `/app/advice-templates` — agronomist: view + edit advice templates with review workflow
- [ ] `/app/extension-workers` — admin: directory management
- [ ] `/app/model-versions` — admin: deployed model registry

---

### `apps/mobile` — Expo domain layer

**Why:** Camera and image picker are missing; the diagnosis flow doesn't exist;
Arabic must be swapped for French; the API client points at a dummy URL.

#### Dependencies to add
- [ ] `expo-camera`
- [ ] `expo-image-picker`
- [ ] `expo-sqlite` (offline cache)

#### i18n
- [ ] Rename `ar.json` → `fr.json`; update i18n config to load `fr` instead of `ar`
- [ ] Wire shared `packages/i18n/fr.json` into the app (or keep mobile-specific keys)
- [ ] Language switcher in settings screen (FR / EN)

#### API client
- [ ] Point `EXPO_PUBLIC_API_URL` at FastAPI backend
- [ ] Import `DiagnosisRequest`, `DiagnosisReply` from `@crop-doctor/shared-types`

#### Features / screens to add
- [ ] `src/features/scan/` — camera + image picker hook, photo preview
- [ ] `src/features/diagnosis/` — crop selector, diagnosis result card, advice display
- [ ] `src/features/history/` — offline-cached past diagnoses (expo-sqlite)
- [ ] Update tab navigation: Home → Scan → History → Settings
- [ ] Consent screen — first-contact: explain data use, opt-in for photo retention
- [ ] Replace demo `feed` feature with crop doctor content

#### Auth
- [ ] Keep Zustand token store for farmer anonymous sessions (no login required for farmers)
- [ ] Add Clerk for extension worker login (separate authenticated tab/section)

#### Offline
- [ ] SQLite schema: `diagnoses(id, crop, class, confidence, advice, created_at, synced)`
- [ ] Queue pending uploads when offline; sync on reconnect

---

### `apps/bots/` — WhatsApp + Telegram adapters

**Why:** Not yet scaffolded. WhatsApp is the primary MVP channel per spec §4.1.

- [ ] Create `apps/bots/` Python package
- [ ] WhatsApp adapter (360dialog): webhook receiver → normalize to `DiagnosisRequest` → call API → format reply
- [ ] Telegram adapter: Bot API → same normalization → same API call → format reply
- [ ] Message state machine: greeting → crop select → photo receive → result send → consent prompt
- [ ] 360dialog signature verification middleware
- [ ] Reply formatter: WhatsApp markdown vs Telegram MarkdownV2

---

### `services/ml/` — ML inference + training pipeline

**Why:** TF Serving needs a model config and a placeholder model to boot;
training pipeline needs structure for reproducibility.

- [ ] `models/models.config` — TF Serving multi-model config (one entry per crop)
- [ ] `models/cassava/1/` — placeholder SavedModel directory (enables TF Serving to start)
- [ ] `training/` — training pipeline stub:
  - `train.py` — data loading, model definition, fine-tuning loop
  - `evaluate.py` — field-test set evaluation (accuracy, ECE, per-class recall)
  - `calibrate.py` — temperature scaling on held-out validation set
  - `export.py` — SavedModel export + upload to R2
- [ ] `requirements.txt` / `pyproject.toml` for training dependencies
- [ ] `Dockerfile` for TF Serving container

---

## Recommended build order

Dependencies flow downward — build in this sequence:

```
1. services/api  (domain models + diagnosis endpoint + R2 + ML client)
        ↓
2. services/ml   (TF Serving config + placeholder model so API can call it)
        ↓
3. apps/bots     (WhatsApp webhook — primary MVP channel)
        ↓
4. apps/web      (admin dashboard + web diagnosis — secondary channel)
        ↓
5. apps/mobile   (farmer mobile app — tertiary channel at MVP, primary post-MVP)
```

Rationale: The API is the single source of truth (TECH_STACK.md §1, principle 1).
Nothing else can be tested end-to-end until the diagnosis endpoint exists.

---

## Repo split readiness

Each service is already split-ready:
- Own `package.json` / `pyproject.toml` and lockfile
- Own `Dockerfile`
- No cross-service code imports (only JSON data shared via `packages/`)
- When splitting: publish `@crop-doctor/shared-types`, `@crop-doctor/i18n`,
  `@crop-doctor/advice-templates` as npm packages, then each service installs them normally.
- Use `git subtree split` to extract history per service if needed.
