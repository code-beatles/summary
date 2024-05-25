VIRTUAL_ENV ?= .venv
PACKAGE = summary

#  Setup Dev Env
#  -------------

poetry.lock: pyproject.toml
	@poetry lock

$(VIRTUAL_ENV): poetry.lock
	@poetry install --with dev
	@poetry self add poetry-bumpversion
	@poetry run pre-commit install
	@poetry export --without-hashes --output assets/requirements.txt
	@touch $(VIRTUAL_ENV)

.PHONY: setup
setup: $(VIRTUAL_ENV)

.PHONY: t test
t test: setup
	@poetry run pytest $(PACKAGE)

.PHONY: lint
lint: setup
	@poetry run mypy
	@poetry run ruff api

# Database
# --------
migrate: setup
	@poetry run muffin $(PACKAGE) peewee-migrate

rollback: setup
	@poetry run muffin $(PACKAGE) peewee-rollback

# Run
# ---

MUFFIN_PORT ?= 5555
.PHONY: run dev
run dev: setup migrate
	@poetry run uvicorn --loop asyncio --reload --reload-dir $(PACKAGE) --port $(MUFFIN_PORT) $(PACKAGE):app

.PHONY: shell
shell: setup
	@poetry run muffin $(PACKAGE) shell --ipython
