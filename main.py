from bs4 import BeautifulSoup
import requests
import spotipy
import config
from spotipy.oauth2 import SpotifyOAuth
def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]
#get the date
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD")
#bilboard url
URL = f"https://www.billboard.com/charts/hot-100/{date}"
#spotify id and secret

URL_REDIRECT = "http://example.com"
response = requests.get(URL)
website_html = response.text
soup = BeautifulSoup(website_html,"html.parser")
all_songs = soup.find_all(name="h3", id="title-of-a-story",class_="u-letter-spacing-0021")
song_titles =  [song.text.strip() for song in all_songs]
song_titles = remove_values_from_list(song_titles, 'Songwriter(s):')
song_titles = remove_values_from_list(song_titles, 'Producer(s):')
song_titles = remove_values_from_list(song_titles, 'Imprint/Promotion Label:')

#Authentication with Spotify
#Documentation : https://pypi.org/project/spotipy/
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
#get current user id: https://spotipy.readthedocs.io/en/2.13.0/#spotipy.client.Spotify.current_user
user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    #print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
       print(f"{song} doesn't exist in Spotify. Skipped.")

#create new playlist: https://spotipy.readthedocs.io/en/2.19.0/
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
#add song found to playlist
result = sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)