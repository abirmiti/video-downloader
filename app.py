import os
import tempfile
from flask import Flask, request, render_template_string, send_file
import yt_dlp

app = Flask(__name__)

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Universal Video Downloader</title>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
    body { background: #0f172a; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }
    .box { width: 100%; max-width: 520px; background: #1e293b; border-radius: 16px; padding: 30px; border: 1px solid #334155; box-shadow: 0 10px 30px rgba(0,0,0,0.5); text-align: center; }
    h1 { font-size: 24px; margin-bottom: 8px; color: #f8fafc; }
    p { color: #94a3b8; font-size: 14px; margin-bottom: 22px; }
    input { width: 100%; padding: 13px 15px; border-radius: 10px; border: 1px solid #475569; background: #0f172a; color: #fff; font-size: 14px; outline: none; margin-bottom: 15px; }
    input:focus { border-color: #6366f1; }
    button { width: 100%; padding: 13px; border-radius: 10px; border: none; background: #6366f1; color: #fff; font-weight: 700; font-size: 15px; cursor: pointer; transition: 0.2s; }
    button:hover { background: #4f46e5; }
    button:disabled { opacity: 0.6; cursor: not-allowed; }
    .status { margin-top: 15px; font-size: 13px; display: none; line-height: 1.5; }
  </style>
</head>
<body>
  <div class="box">
    <h1>🎬 Online Video Downloader</h1>
    <p>Paste video link (Dailymotion, YouTube, FB, etc.)</p>
    <input type="text" id="url" placeholder="https://www.dailymotion.com/video/..." />
    <button id="btn" onclick="startDownload()">Download Video</button>
    <div id="status" class="status"></div>
  </div>

  <script>
    function startDownload() {
      const url = document.getElementById('url').value.trim();
      const status = document.getElementById('status');
      const btn = document.getElementById('btn');

      if (!url) {
        alert('Please enter a video link!');
        return;
      }

      btn.disabled = true;
      btn.innerText = 'Downloading & preparing file...';
      status.style.display = 'block';
      status.style.color = '#818cf8';
      status.innerText = '⏳ Server is fetching the video. Your browser will start downloading shortly...';

      // Redirect to download endpoint
      window.location.href = '/download?url=' + encodeURIComponent(url);

      setTimeout(() => {
        btn.disabled = false;
        btn.innerText = 'Download Video';
        status.innerText = '✅ Download initiated! Check your browser downloads.';
        status.style.color = '#4ade80';
      }, 7000);
    }
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/download')
def download_video():
    url = request.args.get('url')
    if not url:
        return "No URL provided", 400

    temp_dir = tempfile.mkdtemp()
    ydl_opts = {
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'format': 'best[ext=mp4]/best',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Download Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
