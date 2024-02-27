from utils import SilentLogger
import yt_dlp

def download_video(url, output_name, session):
  ydl_opts = {
    'format': 'bv+ba/b',
    'outtmpl': output_name,
    'quiet': True,
    'no_progress': True,
    'http_headers': session,
    'logger': SilentLogger(),
    'concurrent_fragment_downloads': 7,
    'fragment_retries': 50,
    'retry_sleep_functions': {'fragment': 30},
    'buffersize': 104857600,
    'retries': 30,
    'continuedl': True,
    'extractor_retries': 10,
  }
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
