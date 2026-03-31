import statistics

from .metrics import edge_length_ratio, face_aspect_ratio, face_avg_edge_length, face_is_degenerate


def _neighbor_avg_edge_length(face):
    values = []
    for vert in face.verts:
        for linked_face in vert.link_faces:
            if linked_face.index == face.index:
                continue
            values.append(face_avg_edge_length(linked_face))
    if not values:
        return face_avg_edge_length(face)
    return statistics.median(values)


def run_coarse_scan(bm, settings):
    edge_lengths = [e.calc_length() for e in bm.edges]
    median_len = statistics.median(edge_lengths) if edge_lengths else 0.0

    degenerate_faces = set()
    sliver_faces = set()
    tiny_faces = set()
    short_edges = set()

    for face in bm.faces:
        if face_is_degenerate(face, settings.degenerate_area_epsilon):
            degenerate_faces.add(face.index)
            continue

        if face_aspect_ratio(face) >= settings.sliver_aspect_ratio:
            sliver_faces.add(face.index)

        local_avg = _neighbor_avg_edge_length(face)
        this_avg = face_avg_edge_length(face)
        if local_avg > 0 and this_avg <= local_avg * settings.tiny_face_edge_ratio:
            tiny_faces.add(face.index)

    for edge in bm.edges:
        ratio = edge_length_ratio(edge, median_len)
        if ratio < settings.short_edge_ratio:
            short_edges.add(edge.index)

    return {
        "degenerate_faces": sorted(degenerate_faces),
        "sliver_faces": sorted(sliver_faces),
        "tiny_faces": sorted(tiny_faces),
        "short_edges": sorted(short_edges),
        "median_edge_length": median_len,
    }
