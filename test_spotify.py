import os
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_spotify_client():
    # Use the credentials directly for testing purposes
    client_credentials_manager = SpotifyClientCredentials(
        client_id='your_client_id',
        client_secret='your_client_secret'
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

# Test the function with the mood 'Happy'
if __name__ == '__main__':
    mood = 'Happy'
    songs = get_songs_by_mood(mood)
    print(f"Songs for mood '{mood}':")
    for song in songs:
        print(f" - {song['name']} by {song['artist']}")
