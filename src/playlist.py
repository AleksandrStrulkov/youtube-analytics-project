import datetime
import os
import isodate
from googleapiclient.discovery import build


class PlayList:
	def __init__(self, id_playlist):
		self.id_playlist = id_playlist
		self.title = self.get_pl_title()
		self.url = "https://www.youtube.com/playlist?list=" + self.id_playlist

	@staticmethod
	def get_service():
		"""Получение информации о сервисе"""
		api_key: str = os.getenv("YOUTUBE_APY_KEY")
		youtube = build("youtube", "v3", developerKey=api_key)
		return youtube

	def get_playlist_info(self):
		"""Функция, возвращающая информацию о плейлисте"""
		playlist_response = self.get_service().playlistItems() \
			.list(playlistId=self.id_playlist,
				part='contentDetails', maxResults=50, ).execute()
		return playlist_response

	def get_pl_info(self):
		"""Функция, возвращающая информацию о плейлисте"""
		playlist_info = self.get_service().playlistItems().list\
			(playlistId=self.id_playlist, part="ContentDetails,snippet", maxResults=50).execute()

		return playlist_info

	def get_pl_title(self):
		"""Функция, возвращающая название плейлиста"""
		channel_id = self.get_pl_info()["items"][0]["snippet"]["channelId"]
		playlists = self.get_service().playlists().list(channelId=channel_id, part='snippet', maxResults=50).execute()
		for item in playlists["items"]:
			if self.id_playlist == item["id"]:
				pl_title = item["snippet"]["title"]
				break
		return pl_title

	def get_video_stats(self):
		"""Функция получения статистики по видео из плейлиста"""
		video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.get_pl_info()['items']]
		video_response = self.get_service().videos().list\
			(part='contentDetails,statistics',id=','.join(video_ids)).execute()
		return video_response

	@property
	def total_duration(self):
		"""Функция возвращает объект класса datetime.timedelta с суммарной длительность плейлиста"""
		total_time = []
		for video in self.get_video_stats()['items']:
			iso_8601_duration = video['contentDetails']['duration']
			duration = isodate.parse_duration(iso_8601_duration)
			total_time.append(duration)
			result_time = sum(total_time, datetime.timedelta())
		return result_time

	def show_best_video(self):
		"""Функция возвращает ссылку на самое популярное видео в плейлисте (по количеству лайков)"""
		video_likes = []
		for likes in self.get_video_stats()["items"]:
			video_likes.append(int(likes["statistics"]["likeCount"]))
		max_likes_video = max(video_likes)
		for likes in self.get_video_stats()["items"]:
			if int(likes["statistics"]["likeCount"]) == max_likes_video:
				most_liked_video = "https://youtu.be/" + likes["id"]
		return most_liked_video

