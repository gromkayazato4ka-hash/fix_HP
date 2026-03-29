import bpy


def recalc_normals(obj):
    ctx = bpy.context
    prev_active = ctx.view_layer.objects.active
    was_selected = obj.select_get()
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    ctx.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode="OBJECT")
    obj.select_set(was_selected)
    ctx.view_layer.objects.active = prev_active


def clear_custom_normals(obj):
    mesh = obj.data
    if mesh.has_custom_normals:
        mesh.normals_split_custom_set(None)
    mesh.use_auto_smooth = True
    mesh.update()
