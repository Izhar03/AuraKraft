# AuraKraft 

An emotion-aware music player that creates the perfect soundtrack for your mood.

## Overview

AuraKraft is an innovative application that harmonizes emotion recognition with music playback, creating a uniquely personalized listening experience. By utilizing your webcam and advanced AI, the app detects your current emotional state and curates Spotify playlists that resonate with your mood.

## Features

- Real-time emotion detection through webcam
- Spotify integration for dynamic playlist generation
- Emotion-based music recommendations
- Mental health-focused music therapy elements
- User emotion tracking and analysis

## Tech Stack

- **Backend Framework**: Flask
- **Computer Vision**: OpenCV
- **Machine Learning**: TensorFlow
- **Music Integration**: Spotipy (Spotify Web API)
- **ML Acceleration**: Groq API

## Prerequisites

- Python 3.8+
- Functional webcam
- Spotify account
- Groq API key

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd aurakraft
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create a .env file with the following:
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   GROQ_API_KEY=your_groq_api_key
   ```

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Access the web interface**
   - Open your browser and navigate to `http://localhost:5000`
   - Grant camera permissions when prompted
   - Log in with your Spotify account

3. **Begin your emotion-aware music journey**
   - Face the camera
   - Let AuraKraft detect your emotion
   - Enjoy automatically curated music that matches your mood

## User Flow

Below is a detailed workflow diagram showing how users interact with AuraKraft:

![image_alt](https://github.com/Izhar03/AuraKraft/blob/68159592eeb61f7e0d891db6e1783398b9926a37/Flow.png)

The diagram above illustrates the complete user journey from accessing the application to exiting, including all possible interaction paths and decision points.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please:
- Open an issue in the repository
- Contact the development team at izharhamdan@gmail.com


--- 


Built with ❤️ by the AuraKraft Team
