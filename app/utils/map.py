__all__ = ("get_url_map",)


def get_url_map(coordinats: list, profile: str):
    result_url = "https://graphhopper.com/maps/?"

    for coordinat in coordinats:
        result_url += f"point={coordinat[0]}, {coordinat[1]}&"

    result_url += f"profile={profile}&layer=OpenStreetMap"

    return result_url
