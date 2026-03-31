import bpy


class HPMESH_OT_safe_fix_on_duplicate(bpy.types.Operator):
    bl_idname = "hpmesh.safe_fix_on_duplicate"
    bl_label = "Safe Fix on Duplicated Object"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        src = context.active_object
        if not src or src.type != "MESH":
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        settings = context.scene.hpmesh
        if not settings.require_confirm_destructive:
            self.report({"WARNING"}, "Enable Confirm Destructive Actions before safe destructive workflow.")
            return {"CANCELLED"}

        bpy.ops.object.select_all(action="DESELECT")
        src.select_set(True)
        context.view_layer.objects.active = src
        bpy.ops.object.duplicate()
        dup = context.active_object
        dup.name = f"{src.name}_HPFIX"

        bpy.ops.hpmesh.fix_clear_custom_normals()
        bpy.ops.hpmesh.fix_weld_near_duplicates()
        bpy.ops.hpmesh.fix_degenerate_geometry()
        bpy.ops.hpmesh.fix_recalc_normals()

        self.report({"INFO"}, f"Created and fixed duplicate: {dup.name}")
        return {"FINISHED"}
