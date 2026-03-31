import bpy


class HPMESH_PT_report(bpy.types.Panel):
    bl_label = "HighPoly Report"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "HighPoly Repair"

    def draw(self, context):
        layout = self.layout
        p = context.scene.hpmesh
        for line in p.report_text.split("\n"):
            layout.label(text=line)
