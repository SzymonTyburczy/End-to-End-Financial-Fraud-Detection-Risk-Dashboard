PYTHON = python
PIP = pip
UVICORN_PORT = 8001

.PHONY: help install up download load-db train pipeline run-api run-dashboard docker-up docker-down clean

help:
	@echo "===================================================================="
	@echo "PROJECT COMMAND CENTER"
	@echo "===================================================================="
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make pipeline      - Run FULL workflow (Docker -> Download -> DB -> Train)"
	@echo "  make up            - Start infrastructure (docker-compose up -d)"
	@echo "  make download      - Run scripts/download.py"
	@echo "  make load-db       - Run src/db_loader.py"
	@echo "  make train         - Train the model (run main_pipeline.py)"
	@echo "  make run-api       - Start FastAPI server on port $(UVICORN_PORT)"
	@echo "  make run-dashboard - Start Streamlit dashboard"
	@echo "  make docker-down   - Stop and remove Docker containers"
	@echo "  make clean         - Remove pycache files"
	@echo "===================================================================="

install:
	$(PIP) install -r requirements.txt

up:
	docker-compose up -d

download:
	$(PYTHON) scripts/download.py

load-db:
	$(PYTHON) src/db_loader.py

train:
	$(PYTHON) main_pipeline.py

pipeline: up download load-db train
	@echo "Pipeline finished successfully."

run-api:
	uvicorn api.main:app --reload --port $(UVICORN_PORT)

run-dashboard:
	streamlit run dashboard.py

docker-down:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +