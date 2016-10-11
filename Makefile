help:
	@echo "Available targets"
	@echo ""
	@echo " * install: install required 'build' packages."
	@echo " * test: run tests using tox."
	@echo " * serve: serve the demo project"
	@echo " * docs: build the documentation"
	@echo ""
	@echo " Clean methods"
	@echo " * clean-db: delete the demo database"
	@echo " * clean-tox: delete the tox virtualenvs"
	@echo " * clean-all: cleans everything"
	@echo ""
	@echo "Help?"
	@echo " * help: display this help"
	@echo ""

install:
	pip install --upgrade tox pip

test:
	tox

serve:
	tox -e serve

.PHONY: docs
docs:
	tox -e docs

.PHONY: clean-db
clean-db:
	@echo "Drop demo database"
	rm -f db.sqlite3

.PHONY: clean-tox
clean-tox:
	@echo "Delete tox venvs"
	rm -Rf .tox/

.PHONY: clean-all
clean-all: clean-db clean-tox
