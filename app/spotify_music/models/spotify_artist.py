

class SpotifyArtist:
    next_num_id = 1
    artists = []

    def __init__(self, id):
        self.id = id
        self.name = None
        self.followers = None
        self.uri = None
        self.url = None
        self.image_url = None
        self.popularity = None

        self.num_id = self.__class__.next_num_id
        self.__class__.next_num_id += 1
        self.__class__.artists.append(self)

    @classmethod
    def reset(cls):
        cls.next_num_id = 1
        cls.artists = []
