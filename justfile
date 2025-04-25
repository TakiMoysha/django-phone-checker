set dotenv-load

# example: just manage runserver
manage *ARGS:
  uv run python phonechecker/manage.py {{ ARGS }}
