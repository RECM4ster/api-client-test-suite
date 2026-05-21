# GoREST API Client Tests

Small typed Python client for the GoREST public API with unit and integration tests.

## Tech Stack

- Python 3.12
- httpx
- pytest
- pydantic
- respx
- ruff
- mypy

## Setup

Create virtual environment:

```bash
python -m venv .venv
```

Activate it:

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -e ".[dev]"
```

## Environment Variables

Create `.env` file:

```env
GOREST_BASE_URL=https://gorest.co.in/public/v2
GOREST_TOKEN=your_token_here
```

## Running Tests

### Unit tests

```bash
make test-unit
```

### Integration tests

```bash
make test-integration
```

## Linting

```bash
make lint
```

## Type checking

```bash
make typecheck
```

## Full Validation

Runs:
- linting,
- static type checking,
- unit tests.

```bash
make check
```

## Windows Without GNU Make

Windows users without GNU Make can run the commands directly:

```powershell
pytest tests/unit -v
pytest tests/integration -v
ruff check .
mypy --strict src
```


## Notes

- Unit tests run without network access.
- Integration tests hit the real GoREST API.
- Integration tests create and clean up their own test data.
- Integration tests are designed to run independently of execution order.