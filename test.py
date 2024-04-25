import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up Spotify API credentials
CLIENT_ID = '225ed883ac7843f6bb06d7fa11bd9425'
CLIENT_SECRET = '66079bba02ef4080b2544174d45bd9f4'
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'user-library-read playlist-read-private'

# Token file path
TOKEN_FILE = 'token.txt'

# Function to get Spotify token
def get_token():
    # Check if token file exists
    if os.path.exists(TOKEN_FILE):
        # Load token from file
        with open(TOKEN_FILE, 'r') as f:
            token = f.read()
        return token

    # Request new token
    sp_oauth = spotipy.oauth2.SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )
    auth_url = sp_oauth.get_authorize_url()
    print(f'Go to the following URL and authorize the app: {auth_url}')

    # Wait for the user to authorize the app and get the response code
    response_code = input('Enter the response code: ').strip()

    # Get the access token
    token_info = sp_oauth.get_access_token(response_code)
    token = token_info['access_token']

    # Save the token to a file
    with open(TOKEN_FILE, 'w') as f:
        f.write(token)

    return token

# Function to list personal playlists
def list_playlists(sp):
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        print(playlist['name'])

# Main function
def main():
    token = get_token()
    sp = spotipy.Spotify(auth=token)

    list_playlists(sp)

if __name__ == '__main__':
    main()