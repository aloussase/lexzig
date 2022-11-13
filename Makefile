PYTHON := python3
MYPY := mypy
CLI := LexZig.py

TESTS := tests

all: test

test:
	$(PYTHON) -m unittest discover -v -s $(TESTS)

run:
	$(PYTHON) $(CLI)

typecheck:
	$(MYPY) lexzig
