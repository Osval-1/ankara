# Ankara — Tech Stack

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
8. **Per-crop swappability.** Adding a new crop should not require touching client code - only adding a model file, advice templates, and a config entry.

---

## 2. Architecture Overview

### 2.1 System Diagram

```text
Mobile app   Web app   WhatsApp / Telegram bots
React Native Next.js   Python adapters
(Expo)       (Vercel)   (FastAPI sub-routes)
         HTTPS / REST (OpenAPI-typed)
      Backend API
      Python FastAPI
      (Caddy in front)
PostgreSQL   Redis           Object storage
(Supabase /  (cache, queue,  Cloudflare R2
 self-hosted) rate limit)    (photos)
      ML Inference
      TensorFlow Serving
      (per-crop models)
      Model registry
      (S3-compatible + manifest)
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

The same backend endpoint is hit by the React Native app and the Next.js web app - only the adapter layer differs.

### 2.3 Repository Layout

A single monorepo for the MVP, split into per-service packages. We can break it apart later if any one piece outgrows it.

```text
ankara/
apps/
  mobile/             # React Native (Expo)
  web/                # Next.js (admin + landing)
  bots/               # WhatsApp + Telegram adapters
services/
  api/                # FastAPI backend
  ml/                 # Inference service + training pipeline
packages/
  shared-types/       # TypeScript types generated from OpenAPI
  advice-templates/   # Per-crop FR/EN templates (JSON)
  i18n/               # Shared translation files
infra/
  docker/             # Dockerfiles, docker-compose
  caddy/              # Reverse proxy config
  github-actions/     # CI workflows
data/
  manifests/          # Dataset version manifests (CSV in git)
  notebooks/          # Exploratory training notebooks
docs/                 # PROJECT_SPEC.md, PARTNERSHIPS.md, TECH_STACK.md, etc.
```

## 3. Client Stack

### 3.1 Mobile App - React Native + Expo

- **Language:** TypeScript.
- **Framework:** React Native via Expo (managed workflow at MVP; eject only if a native module forces it).
- **State management:** React Query (TanStack Query) for server state; Zustand for local UI state. No Redux at MVP.
- **Camera & image picker:** `expo-camera`, `expo-image-picker`.
- **Offline storage:** `expo-sqlite` for cached diagnoses and pending uploads.
- **On-device inference (v2):** `react-native-fast-tflite` for TFLite model execution.
- **Push notifications:** `expo-notifications` (e.g., for "your diagnosis was reviewed by an extension worker").
- **i18n:** `i18next` with shared translation files.
- **Distribution:** Expo EAS Build for Android APK / AAB; Google Play Store; sideload-friendly APK for areas where the Play Store is not used.

### 3.2 Web App - Next.js

- **Language:** TypeScript.
- **Framework:** Next.js 14+ (App Router, React Server Components where they help).
- **Styling:** Tailwind CSS.
- **Component library:** shadcn/ui (Radix-based, copy-into-repo so we can adapt freely).
- **Forms:** React Hook Form + Zod for validation.
- **Data fetching:** React Query against the FastAPI OpenAPI client.
- **Auth:** Clerk (extension workers, admins, project team) - see §6.
- **Charts (admin dashboard):** Recharts or Visx.
- **Maps (regional dashboards, v2):** MapLibre GL JS with OpenStreetMap tiles (free, no Google Maps lock-in).
- **i18n:** `next-intl` consuming the same translation JSON files as mobile.
- **Hosting:** Vercel free tier at MVP; self-host on the VPS (Caddy + Node) if cost becomes an issue at scale.

### 3.3 WhatsApp & Telegram Bots - Python Adapters

Both bots are thin Python adapters living inside the FastAPI app (separate routers, shared diagnosis logic). They do not duplicate any disease logic.

- **WhatsApp:** 360dialog (Meta Business Solution Provider). Cheaper than Twilio for African volume; cleaner WhatsApp Business API docs.
  - Fallback option: Twilio if 360dialog onboarding stalls.
  - Direct Meta Cloud API as a v2 option once volume justifies it.
- **Telegram:** Official Bot API via `python-telegram-bot` library. Free, no provider needed.

---

## 4. Backend Stack

### 4.1 API Service - FastAPI

- **Language:** Python 3.11+.
- **Framework:** FastAPI.
- **Schemas:** Pydantic v2 for all request/response shapes.
- **OpenAPI:** Auto-generated; consumed by mobile and web via `openapi-typescript` to produce typed clients.
- **DB driver:** SQLAlchemy 2.x + Alembic for migrations.
- **Async:** Async endpoints throughout; sync only where a library forces it.
- **Background jobs:** ARQ (async Redis queue).
- **Validation:** Pydantic everywhere; centralized error responses.
- **Tests:** `pytest` + `httpx` AsyncClient for integration tests.
- **Linting/formatting:** `ruff` + `black` + `mypy` (strict on new modules, lenient on legacy).

### 4.2 ML Inference Service - TensorFlow Serving

- **Trained models:** TensorFlow / Keras -> exported as SavedModel.
- **Server:** TensorFlow Serving in a separate Docker container.
- **Protocol:** REST from FastAPI at MVP.
- **Per-crop models:** Loaded as separate model versions in TF Serving; backend routes by crop.

### 4.3 Database - PostgreSQL

- **Hosted:** Supabase (free tier) at MVP, or Neon.
- **Schemas (initial):** users, interactions, farmers, advice_templates, extension_workers, model_versions, dataset_manifests.

### 4.4 Object Storage - Cloudflare R2

- **Why R2:** S3-compatible API, zero egress fees.
- **Buckets:** `ankara-photos-raw`, `ankara-photos-curated`, `ankara-models`, `ankara-backups`.

---

## 6. Identity, Auth, and Access

- **Farmers:** Identified by phone number (WhatsApp / Telegram chat ID) or anonymous web/mobile session. No account required.
- **Extension workers & admins:** Authenticated via the FastAPI backend's own JWT auth - email + password, cookie-based sessions.
- **API keys:** Per-bot service-to-service auth via signed JWTs.
- **Consent flow:** First-contact message in the bot explains data use; farmer must reply "yes" to opt in for photo retention beyond 90 days.

---

## 8. DevOps & Infrastructure

### 8.4 Domains & Networking

- One root domain (e.g., `ankara.example.com` or a `.org` equivalent).
- Subdomains: `api.`, `admin.`, `bot.`, `labeling.`, `staging.`.
- All HTTPS via Caddy + Let's Encrypt.

---

## 15. Stack Summary (One-Page Cheat Sheet)

| Layer          | Choice                                                              |
| -------------- | ------------------------------------------------------------------- |
| Mobile         | React Native + Expo, TypeScript                                     |
| Web            | Next.js 14 (App Router), TypeScript, Tailwind, shadcn/ui            |
| Chat bots      | Python adapters for WhatsApp (360dialog) and Telegram (Bot API)     |
| Backend API    | FastAPI, Pydantic, SQLAlchemy, Alembic                              |
| ML serving     | TensorFlow Serving (REST at MVP, gRPC post-MVP), separate container |
| Database       | PostgreSQL (Supabase free -> self-hosted)                           |
| Cache / queue  | Redis (Upstash -> self-hosted) + ARQ                                |
| Object storage | Cloudflare R2                                                       |
| Auth           | Own JWT (FastAPI boilerplate)                                       |
| Reverse proxy  | Caddy (auto HTTPS)                                                  |
| CI/CD          | GitHub Actions                                                      |
