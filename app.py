from flask import Flask, render_template, Response, jsonify, request
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import BatchNormalization
import json
import tensorflow as tf
from groq import Groq
import os
from spotify_helper import get_songs_by_mood
import base64

app = Flask(__name__)

# Hardcoded API key (not recommended for production use)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Custom objects dictionary for model loading
custom_objects = {
    'BatchNormalization': BatchNormalization
}

# Load the pre-trained model with custom objects
emotion_model = load_model('FER_model.h5', custom_objects=custom_objects)
print("Model loaded successfully!")

# Print model summary to understand input/output shape
print(emotion_model.summary())

# Dictionary for emotion labels
emotion_dict = {
    0: 'Angry',
    1: 'Disgusted',
    2: 'Fearful',
    3: 'Happy',
    4: 'Neutral',
    5: 'Sad',
    6: 'Surprised'
}

def preprocess_face(face_img):
    """
    Preprocess the face image according to model requirements
    """
    face_img = cv2.resize(face_img, (48, 48))
    face_img = face_img.astype('float32')
    face_img = face_img / 255.0
    face_img = np.expand_dims(face_img, axis=0)
    if emotion_model.input_shape[-1] == 1:
        face_img = np.expand_dims(face_img, axis=-1)
    return face_img

def process_frame(frame):
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        if len(faces) > 0:
            areas = [w * h for (x, y, w, h) in faces]
            max_area_idx = np.argmax(areas)
            (x, y, w, h) = faces[max_area_idx]
            face_roi = gray[y:y+h, x:x+w]
            processed_face = preprocess_face(face_roi)
            prediction = emotion_model.predict(processed_face)
            emotion_idx = np.argmax(prediction[0])
            emotion_label = emotion_dict[emotion_idx]
            confidence = float(prediction[0][emotion_idx])
            return {
                'emotion': emotion_label,
                'confidence': confidence,
                'all_scores': {emotion_dict[i]: float(prediction[0][i]) for i in range(len(emotion_dict))}
            }
        return None
    except Exception as e:
        print(f"Error processing frame: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect_emotion', methods=['POST'])
def detect_emotion():
    try:
        image_data = request.json['image']
        encoded_data = image_data.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        result = process_frame(frame)
        if result:
            return jsonify(result)
        else:
            return jsonify({'error': 'No face detected'})
    except Exception as e:
        print(f"Error in detect_emotion: {str(e)}")
        return jsonify({'error': str(e)})

@app.route('/get_songs/<mood>')
def get_songs(mood):
    try:
        songs = get_songs_by_mood(mood)
        return jsonify({'songs': songs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_song_details', methods=['POST'])
def get_song_details():
    try:
        data = request.json
        song_name = data.get('song_name')
        artist_name = data.get('artist_name')
        
        client = Groq(api_key=GROQ_API_KEY)
        detailed_prompt = (
            f"Provide a comprehensive response divided into three parts for the song '{song_name}' by {artist_name}:\n\n"
            "1. Song History: Detail the origin, release information, and any notable events related to the song.\n"
            "2. Artist History: Provide background information about the artist or band that created the song.\n"
            "3. Fun Facts: List any interesting trivia or lesser-known facts about the song."
        )
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": detailed_prompt}],
            model="llama3-8b-8192",
        )
        
        response = chat_completion.choices[0].message.content
        return jsonify({'details': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
