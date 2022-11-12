PYTHON := python3
MYPY := mypy

TESTS := tests

all: test

test:
	$(PYTHON) -m unittest discover -v -s $(TESTS)

typecheck:
	$(MYPY) lexzig
