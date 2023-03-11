from youtube_stat import YoutubeStats
API_KEY = "AIzaSyA3ZEknnxdu6G-9aNjsIp_PE-sCYh7B72I"
channel_id = "UCbXgNpp0jedKWcQiULLbDTA"

yt = YoutubeStats(API_KEY, channel_id)
# print(yt.get_channel_statistics())
# yt.dump()
yt.get_channel_video_data()