const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const uploadVideo = async () => {
    try {
        const videoPath = '/home/shravan/builds/bits-hackathon/Vid/videoplayback.mp4'; // Change this to your actual video file path
        const formData = new FormData();
        formData.append('video', fs.createReadStream(videoPath));
        
        const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
            headers: {
                ...formData.getHeaders()
            }
        });
        
        console.log('Response:', response.data);
    } catch (error) {
        console.error('Error uploading video:', error);
    }
};

uploadVideo();
