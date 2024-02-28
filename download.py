from utils import SilentLogger
import yt_dlp

def download_video(url, output_name, session):
  ydl_opts = {
    'format': 'bv[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best',
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
    'windows_filenames': True,
    'trim-filenames': 210,
    'extractor_retries': 10,
  }
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
