from rest_framework.throttling import UserRateThrottle

class genreThrottle(UserRateThrottle):
    scope = 'genre'