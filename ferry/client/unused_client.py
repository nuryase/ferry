# Unused Client method to get cover image


def get_cover(self, data) -> None:
    """
    Obtains track cover art.

    Parameters:

       data - track data (JSON)

    Returns:

       Outputs track cover art in three size formats.
    """

    search_data = data.json()

    for track in search_data["tracks"]["items"]:
        print("")
        print("Image URL: {}".format(track["name"]))

        for image in track["album"]["images"]:
            cover_url = image["url"]

            print("")
            print(cover_url)

        print("")
        break

    # Old get_recommendations method that output cover image and profile links
    def get_recommendations(self, data) -> None:
        """
        Uses recommendation search to obtain recommended artists based on params.

        Parameters:

            data - recommendation data (JSON)

        Returns:
            Outputs recommended artist, track, artist profile link, and track cover art.
        """

        # Start here
        search_data = data.json()
        recommendations = ""

        # print("")
        for i in range(10):
            for d in search_data["tracks"][i]["album"]["artists"]:
                # print("Artist:", d["name"])
                recommendations += "Artist: " + d["name"] + "\n"
                # print("Song:", search_data["tracks"][i]["name"])
                recommendations += "Song: " + search_data["tracks"][i]["name"] + "\n"
                # Get Image
                # image_data = self.search(search_data["tracks"][i]["name"], "track")
                # self.get_cover(image_data)

                for _ in d["external_urls"]["spotify"]:
                    pass

                recommendations += "\n"
                # print("Profile Link:", d["external_urls"]["spotify"])
                # print("")
        return recommendations
