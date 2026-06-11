# Ankara — Monorepo Tooling Plan

**Owner:** asvaldr04@gmail.com
**Date:** 2026-05-31
**Status:** Implementation in progress

This document describes the monorepo tooling for the repo and the rationale for each choice.

---

## 1. Overview

The repo mixes TypeScript (Next.js, Expo, shared packages) and Python (FastAPI, ML, bots).

| Concern                           | JS/TS tool                          | Python tool                      |
| --------------------------------- | ----------------------------------- | -------------------------------- |
| Workspace / dep management        | pnpm workspaces                     | uv workspace                     |
| Build orchestration & caching     | Turborepo                           | turbo drives uv tasks via script |
| Lint / format on commit           | husky + lint-staged                 | husky + lint-staged (calls ruff) |
| Commit message standard           | commitlint                          | same hook                        |
| Cross-package version consistency | syncpack                            | -                                |
| Automated dep updates             | Renovate                            | Renovate                         |
| Package versioning + changelogs   | Changesets                          | -                                |
| Task aliases                      | Makefile                            | Makefile                         |
| CI pipeline                       | GitHub Actions + Turbo remote cache | GitHub Actions + uv              |

---

## 3. uv Workspace

**File:** `pyproject.toml` (root)

All three Python services (`services/api`, `services/ml`, `apps/bots`) are declared as workspace members.

### Benefits

- `uv sync` installs all Python deps in one command.
- `uv run --package ankara-api ruff check .` runs a tool scoped to one service.
- No manual venv activation per service.

### Usage

```bash
uv sync
uv run --package ankara-api pytest
uv run --package ankara-api ruff check services/api
```

---

## 9. Makefile

| Target         | What it runs                                       |
| -------------- | -------------------------------------------------- |
| `make migrate` | `uv run --package ankara-api alembic upgrade head` |

---

## 10. CI Pipeline

1. JS/TS jobs run `turbo lint typecheck test build`.
2. Python job uses `uv sync` at root then runs ruff, mypy, and pytest for each service.
3. Docker build job (on `main` only) builds and tags all images with the commit SHA.
