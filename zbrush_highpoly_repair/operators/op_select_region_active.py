import bpy
import bmesh


class HPMESH_OT_select_region_around_active(bpy.types.Operator):
    bl_idname = "hpmesh.select_region_around_active"
    bl_label = "Select Problem Region Around Active Face"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        bpy.ops.object.mode_set(mode="EDIT")
        bm = bmesh.from_edit_mesh(obj.data)
        active = bm.faces.active
        if active is None:
            self.report({"WARNING"}, "Set an active face first.")
            return {"CANCELLED"}

        steps = context.scene.hpmesh.region_expand_steps
        frontier = {active}
        visited = {active}

        for _ in range(steps):
            nxt = set()
            for face in frontier:
                for edge in face.edges:
                    for lf in edge.link_faces:
                        if lf not in visited:
                            visited.add(lf)
                            nxt.add(lf)
            frontier = nxt

        for f in bm.faces:
            f.select = f in visited
        bm.faces.active = active
        bmesh.update_edit_mesh(obj.data)
        self.report({"INFO"}, f"Selected region of {len(visited)} faces")
        return {"FINISHED"}
