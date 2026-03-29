import bpy

from ..core.fixes.fix_normals import recalc_normals


class HPMESH_OT_fix_recalc_normals(bpy.types.Operator):
    bl_idname = "hpmesh.fix_recalc_normals"
    bl_label = "Fix: Recalculate Normals"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        recalc_normals(obj)
        self.report({"INFO"}, "Normals recalculated")
        return {"FINISHED"}
