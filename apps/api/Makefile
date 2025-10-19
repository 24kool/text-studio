.PHONY: help run dev clean test

help:
	@echo "Text Studio API - Available Commands"
	@echo ""
	@echo "  make run        - Run the API server in development mode"
	@echo "  make dev        - Run the API server in development mode (alias for run)"
	@echo "  make clean      - Clean Python cache files"
	@echo "  make test       - Run tests (when available)"
	@echo "  make help       - Show this help message"

run:
	@echo "Starting API server..."
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

dev: run

clean:
	@echo "Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete!"

test:
	@echo "Running tests..."
	@echo "No tests configured yet."

