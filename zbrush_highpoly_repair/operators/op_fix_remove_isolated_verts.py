import bpy

from ..core.fixes.fix_geometry import remove_isolated_vertices
from ..core.fixes.fix_safety import destructive_allowed
from ..utils.mesh_access import bmesh_from_object, write_bmesh_to_object


class HPMESH_OT_fix_remove_isolated_vertices(bpy.types.Operator):
    bl_idname = "hpmesh.fix_remove_isolated_vertices"
    bl_label = "Fix: Remove Isolated Vertices"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        settings = context.scene.hpmesh
        if not destructive_allowed(settings):
            self.report({"WARNING"}, "Enable 'Confirm Destructive Actions' first")
            return {"CANCELLED"}

        bm = bmesh_from_object(obj)
        candidate_count = len([v for v in bm.verts if not v.link_faces and not v.link_edges])
        if settings.dry_run:
            bm.free()
            self.report({"INFO"}, f"Dry run: {candidate_count} isolated vertices")
            return {"FINISHED"}

        removed = remove_isolated_vertices(bm)
        write_bmesh_to_object(bm, obj)
        self.report({"INFO"}, f"Removed {removed} isolated vertices")
        return {"FINISHED"}
