help:
	@echo "Available targets"
	@echo ""
	@echo " * install: install required 'build' packages."
	@echo " * test: run tests using tox."
	@echo " * help: display this help"
	@echo ""

install:
	pip install --upgrade tox pip

test:
	tox
