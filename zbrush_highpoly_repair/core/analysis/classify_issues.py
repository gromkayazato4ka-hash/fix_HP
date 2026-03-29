from ...data.issue_types import ISSUE_GEOMETRY, ISSUE_MIXED, ISSUE_NORMALS


def classify_region(normals_score, geo_score, bias=1.25):
    if normals_score > geo_score * bias:
        return ISSUE_NORMALS
    if geo_score > normals_score * bias:
        return ISSUE_GEOMETRY
    return ISSUE_MIXED
