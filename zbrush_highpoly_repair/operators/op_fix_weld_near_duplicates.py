import bpy
import bmesh

from ..core.fixes.fix_geometry import find_near_duplicate_vertices
from ..core.fixes.fix_safety import enforce_limit
from ..data.cache_store import get_cache
from ..utils.mesh_access import bmesh_from_object, write_bmesh_to_object


class HPMESH_OT_fix_weld_near_duplicates(bpy.types.Operator):
    bl_idname = "hpmesh.fix_weld_near_duplicates"
    bl_label = "Fix: Weld Near-Duplicates"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        settings = context.scene.hpmesh
        bm = bmesh_from_object(obj)

        verts_subset = None
        if settings.use_suspect_region_only:
            cache = get_cache(obj.name)
            suspect_faces = set()
            for region in cache.get("detailed", {}).get("regions", []):
                suspect_faces.update(region.get("faces", []))
            verts = set()
            for fi in suspect_faces:
                if fi < len(bm.faces):
                    for v in bm.faces[fi].verts:
                        verts.add(v)
            verts_subset = list(verts) if verts else None

        pairs = find_near_duplicate_vertices(bm, settings.duplicate_vertex_epsilon, verts_subset)

        if settings.dry_run:
            bm.free()
            self.report({"INFO"}, f"Dry run: {len(pairs)} potential duplicate pairs")
            return {"FINISHED"}

        if not enforce_limit(len(pairs), settings.max_elements_to_modify):
            bm.free()
            self.report({"WARNING"}, "Aborted: pair count exceeds max_elements_to_modify")
            return {"CANCELLED"}

        verts = [bm.verts[p[0]] for p in pairs] + [bm.verts[p[1]] for p in pairs]
        if verts:
            bmesh.ops.remove_doubles(bm, verts=verts, dist=settings.duplicate_vertex_epsilon)
        write_bmesh_to_object(bm, obj)
        self.report({"INFO"}, f"Weld pass complete ({len(pairs)} candidate pairs)")
        return {"FINISHED"}
