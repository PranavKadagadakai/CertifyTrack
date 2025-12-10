# CertifyTrack Agent Guidelines

## Build/Lint/Test Commands

### Backend (Django)
- Run all tests: `python manage.py test`
- Run specific test: `python manage.py test api.tests.TestClass.test_method -v 2`
- Coverage: `coverage run --source='api' manage.py test && coverage report`
- Lint: `ruff check api/`
- Lint fix: `ruff check --fix api/`

### Frontend (React/Vite)
- Install: `pnpm install`
- Dev server: `pnpm dev`
- Build: `pnpm build`
- Lint: `pnpm lint`
- Lint fix: `pnpm lint:fix`

## Code Style Guidelines

### Python (Django)
- Imports: Std lib → third-party → local; one per line.
- Naming: snake_case vars/fns, PascalCase classes, UPPER_CASE constants.
- Docstrings: Triple quotes for public fns/classes.
- Error Handling: try/except, specific exceptions, logging.
- Types: Add hints where possible.
- Formatting: PEP 8 (4 spaces, 79 chars).

### JavaScript/React
- Components: Functional with hooks, PascalCase.
- Imports: React → third-party → local.
- State: useState/useEffect, no class components.
- Error Handling: try/catch in async, user-friendly messages.
- Styling: Tailwind classes, mobile-first responsive.
- File Org: One component per file.

### General
- Commits: Conventional (feat:, fix:, etc.)
- Docs: Update README/docstrings on changes.
- Security: No secrets, validate inputs, parameterized queries.
- Testing: 80%+ coverage, tests for new features.