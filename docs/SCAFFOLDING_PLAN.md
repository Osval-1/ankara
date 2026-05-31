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
- [x] `Crop` enum: cassava | maize | plantain | tomato | cocoa
- [x] `CropClass` enum: all 25 classes across 5 crops (5 per crop)
- [x] `Channel` enum: whatsapp | telegram | mobile | web
- [x] `Language` enum: fr | en
- [x] `ConfidenceLevel` enum: low | medium | high
- [x] `Interaction` model — every diagnosis call logged
- [x] `Farmer` model — opt-in record per phone/chat ID
- [x] `AdviceTemplate` model — versioned per (crop, class, language)
- [x] `ExtensionWorker` model — escalation directory
- [x] `ModelVersion` model — ML model registry

#### Schemas (Pydantic v2)
- [x] `DiagnosisRequest` / `DiagnosisReply`
- [x] `InteractionCreate` / `InteractionRead`
- [x] `FarmerCreate` / `FarmerRead`
- [x] `AdviceTemplateRead` / `AdviceTemplateUpdate`
- [x] `ExtensionWorkerRead`
- [x] `ModelVersionRead`

#### Services / business logic
- [x] `DiagnosisService` — stub (raises NotImplementedError; full flow to be implemented)
- [x] `R2Client` — stub interface
- [x] `MLClient` — stub (REST to TF Serving; gRPC deferred to post-MVP)
- [x] `ConfidenceCalibrator` — temperature scaling with per-crop config dict
- [x] `ConsentService` — stub interface

#### Endpoints (routers)
- [x] `POST /api/v1/diagnosis` — stub
- [x] `POST /api/v1/webhooks/whatsapp` — stub
- [x] `POST /api/v1/webhooks/telegram` — stub
- [x] `GET  /api/v1/interactions` — stub
- [x] `GET  /api/v1/advice-templates` — stub
- [x] `PUT  /api/v1/advice-templates/{id}` — stub
- [x] `GET  /api/v1/extension-workers` — stub
- [x] `GET  /api/v1/model-versions` — stub

#### Background jobs (ARQ)
- [x] `process_diagnosis_image` — stub
- [x] `delete_expired_photos` — stub

#### Alembic migrations
- [x] `0001_crop_doctor_domain.py` — all new models + enums

---

### `apps/web` — Next.js domain layer

**Why:** Custom cookie auth must be replaced with Clerk; i18n must be added;
admin dashboard needs real Crop Doctor pages; API client must point at FastAPI.

#### Auth
- [x] Keep template's own JWT auth (no Clerk). Role field added to `types/api.ts` as `admin | agronomist | extension_worker | labeler`
- [x] `lib/authorization.ts` updated with Crop Doctor role checks

#### i18n
- [ ] Install `next-intl` (deferred — admin UI is internal, FR/EN switcher not MVP-critical)

#### API client
- [x] `types/api.ts` updated with all Crop Doctor domain types
- [x] `config/paths.ts` updated with all Crop Doctor routes
- [ ] Generate typed client from FastAPI OpenAPI spec via `openapi-typescript` (deferred — manual types sufficient at scaffold)

#### Pages / features
- [x] Discussions feature deleted
- [x] `/app/diagnose` — crop select + photo upload + result display
- [x] `/app/interactions` — interaction log table
- [x] `/app/escalations` — escalated (low-confidence) interactions
- [x] `/app/advice-templates` — list + activate/deactivate
- [x] `/app/extension-workers` — directory table
- [x] `/app/model-versions` — model registry table
- [x] Dashboard nav updated with all new routes

---

### `apps/mobile` — Expo domain layer

**Why:** Camera and image picker are missing; the diagnosis flow doesn't exist;
Arabic must be swapped for French; the API client points at a dummy URL.

#### Dependencies to add
- [ ] `expo-camera`
- [ ] `expo-image-picker`
- [ ] `expo-sqlite` (offline cache)

#### i18n
- [x] `ar.json` → `fr.json`; i18n config updated to load `fr` instead of `ar`
- [x] FR and EN translation files updated with diagnosis, crops, history, consent namespaces
- [x] RTL forced off (no Arabic)

#### API client
- [x] `lib/api/client.tsx` points at `EXPO_PUBLIC_API_URL` (FastAPI)
- [x] `features/diagnosis/api.ts` — multipart POST /diagnosis typed with DiagnosisReply

#### Features / screens added
- [x] `features/diagnosis/scan-screen.tsx` — crop selector + camera/picker + run diagnosis
- [x] `features/diagnosis/result-card.tsx` — result display with confidence colour + escalation warning
- [x] `features/diagnosis/use-diagnosis-store.ts` — Zustand + MMKV persistence (offline history)
- [x] `features/history/history-screen.tsx` — past diagnoses from local store
- [x] `features/consent/consent-screen.tsx` — first-contact data use consent
- [x] Tab nav updated: Home → Scan → History → Settings
- [x] Feed feature deleted

#### Auth
- [x] Zustand token store kept for farmer anonymous sessions (no Clerk)

#### Offline
- [x] Diagnosis records persisted via Zustand + MMKV (simpler than SQLite at scaffold; upgrade path open)
- [ ] Queue pending uploads when offline; sync on reconnect (deferred to post-MVP)

---

### `apps/bots/` — WhatsApp + Telegram adapters

**Why:** Not yet scaffolded. WhatsApp is the primary MVP channel per spec §4.1.

- [x] Create `apps/bots/` Python package
- [x] WhatsApp adapter (360dialog): webhook → state machine → API → format reply
- [x] Telegram adapter: Bot API → state machine → API → format reply
- [x] Message state machine: greeting → awaiting_crop → awaiting_photo → awaiting_consent → idle
- [x] 360dialog signature verification (HMAC-SHA256 on D360-Signature header)
- [x] Reply formatter: WhatsApp `*bold*` vs Telegram MarkdownV2 `**bold**`

---

### `services/ml/` — ML inference + training pipeline

**Why:** TF Serving needs a model config and a placeholder model to boot;
training pipeline needs structure for reproducibility.

- [x] `models/models.config` — TF Serving multi-model config (cassava entry; add per crop as they roll out)
- [x] `models/cassava/1/` — placeholder SavedModel directory (variables/ stubs + generate_placeholder_model.py script)
- [x] `training/train.py` — stub
- [x] `training/evaluate.py` — stub
- [x] `training/calibrate.py` — stub
- [x] `training/export.py` — stub
- [x] `pyproject.toml` for training dependencies
- [x] `Dockerfile` for TF Serving container

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
