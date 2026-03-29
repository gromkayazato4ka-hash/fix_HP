from ...data.issue_types import ISSUE_LABELS


def build_text_report(obj_name, result):
    issue_type = result.get("issue_type", "MIXED")
    label = ISSUE_LABELS.get(issue_type, issue_type)
    scores = result.get("scores", {})
    regions = result.get("regions", [])
    return (
        f"Object: {obj_name}\n"
        f"Classification: {label}\n"
        f"Regions: {len(regions)}\n"
        f"Normals score: {scores.get('normals', 0):.2f}\n"
        f"Geometry score: {scores.get('geometry', 0):.2f}"
    )
