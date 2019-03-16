from math import sin, cos, sqrt, atan2, radians


def coord_dist(coord_set):
    """
    calculates distance between coordinate pairs in meters
    :param coord_set: [x1, y1, x2, y2]
    :return:
    """
    x1 = float(coord_set[0])
    y1 = float(coord_set[1])
    x2 = float(coord_set[2])
    y2 = float(coord_set[3])

    # approximate radius of Earth in meters
    r = 6373000.0

    lat1 = radians(y1)
    lon1 = radians(x1)
    lat2 = radians(y2)
    lon2 = radians(x2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = r * c
    return round(distance)


def coord_dist_3d(coord_set):
    """
    calculates distance between coordinate pairs in meters
    :param coord_set: [x1, y1, z1, x2, y2, z2]
    :return:
    """
    x1 = float(coord_set[0])
    y1 = float(coord_set[1])
    z1 = float(coord_set[2])

    x2 = float(coord_set[3])
    y2 = float(coord_set[4])
    z2 = float(coord_set[5])

    # approximate radius of Earth in meters
    r = 6373000.0

    lat1 = radians(y1)
    lon1 = radians(x1)
    lat2 = radians(y2)
    lon2 = radians(x2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = r * c

    h = abs(z1 - z2)

    distance_3d = distance**2 + h**2
    distance_3d = sqrt(distance_3d)

    return round(distance_3d)
