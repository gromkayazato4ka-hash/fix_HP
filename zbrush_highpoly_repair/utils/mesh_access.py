import bmesh


def bmesh_from_object(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    return bm


def write_bmesh_to_object(bm, obj):
    bm.to_mesh(obj.data)
    obj.data.update()
    bm.free()
