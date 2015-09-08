help:
	@echo "Available targets"
	@echo ""
	@echo " * install: install required 'build' packages."
	@echo " * test: run tests using tox."
	@echo " * serve: serve the demo project"
	@echo " * docs: build the documentation"
	@echo " * help: display this help"
	@echo ""

install:
	pip install --upgrade tox pip

test:
	tox

serve:
	tox -e serve

docs:
	tox -e docs
