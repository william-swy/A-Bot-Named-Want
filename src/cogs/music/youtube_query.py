import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

from src.common.Errors.custom_errors import CannotFindMedia
import utils


class YoutubeQuery:
    """makes requests to google api"""
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    SEARCH_TIMES = 3
    YOUTUBE_URL = 'https://www.youtube.com/watch?v='

    def __init__(self) -> None:
        """grabs google api key from environment variables"""
        load_dotenv(utils.ENV_PATH)
        self.DEVELOPER_KEY = os.getenv('YOUTUBE_TOKEN')

    def search_youtube(self, q: str, order='relevance', token=None, times=SEARCH_TIMES) -> str:
        """returns the url of the youtube search keyword based on relevance"""
        counter = times
        youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, developerKey=self.DEVELOPER_KEY)
        search_response = youtube.search().list(
            q=q,
            type='video',
            pageToken=token,
            order=order,
            part='id,snippet',
            maxResults=5,
            location=None,
            locationRadius=None
        ).execute()

        counter = counter - 1

        url = self.find_url(q, search_response, counter)
        return url

    def find_url(self, q: str, response: dict, counter: int) -> str:
        """searches next page if first page cannot find a video"""
        result = None
        for search_result in response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                result = self.YOUTUBE_URL + search_result['id']['videoId']
                break

        if result is None:
            if counter == 0:
                raise CannotFindMedia()
            else:
                result = self.search_youtube(q, order='relevance', token=response[0], times=counter)

        return result


# test youtube search results
if __name__ == "__main__":
    test = YoutubeQuery()
    print(test.search_youtube('despacito'))
