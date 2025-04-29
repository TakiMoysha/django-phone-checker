set dotenv-load

# example: just manage runserver, just manage test phones
manage *ARGS:
  uv run python phonechecker/manage.py {{ ARGS }}

# example: just test phones
test *ARGS:
  USE_TEST_DATABASE=true \\
  uv run python phonechecker/manage.py test {{ ARGS }}

# example: just setup_db -q
setup_db *ARGS:
  uv run tooling/setup_db.py {{ ARGS }} \\
  uv run manage migrate \\
  uv run manage migrate --database db_inmemory

