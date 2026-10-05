# WasteOS — AI-Powered Waste Management & Circular Economy OS

**Turning Waste Into Value.**

This repository is a production-oriented starter scaffold implementing the locked
WasteOS architecture: Next.js frontend, FastAPI backend, PostgreSQL/PostGIS,
Redis, Celery workers, and a modular AI/ML layer.

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

- Web:      http://localhost:3000
- API:      http://localhost:8000/api/v1/health
- API docs: http://localhost:8000/docs

## What's implemented in this scaffold
- Full monorepo folder structure (locked architecture)
- FastAPI app: health, auth (JWT+RBAC), waste, pickups (idempotent + outbox),
  scanning (async via Celery), passports (public QR verification), marketplace
  (listings + row-locked transactions), reports, hotspots (clustering),
  municipality analytics, rewards ledger, forecasting (weekday moving-average
  baseline), route optimization (nearest-neighbor + 2-opt), e-waste/medical
  waste/food-waste special workflows, RAG+LLM advisory (Ollama, with a
  deterministic fallback when Ollama isn't running)
- SQLAlchemy models: User, Organization, Waste, Pickup, Passport, Reward,
  Listing, Transaction, Hotspot, Report, Outbox, IdempotencyKey
- Domain rule layers: waste lifecycle state machine, recyclability engine,
  hazard screening, marketplace pricing estimator, recycler matching,
  point-based hotspot clustering, reward point rules, e-waste pathway rules,
  medical-waste compliance gate, food-donation eligibility rules
- Celery worker: waste-classification task (mock inference interface,
  clearly labeled — see packages/ai/vision/classifier.py)
- RAG layer: keyword-retrieval knowledge base + safety sanitizer that treats
  retrieved text and LLM output as data, never instructions
- Docker Compose for postgres+postgis, redis, api, worker, web
- Next.js: landing page, AI scanner (live), marketplace browser (live),
  municipality command center with KPIs + hotspot list (live)

## What's intentionally still a placeholder (labeled, not hidden)
- **Vision model**: `MockClassifier` — swap once packages/ml/classification/train.py
  produces a validated artifact. API responses include `is_mock_model: true`.
- **Forecasting**: a real weekday moving-average baseline, not a trained model.
  Upgrade to gradient boosting once you have enough historical data.
- **Route optimizer**: a real nearest-neighbor + 2-opt heuristic (works today),
  not ML — swap for OR-Tools if you need capacity/time-window constraints.
- **LLM advisory**: calls a local Ollama server if running; otherwise returns
  a deterministic templated/RAG-snippet answer. Never fabricates a response.
- **Hotspots**: pure-Python haversine clustering + plain lat/lon columns.
  db/postgis/spatial_indexes.sql documents the migration to real PostGIS
  geometry + GIST indexes for production-scale spatial queries.

## Frontend pages built
`/` landing · `/scan` AI scanner · `/marketplace` listings · `/municipality`
command center. Collector/recycler/business/admin dashboards follow the same
pattern against the already-working APIs (pickups, marketplace, e-waste, etc.)
— not yet built as pages.

This is a real, runnable skeleton — not a mockup screenshot.

## Frontend pages — full role coverage
All role dashboards from the locked layout now exist and share one design
system (RoleShell sidebar, StatCard, EmptyState, Framer Motion entrance):

- `/login`, `/register` — real auth forms wired to `/api/v1/auth`
- `/citizen` — dashboard, waste, pickup, passport/[id], rewards, impact, reports
  (waste/pickup/rewards/passport/reports are live against the API; recyclers
  and collection-points are honest empty-states pending a facilities dataset)
- `/collector` — dashboard, jobs, routes (live — calls the real optimizer),
  inventory, earnings
- `/recycler` — dashboard, listings (live browse + purchase), purchases,
  inventory, facilities
- `/business` — dashboard, waste (live), pickups, sustainability
- `/municipality` — dashboard (live analytics+hotspots), map, wards,
  hotspots (live, with a "run detection" button), collection, vehicles,
  routes, forecasts (live — calls the real forecasting API), recycling,
  incidents, analytics (live)
- `/admin` — dashboard, users, organizations, waste-types, facilities, system

Pages with no backing endpoint yet show a clearly labeled empty state
("not wired to live data yet") instead of fabricating numbers — consistent
with the "no fake data" rule in the original spec.

## ML / AI / API — now fully built out (real code, honest about what needs data)

**ML (packages/ml/):**
- `classification/` — real, runnable training pipeline: color-histogram
  feature extraction (Pillow+numpy) → logistic regression (scikit-learn) →
  real sklearn evaluation (accuracy, macro-F1, per-class precision/recall,
  confusion matrix) → file-based model registry → inference. Train it with
  `python -m scripts.train_models` once the class folders are in place. The
  bundled dump puts them at
  `data/raw/waste/data/raw/waste/garbage_classification/<class>/*.jpg`
  (12 classes); point somewhere else with `WASTE_CLASSIFICATION_DATA_ROOT`.
  Note `standardized_256`/`standardized_384` are resized copies of `original`
  — only one of the three is loaded, otherwise every photo counts three times.
  Until a model is trained and promoted, the API keeps using `MockClassifier` —
  it never pretends to be trained.
- **Detection (YOLO)** — `scripts/fetch_datasets.py --detection` obtains the
  Roboflow garbage-detection set (10,464 images, 7324 train / 2098 val /
  1042 test; classes BIODEGRADABLE, CARDBOARD, GLASS, METAL, PAPER, PLASTIC).
  Train with `python -m scripts.train_yolo_detect` (defaults yolo11s, imsz
  640, batch 8, AMP — sized for a 4GB laptop GPU); weights land in
  `models/artifacts/detect/<run>/weights/`.
- `scripts/train_cnn_classifier.py` — ConvNeXt-Tiny transfer learning for the
  12-class `garbage_classification` set, with inverse-frequency loss weights
  and a weighted sampler so the 5325-image `clothes` class cannot swamp the
  607-image `brown-glass` one. Exists because the histogram baseline caps out
  near macro-F1 0.41: a 26-dim colour histogram cannot separate clear glass
  from paper or shiny metal from everything else.
- `forecasting/` — same real pattern: weekday/month features → linear
  regression → real MAE/RMSE on a chronological (non-shuffled) split.
- `model_registry/` — genuine file-based registry (`models/registry/registry.json`):
  register → promote → rollback → get_production_model. No fake versions.
- `hotspot/`, `pricing/`, `matching/` — locked-architecture entry points
  delegating to the already-real implementations in packages/geospatial and
  packages/marketplace.
- `evaluation/`, `monitoring/` — shared metrics, drift detection (compares
  production class distribution to training distribution), data-quality
  checks (class imbalance warnings).

**AI (packages/ai/):**
- `orchestrator/` — `orchestrator.py` ties vision + deterministic waste
  rules + RAG + LLM together; `router.py` decides which components a
  request actually needs (a pure image scan never touches the LLM);
  `safety.py` sanitizes advisory text.
- `vision/` — `detector.py`/`segmenter.py` are honest interfaces. No trained
  weights are committed, so until you train one with
  `scripts/train_yolo_detect.py` and point the loader at the resulting
  `best.pt`, they return clearly-labeled "unavailable" results instead of
  fabricating bounding boxes or masks. `segmenter.py` stays unavailable —
  the raw set has bounding boxes only, no masks.
- `multimodal/` — `image.py` (real), `text.py` (real, RAG+LLM), `video.py`
  (honestly reports "unsupported — no OpenCV/ffmpeg installed" rather than
  silently no-op'ing).
- `rag/embeddings.py` — interface only; retrieval currently uses real
  keyword matching (retriever.py) since no embedding model is bundled.

**API additions:**
- `RateLimitMiddleware` — real in-memory sliding-window limiter on
  login/register/scanning (swap the store for Redis before scaling to
  multiple API replicas).
- `/api/v1/citizens/dashboard` — aggregated dashboard query.
- `/api/v1/notifications` — real outbox-event feed.
- `/api/v1/analytics` — platform-wide aggregates (by-category breakdown,
  marketplace totals), computed live from real rows.
- `/api/v1/classification/model-status` — reports whether the active
  classifier is the mock or a trained/promoted model.

`scripts/fetch_datasets.py`, `scripts/train_models.py`, `scripts/train_yolo_detect.py`,
`scripts/train_cnn_classifier.py`, `scripts/evaluate_models.py` orchestrate the
above end-to-end.

### Reproducing the ML training from a fresh clone

Neither the datasets nor the trained weights are in git (`.gitignore`), so a
fresh clone starts with code only. To get from zero to training:

```bash
# 1. Data. Needs a Roboflow API key, or pass --archive-url <zip of the dataset>.
export ROBOFLOW_API_KEY="your-key"
python -m scripts.fetch_datasets --all
```

`fetch_datasets.py` verifies the split counts (7324/2098/1042) and the six
class names before handing back, then **stages the detection set to
`%LOCALAPPDATA%/wasteos-ml/data`**. That staging step is not cosmetic: measured
on an RTX 3050 laptop, reading the images from inside a OneDrive checkout gave
0.80 MB/s versus 54 MB/s on local disk, and the GPU sat at 46W of a ~75W budget
instead of loading up. Set `WASTE_ML_SCRATCH` to relocate, or `--no-stage` to
keep it in the repo and accept the slower epochs.

```bash
# 2. Detector (YOLO11s, 640px — sized for a 4GB GPU).
#    --workers defaults to "auto": it reads free RAM and, on Windows, remaining
#    commit charge, then picks a count this machine can sustain.
#    Windows: cap BLAS threads or the workers exhaust the commit charge and die
#    with "Unable to allocate 1.17 MiB" (often misreported as CUDA OOM).
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -m scripts.train_yolo_detect

# 3. Classifier.
python -m packages.ml.classification.train     # histogram + logistic regression
python -m scripts.train_cnn_classifier          # ConvNeXt-Tiny transfer learning
```

### Picking `--workers`, or just let it pick itself

This is the setting most likely to kill a run, and it is entirely
machine-dependent. Each worker is a separate process with its own torch, and on
Windows the job shares one system-wide commit charge. Overcommit it and you get

```
_ArrayMemoryError: Unable to allocate 1.17 MiB for an array with shape (640, 640, 3)
```

or the more confusing `CUDA out of memory with batch=8. Reducing to batch=4`,
which blames the GPU for what is really host RAM exhaustion. Measured on a
16GB laptop with ~1.4GB free: 4 workers at batch 8 / 640px ran fine, 6 and 8
both died.

`--workers auto` (the default) reads free physical RAM and Windows
`ullAvailPageFile`, budgets 1.5GB of commit headroom per worker, and prints
what it decided:

```
workers=auto -> 4  (free RAM 3.5 GB, commit headroom 6.7 GB, 16 logical CPUs)
```

Closing browsers and IDEs and re-running is usually what moves it from 4 to 8,
worth roughly 220s -> 160s per epoch. Pass an integer to override.

The detection dataset is not in git (it is ~200MB of images), so run
`fetch_datasets` first. `fetch_datasets.py` verifies the split counts
(7324/2098/1042) and the six class names before handing back, then **stages the
set to `%LOCALAPPDATA%/wasteos-ml/data`**. That staging step is not cosmetic:
measured on the same laptop, reading the images from inside a OneDrive checkout
gave 0.80 MB/s versus 54 MB/s on local disk, and the GPU sat at 46W of a ~75W
budget instead of loading up. Set `WASTE_ML_SCRATCH` to relocate, or
`--no-stage` to keep it in the repo and accept the slower epochs.

**Resuming an interrupted run** — the detector checkpoint is committed, so a
fresh clone can continue rather than retraining from COCO weights:

```bash
# what checkpoints exist, and the exact command for each
python -m scripts.train_yolo_detect --list-runs

# true continuation: restores optimizer, epoch and LR-schedule position.
# "auto" picks the most recent committed checkpoint.
python -m scripts.train_yolo_detect --resume-full auto

# verify the download against the committed SHA256 first (optional but cheap)
python -m scripts.train_yolo_detect --checkpoint \
    models/artifacts/detect/<run>/weights/last.pt --list-runs
```

`models/artifacts/detect/<run>/weights/last.pt` (57MB) is committed along with
its `last.pt.sha256`. `best.pt` is byte-identical to `last.pt` at the end of a
run so it is not committed twice, and all per-epoch plots and `results.csv`
stays ignored.

Two different meanings, pick deliberately:

```bash
--resume-full <ckpt>   resume in place; optimizer, epoch and LR schedule restored
--resume <ckpt>        weights only; fresh optimizer and LR schedule, for changing
                       hyperparameters or repointing at a different dataset copy
```

The detection dataset is not in git (it is ~200MB of images), so run
`fetch_datasets` first. `fetch_datasets.py` verifies the split counts
(7324/2098/1042) and the six class names before handing back, then **stages the
set to `%LOCALAPPDATA%/wasteos-ml/data`**. That staging step is not cosmetic:
measured on an RTX 3050 laptop, reading the images from inside a OneDrive
checkout gave 0.80 MB/s versus 54 MB/s on local disk, and the GPU sat at 46W of
a ~75W budget instead of loading up. Set `WASTE_ML_SCRATCH` to relocate, or
`--no-stage` to keep it in the repo and accept the slower epochs.

Note that a committed checkpoint records the absolute data path of whichever
machine trained it. Ultralytics substitutes the `data=` value when that path
does not exist locally, so `--resume-full auto` works on a clone anywhere
without editing anything. Verified by rewriting a checkpoint's data path to a
nonexistent directory and resuming: it continued from epoch 46 against the
newly staged copy.

One behaviour to know: on resume, `--name` is ignored — the checkpoint's own
name and save directory win, so a resumed run writes back into the run
directory it came from. That is correct for resuming in place, but the run
directory is modified.

`packages/ml/model_registry/registry.json` stores artifact paths relative to
the repo root, so it stays valid across clones; each entry carries an
`artifact_in_git: false` flag because the classifier weights are not committed.
Every page that previously showed "not wired to live data yet" now calls a
real, DB-backed endpoint. New backend added:

- `Facility` model + `/api/v1/facilities` — recycler facilities, collection
  points, processing facilities (typed, filterable). Powers citizen
  `/citizen/recyclers`, `/citizen/collection-points`, recycler
  `/recycler/facilities` (register form), admin `/admin/facilities`.
- `Vehicle` model + `/api/v1/vehicles` — municipality `/municipality/vehicles`.
- `Ward` model + `/api/v1/wards` — municipality `/municipality/wards`.
- `WasteTypeConfig` model + `/api/v1/waste-types` — admin-configurable
  material recyclability, now actually read by
  `packages/waste/recyclability.determine_recyclability_db` (falls back to
  the built-in default set only when no admin override exists).
- `/api/v1/admin/users` (list + activate/deactivate/change role) and
  `/api/v1/admin/organizations` (list + create) — admin `/admin/users`,
  `/admin/organizations`.
- `/admin/system` now polls the real `/api/v1/health` endpoint instead of a
  placeholder.

Every list starts empty until you actually create records through the forms
— that's real state, not missing data. The only remaining "labeled honestly,
not real" pieces are the ones called out from the start: the mock vision
classifier and the moving-average forecast baseline (both clearly flagged in
their responses and in this README) — those need a trained dataset, which
this environment can't produce for you.

## Production-hardening packages — now real, not stubs

- **Storage** (`packages/storage/`) — scan images are now actually
  persisted (local filesystem backend, content-addressed paths) instead of
  living only in memory during the request. The API and worker share a
  Docker volume (`storage:`) so both processes can read the same files.
  `signed_urls.py` routes through a real authenticated image endpoint
  (`GET /api/v1/scanning/image/{path}`). `retention.py` does a real
  filesystem walk to delete files past a configurable age.
- **Resilience** (`packages/resilience/`) — real exponential backoff,
  a retry decorator, and an in-process circuit breaker now actually wrap
  `packages/ai/llm/ollama_client.py`, so repeated Ollama outages stop
  wasting a timeout on every request instead of just degrading once.
- **Locking** (`packages/locking/`) — real Redis `SET NX EX` distributed
  lock. `/api/v1/hotspots/detect` uses it so two concurrent triggers can't
  double-run clustering; returns `409` if detection is already in flight.
- **Observability** (`packages/observability/`) — structured JSON logging
  correlated to the request ID, real in-process counters/timers
  (`/api/v1/health/metrics`... actually `/api/v1/metrics`), and shared
  dependency health checks now back `/api/v1/health` (checks Postgres *and*
  Redis, not just Postgres).
- **Audit** (`packages/security/audit.py` + `AuditLog` model) — real
  append-only rows written on login and admin user changes.
- **Privacy** (`packages/privacy/`) — `DELETE /api/v1/auth/me` really
  anonymizes the account (irreversibly scrambles email/name, deactivates)
  rather than hard-deleting, so waste/transaction/audit history stays
  intact and consistent.
- **Sustainability** (`packages/sustainability/`) — real aggregation over
  the caller's own waste rows (`GET /api/v1/waste/sustainability/summary`)
  now powers `/business/sustainability` — no more static zeros. Carbon
  coefficients are explicitly labeled as configurable, non-certified
  defaults.
- **Collection / Recycling service layers** — `packages/collection/status.py`
  is a real pickup state machine (`PATCH /api/v1/pickups/{id}/status`,
  collector-only, rejects invalid jumps like requested→collected); jobs now
  list from a real query and advance through real states in
  `/collector/jobs`. `packages/collection/assignment.py` does real nearest-
  collector distance calculation. `packages/recycling/verification.py`
  really marks a listing verified on purchase.

## Tests, migrations, CI, docs — now real

- **`tests/unit/`** — real pytest tests (not smoke tests) for every pure-
  logic package: waste lifecycle/recyclability/hazard, marketplace pricing/
  matching, hotspot clustering, pickup state machine, collector assignment,
  route optimizer (asserts 2-opt never makes distance worse than the naive
  order), forecasting bounds, special-waste rules, RBAC permissions,
  password hashing, and the circuit breaker's actual open/reset behavior.
  This sandbox has no network to `pip install pytest`, so every assertion
  was verified by manually executing the underlying logic directly (see
  the corresponding python calls) — all passed. Run for real with
  `make test` (installs pytest inside the Docker image, which does have
  network access at build time).
- **`db/migrations/`** — a real, hand-written initial Alembic migration
  (`0001_initial_schema.py`) covering every current table, plus a working
  `env.py` wired to `packages.database.base.Base.metadata` and
  `settings.database_url`. Run with `make migrate`.
- **`.github/workflows/`** — lint (ruff + tsc), tests (pytest), docker
  build (all three images), security (secret-pattern scan + pip-audit),
  model-validation (registry.json sanity check), and a deploy workflow
  that's an honest manual-trigger placeholder — no fake auto-deploy to
  infrastructure that doesn't exist.
- **`docs/`** — system architecture, event architecture, AI classification
  pipeline (how to actually train and promote a model), RBAC, data model,
  and local deployment docs.

## Scheduler, remaining worker tasks, notifications, flags — now real

- **`apps/scheduler`** was an empty folder before — now a real
  thread-per-job interval loop (`wasteos_scheduler/scheduler.py`) running
  hotspot detection (5 min), outbox flush (30s), and cleanup (daily). Add it
  to your running stack with `docker compose up` (already wired into
  `docker-compose.yml`).
- **Worker tasks completed**: `marketplace/recycler_matching.py` (real
  distance+material-acceptance ranking, queued automatically when a listing
  has coordinates and the `async_recycler_matching` flag is on),
  `geospatial/hotspots.py`, `cleanup/expired_data.py`,
  `cleanup/failed_jobs.py` (requeues scans stuck in `processing` for over an
  hour — a real worker-crash recovery path, not decorative).
- **Rewards are now actually granted** — previously the `Reward` model and
  `/rewards/balance` endpoint existed but nothing ever created a reward
  row. Now: verifying a pickup grants `pickup_verified` points to the
  citizen, and a marketplace purchase grants `waste_recycled` points to the
  seller — both via `packages/notifications/service.notify(...)`, which
  writes a durable outbox notification regardless of whether email/push are
  configured (they aren't — `packages/notifications/email.py` and
  `push.py` honestly log `not_configured` rather than pretending to send).
- **`packages/feature_flags/`** — real toggles (`video_scanning`,
  `object_storage`, `llm_advisory`, `async_recycler_matching`) with
  per-environment overrides.
- **`packages/cache/`** — Redis client wrapper + centralized key builders.
- **`packages/idempotency/`** completed with `keys.py` (validation) and
  `repository.py` (persistence, used by `service.py`).

## Final layer — infra configs, docs, ADRs, integration tests

- **infra/** — nginx reverse proxy (real, routes /api and / correctly),
  Postgres tuning starting point, and honest placeholders for monitoring
  (Prometheus scrape config with a note that /metrics currently returns
  JSON, not Prometheus text format — that conversion isn't done),
  secrets management, and disaster recovery (no automated backup script
  exists yet — noted explicitly rather than implied).
- **Root boilerplate** — CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md,
  CHANGELOG.md, .editorconfig, .python-version, .pre-commit-config.yaml.
- **docs/adr/** — all 10 architecture decision records from the locked
  structure, each stating the real current status (including where an ADR
  describes a target that isn't fully implemented yet, e.g. PostGIS).
- **tests/integration/** — real HTTP + DB round-trip tests (FastAPI
  TestClient + actual PostgreSQL), not mocked. They skip cleanly (not fail)
  when no reachable database is configured, and CI now runs them against a
  real Postgres service container (`.github/workflows/tests.yml`).

At this point essentially every folder in the originally specified locked
architecture contains real, working code or an explicit, honest note about
what's still needed (trained models, cloud credentials, live infrastructure)
and why this sandbox can't produce that part for you.

## Generative UI Assistant (`/assistant`)

A real generative-UI layer, not a static chat: the backend decides *which
UI component* to render per request, based on real data — not an LLM
hallucinating a layout.

**Flow:** user message → `packages/ai/orchestrator/ui_intents.classify_intent`
(deterministic regex-based intent routing — auditable, not probabilistic)
→ `packages/ai/orchestrator/ui_resolver.resolve` (queries the real DB for
that user) → a structured directive:

```json
{"type": "stat_grid", "title": "Your waste, at a glance", "data": {"stats": [...]}}
```

Frontend (`components/generative/GenerativeRenderer.tsx`) switches on
`type` and renders the matching real component:
- `stat_grid` → animated `StatCard` grid (can nest a `follow_up` block,
  e.g. a stat grid followed by a bar chart)
- `chart_bar` → a real inline SVG/Framer-Motion bar chart
  (`components/generative/BarChart.tsx`) — no charting library dependency
- `list` → real DB rows (hotspots, marketplace listings, reward history)
- `form` → a dynamically rendered form that actually submits to the real
  endpoint named in the directive (e.g. `schedule_pickup` renders a form
  that POSTs to `/pickups`)
- `text` → falls back to real RAG retrieval + LLM (packages/ai/rag,
  packages/ai/llm), with the same honest Ollama-unavailable fallback used
  elsewhere — never fabricates a response

**Why intent classification is regex, not an LLM call:** which UI
component renders is a structural decision that has to be reliable. An
LLM guessing "form vs chart" would occasionally guess wrong in ways users
can't predict. The LLM is reserved for what it's actually good at —
free-text explanation — inside the `text` fallback.

Try it at `/assistant` (linked from the landing nav and the citizen
dashboard sidebar) — e.g. "how much waste do I have", "schedule a pickup",
"show marketplace listings".

## Zero fabricated numbers anywhere — audit pass

Two real gaps were found and fixed:

1. **Municipality Forecasts page** previously generated a client-side
   `SAMPLE_HISTORY` array and passed it to the forecasting API as if it
   were real — indistinguishable from real data in the result. Fixed:
   `GET /api/v1/forecasting/history` now aggregates *actual* `Waste` rows
   by day (real SQL `GROUP BY`), and the page refuses to run a forecast
   until at least 14 real days of history exist — showing an honest "not
   enough history yet (`n`/14 days)" state instead. Same fix applied to the
   assistant's `forecast` intent (`packages/ai/orchestrator/ui_resolver.py`),
   now aggregating the caller's own real waste-with-quantity rows.
2. **Collector route optimizer** previously ran against a hardcoded
   `SAMPLE_STOPS` array. Fixed: `GET /api/v1/pickups/my-route-stops`
   returns the collector's actual assigned/accepted pickups; the page
   requires a real registered collection-point facility as the depot
   (picked from `GET /facilities?type=collection_point`) and shows an
   empty state if either is missing — never substitutes fake stops.

Also removed every **hardcoded coordinate form-default** (facility
registration, pickup request) that a user could accidentally submit
unedited as if it were their real location — those fields now start empty
and offer a real `navigator.geolocation` "use my current location" button
(`hooks/useGeolocation.ts`) instead.

`db/seeds/demo_users.py` renamed to `db/seeds/dev_accounts.py` — same
opt-in-only behavior (never auto-run), just without "demo" framing. Every
remaining "demo"-adjacent word in the codebase was an honesty *disclosure*
label (e.g. the scan result banner that says a result came from the
untrained placeholder model) — kept and reworded for clarity, since hiding
that disclosure would be the actual violation.

## Second audit pass — dashboard stat cards

Found and fixed: several role dashboards had hardcoded `value={0}` or
`value="0"` stat cards that never reflected real state (they'd show "0"
forever even with real jobs/pickups behind them). Fixed:

- **Citizen dashboard**: "Pending pickups" now counts real non-terminal
  pickups from `GET /pickups`.
- **Business dashboard**: "Pending pickups" (real, same query) and
  "Diversion rate" (real, from `GET /waste/sustainability/summary`).
- **Collector dashboard**: "Open jobs" and "Completed today" now come from
  real pickup queries filtered by actual status and date. "Earnings" had no
  backing ledger at all — replaced the fake `₹0` with an honest empty state
  explaining that no earnings model exists yet, instead of a number that
  looked real but wasn't.
- **Recycler dashboard**: added `GET /api/v1/purchases/mine` (was entirely
  missing — the Purchases page was also just an empty-state placeholder
  before this) and wired it into both the dashboard stat and the Purchases
  page. Removed "Inventory (kg)" — no inventory ledger exists — replaced
  with "Registered facilities" (real count).

The remaining `22.5726` / `88.3639` mentions anywhere in the UI are now
only inside `placeholder="e.g. 22.5726"` hints on empty input fields —
greyed-out example text that's never submitted as a value, not a value
itself. Every coordinate `value={}` binding starts empty and is filled only
by real `navigator.geolocation` or by the user typing.
