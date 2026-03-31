import bpy
import bmesh

from ..data.cache_store import get_cache


class HPMESH_OT_select_sliver_faces(bpy.types.Operator):
    bl_idname = "hpmesh.select_sliver_faces"
    bl_label = "Select Sliver Faces"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        cache = get_cache(obj.name)
        coarse = cache.get("coarse", {})
        slivers = set(coarse.get("sliver_faces", []))
        if not slivers:
            self.report({"WARNING"}, "No sliver faces in cache. Run scan first.")
            return {"CANCELLED"}

        bpy.ops.object.mode_set(mode="EDIT")
        bm = bmesh.from_edit_mesh(obj.data)
        for f in bm.faces:
            f.select = f.index in slivers
        bmesh.update_edit_mesh(obj.data)

        self.report({"INFO"}, f"Selected {len(slivers)} sliver faces")
        return {"FINISHED"}
