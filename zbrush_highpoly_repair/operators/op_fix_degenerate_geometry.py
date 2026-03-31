import bpy

from ..core.fixes.fix_geometry import remove_bad_faces
from ..data.cache_store import get_cache
from ..utils.mesh_access import bmesh_from_object, write_bmesh_to_object


class HPMESH_OT_fix_degenerate_geometry(bpy.types.Operator):
    bl_idname = "hpmesh.fix_degenerate_geometry"
    bl_label = "Fix: Degenerate/Sliver Faces"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        settings = context.scene.hpmesh
        bm = bmesh_from_object(obj)

        face_subset = None
        if settings.use_suspect_region_only:
            cache = get_cache(obj.name)
            faces = set(cache.get("coarse", {}).get("degenerate_faces", []))
            faces |= set(cache.get("coarse", {}).get("sliver_faces", []))
            face_subset = [bm.faces[i] for i in faces if i < len(bm.faces)]

        count = len([f for f in (face_subset or bm.faces) if f.calc_area() <= settings.degenerate_area_epsilon])
        if settings.dry_run:
            bm.free()
            self.report({"INFO"}, f"Dry run: {count} strict degenerates in scope")
            return {"FINISHED"}

        removed = remove_bad_faces(bm, settings.degenerate_area_epsilon, settings.sliver_aspect_ratio, face_subset)
        write_bmesh_to_object(bm, obj)
        self.report({"INFO"}, f"Removed {removed} bad faces (degenerate/sliver)")
        return {"FINISHED"}
