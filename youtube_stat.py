import requests
import json

class YoutubeStats:

    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_stats = None
        self.video_data = None


    def get_channel_statistics(self):
        """Method to obtain channel statistics"""
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}"
        #print(url)
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        #print(data)
        try:
            data = data['items'][0]['statistics']
        except:
            data = None

        self.channel_stats=data
        return data
    
    def get_channel_video_data(self):
        # get video ids
        channel_videos = self._get_channel_videos(limit=50) # line of code automatically outputs the url despite not printing channel_videos, print(outputs channel vs return (doesnt output anything)
        print(channel_videos)


        # get video statistics, #TODO 
    
    def _get_channel_videos(self, limit = None): 
        url = f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&order=date"
        if limit is not None and isinstance(limit, int):
            url += f"&maxResults={limit}"
        vid, npt = self._get_channel_videos_per_page(url)
        idx = 0
        while(npt is not None and idx < 10):
            next_url = url + f"&pageToken={npt}"
            next_vid, npt = self._get_channel_videos_per_page(next_url)
            vid.update(next_vid)
            idx += 1

        return vid
        

    def _get_channel_videos_per_page(self, url): # root function
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        channel_video = {}
        if "items" not in data:
            return channel_video, None
        
        item_data = data['items']
        nextpageToken = data.get("nextpageToken", None)

        for item in item_data:
            try:
                kind = item['id']['kind']
                if kind == 'youtube#video':
                    video_id = item['id']['videoId']
                    channel_video[video_id] = dict()
            except KeyError:
                print("Error, not a video")
        return channel_video, nextpageToken

    
    def dump(self):
        if self.channel_stats is None:
            return
        

        # process to create filename
        channel_title = "Python Engineer"  #TODO: GET CHANNEL NAME FROM API
        channel_title = channel_title.replace(" ", "_").lower()
        file_name = channel_title + ".json"
        with open(file_name, mode="w") as f:
            json.dump(self.channel_stats, f, indent=4) # indent for proper styling of json file
        print("file dumped")