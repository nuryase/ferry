from ferry.client.client_auth import get_access_token
from ferry.client.client_credentials import get_client_id, get_client_secret
import json
import requests

# import urllib.request
from urllib.parse import urlencode

endpoint = "https://api.spotify.com/v1/"
# endpoint = 'https://api.spotify.com/v1/recommendations'


class Client:
    _base_url: str
    _access_token: None

    def __init__(self, *, base_url: str = endpoint) -> None:
        self._base_url = base_url

    def _ensure_access_token(self) -> None:
        """
        Obtains/Ensures access token.

        Parameters:

            None
        """
        client_id = get_client_id()
        client_secret = get_client_secret()

        self._access_token = get_access_token(client_id, client_secret)

    def _api_get_search(self, endpoint: str, params: dict) -> None:
        """
        Create and exectute GET request to API with search endpoint.

        Parameters:

            params - dictionary of search queries (dict)

        Returns:

            Creates URL for GET request and outputs response data (if response 200)
        """
        self._ensure_access_token()

        headers = {"Authorization": "Bearer {}".format(self._access_token)}

        query = urlencode(params)

        url = f"{self._base_url}{endpoint}?{query}"

        data = requests.get(url, headers=headers)

        return data

    def search(self, search_query: str, type_query: str) -> None:
        """
        Search
        """
        data = self._api_get_search("search", {"q": search_query, "type": type_query})

        return data

    def _api_get_recommendations(self, params: dict) -> None:
        """
        Create and exectute GET request to API with recommendations endpoint.

        Parameters:

            params - dictionary of given seed entities (dict)

        Returns:

            Creates URL for GET request and outputs response data (if response 200)
        """
        self._ensure_access_token()
        headers = {"Authorization": "Bearer {}".format(self._access_token)}

        query = urlencode(params)
        endpoint = "recommendations"

        url = f"{self._base_url}{endpoint}?{query}"

        data = requests.get(url, headers=headers)

        return data

    def _get_artist_id(self, artist: str):
        """
        Helper method to obtain artist id from inputted string.

        Parameters:

            artist - artist name (str)

        Returns:

            Outputs artist id (str)
        """
        data = self.search(artist, "track")

        search_data = data.json()

        for track in search_data["tracks"]["items"]:
            for image in track["album"]["artists"]:
                artist_id = image["id"]
                break
            break
        return artist_id

    def _get_track_id(self, track: str):
        """
        Helper method to obtain track id from inputted string.

        Parameters:

            track - track name (str)

        Returns:

            Outputs track id (str)
        """
        data = self.search(track, "track")
        search_data = data.json()

        for track in search_data["tracks"]["items"]:
            track_id = track["id"]
            break

        return track_id

    def recommendations_search(self, artist: str, seed_genres: str, track: str):
        """
        Search for recommendations.

        Parameters:

            artist - name of artist(s) (str)
            seed_genres - seed genre(s) for recommendations (str)
            track - track name(s) for recommendations (str)

        Returns:

            Outputs recommendation metadata.
        """
        limit = 10
        seed_artist = self._get_artist_id(artist)
        seed_track = self._get_track_id(track)
        data = self._api_get_recommendations(
            {
                "limit": limit,
                "seed_artists": seed_artist,
                "seed_genres": seed_genres,
                "seed_tracks": seed_track,
            }
        )

        return data

    def get_recommendations(self, data) -> None:
        """
        Uses recommendation search to obtain recommended artists based on params.

        Parameters:

            data - recommendation data (JSON)

        Returns:
            Outputs recommended artist, track, artist profile link, and track cover art.
        """
        search_data = data.json()
        recommendations = ""

        for i in range(10):
            for d in search_data["tracks"][i]["album"]["artists"]:
                recommendations += "Artist: " + d["name"] + "\n"

                recommendations += "Song: " + search_data["tracks"][i]["name"] + "\n"

                for _ in d["external_urls"]["spotify"]:
                    pass

                recommendations += "\n"

        return recommendations
