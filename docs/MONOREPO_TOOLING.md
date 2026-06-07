# Cameroon Crop Doctor — Monorepo Tooling Plan

**Owner:** asvaldr04@gmail.com
**Date:** 2026-05-31
**Status:** Implementation in progress

This document describes every layer of production-ready monorepo tooling for this
repo and explains the rationale for each choice.

---

## 1. Overview

The repo mixes TypeScript (Next.js, Expo, shared packages) and Python (FastAPI, ML,
bots). The tooling stack is split accordingly:

| Concern                           | JS/TS tool                          | Python tool                        |
| --------------------------------- | ----------------------------------- | ---------------------------------- |
| Workspace / dep management        | pnpm workspaces                     | uv workspace                       |
| Build orchestration & caching     | Turborepo                           | (turbo drives uv tasks via script) |
| Lint / format on commit           | husky + lint-staged                 | husky + lint-staged (calls ruff)   |
| Commit message standard           | commitlint (conventional commits)   | same hook                          |
| Cross-package version consistency | syncpack                            | —                                  |
| Automated dep updates             | Renovate                            | Renovate (pip ecosystem)           |
| Package versioning + changelogs   | Changesets                          | —                                  |
| Task aliases                      | Makefile                            | Makefile                           |
| CI pipeline                       | GitHub Actions + Turbo remote cache | GitHub Actions + uv                |

---

## 2. Turborepo

**File:** `turbo.json`

Turborepo sits on top of pnpm workspaces and adds:

- **Build cache** — only re-runs tasks for changed packages and their dependents.
- **Remote cache** — Vercel's free remote cache shares build artefacts across
  developer machines and CI (opt-in; local-only cache works without a token).
- **Correct task ordering** — `shared-types` is always built before `web` or
  `mobile` consume it.

### Pipeline definition

```
lint → typecheck → build → test
```

Each stage declares its `dependsOn` and `outputs` so Turbo knows what to cache.

### Usage

```bash
turbo build           # build all changed packages
turbo lint typecheck  # lint + typecheck in parallel, only changed
turbo dev             # start all dev servers concurrently
```

Remote cache (optional):

```bash
npx turbo login       # authenticate with Vercel
npx turbo link        # link this repo to the remote cache
```

---

## 3. uv Workspace

**File:** `pyproject.toml` (root)

All three Python services (`services/api`, `services/ml`, `apps/bots`) are
declared as workspace members. A single `uv.lock` at the root ensures consistent
transitive deps across services.

### Benefits

- `uv sync` installs all Python deps in one command (< 10 s on a cold machine).
- `uv run --package crop-doctor-api ruff check .` runs a tool scoped to one service.
- No manual venv activation per service.

### Usage

```bash
uv sync                                    # install all Python deps
uv run --package crop-doctor-api pytest    # run API tests
uv run --package crop-doctor-api ruff check services/api
```

---

## 4. Root husky + lint-staged

**Files:** `.husky/pre-commit`, `.husky/commit-msg`, `.lintstagedrc.json`

The `apps/mobile` package already has its own husky setup. We lift hooks to the
root so they run for all packages and Python files.

### pre-commit hook

- JS/TS files → `eslint --fix` + `prettier --write` (via lint-staged, only staged files)
- Python files → `ruff check --fix` + `ruff format` (via lint-staged, only staged files)

### Why lift to root?

A hook per-package means a developer working in `services/api` never triggers the
web linter and vice versa — correct. But without a root hook, Python files have no
commit-time check unless the developer is inside `apps/bots`. Root hooks cover the
whole tree.

---

## 5. Commitlint

**File:** `.commitlintrc.json`

