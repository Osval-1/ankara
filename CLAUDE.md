# Ankara — CLAUDE.md

Monorepo for the Ankara project: a WhatsApp-first crop disease diagnosis tool
for smallholder farmers in Cameroon. See `docs/` for the full spec.

## Repo layout

```
apps/web/       Next.js 14 (App Router) — admin dashboard + landing page
apps/mobile/    Expo (React Native) — farmer-facing mobile app
apps/bots/      Python — WhatsApp (360dialog) + Telegram adapter routers
services/api/   FastAPI — core backend (diagnosis, logs, templates, auth)
services/ml/    TensorFlow Serving config + training pipeline
packages/
  advice-templates/   Per-crop FR/EN JSON advice templates
  i18n/               Shared translation files (fr, en)
  shared-types/       TypeScript types generated from FastAPI OpenAPI spec
infra/
  docker/             docker-compose.yml — full local stack
  caddy/              Caddyfile (reverse proxy + HTTPS)
  github-actions/     CI workflow files
data/
  manifests/          Dataset version manifests (CSV, tracked in git)
  notebooks/          Training + exploratory notebooks
docs/               PROJECT_SPEC.md, TECH_STACK.md, PARTNERSHIPS.md
```

## Tech stack (short)

| Layer       | Choice                                                 |
| ----------- | ------------------------------------------------------ |
| Mobile      | React Native + Expo (TypeScript)                       |
| Web         | Next.js 14, Tailwind, shadcn/ui, React Query           |
| Bots        | Python FastAPI sub-routers (WhatsApp + Telegram)       |
| API         | FastAPI, Pydantic v2, SQLAlchemy 2 async, Alembic      |
| ML          | TensorFlow/Keras -> TF Serving (gRPC), per-crop models |
| DB          | PostgreSQL (Supabase free tier -> self-hosted)         |
| Cache/queue | Redis + ARQ                                            |
| Storage     | Cloudflare R2                                          |
| Auth        | Clerk (web/mobile UI) + JWT (service-to-service)       |
| Proxy       | Caddy (auto HTTPS)                                     |
| CI/CD       | GitHub Actions                                         |

## Key rules

- The API is the single source of truth. Mobile, web, and bots all call
  `services/api` - no disease logic lives in the clients.
- Never recommend specific pesticide/chemical brands anywhere in code or templates.
  Advice templates say "consult your extension worker before any chemical application."
- Every advice template change requires review by an agronomist - enforced in the
  PR template checklist.
- Confidence shown as low/medium/high, never raw float. Calibration is applied
  in the API before the response leaves the backend.
- Photo storage: encrypted at rest, default 90-day deletion, farmer consent required
  for retention.

## Running locally

```bash
cp .env.example .env          # fill in secrets
docker compose -f infra/docker/docker-compose.yml up
```

- API: http://localhost:8000/docs
- Web: http://localhost:3000
- Label Studio: http://localhost:8080

## Crop rollout order

Cassava -> Maize -> Plantain -> Tomato -> Cocoa (sequential, one at a time).
MVP = cassava only.
