import bpy


def cleanup_blender_data():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj)
    for mesh in list(bpy.data.meshes):
        bpy.data.meshes.remove(mesh)
    for material in list(bpy.data.materials):
        bpy.data.materials.remove(material)


def mesh_object_add(name: str):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name=name, object_data=mesh)
    return obj
