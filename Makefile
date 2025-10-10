.PHONY: run commit init test

init:
	pip install uv && uv sync

run:
	uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8888

test:
	PYTHONPATH=. uv run pytest
