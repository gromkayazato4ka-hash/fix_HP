import bpy

from ..core.analysis.scan_coarse import run_coarse_scan
from ..core.analysis.scan_detailed import run_detailed_scan
from ..core.fixes.fix_geometry import find_near_duplicate_vertices
from ..core.reporting.report_builder import build_text_report
from ..data.cache_store import set_cache
from ..utils.mesh_access import bmesh_from_object


class HPMESH_OT_scan_issues(bpy.types.Operator):
    bl_idname = "hpmesh.scan_issues"
    bl_label = "Scan Issues"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        settings = context.scene.hpmesh
        bm = bmesh_from_object(obj)
        coarse = run_coarse_scan(bm, settings)
        near_duplicate_pairs = find_near_duplicate_vertices(bm, settings.duplicate_vertex_epsilon)
        detailed = run_detailed_scan(bm, obj, settings, coarse, near_duplicate_pairs)
        bm.free()

        payload = {"coarse": coarse, "detailed": detailed}
        set_cache(obj.name, payload)

        report = build_text_report(obj.name, detailed, coarse)
        settings.report_text = report
        self.report({"INFO"}, "Scan complete")
        return {"FINISHED"}
