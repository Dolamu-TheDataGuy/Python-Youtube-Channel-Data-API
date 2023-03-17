import requests
import json
from tqdm import tqdm
import keys


class YoutubeStats:

    def  __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        self.video_data = None

    def get_channel_statistics(self):
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}"
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        
        try:
            data = data['items'][0]['statistics'] # even if the content of a list is just 1 the index which is 0 must be referenced
        except KeyError:
            data = None

        self.channel_statistics = data  
        return data
    
    def get_channel_video_statistics(self):
        channel_videos = self.get_channel_video(limit=50)
        # get video statistics
        parts = ['snippet', 'statistics', 'contentDetails']
        for video in channel_videos:
            for part in parts:
                data = self.get_single_video_data(video, part) # data for each video
                channel_videos[video].update(data)   #adds the information to each video id in the dict

        self.video_data = channel_videos
        return channel_videos

        
    def get_single_video_data(self, video_id, part):
        url = f"https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={self.api_key}"
        json_url = requests.get(url)
        data = json.loads(json_url.text) # convert to python object 
        try:
            data = data['items'][0][part]
        except:
           print("Error")
           data = dict()

        return data





    def get_channel_video(self, limit=None):
        url = f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&order=date"
    
        if limit is not None and isinstance(limit, int):
            url += f"&maxResults={limit}"
        vid, npt = self._get_channel_video_id_per_page(url)
        idx = 0
        while(npt is not None and idx < 10):
            next_url = url + f"&pageToken={npt}"
            next_vid, npt = self._get_channel_video_id_per_page(next_url)
            vid.update(next_vid)
            idx += 1

        return vid


    def _get_channel_video_id_per_page(self, url):
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        channel_video = {} # dictionary that will hold channel video information
        if "items" not in data:
            return channel_video, None     # empty dict and no next page token
        
        item_data = data['items']
        nextpageToken = data.get('nextpageToken', None)

        # looping through item data to get each video_id
        for item in item_data:
            try:
                kind = item['id']['kind']
                if kind == "youtube#video":
                    video_id = item['id']['videoId']
                    channel_video[video_id] = dict()
            except KeyError:
                print("Error, not a video")
        return channel_video, nextpageToken

    
    def dump(self):
        """Function that writes channel and video data into a json file"""
        if self.channel_statistics is None or self.video_data is None:
            print("Data is None")
            return
        
        merged_data = {self.channel_id:{"channel_statistics": self.channel_statistics, "video_data": self.video_data }}

        # process to create filename
        channel_title = self.video_data.popitem()[1].get("channelTitle", self.channel_id) # pppitem() randomly outputs a tuple of key and value, key(channelid), value (other properties)
        print(channel_title)
        channel_title = channel_title.replace(" ", "_").lower()
        file_name = channel_title + ".json"
        with open(file_name, mode="w") as f:
            json.dump(merged_data, f, indent=4) # indent for proper styling of json file
        
        print("file dumped")
    

        
        

 
        
    

        