Enforces [Conventional Commits](https://www.conventionalcommits.org/) via
`@commitlint/config-conventional`. This enables:

- Automated changelog generation (via Changesets or `conventional-changelog`).
- Semantic version inference.
- Readable `git log`.

### Allowed types

`feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

### Examples

```
feat(api): add diagnosis endpoint
fix(mobile): correct confidence colour threshold
chore(deps): bump next to 14.3.0
```

---

## 6. syncpack

**File:** `.syncpackrc.json`

Checks that the same package is not pinned at different versions across
`apps/web/package.json`, `apps/mobile/package.json`, and `packages/*/package.json`.

Run manually or in CI:

```bash
pnpm syncpack list-mismatches
pnpm syncpack fix-mismatches
```

---

## 7. Changesets

**File:** `.changeset/config.json`

Manages versioning and changelogs for the three publishable shared packages:

- `@crop-doctor/shared-types`
- `@crop-doctor/i18n`
- `@crop-doctor/advice-templates`

### Workflow

1. When you make a change to a shared package, run `pnpm changeset` and describe
   the change (patch / minor / major).
2. On merge to `main`, the Changesets GitHub Action opens a "Version Packages" PR.
3. Merging that PR bumps versions and publishes changelogs.

The apps (`web`, `mobile`) and services are private and excluded from publishing.

---

## 8. Renovate

**File:** `renovate.json`

Keeps all dependencies up to date via automated PRs:

- **JS/TS:** npm/pnpm packages across all `package.json` files.
- **Python:** pip packages in all `pyproject.toml` files.
- **Docker:** base image tags in `Dockerfiles` and `docker-compose.yml`.
- **GitHub Actions:** action versions in workflow files.

### Grouping strategy

- Patch/minor updates grouped by ecosystem (one PR per week).
- Major updates as individual PRs for human review.
- `main` branch protection — Renovate targets `main` but requires CI to pass.

---

## 9. Makefile

**File:** `Makefile`

A thin alias layer so developers don't need to remember pnpm/turbo/uv command
syntax. Every target delegates to the right underlying tool.

| Target           | What it runs                                            |
| ---------------- | ------------------------------------------------------- |
| `make dev`       | `turbo dev`                                             |
| `make build`     | `turbo build`                                           |
| `make lint`      | `turbo lint && uv run ruff check .`                     |
| `make typecheck` | `turbo typecheck`                                       |
| `make test`      | `turbo test && uv run pytest`                           |
| `make migrate`   | `uv run --package crop-doctor-api alembic upgrade head` |
| `make format`    | `turbo format && uv run ruff format .`                  |
| `make install`   | `pnpm install && uv sync`                               |
| `make docker-up` | `docker compose -f infra/docker/docker-compose.yml up`  |
| `make changeset` | `pnpm changeset`                                        |
| `make syncpack`  | `pnpm syncpack list-mismatches`                         |

---

## 10. CI Pipeline (GitHub Actions)

**File:** `infra/github-actions/ci.yml`

Upgraded from per-service jobs to a single workflow with:

1. **JS/TS jobs** run `turbo lint typecheck test build` with Vercel remote cache.
   Turbo automatically skips unchanged packages.
2. **Python job** uses `uv sync` at root then runs ruff, mypy, and pytest for each
   service in one job (no need for separate jobs since uv workspace handles isolation).
3. **Docker build job** (on `main` only) builds and tags all images with the commit SHA.

### Branch strategy

- Every PR → lint + typecheck + test.
- Merge to `main` → everything above + Docker build.
- Manual trigger → deploy to staging / production.

---

## 11. Implementation Checklist

- [x] `docs/MONOREPO_TOOLING.md` (this file)
- [x] `turbo.json`
- [x] `pyproject.toml` (root uv workspace)
- [x] `.husky/pre-commit` (root)
- [x] `.husky/commit-msg` (root)
- [x] `.lintstagedrc.json`
- [x] `.commitlintrc.json`
- [x] `.syncpackrc.json`
- [x] `.changeset/config.json`
- [x] `renovate.json`
- [x] `Makefile`
- [x] `infra/github-actions/ci.yml` (upgraded)
- [x] `package.json` (root — add turbo, commitlint, syncpack, changesets to devDeps; update scripts)
