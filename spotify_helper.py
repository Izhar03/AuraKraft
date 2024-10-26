import os
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def get_spotify_client():
    # Retrieve credentials from environment variables
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    # Set up the Spotify client with credentials from the environment
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_songs_by_mood(mood):
    sp = get_spotify_client()
    
    # Map emotions to search terms
    mood_mapping = {
        'Happy': 'happy upbeat',
        'Sad': 'sad emotional',
        'Angry': 'angry intense',
        'Surprised': 'exciting energetic',
        'Fearful': 'calm relaxing',
        'Disgusted': 'powerful aggressive',
        'Neutral': 'chill ambient'
    }
    
    search_term = mood_mapping.get(mood, 'popular')
    random_offset = random.randint(0, 50)  # Randomly choose an offset between 0 and 50
    
    results = sp.search(
        q=f'{search_term}',
        type='track',
        limit=10,
        offset=random_offset
    )
    
    songs = []
    for track in results['tracks']['items']:
        songs.append({
            'name': track['name'],
            'artist': track['artists'][0]['name']
        })
    
    return songs