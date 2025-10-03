.PHONY: run commit init

init:
	pip install uv && uv sync

run:
	uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8888

