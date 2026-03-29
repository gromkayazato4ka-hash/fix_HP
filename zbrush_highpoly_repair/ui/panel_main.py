import bpy


class HPMESH_PT_main(bpy.types.Panel):
    bl_label = "HighPoly Repair"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "HighPoly Repair"

    def draw(self, context):
        layout = self.layout
        p = context.scene.hpmesh

        col = layout.column(align=True)
        col.prop(p, "scan_scope")
        col.prop(p, "normal_outlier_angle_deg")
        col.prop(p, "degenerate_area_epsilon")
        col.prop(p, "duplicate_vertex_epsilon")
        col.prop(p, "dry_run")
        col.prop(p, "max_elements_to_modify")
        col.prop(p, "require_confirm_destructive")

        layout.separator()
        layout.operator("hpmesh.scan_issues", icon="VIEWZOOM")
        layout.operator("hpmesh.select_issues", icon="RESTRICT_SELECT_OFF")
        layout.operator("hpmesh.report_issues", icon="TEXT")

        layout.separator()
        layout.label(text="Conservative Fixes")
        layout.operator("hpmesh.fix_recalc_normals")
        layout.operator("hpmesh.fix_clear_custom_normals")
        layout.operator("hpmesh.fix_degenerate_geometry")
        layout.operator("hpmesh.fix_weld_near_duplicates")
        layout.operator("hpmesh.fix_remove_isolated_vertices")
        layout.operator("hpmesh.rescan_touched_regions", icon="FILE_REFRESH")
