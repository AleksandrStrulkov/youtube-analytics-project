import os
import json
from googleapiclient.discovery import build


class Video:
	"""Класс для работы с видео c реализацией исключений"""
	def __init__(self, video_id: str):
		self.video_id = video_id
		try:
			self.info = self.get_info()
			self.title = self.info["items"][0]["snippet"]["title"]
		except IndexError:
			print(f'Неправильно указан id видео')
			self.info = None
			self.title = None
			self.url = None
			self.view_count = None
			self.like_count = None
		else:
			self.url = 'https://www.youtube.com/watch?=' + self.video_id
			self.view_count = self.info["items"][0]["statistics"]["viewCount"]
			self.like_count = self.info["items"][0]["statistics"]["likeCount"]

	def __str__(self):
		"""Функция, возвращающая строку с информацией для пользователя"""
		return f'{self.title}'

	@staticmethod
	def get_service():
		"""Функция, возвращающая сервис для работы с видео"""
		api_key: str = os.getenv('YOUTUBE_APY_KEY')
		youtube = build('youtube', 'v3', developerKey=api_key)
		return youtube

	def get_info(self):
		"""Функция, возвращающая информацию о видео"""
		video_response = self.get_service().videos().list(id=self.video_id, part='snippet, statistics').execute()
		return video_response

	def to_json(self, json_name):
		"""Запись информации о видео в файл json"""
		data = {"video_id": self.video_id,
				"video_title": self.title,
				"video_url": self.url,
				"video_views": self.view_count,
				"video_likes": self.video_likes}
		with open(json_name, "w", encoding="utf-8") as file:
			json.dump(data, file, indent=2, ensure_ascii=False)


class PLVideo(Video):
	"""Дочерний класс для работы с видео на плейлисте"""
	def __init__(self, video_id: str, id_playlist: str):
		"""Конструктор класса для работы с видео и плейлиста"""
		super().__init__(video_id)
		self.id_playlist = id_playlist
		self.playlist_info = self.get_playlist_info

	def get_playlist_info(self):
		"""Функция, возвращающая информацию о плейлисте"""
		playlist_response = self.get_service().playlistItems() \
			.list(playlistId=self.id_playlist,
				  part='contentDetails', maxResults=50, ).execute()
		return playlist_response

	def to_json(self, json_name):
		"""Запись информации о видео в файл json"""
		data = {"video_id": self.video_id,
				"id_playlist": self.id_playlist,
				"video_title": self.title,
				"video_url": self.url,
				"video_views": self.view_count,
				"video_likes": self.video_likes,
				}
		with open(json_name, "w", encoding="utf-8") as file:
			json.dump(data, file, indent=2, ensure_ascii=False)
