const axios = require("axios");
const FormData = require("form-data");
const fs = require("fs");

const uploadVideo = async () => {
  try {
    const videoPath =
      "/Users/fardeenshaikh/Documents/BITS-Hyd-Hackathon/python-backend/backend/video6.mp4"; // Change this to your actual video file path
    const formData = new FormData();
    formData.append("video", fs.createReadStream(videoPath));

    const response = await axios.post(
      "http://127.0.0.1:5001/upload",
      formData,
      {
        headers: {
          ...formData.getHeaders(),
        },
      }
    );

    console.log("\n=== Response Data ===");
    if (Array.isArray(response.data)) {
      console.table(response.data);
    } else {
      console.log(JSON.stringify(response.data, null, 2));
    }
    console.log("==================\n");
  } catch (error) {
    console.error("Error uploading video:", error);
  }
};

uploadVideo();
