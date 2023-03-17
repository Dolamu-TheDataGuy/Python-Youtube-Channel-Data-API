from youtube_stat import YoutubeStats
import keys


yt = YoutubeStats(keys.API_KEY, keys.channel_id)
yt.get_channel_statistics()
yt.get_channel_video_statistics()
yt.dump()
