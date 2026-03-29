import bpy

from ..core.fixes.fix_geometry import remove_degenerate_faces
from ..utils.mesh_access import bmesh_from_object, write_bmesh_to_object


class HPMESH_OT_fix_degenerate_geometry(bpy.types.Operator):
    bl_idname = "hpmesh.fix_degenerate_geometry"
    bl_label = "Fix: Degenerate Geometry"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        settings = context.scene.hpmesh
        bm = bmesh_from_object(obj)
        count = len([f for f in bm.faces if f.calc_area() <= settings.degenerate_area_epsilon])
        if settings.dry_run:
            bm.free()
            self.report({"INFO"}, f"Dry run: {count} degenerate faces detected")
            return {"FINISHED"}

        removed = remove_degenerate_faces(bm, settings.degenerate_area_epsilon)
        write_bmesh_to_object(bm, obj)
        self.report({"INFO"}, f"Removed {removed} degenerate faces")
        return {"FINISHED"}
