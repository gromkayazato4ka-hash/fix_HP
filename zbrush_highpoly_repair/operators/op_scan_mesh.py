import bpy

from ..core.analysis.scan_coarse import run_coarse_scan
from ..core.analysis.scan_detailed import run_detailed_scan
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
        detailed = run_detailed_scan(bm, settings, coarse)
        bm.free()

        payload = {"coarse": coarse, "detailed": detailed}
        set_cache(obj.name, payload)

        report = build_text_report(obj.name, detailed)
        settings.report_text = report
        self.report({"INFO"}, "Scan complete")
        return {"FINISHED"}
