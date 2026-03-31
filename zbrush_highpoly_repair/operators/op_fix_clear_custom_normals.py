import bpy

from ..core.fixes.fix_normals import clear_custom_normals


class HPMESH_OT_fix_clear_custom_normals(bpy.types.Operator):
    bl_idname = "hpmesh.fix_clear_custom_normals"
    bl_label = "Fix: Clear Custom Normals"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        settings = context.scene.hpmesh
        if obj.data.has_custom_normals and not settings.require_confirm_destructive:
            self.report({"WARNING"}, "Custom normals detected. Enable Confirm Destructive Actions first.")
            return {"CANCELLED"}

        clear_custom_normals(obj)
        self.report({"INFO"}, "Custom normals cleared")
        return {"FINISHED"}
