import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty


class HPMESH_Properties(bpy.types.PropertyGroup):
    scan_scope: EnumProperty(
        name="Scan Scope",
        items=[
            ("FULL", "Full Object", "Scan entire object"),
            ("SELECTED", "Selected", "Scan selected elements where possible"),
        ],
        default="FULL",
    )
    normal_outlier_angle_deg: FloatProperty(name="Normal Outlier Angle", default=35.0, min=1.0, max=180.0)
    custom_normal_edge_angle_deg: FloatProperty(name="Custom Normal Discontinuity", default=40.0, min=1.0, max=180.0)
    degenerate_area_epsilon: FloatProperty(name="Degenerate Area Epsilon", default=1e-12, min=0.0, precision=12)
    sliver_aspect_ratio: FloatProperty(name="Sliver Aspect Ratio", default=18.0, min=2.0, max=1000.0)
    tiny_face_edge_ratio: FloatProperty(name="Tiny Face Edge Ratio", default=0.35, min=0.01, max=1.0)
    short_edge_ratio: FloatProperty(name="Short Edge Ratio", default=0.05, min=0.001, max=1.0)
    duplicate_vertex_epsilon: FloatProperty(name="Weld Epsilon", default=1e-6, min=0.0, precision=8)
    island_min_size: IntProperty(name="Min Island Size", default=4, min=1)
    region_expand_steps: IntProperty(name="Region Expand Steps", default=2, min=0, max=8)
    dry_run: BoolProperty(name="Dry Run", default=True)
    use_suspect_region_only: BoolProperty(name="Fix Suspect Region Only", default=True)
    duplicate_before_destructive: BoolProperty(name="Duplicate Before Destructive Fix", default=True)
    max_elements_to_modify: IntProperty(name="Max Elements To Modify", default=5000, min=1)
    require_confirm_destructive: BoolProperty(name="Confirm Destructive Actions", default=False)
    report_text: bpy.props.StringProperty(name="Report", default="")


def register_properties():
    bpy.utils.register_class(HPMESH_Properties)
    bpy.types.Scene.hpmesh = PointerProperty(type=HPMESH_Properties)


def unregister_properties():
    del bpy.types.Scene.hpmesh
    bpy.utils.unregister_class(HPMESH_Properties)
