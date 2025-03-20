const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const uploadVideo = async () => {
    try {
        const videoPath = 'C:\\Users\\INDRANEEL KVS\\skillscraft\\videoplayback (1).mp4'; // Change this to your actual video file path
        const formData = new FormData();
        formData.append('video', fs.createReadStream(videoPath));
        
        const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
            headers: {
                ...formData.getHeaders()
            }
        });
        
        console.log('Response:', response.data);
        const fdata = new FormData();
        fdata.append('report',response.data);
        await axios.post('http://127.0.0.1:5000/tts',fdata,{
            headers: {
                ...formData.getHeaders()
            }  
        });
    } catch (error) {
        console.error('Error uploading video:', error);
    }
};

uploadVideo();
