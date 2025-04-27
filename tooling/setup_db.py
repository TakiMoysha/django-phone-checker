#!.venv/bin/python

import os
import argparse
import sys
import psycopg
import getpass

from psycopg.errors import DuplicateDatabase, DuplicateObject


def create_dev_environment(connection_url):
    username = "phonechecker"
    database = "phonechecker"
    password = "phonechecker"

    SQL_CREATE_DB = f"CREATE DATABASE {database};"
    SQL_CREATE_USER = f"CREATE USER {username} WITH PASSWORD '{password}';"
    SQL_GRANT_PRIVILEGES = f"GRANT ALL PRIVILEGES ON DATABASE {database} TO {username};"
    SQL_GRANT_SCHEMA_PRIVILEGES = f"GRANT ALL ON SCHEMA public TO {username};"
    SQL_ALTER_OWNER = f"ALTER DATABASE {database} OWNER TO {username};"

    def _autocommit_exec(conn, sql):
        conn.autocommit = True
        try:
            conn.execute(sql)
        except (DuplicateDatabase, DuplicateObject) as e:
            print(f"DUPLICATION: {e}.")
        except psycopg.errors.OperationalError as e:
            print(f"Error: {e}, exit with code 1")
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)

    with psycopg.connect(connection_url) as conn:
        _autocommit_exec(conn, SQL_CREATE_USER)
        _autocommit_exec(conn, SQL_CREATE_DB)

    db_url = f"{connection_url}{database}"
    try:
        with psycopg.connect(db_url) as conn:
            with conn.cursor() as cur:
                cur.execute(SQL_GRANT_PRIVILEGES)
                cur.execute(SQL_GRANT_SCHEMA_PRIVILEGES)
                cur.execute(SQL_ALTER_OWNER)
    except psycopg.errors.OperationalError as e:
        print(f"Error: {e}, exit with code 1")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-url",
        type=str,
        default="localhost:5432",
        help="address:port [default: localhost:5432]",
    )
    parser.add_argument(
        "-u",
        "--username",
        default="postgres",
        help='username for connection or take value from TOOLS_POSTGRES_USER [default: "postgres"]',
    )
    parser.add_argument(
        "-q",
        "--quite",
        action="store_true",
        help='ignore password input and take "postgres" value or from TOOLS_POSTGRES_PASSWORD [default: False]',
    )
    args = parser.parse_args()

    username = args.username or os.getenv("TOOLS_POSTGRES_USER", "postgres")
    password = os.getenv("TOOLS_POSTGRES_PASSWORD", "postgres")

    if not args.quite:
        password = getpass.getpass() or password

    connect_url = f"postgresql://{username}:{password}@{args.url}/"
    create_dev_environment(connect_url)
