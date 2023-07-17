from ferry.client.client_credentials import get_client_id, get_client_secret

import base64
import json
import requests

# Query Parameters // Set Client ID and Client Secret
CLIENT_ID = get_client_id()
CLIENT_SECRET = get_client_secret()


def get_access_token(CLIENT_ID, CLIENT_SECRET) -> json:
    """
    Uses Client Credentials Flow to request authorization and obtain access token.
    """
    auth_code = base64.b64encode(
        (CLIENT_ID + ":" + CLIENT_SECRET).encode("ascii")
    ).decode("ascii")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + auth_code,
    }
    payload = {"grant_type": "client_credentials"}

    response = requests.post(
        "https://accounts.spotify.com/api/token", data=payload, headers=headers
    )
    # Check if response OK before obtaining access token.
    if response.status_code == 200:
        data = response.json()
        formatted_data = json.dumps(
            response.json(), indent=4
        )  # formats into example from Spotify documentation
        token = data["access_token"]
        return token


access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
