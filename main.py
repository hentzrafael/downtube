from pytube import Playlist, YouTube
"""
    Downloads a video from a given URL and saves it to the specified path.

    Parameters:
        url (str): The URL of the video to download.
        path (str): The path where the downloaded video will be saved.

    Returns:
        None
"""
def download(url, path):
    yt = Playlist(url)
    for item in yt.video_urls:
        yout = YouTube(item)
        yout.streams.filter(only_audio=False,only_video=False,progressive=True).get_highest_resolution().download(path)

download("https://www.youtube.com/playlist?list=PL85ITvJ7FLogLBIWuoRR8WQiQb-gwDtOz", "./videos")