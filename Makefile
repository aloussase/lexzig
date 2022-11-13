PYTHON := python

TESTS := tests

all: test

test:
	$(PYTHON) -m unittest discover -v -s $(TESTS)
