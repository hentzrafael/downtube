from celery import shared_task
from celery_progress.backend import ProgressRecorder
import os
from pytube import Playlist, YouTube
from moviepy.editor import *

@shared_task(bind=True)
def download_playlist(self,url, path,only_audio=False):
    yt = Playlist(url)
    progress_recorder = ProgressRecorder(self)
    for index,item in enumerate(yt.video_urls):
        yout = YouTube(item)
        if only_audio == "True":
            out_file = yout.streams.filter(progressive=True,mime_type='video/mp4').first().download(path)
            videoclip = VideoFileClip(out_file)
            audioclip = videoclip.audio
            audioclip.write_audiofile(out_file[0:-4] + '.mp3',ffmpeg_params=['-metadata', 'title='+yout.title,'-metadata', 'artist='+yout.author,'-metadata', 'album='+yout.author])
            videoclip.close()
            audioclip.close()
            os.remove(out_file)
        else:
            yout.streams.filter(only_audio=False,only_video=False,progressive=True).get_highest_resolution().download(path)
        progress_recorder.set_progress(index + 1, len(yt.video_urls), f'Downloading {index+1}/{len(yt.video_urls)}')

@shared_task(bind=True)
def download_video(self,url, path:str,only_audio=False):
    yout = YouTube(url)
    progress_recorder = ProgressRecorder(self)
    if only_audio == "True":
        progress_recorder.set_progress(0, 2, f'Downloading Video...')
        out_file = yout.streams.filter(progressive=True,mime_type='video/mp4').first().download(path)
        videoclip = VideoFileClip(out_file)
        audioclip = videoclip.audio
        progress_recorder.set_progress(1, 2, f'Converting to Audio...')
        audioclip.write_audiofile(out_file[0:-4] + '.mp3',ffmpeg_params=['-metadata', 'title='+yout.title,'-metadata', 'artist='+yout.author,'-metadata', 'album='+yout.author])
        videoclip.close()
        audioclip.close()
        os.remove(out_file)
        progress_recorder.set_progress(2, 2, f'Done!')
    else:
        progress_recorder.set_progress(0, 1, f'Downloading Video...')
        yout.streams.filter(only_audio=False,only_video=False,progressive=True).get_highest_resolution().download(path)
        progress_recorder.set_progress(1, 1, f'Done!')