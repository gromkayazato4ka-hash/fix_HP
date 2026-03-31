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
        col.prop(p, "custom_normal_edge_angle_deg")
        col.prop(p, "degenerate_area_epsilon")
        col.prop(p, "sliver_aspect_ratio")
        col.prop(p, "tiny_face_edge_ratio")
        col.prop(p, "short_edge_ratio")
        col.prop(p, "duplicate_vertex_epsilon")
        col.prop(p, "region_expand_steps")

        layout.separator()
        row = layout.row(align=True)
        row.operator("hpmesh.scan_issues", icon="VIEWZOOM")
        row.operator("hpmesh.report_issues", icon="TEXT")
        layout.operator("hpmesh.select_issues", icon="RESTRICT_SELECT_OFF")
        layout.operator("hpmesh.select_sliver_faces", icon="SELECT_INTERSECT")
        layout.operator("hpmesh.select_region_around_active", icon="FACESEL")

        layout.separator()
        layout.label(text="Safe Fix Options")
        layout.prop(p, "dry_run")
        layout.prop(p, "use_suspect_region_only")
        layout.prop(p, "max_elements_to_modify")
        layout.prop(p, "require_confirm_destructive")
        layout.prop(p, "duplicate_before_destructive")

        layout.separator()
        layout.label(text="Conservative Fixes")
        layout.operator("hpmesh.fix_recalc_normals")
        layout.operator("hpmesh.fix_clear_custom_normals")
        layout.operator("hpmesh.fix_degenerate_geometry")
        layout.operator("hpmesh.fix_weld_near_duplicates")
        layout.operator("hpmesh.fix_remove_isolated_vertices")
        layout.operator("hpmesh.safe_fix_on_duplicate", icon="DUPLICATE")
        layout.operator("hpmesh.rescan_touched_regions", icon="FILE_REFRESH")
