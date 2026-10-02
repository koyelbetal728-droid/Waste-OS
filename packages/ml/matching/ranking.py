from packages.ml.matching.matcher import rank_recyclers


def rank(listing_lat: float, listing_lon: float, recyclers: list[dict]) -> list[dict]:
    return rank_recyclers(listing_lat, listing_lon, recyclers)
