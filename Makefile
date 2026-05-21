setup:
	pip install -e ".[dev]"

test-unit:
	pytest tests/unit -v

test-integration:
	pytest tests/integration -v

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy --strict src

check: lint typecheck test