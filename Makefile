# Makefile for DebateGPT

# ENV
PYTHON := python
PIP := pip
APP := app.py
STREAMLIT_APP := streamlit_app.py
TEST_DIR := test

# Targets

install:
	$(PIP) install -r requirements.txt

run:
	. my_env/bin/activate && python app.py

ui:
	streamlit run $(STREAMLIT_APP)

test:
	pytest $(TEST_DIR) -s

lint:
	ruff check . --fix || true

export:
	$(PIP) freeze > requirements.txt

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -r {} +

.PHONY: install run ui test lint export clean
