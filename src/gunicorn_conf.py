workers = 4

bind = "0.0.0.0:8888"

worker_class = "uvicorn.workers.UvicornWorker"


loglevel = "info"


backlog = 2048


timeout = 120