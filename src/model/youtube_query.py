# establish connection to youtube API, queries for an video url
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from custom_errors import CannotFindMedia
import utils


class YoutubeQuery:
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    SEARCH_TIMES = 3
    YOUTUBE_URL = 'https://www.youtube.com/watch?v='

    def __init__(self) -> None:
        load_dotenv(utils.ENV_PATH)
        self.DEVELOPER_KEY = os.getenv('YOUTUBE_TOKEN')

    # returns the url of the search keyword based on relevance
    def search_youtube(self, q, order='relevance', token=None, times=SEARCH_TIMES) -> str:
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

    # searches next page if first page cannot find a video
    def find_url(self, q, response, counter) -> str:
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
