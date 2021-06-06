

class Asteroid:

    def __init__(self, id, neo_reference_id, name):
        self.id = id
        self.neo_reference_id = neo_reference_id
        self.name = name

        self.close_approach_date = None
        self.nasa_jpl_url = None
        self.absolute_magnitude_h = None
        self.estimated_diameter_km_min = None
        self.estimated_diameter_km_max = None
        self.is_potentially_hazardous_asteroid = None
        self.relative_velocity_km_per_sec = None
        self.relative_velocity_km_per_hour = None
        self.miss_distance_km = None
        self.miss_distance_astronomical = None
        self.orbiting_body = None
        self.is_sentry_object = None
