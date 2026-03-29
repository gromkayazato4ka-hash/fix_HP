import bpy

from ..data.cache_store import get_cache
from ..core.reporting.report_builder import build_text_report


class HPMESH_OT_report_issues(bpy.types.Operator):
    bl_idname = "hpmesh.report_issues"
    bl_label = "Refresh Report"

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        payload = get_cache(obj.name)
        detailed = payload.get("detailed", {})
        if not detailed:
            self.report({"WARNING"}, "No analysis cache available.")
            return {"CANCELLED"}

        context.scene.hpmesh.report_text = build_text_report(obj.name, detailed)
        self.report({"INFO"}, "Report updated")
        return {"FINISHED"}
