import bmesh
from mathutils import kdtree

from ..analysis.metrics import face_aspect_ratio


def find_near_duplicate_vertices(bm, epsilon, verts_subset=None):
    verts = list(verts_subset) if verts_subset else list(bm.verts)
    kd = kdtree.KDTree(len(verts))
    for i, v in enumerate(verts):
        kd.insert(v.co, i)
    kd.balance()

    seen = set()
    pairs = []
    for i, v in enumerate(verts):
        for _co, j, dist in kd.find_range(v.co, epsilon):
            if i == j:
                continue
            a = verts[i].index
            b = verts[j].index
            pair = tuple(sorted((a, b)))
            if pair in seen:
                continue
            seen.add(pair)
            pairs.append((pair[0], pair[1], dist))
    return pairs


def remove_bad_faces(bm, epsilon, sliver_aspect_ratio, faces_subset=None):
    candidates = list(faces_subset) if faces_subset else list(bm.faces)
    doomed = [f for f in candidates if f.calc_area() <= epsilon or face_aspect_ratio(f) >= sliver_aspect_ratio]
    if doomed:
        bmesh.ops.delete(bm, geom=doomed, context="FACES")
    return len(doomed)


def remove_isolated_vertices(bm):
    isolated = [v for v in bm.verts if not v.link_faces and not v.link_edges]
    if isolated:
        bmesh.ops.delete(bm, geom=isolated, context="VERTS")
    return len(isolated)
