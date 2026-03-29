import bpy
import bmesh

from ..data.cache_store import get_cache


class HPMESH_OT_select_issues(bpy.types.Operator):
    bl_idname = "hpmesh.select_issues"
    bl_label = "Select Issue Faces"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        data = get_cache(obj.name)
        detailed = data.get("detailed", {})
        regions = detailed.get("regions", [])
        if not regions:
            self.report({"WARNING"}, "No cached regions. Run scan first.")
            return {"CANCELLED"}

        face_indices = set()
        for region in regions:
            face_indices.update(region.get("faces", []))

        bpy.ops.object.mode_set(mode="EDIT")
        bm = bmesh.from_edit_mesh(obj.data)
        for f in bm.faces:
            f.select = f.index in face_indices
        bmesh.update_edit_mesh(obj.data)

        self.report({"INFO"}, f"Selected {len(face_indices)} faces")
        return {"FINISHED"}
