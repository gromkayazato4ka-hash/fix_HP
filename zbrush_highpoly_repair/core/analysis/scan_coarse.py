import statistics

from .metrics import edge_length_ratio, face_is_degenerate


def run_coarse_scan(bm, settings):
    edge_lengths = [e.calc_length() for e in bm.edges]
    median_len = statistics.median(edge_lengths) if edge_lengths else 0.0

    degenerate_faces = set()
    short_edges = set()
    for face in bm.faces:
        if face_is_degenerate(face, settings.degenerate_area_epsilon):
            degenerate_faces.add(face.index)
    for edge in bm.edges:
        ratio = edge_length_ratio(edge, median_len)
        if ratio < 0.05:
            short_edges.add(edge.index)

    return {
        "degenerate_faces": sorted(degenerate_faces),
        "short_edges": sorted(short_edges),
        "median_edge_length": median_len,
    }
