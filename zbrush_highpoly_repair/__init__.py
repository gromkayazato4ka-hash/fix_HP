from .addon_manifest import bl_info

import bpy

from .data.properties import register_properties, unregister_properties
from .operators.op_fix_clear_custom_normals import HPMESH_OT_fix_clear_custom_normals
from .operators.op_fix_degenerate_geometry import HPMESH_OT_fix_degenerate_geometry
from .operators.op_fix_recalc_normals import HPMESH_OT_fix_recalc_normals
from .operators.op_fix_remove_isolated_verts import HPMESH_OT_fix_remove_isolated_vertices
from .operators.op_fix_weld_near_duplicates import HPMESH_OT_fix_weld_near_duplicates
from .operators.op_report_issues import HPMESH_OT_report_issues
from .operators.op_rescan_touched_regions import HPMESH_OT_rescan_touched_regions
from .operators.op_scan_mesh import HPMESH_OT_scan_issues
from .operators.op_select_issues import HPMESH_OT_select_issues
from .ui.panel_main import HPMESH_PT_main
from .ui.panel_report import HPMESH_PT_report


CLASSES = (
    HPMESH_OT_scan_issues,
    HPMESH_OT_select_issues,
    HPMESH_OT_report_issues,
    HPMESH_OT_fix_recalc_normals,
    HPMESH_OT_fix_clear_custom_normals,
    HPMESH_OT_fix_degenerate_geometry,
    HPMESH_OT_fix_weld_near_duplicates,
    HPMESH_OT_fix_remove_isolated_vertices,
    HPMESH_OT_rescan_touched_regions,
    HPMESH_PT_main,
    HPMESH_PT_report,
)


def register():
    register_properties()
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
    unregister_properties()
