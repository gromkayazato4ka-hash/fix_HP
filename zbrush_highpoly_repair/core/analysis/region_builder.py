def regions_from_faces(face_indices):
    return [{"faces": sorted(face_indices)}] if face_indices else []
