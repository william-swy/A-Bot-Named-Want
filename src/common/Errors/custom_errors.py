class NoMemberError(Exception):
    """Error representing no member found"""
    pass


class CannotFindMedia(Exception):
    """Error representing no media found from youtube query"""
    pass


class TooManySongs(Exception):
    """Error representing too many songs in cache"""
    pass


class NoCityFound(Exception):
    """Error representing no city found"""
    pass
