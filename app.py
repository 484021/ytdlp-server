from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import tempfile
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        output_template = os.path.join(temp_dir, 'audio.%(ext)s')
        
        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
        }
        
        # Download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'audio')
            ext = info.get('ext', 'webm')
            
            # Find the downloaded file
            audio_file = os.path.join(temp_dir, f'audio.{ext}')
            
            if not os.path.exists(audio_file):
                # Try to find any audio file
                files = [f for f in os.listdir(temp_dir) if f.startswith('audio')]
                if files:
                    audio_file = os.path.join(temp_dir, files[0])
                else:
                    return jsonify({"error": "Downloaded file not found"}), 500
            
            # Return file info
            return jsonify({
                "title": title,
                "ext": ext,
                "file_path": audio_file,
                "size": os.path.getsize(audio_file)
            })
            
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
