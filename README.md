# lexzig

Lexical and syntactical analyzer for a subset of the Zig programming language

## Contributing

1. Clone this repository

```bash
git clone https://github.com/aloussase/lexzig.git
```

3. Start a virtual environment.

```bash
python -m venv .venv

source .venv/bin/activate # For linux
```

2. Install the pip dependencies

```bash
python -m pip install -r requirements.txt
```

3. Do your changes.

4. **Test your changes** Any functionality added should be tested. Tests go in the
   `tests` directory. The naming convention should be `test_<feature>.py` so that
   unittest can discover it. For more on testing with Python see:
   https://realpython.com/python-testing/.

```bash
# Using the Makefile
make test

# Or with python
python -m unittest discover -s tests
```

5. Open a PR.

## License

MIT
