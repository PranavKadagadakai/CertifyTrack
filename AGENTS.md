# CertifyTrack Agent Guidelines

## Build/Lint/Test Commands

### Backend (Django, uv)
- All tests: `uv run manage.py test`
- Single test: `uv run manage.py test api.tests.TestClass.test_method -v 2`
- Coverage: `uv run coverage run --source='api' manage.py test && uv run coverage report`
- Lint: `uv run ruff check api/`
- Lint fix: `uv run ruff check --fix api/`

### Frontend (React/Vite, pnpm)
- Install: `pnpm install`
- Dev: `pnpm dev`
- Build: `pnpm build`
- Lint: `pnpm lint`
- Lint fix: `pnpm lint:fix`

## Code Style Guidelines

### Python (Django)
- Imports: std lib → third-party → local; one per line
- Naming: snake_case vars/fns, PascalCase classes, UPPER_CASE constants
- Docstrings: triple quotes for public fns/classes
- Error handling: try/except, specific exceptions, logging
- Types: add hints where possible
- Formatting: PEP 8 (4 spaces, 79 chars)

### JavaScript/React
- Components: functional with hooks, PascalCase
- Imports: React → third-party → local
- State: useState/useEffect, no class components
- Error handling: try/catch in async, user-friendly messages
- Styling: Tailwind classes, mobile-first responsive
- File org: one component per file

### General
- Commits: conventional (feat:, fix:, etc.)
- Docs: update README/docstrings on changes
- Security: no secrets, validate inputs, parameterized queries
- Testing: 80%+ coverage, tests for new features