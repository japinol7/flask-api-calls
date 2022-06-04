

class SpotifyArtist:
    next_num_id = 1

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

    @classmethod
    def reset_num_id(cls):
        cls.next_num_id = 1
