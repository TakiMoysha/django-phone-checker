set dotenv-load

# example: just manage runserver
manage *ARGS:
  uv run python phonechecker/manage.py {{ ARGS }}

# example: just unittest -v -s
unittest *ARGS:
  uv run pytest {{ ARGS }}

setup_db:
  uv run tooling/setup_db.py -q

