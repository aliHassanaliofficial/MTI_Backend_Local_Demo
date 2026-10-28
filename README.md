# MTI — Local backend demonstration 0.1.0

STATUS: Internal proof of concept, NOT production, NOT the complete v5 implementation.

## What is real
Python application code with FastAPI routes, SQLite persistence, input validation,
parameterized database queries, and missing-record / duplicate-deal handling.
A request -> offer -> draft demo deal path is implemented.
Creating a demo deal does NOT constitute acceptance of an offer or a contract.

## What is not implemented
Authentication, tenant isolation, approval workflow, vault architecture, immutable audit,
licensed-provider integration, payments, contract signing, frontend connection,
production database migrations, concurrency hardening, backups or deployment.
Do NOT expose this server publicly. Do NOT enter personal data, credentials, contracts,
or real financial information. No funds are held or moved.
SQLite is a local demonstration choice, not an approved replacement for PostgreSQL.

## Run locally (developer instructions)
Install Python 3.11 or later, then in the extracted folder:

python -m venv .venv

Windows: .venv\Scripts\activate
macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8000

Open http://127.0.0.1:8000/docs

1. POST /v1/trade-requests with a fictional title; copy its id.
2. POST /v1/trade-requests/{request_id}/offers with a fictional amount/currency; copy id.
3. POST /v1/offers/{offer_id}/demo-deal; copy the deal id.
4. GET /v1/deals/{deal_id}.
5. Restart server and retrieve the deal again to check persistence.

## Verification honestly performed during packaging
Python AST syntax parsing passed. ZIP contents and non-empty files checked.
No live FastAPI server, PostgreSQL, browser integration or security assessment was run.
Dependency versions must be resolved, vulnerability-scanned and locked by developers
before any shared environment; requirements here are not a reproducible production lockfile.

## Before a shared pilot
Implement and test authentication and per-organization authorization, tokenized data and
external vault boundaries, traceable approvals, protected audit records, concurrency
controls, migrations, secret management and a scoped security review.
Determine regulatory applicability with qualified advisers; no licensing claim is made.
