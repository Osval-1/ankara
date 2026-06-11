# Ankara — Scaffolding Plan

**Status:** Monorepo scaffold complete. Templates copied and cleaned. Ready for domain modifications.
**Last updated:** 2026-05-31

---

## What is done

### Monorepo root (`ankara/`)

- [x] Git initialized, `main` branch set
- [x] `package.json` (pnpm workspaces: apps/web, apps/mobile, packages/\*)
- [x] `.gitignore` (Node, Python, Expo, ML artifacts)
- [x] `.env.example` (all env vars for all services)
- [x] `CLAUDE.md` (monorepo orientation for future sessions)

### `apps/web` - Next.js 14

- [x] Template copied, `.git` and README/LICENSE removed
- [x] All template branding replaced
- [x] Package name: `@ankara/web`
- [x] App metadata, titles, homepage updated

### `apps/mobile` - Expo React Native

- [x] Template copied, `.git`/README/LICENSE/claude.md removed
- [x] All template branding replaced
- [x] Package name: `@ankara/mobile`
- [x] Expo slug: `ankara`
- [x] Onboarding screen copy updated

### `services/api` - FastAPI

- [x] Template copied, `.git`/README/LICENSE/CONTRIBUTING/docs removed
- [x] All template branding replaced
- [x] `pyproject.toml`: name `ankara-api`, author Ankara Team
- [x] `config.py`: default `APP_NAME = "Ankara"`

### `packages/`

- [x] `advice-templates/cassava/en.json`
- [x] `advice-templates/cassava/fr.json`
- [x] `i18n/en.json`
- [x] `i18n/fr.json`
- [x] `shared-types/index.ts`

### `infra/`

- [x] `docker/docker-compose.yml`
- [x] `caddy/Caddyfile`
- [x] `github-actions/ci.yml`

### `docs/`

- [x] `PROJECT_SPEC.md` copied in
- [x] `TECH_STACK.md` copied in
- [x] `PARTNERSHIPS.md` copied in
- [x] `SCAFFOLDING_PLAN.md` (this file)

---

## What is NOT yet done - domain modifications needed

### Repo structure constraint

Each service is self-contained: its own `package.json`/`pyproject.toml`, lockfile, and Dockerfile.

---

### `services/api` - domain layer

**Why:** The template has the engine (async DB, JWT, Redis, ARQ) but no domain logic.

#### Models

- [x] `Crop` enum
- [x] `CropClass` enum
- [x] `Channel` enum
- [x] `Language` enum
- [x] `ConfidenceLevel` enum

#### Schemas

- [x] `DiagnosisRequest` / `DiagnosisReply`

#### Services / business logic

- [x] `DiagnosisService` stub
- [x] `R2Client` stub
- [x] `MLClient` stub
- [x] `ConfidenceCalibrator` stub
- [x] `ConsentService` stub

#### Endpoints

- [x] `POST /api/v1/diagnosis` stub
- [x] `POST /api/v1/webhooks/whatsapp` stub
- [x] `POST /api/v1/webhooks/telegram` stub

---

## Recommended build order

1. `services/api`
2. `services/ml`
3. `apps/bots`
4. `apps/web`
5. `apps/mobile`
