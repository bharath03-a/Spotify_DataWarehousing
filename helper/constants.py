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
    "TRACKS" : "tracks?ids=<IDS>"}

PLAYLIST_CSV_PATH = "./data/spotify_playlist.csv"
PLAYLIST_JSON_PATH = "./data/spotify_playlist.json"

ARTIST_CSV_PATH = "./data/spotify_artist.csv"
ARTIST_JSON_PATH = "./data/spotify_artist.json"

TRACK_CSV_PATH = "./data/spotify_track.csv"
TRACK_JSON_PATH = "./data/spotify_track.json"