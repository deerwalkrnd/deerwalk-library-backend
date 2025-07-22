run:
	uv run uvicorn app.main:app --reload

seed_admin:
	uv run -m app.cli.seed_admin

ruff:
	uv run ruff format .

isort:
	uv run isort .