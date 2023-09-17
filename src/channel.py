import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YOUTUBE_APY_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.info = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.info["items"][0]["snippet"]["title"]
        self.description = self.info["items"][0]["snippet"]["description"]
        self.url = 'https://www.youtube.com/' + self.info["items"][0]["snippet"]["customUrl"]
        self.viewCount = self.info["items"][0]["statistics"]["viewCount"]
        self.subscriberCount = int(self.info["items"][0]["statistics"]["subscriberCount"])
        self.video_count = self.info["items"][0]["statistics"]["videoCount"]

    def __str__(self):
        """Выводит в консоль информацию о канале."""
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        """Суммирует количество подписчиков в двух каналах."""
        return self.subscriberCount + other.subscriberCount

    def __sub__(self, other):
        """Выводит разницу подписчиков в двух каналах."""
        return self.subscriberCount - other.subscriberCount

    def __eq__(self, other):
        """Сравнивает количество подписчиков в двух каналах"""
        return self.subscriberCount == other.subscriberCount

    def __lt__(self, other):
        """Выводит булево значение сравнения подписчиков в двух каналах."""
        return self.subscriberCount < other.subscriberCount

    def __gt__(self, other):
        """Выводит булево значение сравнения подписчиков в двух каналах."""
        return self.subscriberCount > other.subscriberCount

    def __ge__(self, other):
        """Выводит булево значение сравнения подписчиков в двух каналах."""
        return self.subscriberCount >= other.subscriberCount

    def __le__(self, other):
        """Выводит булево значение сравнения подписчиков в двух каналах."""
        return self.subscriberCount <= other.subscriberCount

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.channel_id,
                                                     part="snippet,statistics").execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Возвращает экземпляр API"""
        return Channel.youtube

    @property
    def channel_id(self):
        """Получение id канала."""
        return self.__channel_id

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

