from math import degrees


def face_is_degenerate(face, epsilon):
    return face.calc_area() <= epsilon


def edge_length_ratio(edge, median_len):
    if median_len <= 0.0:
        return 1.0
    return edge.calc_length() / median_len


def face_edge_lengths(face):
    return [e.calc_length() for e in face.edges]


def face_aspect_ratio(face):
    lengths = face_edge_lengths(face)
    if not lengths:
        return 1.0
    mn = min(lengths)
    mx = max(lengths)
    if mn <= 0.0:
        return float("inf")
    return mx / mn


def face_avg_edge_length(face):
    lengths = face_edge_lengths(face)
    return sum(lengths) / len(lengths) if lengths else 0.0


def angle_between(v1, v2):
    return degrees(v1.angle(v2)) if v1.length > 0 and v2.length > 0 else 0.0
