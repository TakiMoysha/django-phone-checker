set dotenv-load

# example: just manage runserver, just manage test phones
manage *ARGS:
  uv run python phonechecker/manage.py {{ ARGS }}

# example: just test -v -s -m tdd
test *ARGS:
  uv run pytest {{ ARGS }}

# example: just setup_db -q
setup_db *ARGS:
  uv run tooling/setup_db.py {{ ARGS }}

