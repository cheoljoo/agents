# Makefile for KOSPI50 and Investment Agents

.PHONY: help install run-kospi run-investment clean lint skills-sync

# Default target
help:
	@echo "Available commands:"
	@echo "  make install        - Install dependencies using uv"
	@echo "  make run-kospi      - Run KOSPI 50 agents pipeline"
	@echo "  make run-investment - Run Investment Committee agents"
	@echo "  make lint           - Run linting (ruff)"
	@echo "  make skills-sync    - Sync .github instructions to .gemini/skills"
	@echo "  make clean          - Remove temporary files (except .py files as per GEMINI.md)"

install:
	uv sync

run-kospi:
	uv run kospi-50/main.py

run-investment:
	uv run investment/main.py

lint:
	uv run ruff check .
lint-fix:
	uv run ruff check . --fix

skills-sync:
	@chmod +x scripts/sync_skills.sh
	./scripts/sync_skills.sh

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Cleaned up __pycache__ and .pyc files."
	@echo "Note: .py files are preserved as per project instructions."
