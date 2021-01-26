class CannotFindMedia(Exception):
    """
    Error representing no media found from youtube query
    """
    pass


class TooManySongs(Exception):
    """
    Error representing too many songs in cache
    """
    pass


class NoCityFound(Exception):
    """
    Error representing no city found
    """
    pass


class NoExistingWeatherData(Exception):
    """
    Error representing no weather data either from not initially making a request or there is nothing from the
    parsed json from the request
    """
    pass


class NoWeatherDataInResponse(Exception):
    """
    Error representing existing response data but no information on weather data is contained in response json
    """
