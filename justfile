set dotenv-load

APP_DIR := "src"

# example: just manage runserver, just manage test phones
manage *ARGS:
  uv run python {{APP_DIR}}/manage.py {{ ARGS }}

# example: just test phones -k TestServerTasks -v 2
test *ARGS:
  USE_TEST_DATABASE=true \\
  uv run python {{APP_DIR}}/manage.py test {{ ARGS }}

# example: just setup_db -q
setup_db *ARGS:
  uv run tooling/setup_db.py {{ ARGS }} \\
  uv run manage migrate \\
  uv run manage migrate --database db_inmemory

