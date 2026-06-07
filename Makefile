.PHONY: install dev build lint typecheck test format migrate docker-up docker-down \
        changeset syncpack clean help

# ── Install ────────────────────────────────────────────────────────────────────
install:
	pnpm install && uv sync

# ── Development ────────────────────────────────────────────────────────────────
dev:
	turbo dev

dev-api:
	uv run --package crop-doctor-api uvicorn src.app.main:app --reload --port 8000

dev-web:
	pnpm --filter @crop-doctor/web dev

dev-mobile:
	pnpm --filter @crop-doctor/mobile start

# ── Build ──────────────────────────────────────────────────────────────────────
build:
	turbo build

# ── Lint & format ──────────────────────────────────────────────────────────────
lint:
	turbo lint
	uv run ruff check .

format:
	turbo format
	uv run ruff format .

# ── Type checking ──────────────────────────────────────────────────────────────
typecheck:
	turbo typecheck
	uv run mypy services/api/src services/ml/src apps/bots/src

# ── Tests ──────────────────────────────────────────────────────────────────────
test:
	turbo test
	uv run pytest

test-api:
	uv run --package crop-doctor-api pytest services/api/tests -v

test-web:
	pnpm --filter @crop-doctor/web test --run

# ── Database ───────────────────────────────────────────────────────────────────
migrate:
	uv run --package crop-doctor-api alembic -c services/api/src/alembic.ini upgrade head

migrate-down:
	uv run --package crop-doctor-api alembic -c services/api/src/alembic.ini downgrade -1

migrate-new:
	uv run --package crop-doctor-api alembic -c services/api/src/alembic.ini revision --autogenerate -m "$(name)"

# ── Docker ─────────────────────────────────────────────────────────────────────
docker-up:
	docker compose -f infra/docker/docker-compose.yml up

docker-up-d:
	docker compose -f infra/docker/docker-compose.yml up -d

docker-down:
	docker compose -f infra/docker/docker-compose.yml down

docker-build:
	docker compose -f infra/docker/docker-compose.yml build

# ── Release management ─────────────────────────────────────────────────────────
changeset:
	pnpm changeset

changeset-version:
	pnpm changeset version

# ── Dependency hygiene ─────────────────────────────────────────────────────────
syncpack:
	pnpm syncpack list-mismatches

syncpack-fix:
	pnpm syncpack fix-mismatches

# ── Clean ──────────────────────────────────────────────────────────────────────
clean:
	turbo clean
	find . -type d -name __pycache__ -not -path '*/.venv/*' | xargs rm -rf
	find . -type d -name .pytest_cache -not -path '*/.venv/*' | xargs rm -rf

# ── Help ───────────────────────────────────────────────────────────────────────
help:
	@echo "Crop Doctor — available make targets:"
	@echo ""
	@echo "  install         pnpm install + uv sync"
	@echo "  dev             start all dev servers (turbo dev)"
	@echo "  dev-api         start FastAPI dev server only"
	@echo "  dev-web         start Next.js dev server only"
	@echo "  dev-mobile      start Expo dev server only"
	@echo "  build           build all packages"
	@echo "  lint            lint JS/TS + Python"
	@echo "  format          format JS/TS + Python"
	@echo "  typecheck       tsc + mypy"
	@echo "  test            run all tests"
	@echo "  test-api        run API tests only"
	@echo "  test-web        run web tests only"
	@echo "  migrate         alembic upgrade head"
	@echo "  migrate-down    alembic downgrade -1"
	@echo "  migrate-new     alembic autogenerate (pass name=<msg>)"
	@echo "  docker-up       docker compose up"
	@echo "  docker-down     docker compose down"
	@echo "  changeset       create a changeset for a shared package release"
	@echo "  syncpack        list cross-package version mismatches"
	@echo "  clean           remove build artefacts and caches"
