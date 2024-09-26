# YouTube Downloader

This project is a simple YouTube downloader built using Python with the `pytube`, `aiohttp`, and `ffmpeg` libraries. It provides a basic web server that allows users to download YouTube videos either as audio or video files.

## Setup

To run the YouTube downloader, follow these steps:

1. Install the required Python packages by running:
   ```
   pip install pytube aiohttp ffmpeg-python
   ```

2. Clone or download the project repository.

3. Navigate to the project directory in your terminal.

4. Run the following command to start the server:
   ```
   python main.py
   ```

5. The server should now be running, and you can access it at `http://localhost:<port>`, where `<port>` is the port number specified in the code (default is 8000).

## Usage

### Downloading Videos

To download a video, make a GET request to the root URL (`/`) with the following query parameters:

- `url`: The URL of the YouTube video you want to download.
- `format`: The desired format of the video. Options are `"audio"` for audio-only or specific resolutions like `"144p"`, `"240p"`, `"360p"`, `"480p"`, `"720p"`, `"1080p"`, etc.

Example:
```
GET /?url=https://www.youtube.com/watch?v=VIDEO_ID&format=audio
```

### Getting Video Details

To retrieve details about a YouTube video, make a GET request to the `/details` endpoint with the `url` query parameter set to the YouTube video URL.

Example:
```
GET /details?url=https://www.youtube.com/watch?v=VIDEO_ID
```

## Notes

- Downloaded files are stored in the `downloads` directory within the project folder.
- The server automatically cleans up the `downloads` directory by removing older files if it contains more than three files.
- If no proper parameters are provided or if the URL is incorrect, appropriate error responses are returned.
