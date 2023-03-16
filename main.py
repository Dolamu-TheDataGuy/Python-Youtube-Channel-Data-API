from youtube_stat import YoutubeStats
import keys


yt = YoutubeStats(keys.API_KEY, keys.channel_id)
# print(yt.get_channel_statistics())
# yt.dump()
# print(yt.get_channel_video(limit=50))

print(yt.get_channel_video_statistics())