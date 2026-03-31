import bpy


class HPMESH_OT_rescan_touched_regions(bpy.types.Operator):
    bl_idname = "hpmesh.rescan_touched_regions"
    bl_label = "Rescan Touched Regions"

    def execute(self, context):
        result = bpy.ops.hpmesh.scan_issues()
        return result
