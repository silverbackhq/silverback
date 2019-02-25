PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
COVERAGE ?= coverage


config:
	$(PIP) install pycodestyle
	$(PIP) install coverage
	$(PIP) install flake8
	$(PIP) install -r requirements.txt


lint-pycodestyle:
	@echo "\n==> Pycodestyle Linting:"
	@find app -type f -name \*.py | while read file; do echo "$$file" && pycodestyle --config=./pycodestyle --first "$$file" || exit 1; done


lint-flake8:
	@echo "\n==> Flake8 Linting:"
	@find app -type f -name \*.py | while read file; do echo "$$file" && flake8 --config=flake8.ini "$$file" || exit 1; done


lint: lint-pycodestyle lint-flake8
	@echo "\n==> All linting cases passed!"


test:
	@echo "\n==> Run Test Cases:"
	$(PYTHON) manage.py test


migration:
	@echo "\n==> Make Migrations:"
	$(PYTHON) manage.py makemigrations


migrate:
	@echo "\n==> Migrate:"
	$(PYTHON) manage.py migrate


run:
	@echo "\n==> Run Server:"
	$(PYTHON) manage.py runserver


coverage:
	$(COVERAGE) run --source='.' manage.py test app
	$(COVERAGE) report -m


liteci: test coverage lint
	@echo "\n==> All quality checks passed"

ci: config test coverage lint
	@echo "\n==> All quality checks passed"


.PHONY: ci