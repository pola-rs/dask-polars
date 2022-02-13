
.PHONY: clean fmt lint test

.venv:
	@python -m venv .venv
	@.venv/bin/pip install -U pip
	@.venv/bin/pip install -r build.requirements.txt

test: .venv
	@.venv/bin/pytest dask_polars/tests

clean:
	@rm -r .venv

fmt: .venv
	@.venv/bin/isort .
	@.venv/bin/black .

lint: .venv
	@.venv/bin/flake8 .
	@.venv/bin/mypy

pre-commit: fmt lint
