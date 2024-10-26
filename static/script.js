const startButton = document.getElementById('startButton');
const videoContainer = document.getElementById('videoContainer');
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const result = document.getElementById('result');
const emotionSpan = document.getElementById('emotion');
const retryButton = document.getElementById('retryButton');

let stream;

// Function to start video streaming
async function startVideo() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        videoContainer.classList.remove('hidden');
    } catch (err) {
        alert('Error accessing webcam: ' + err.message);
    }
}

// Function to capture image from video
function captureImage() {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/jpeg');
    return dataURL;
}

// Function to send image to backend and get emotion
async function getEmotion(imageData) {
    try {
        const response = await fetch('/detect_emotion', {  // Updated this line
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });

        const data = await response.json();

        if (response.ok) {
            return data.emotion;
        } else {
            throw new Error(data.error || 'Unknown error');
        }
    } catch (err) {
        alert('Error: ' + err.message);
    }
}


// Function to handle the emotion detection flow
async function handleEmotionDetection() {
    startButton.classList.add('hidden');
    await startVideo();

    // Wait for the video to start
    video.addEventListener('loadeddata', async () => {
        // Capture image after 5 seconds
        setTimeout(async () => {
            const imageData = captureImage();
            stopVideo();

            // Show loading or processing message
            emotionSpan.textContent = 'Detecting...';
            result.classList.remove('hidden');

            const emotion = await getEmotion(imageData);
            emotionSpan.textContent = emotion || 'Could not detect emotion';
        }, 5000);
    }, { once: true });
}


async function fetchSongs(emotion) {
    try {
        const response = await fetch(`/get_songs/${emotion}`);
        const data = await response.json();
        
        if (response.ok) {
            displaySongs(data.songs);
        } else {
            throw new Error(data.error || 'Failed to fetch songs');
        }
    } catch (error) {
        console.error('Error fetching songs:', error);
        alert('Failed to fetch songs. Please try again.');
    }
}

function displaySongs(songs) {
    const songsContainer = document.getElementById('songs');
    const songList = document.getElementById('songList');
    
    songsContainer.innerHTML = '';
    songs.forEach(song => {
        const songElement = document.createElement('div');
        songElement.className = 'song-card';
        songElement.innerHTML = `
            <div class="song-title">${song.name}</div>
            <div class="song-artist">${song.artist}</div>
        `;
        
        songElement.addEventListener('click', () => fetchSongDetails(song.name, song.artist));
        songsContainer.appendChild(songElement);
    });
    
    songList.classList.remove('hidden');
}

async function fetchSongDetails(songName, artistName) {
    try {
        const songList = document.getElementById('songList');
        const songDetails = document.getElementById('songDetails');
        const detailsContent = document.getElementById('detailsContent');
        
        // Show loading state
        detailsContent.innerHTML = '<div class="loading"></div>';
        songList.classList.add('hidden');
        songDetails.classList.remove('hidden');
        
        const response = await fetch('/get_song_details', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ song_name: songName, artist_name: artistName })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            detailsContent.textContent = data.details;
        } else {
            throw new Error(data.error || 'Failed to fetch song details');
        }
    } catch (error) {
        console.error('Error fetching song details:', error);
        detailsContent.textContent = 'Failed to load song details. Please try again.';
    }
}

// Modify the existing handleEmotionDetection function
async function handleEmotionDetection() {
    startButton.classList.add('hidden');
    await startVideo();

    video.addEventListener('loadeddata', async () => {
        setTimeout(async () => {
            const imageData = captureImage();
            stopVideo();

            emotionSpan.textContent = 'Detecting...';
            result.classList.remove('hidden');

            const emotion = await getEmotion(imageData);
            emotionSpan.textContent = emotion || 'Could not detect emotion';
            
            if (emotion) {
                // Fetch songs based on detected emotion
                await fetchSongs(emotion);
            }
        }, 5000);
    }, { once: true });
}

// Add event listener for back button
document.getElementById('backToSongs').addEventListener('click', () => {
    document.getElementById('songDetails').classList.add('hidden');
    document.getElementById('songList').classList.remove('hidden');
});

// Modify the retry button event listener
retryButton.addEventListener('click', () => {
    result.classList.add('hidden');
    emotionSpan.textContent = '';
    document.getElementById('songList').classList.add('hidden');
    document.getElementById('songDetails').classList.add('hidden');
    startButton.classList.remove('hidden');
});

// Function to stop video streaming
function stopVideo() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    videoContainer.classList.add('hidden');
    canvas.classList.add('hidden');
}

// Event listener for start button
startButton.addEventListener('click', handleEmotionDetection);

// Event listener for retry button
retryButton.addEventListener('click', () => {
    result.classList.add('hidden');
    emotionSpan.textContent = '';
    startButton.classList.remove('hidden');
});
