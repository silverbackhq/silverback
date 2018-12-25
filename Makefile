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


coverage:
	$(COVERAGE) run --source='.' manage.py test app
	$(COVERAGE) report -m


ci: test coverage lint
	@echo "\n==> All quality checks passed"


.PHONY: ci