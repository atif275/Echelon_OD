function startStream() {
    // Send a request to start the stream
    fetch('/start_stream')
        .then(response => response.json())
        .then(data => {
            console.log('Start Stream:', data);
            document.getElementById('videoStream').src = '/video_feed';  // Updated line
        });
}

function stopStream() {
    // Send a request to stop the stream
    fetch('/stop_stream')
        .then(response => response.json())
        .then(data => {
            console.log('Stop Stream:', data);
            document.getElementById('videoStream').src = ''; // Clear the video source
        });
}

function toggleDropdown() {
    var dropdownContent = document.getElementById("dropdownContent");
    dropdownContent.style.display = (dropdownContent.style.display === "block") ? "none" : "block";
  }
  
  function playVideo(videoSource) {
    var videoPlayer = document.getElementById("videoPlayer");
    videoPlayer.src = videoSource;
    videoPlayer.load();
    videoPlayer.play();
    toggleDropdown(); // Close the dropdown after selecting a video
  }

  // script.js

// Define a function to fetch and parse the JSON file
    async function fetchVideos() {
        try {
            const response = await fetch('/static/list_videos');
            const videos = await response.json();
            return videos;
        } catch (error) {
            console.error('Error fetching videos:', error);
            return [];
        }
    }
    
    // Define a function to dynamically populate the dropdown
    async function populateDropdown() {

        const videos = await fetchVideos();
        const dropdownContent = document.getElementById('dropdownContent');

        // Clear existing options
        dropdownContent.innerHTML = '';

        // Add options based on the video details
        videos.forEach(video => {
            const option = document.createElement('a');
            option.href = '#';
            option.className = 'dropdown-item';
            option.textContent = video;
            option.onclick = () => {
                console.log('Selected Video URL:', `/videos/${video}`);
                playVideo(`/videos/${video}`);
            };
            dropdownContent.appendChild(option);
        });
    }
    
    
  
  // Call the function to populate the dropdown on page load
populateDropdown();
  