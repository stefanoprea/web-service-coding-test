import os


def get_database_url():
    ENV_VAR = "DATABASE_URL"
    database_url = os.getenv(ENV_VAR)
    if not database_url:
        raise Exception(f"Please provide environment variable {ENV_VAR}")
    return database_url

database_url = get_database_url()
