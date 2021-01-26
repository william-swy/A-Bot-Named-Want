from youtubesearchpython import VideosSearch

from common.Errors.botexceptions import CannotFindMedia


class YoutubeQuery:
    """
    makes requests to google api to find youtube video urls based on keyword
    """
    VIDEO_LIMIT = 5
    VIDEO_URLS = []

    def __init__(self) -> None:
        self.curr_vid_index = 0

    def search_youtube(self, keyword: str) -> str:
        """
        searches youtube for videos that match the keyword and returns the url of the first video. This function will
        also store the urls of all VIDEO_LIMIT videos in VIDEO_URLS overriding any urls obtained from the last search.
        Will raise a CannotFindMedia exception if no videos are found for the given keyword.
        :param keyword: Keyword used to search for a youtube video.
        :return: The url of the first video found
        """
        videos_search = VideosSearch(keyword, limit=self.VIDEO_LIMIT).result()["result"]

        if not videos_search:
            raise CannotFindMedia(f"No videos were found for {keyword}")

        self.VIDEO_URLS = [video["link"] for video in videos_search]
        return self.VIDEO_URLS[0]

    def get_next_url(self) -> str:
        """
        Gets the next video in the list of videos found. Will raise a CannotFindMedia exception if there are no more
        next videos. Expects that search_youtube has been previously called to make VIDEO_URLS a non-empty list.
        :return: The url of the next video found in youtube keyword search.
        """
        if self.curr_vid_index < self.VIDEO_LIMIT - 1:
            self.curr_vid_index += 1
            return self.VIDEO_URLS[self.curr_vid_index]
        else:
            raise CannotFindMedia("No more video urls available")

    def get_previous_url(self):
        """
        Gets the previous video in the list of videos found. Will raise a CannotFindMedia exception if this function is
        called and the current video url is the first url in the list of video urls. Expects that search_youtube has
        been previously called to make VIDEO_URLS a non-empty list.
        :return: The url of the previous video found in youtube keyword search.
        """
        if self.curr_vid_index > 1:
            self.curr_vid_index -= 1
            return self.VIDEO_URLS[self.curr_vid_index]
        else:
            raise CannotFindMedia("No more video urls available")


# test youtube search results
if __name__ == "__main__":
    test = YoutubeQuery()
    print(test.search_youtube('despacito'))
