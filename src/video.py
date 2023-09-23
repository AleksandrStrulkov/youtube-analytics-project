import os
import json
from googleapiclient.discovery import build

from helper.youtube_api_manual import youtube


class Video:
	def __init__(self):
		pass

	def __str__(self):
		pass

	@staticmethod
	def get_youtube():
		api_key: str = os.getenv('YOUTUBE_APY_KEY')
		youtube = build('youtube', 'v3', developerKey=api_key)
		return youtube

	def get_video_info(self, video_id: str) -> dict:
		pass


