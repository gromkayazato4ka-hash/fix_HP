import bmesh
from mathutils import kdtree


def find_near_duplicate_vertices(bm, epsilon):
    kd = kdtree.KDTree(len(bm.verts))
    for v in bm.verts:
        kd.insert(v.co, v.index)
    kd.balance()

    seen = set()
    pairs = []
    for v in bm.verts:
        if v.index in seen:
            continue
        for co, idx, dist in kd.find_range(v.co, epsilon):
            if idx == v.index:
                continue
            pair = tuple(sorted((v.index, idx)))
            if pair in seen:
                continue
            seen.add(pair)
            pairs.append((pair[0], pair[1], dist))
    return pairs


def remove_degenerate_faces(bm, epsilon):
    doomed = [f for f in bm.faces if f.calc_area() <= epsilon]
    if doomed:
        bmesh.ops.delete(bm, geom=doomed, context="FACES")
    return len(doomed)


def remove_isolated_vertices(bm):
    isolated = [v for v in bm.verts if not v.link_faces and not v.link_edges]
    if isolated:
        bmesh.ops.delete(bm, geom=isolated, context="VERTS")
    return len(isolated)
