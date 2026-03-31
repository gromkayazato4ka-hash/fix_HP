"""Compatibility manifest module.

Some Blender install paths may probe top-level modules from an archive.
Keeping register/unregister here prevents install-time crashes if this module
is discovered directly.
"""

bl_info = {
    "name": "ZBrush High-Poly Repair",
    "author": "Codex",
    "version": (0, 2, 1),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > HighPoly Repair",
    "description": "Detect and conservatively repair ZBrush import shading artifacts on dense meshes.",
    "category": "Mesh",
}


def register():
    return None


def unregister():
    return None
