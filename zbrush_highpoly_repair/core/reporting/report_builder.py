from ...data.issue_types import ISSUE_LABELS


def build_text_report(obj_name, detailed, coarse):
    issue_type = detailed.get("issue_type", "MIXED")
    label = ISSUE_LABELS.get(issue_type, issue_type)
    scores = detailed.get("scores", {})
    regions = detailed.get("regions", [])

    return (
        f"Object: {obj_name}\n"
        f"Classification: {label}\n"
        f"Regions: {len(regions)}\n"
        f"Normals score: {scores.get('normals', 0):.2f}\n"
        f"Geometry score: {scores.get('geometry', 0):.2f}\n"
        f"Degenerate faces: {len(coarse.get('degenerate_faces', []))}\n"
        f"Sliver faces: {len(coarse.get('sliver_faces', []))}\n"
        f"Tiny faces: {len(coarse.get('tiny_faces', []))}\n"
        f"Short edges: {len(coarse.get('short_edges', []))}\n"
        f"Near-duplicate pairs: {detailed.get('near_duplicate_pairs', 0)}\n"
        f"Custom-normal discontinuities: {len(detailed.get('custom_normal_faces', []))}"
    )
