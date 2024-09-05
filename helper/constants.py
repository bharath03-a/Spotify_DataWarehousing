# Spotify API 
TOKEN_URL = "https://accounts.spotify.com/api/token"
TOKEN_HEADER = {"Content-Type" : "application/x-www-form-urlencoded"}
TOKEN_REQUEST_BODY = {
    "grant_type" : "client_credentials",
    "client_id" : "<client_id>",
    "client_secret" : "<client_secret>"
}

CLIENT_ID = "96492b24e4e4451aab57111b69c56b9a"
CLIENT_SECRET = "8ade0b30e21e434c9661d738e208e7e8"

API = "https://api.spotify.com/v1/<PLACE_HOLDER>"
PLAYLIST_API = "playlists/<PLAYLIST_ID>/tracks"
PLAYLIST_ID = "7x7TlR1Z4T2vtje93uhdtm"
API_HEADER = {"Authorization": "Bearer <ACCESS_TOKEN>"}

API_QUERY = {
    "ARTISTS" : "artists?ids=<IDS>",
    "AUDIO_FEATURES" : "audio-features?ids=<IDS>"}

AUDIO_ANALYSIS_API = "audio-analysis/<ID>"

PLAYLIST_CSV_PATH = "./data/spotify_playlist.csv"
PLAYLIST_JSON_PATH = "./data/spotify_playlist.json"

ARTIST_CSV_PATH = "./data/spotify_artist.csv"
ARTIST_JSON_PATH = "./data/spotify_artist.json"

AUDIO_CSV_PATH = "./data/spotify_audio.csv"
AUDIO_JSON_PATH = "./data/spotify_audio.json"

PLAYLIST_KEYS = {
    'added_at', 'added_by', 'id', 'type', 'track', 'album', 'album_type', 'name', 'release_date',
    'release_date_precision', 'uri', 'artists', 'total_tracks', 'disc_number', 'track_number', 
    'duration_ms', 'popularity'
    }

ARTIST_KEYS = {
    'followers', 'total', 'genres', 'id', 'name', 'popularity', 'type'
}

AUDIO_KEYS = {
    'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
    'liveness', 'valence', 'tempo', 'type', 'id', 'duration_ms', 'time_signature'
}

# Snowflake Table Schema
AUDIO_FEATURES_SCHEMA = "(danceability float, energy float, key integer, loudness float, mode integer, \
                         speechiness float, acousticness float, instrumentalness float, \
                         liveness float, valence float, tempo float, id STRING(50), duration_ms integer,\
                         time_signature integer)"

ARTISTS_SCHEMA = "(followers_count integer, name STRING(50), artist_genres STRING(50), id STRING(50), popularity integer)"