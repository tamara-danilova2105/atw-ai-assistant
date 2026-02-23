lint:
	poetry run ruff check .

format:
	poetry run ruff format .

typecheck:
	poetry run pyright

check: lint typecheck