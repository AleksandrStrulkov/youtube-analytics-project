import os
import json
from googleapiclient.discovery import build



class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YOUTUBE_APY_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.info = None
        self.title = None
        self.description = None
        self.url = None
        self.subscriberCount = None
        self.video_count = None
        self.viewCount = None

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel_id = self.channel_id  # HighLoad Channel
        channel = Channel.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return Channel.youtube

    def to_json(self, json_name):
        """Запись информации о канале в файл json"""
        data = {"channel_id": self.channel_id,
                "channel_title": self.title,
                "channel_description": self.description,
                "channel_url": self.url,
                "channel_subscribers_count": self.subscriberCount,
                "channel_video_count": self.video_count,
                "channel_views": self.viewCount}
        with open(json_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
