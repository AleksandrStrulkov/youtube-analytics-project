import os
import json
from googleapiclient.discovery import build


class Video:
	def __init__(self, video_id: str):
		self.video_id = video_id
		self.info = self.get_info()
		self.title = self.info["items"][0]["snippet"]["title"]
		self.url = 'https://www.youtube.com/watch?=' + self.video_id
		self.view_count = self.info["items"][0]["statistics"]["viewCount"]
		self.video_likes = self.info["items"][0]["statistics"]["likeCount"]

	def __str__(self):
		return f'{self.title})'

	@staticmethod
	def get_service():
		api_key: str = os.getenv('YOUTUBE_APY_KEY')
		youtube = build('youtube', 'v3', developerKey=api_key)
		return youtube

	def get_info(self):
		video_response = self.get_service().videos().list(id=self.video_id, part='snippet, statistics').execute()
		return video_response

	def to_json(self, json_name):
		"""Запись информации о канале в файл json"""
		data = {"video_id": self.video_id,
				"video_title": self.title,
				"video_url": self.url,
				"video_views": self.view_count,
				"video_likes": self.video_likes}
		with open(json_name, "w", encoding="utf-8") as file:
			json.dump(data, file, indent=2, ensure_ascii=False)









