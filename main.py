from pytube import Playlist, YouTube
def download(url, path):
    yt = Playlist(url)
    for item in yt.video_urls:
        yout = YouTube(item)
        yout.streams.filter(only_audio=False,only_video=False,progressive=True).get_highest_resolution().download(path)

download("https://www.youtube.com/playlist?list=PL85ITvJ7FLogLBIWuoRR8WQiQb-gwDtOz", "./videos")
