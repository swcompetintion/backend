FROM python:3.13-slim 
WORKDIR /app

COPY . /app

RUN pip install uv && uv sync

CMD [".venv/bin/gunicorn", "-c", "src/gunicorn_conf.py", "src.main:app"]