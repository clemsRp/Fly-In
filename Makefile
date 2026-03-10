NAME = flyin
EXEC = python
DEBUGER = pdb

install:
	uv init
	uv add mypy
	uv add flake8
	uv add pydantic
	uv add numpy
	uv add PyQt6

run:
	uv run $(EXEC) -m $(NAME)

debug:
	uv run $(EXEC) -m $(DEBUGER) $(NAME)

lint:
	flake8 . --exclude=.venv
	mypy .
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8 . --exclude=.venv
	mypy . --strict

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf *.pyc
	rm -rf .venv

.PHONY: install run debug lint lint-strict clean