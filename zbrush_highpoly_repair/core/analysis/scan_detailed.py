from .classify_issues import classify_region
from .metrics import angle_between
from .region_builder import regions_from_faces


def _loop_normal_map(mesh):
    mesh.calc_normals_split()
    loop_map = {}
    for poly in mesh.polygons:
        for li in poly.loop_indices:
            loop = mesh.loops[li]
            loop_map[(poly.index, loop.vertex_index)] = loop.normal.copy()
    return loop_map


def _custom_normal_discontinuity_faces(bm, mesh, settings):
    if not mesh.has_custom_normals:
        return set(), 0.0

    loop_normals = _loop_normal_map(mesh)
    flagged_faces = set()
    score = 0.0

    for edge in bm.edges:
        if len(edge.link_faces) != 2:
            continue
        f1, f2 = edge.link_faces[0], edge.link_faces[1]
        face_angle = angle_between(f1.normal, f2.normal)
        for vert in edge.verts:
            n1 = loop_normals.get((f1.index, vert.index))
            n2 = loop_normals.get((f2.index, vert.index))
            if n1 is None or n2 is None:
                continue
            loop_angle = angle_between(n1, n2)
            if loop_angle > max(face_angle + 20.0, settings.custom_normal_edge_angle_deg):
                flagged_faces.add(f1.index)
                flagged_faces.add(f2.index)
                score += 1.0
                break

    return flagged_faces, score


def run_detailed_scan(bm, obj, settings, coarse_data, near_duplicate_pairs):
    suspect_faces = set(coarse_data["degenerate_faces"]) | set(coarse_data["sliver_faces"]) | set(coarse_data["tiny_faces"])

    for edge_idx in coarse_data["short_edges"]:
        e = bm.edges[edge_idx]
        for face in e.link_faces:
            suspect_faces.add(face.index)

    for a, b, _dist in near_duplicate_pairs:
        va = bm.verts[a]
        vb = bm.verts[b]
        for f in va.link_faces:
            suspect_faces.add(f.index)
        for f in vb.link_faces:
            suspect_faces.add(f.index)

    custom_faces, custom_score = _custom_normal_discontinuity_faces(bm, obj.data, settings)
    suspect_faces |= custom_faces

    normals_score = custom_score
    for vert in bm.verts:
        linked_faces = vert.link_faces
        if len(linked_faces) < 2:
            continue
        base = linked_faces[0].normal
        peak = max((angle_between(base, f.normal) for f in linked_faces[1:]), default=0.0)
        if peak > settings.normal_outlier_angle_deg:
            normals_score += 0.5

    geo_score = float(
        len(coarse_data["degenerate_faces"])
        + len(coarse_data["sliver_faces"])
        + len(coarse_data["tiny_faces"])
        + len(coarse_data["short_edges"])
        + len(near_duplicate_pairs)
    )

    issue_type = classify_region(normals_score=normals_score, geo_score=geo_score)
    regions = regions_from_faces(suspect_faces)
    return {
        "issue_type": issue_type,
        "regions": regions,
        "scores": {"normals": normals_score, "geometry": geo_score},
        "custom_normal_faces": sorted(custom_faces),
        "near_duplicate_pairs": len(near_duplicate_pairs),
    }
