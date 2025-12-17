# YT-DLP Server

A Python Flask server for downloading YouTube audio using yt-dlp.

## Deploy to Railway (Free)

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this folder or create a new repo
5. Railway will auto-detect and deploy
6. Copy the public URL

## Deploy to Render (Free)

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repo
5. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
6. Deploy and copy the URL

## Environment Variables

No environment variables needed!

## API Endpoints

### POST /download
Request body:
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

Response:
```json
{
  "title": "Video Title",
  "ext": "webm",
  "file_path": "/tmp/audio.webm",
  "size": 1234567
}
```

### GET /health
Health check endpoint.
