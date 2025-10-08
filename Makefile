.PHONY: run lint fmt test

run:
uvicorn app.main:app --reload

lint:
@echo "linting disabled for brevity"

fmt:
@echo "formatting disabled"

test:
pytest -q
