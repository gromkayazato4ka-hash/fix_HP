from .classify_issues import classify_region
from .metrics import angle_between
from .region_builder import regions_from_faces


def run_detailed_scan(bm, settings, coarse_data):
    suspect_faces = set(coarse_data["degenerate_faces"])
    normals_score = 0.0
    geo_score = float(len(coarse_data["degenerate_faces"])) + float(len(coarse_data["short_edges"]))

    for vert in bm.verts:
        linked_faces = vert.link_faces
        if len(linked_faces) < 2:
            continue
        base = linked_faces[0].normal
        local_angles = [angle_between(base, f.normal) for f in linked_faces[1:]]
        if not local_angles:
            continue
        peak = max(local_angles)
        if peak > settings.normal_outlier_angle_deg:
            normals_score += 1.0
            for lf in linked_faces:
                suspect_faces.add(lf.index)

    issue_type = classify_region(normals_score=normals_score, geo_score=geo_score)
    regions = regions_from_faces(suspect_faces)
    return {
        "issue_type": issue_type,
        "regions": regions,
        "scores": {"normals": normals_score, "geometry": geo_score},
    }
