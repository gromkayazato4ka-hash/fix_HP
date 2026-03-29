from math import degrees


def face_is_degenerate(face, epsilon):
    return face.calc_area() <= epsilon


def edge_length_ratio(edge, median_len):
    if median_len <= 0.0:
        return 1.0
    return edge.calc_length() / median_len


def angle_between(v1, v2):
    return degrees(v1.angle(v2)) if v1.length > 0 and v2.length > 0 else 0.0
