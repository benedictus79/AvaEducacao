from utils import SilentLogger, random_sleep
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
  while True:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      try:
        ydl.download([url])
        return
      except yt_dlp.utils.DownloadError as e:
        if '403' or '429' in str(e):
          msg = f'''Verifique manualmente, se não baixou tente novamente mais tarde: {ydl_opts['outtmpl']} ||| {url}'''
          return
      except PermissionError as e:
        random_sleep()
