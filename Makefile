.PHONY: run commit init

init:
	pip install uv && uv sync

run:
	uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8888

commit:
	echo "커밋 메시지를 입력하세요:"
	read msg
	git add .
	git commit -m "$msg"


