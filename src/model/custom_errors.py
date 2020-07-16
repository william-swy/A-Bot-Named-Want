# Error representing no member found
class NoMemberError(Exception):
    pass


# Error representing no media found from query
class CannotFindMedia(Exception):
    pass


# Error representing too many currently used songs
class TooManySongs(Exception):
    pass


# Error representing no city found
class NoCityFound(Exception):
    pass
