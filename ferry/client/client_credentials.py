import os


def get_client_id() -> str:
    """
    Obtains Client ID token -- Initialized in environment variables.
    """
    return os.environ["CLIENT_ID"]


def get_client_secret() -> str:
    """
    Obtains Client SECRET token -- Initialized in environment variables.
    """
    return os.environ["CLIENT_SECRET"]
