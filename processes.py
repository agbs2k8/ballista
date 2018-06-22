import math


class Distance:
    """
    A distance, regardless of the unit of measure
    handles meters, kilometers, yards and miles
    """

    def __init__(self, value: float, unit_of_measure: str):
        if unit_of_measure.lower() == 'km' or unit_of_measure.lower() == 'kilometer' or \
                unit_of_measure.lower() == 'kilometers':
            self.distance = value * 100000
        elif unit_of_measure.lower() == 'm' or unit_of_measure.lower() == 'meter' or \
                unit_of_measure.lower() == 'meters':
            self.distance = value * 100
        elif unit_of_measure.lower() == 'mile' or unit_of_measure.lower() == 'miles':
            self.distance = value * 160934.4
        elif unit_of_measure.lower() == 'yard' or unit_of_measure.lower() == 'yards':
            self.distance = value * 91.44
        elif unit_of_measure.lower() == 'foot' or unit_of_measure.lower() == 'feet':
            self.distance = value * 30.48
        else:
            self.distance = value

    def __repr__(self):
        return f"<Distance: {self.distance} CM>"

    def meters(self):
        return self.distance / 100

    def kilometers(self):
        return self.distance / 100000

    def yards(self):
        return self.distance * .010936132983377

    def miles(self):
        return self.distance * 0.00000621371

    def feet(self):
        return self.distance * 0.0328084


class ScopeMeasure:
    """
    Angles measured in a Scope by a MIL or MOA reticle
    """
    _moa_per = 21600
    _mil_per = 6283.2

    def __init__(self, value: float, unit_of_measure: str):
        if not unit_of_measure.lower() in ['mil', 'moa']:
            raise ValueError(f'Could not find {unit_of_measure} in ["moa, "mil"]')
        else:
            self.clicks = value
            self.units = unit_of_measure.lower()

    def __repr__(self):
        return f"<ScopeMeasure: {self.clicks} {self.units.upper()}>"

    def moa(self):
        if self.units == 'moa':
            return self.clicks
        else:
            return self.clicks * (self._moa_per / self._mil_per)

    def mil(self):
        if self.units == 'mil':
            return self.clicks
        else:
            return self.clicks * (self._mil_per / self._moa_per)


def get_distance(lat1, lon1, lat2, lon2):
    earth_rad = float(6371.008)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lat_change = lat2 - lat1
    lon_change = math.radians(lon2 - lon1)
    haversine = (math.sin(lat_change / 2) ** 2) + (math.sin(lon_change / 2) ** 2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(haversine), math.sqrt(1.0 - haversine))
    distance = earth_rad * c
    return distance


def get_heading(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lon_change = math.radians(lon2 - lon1)
    x = math.sin(lon_change) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(lon_change))
    z = math.atan2(x, y)
    return (math.degrees(z) + 360) % 360


def get_elev_angle(el_from: Distance, el_tgt: Distance, dist_between: Distance):
    return (180 / math.pi) * (
                (el_tgt.feet() - el_from.feet()) / dist_between.feet() - dist_between.miles() / (2 * 3956))


class Location:
    """
    Physical location with latitude, longitude, altitude (distance over sea level)
    TODO: add other atmospheric conditions
    """

    def __init__(self, lat: float, lon: float, alt: float, time):
        self.latitude = lat
        self.longitude = lon
        self.altitude = Distance(alt, 'feet')
        self.last_set = time

    def __repr__(self):
        return f"<Location {self.latitude}, {self.longitude} @ {self.altitude} MSL @ {self.last_set}"

    def distance_to(self, alt_location):
        dist = get_distance(self.latitude, self.longitude, alt_location.latitude, alt_location.longitude)
        return Distance(dist, 'km')

    def heading_to(self, alt_location):
        return get_heading(self.latitude, self.longitude, alt_location.latitude, alt_location.longitude)

    def angle_to(self, alt_location):
        return get_elev_angle(self.altitude, alt_location.altitude, self.distance_to(alt_location))

    def ballistic_dist_to(self, alt_location):
        dist = self.distance_to(alt_location).meters()
        theta = math.cos(math.radians(self.angle_to(alt_location)))
        return Distance(dist * theta, 'meters')
