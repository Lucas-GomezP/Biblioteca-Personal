def split_artists(value):
    if not value:
        return []

    return [
        artist.strip()
        for artist in value.split(",")
        if artist.strip()
    ]