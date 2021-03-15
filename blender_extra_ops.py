# BlenderExtraTools - Blender Add-on with extra tools.
# Copyright (C) 2021  Andrei Alexeenco (https://github.com/aalexeenco)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License,
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import bpy
import itertools


class OBJECT_BLENDER_EXTRA_OT_link_all_materials_to_object(bpy.types.Operator):
    """
    Links all the materials currently linked to the object's Mesh data directly to the Object data-block.
    Blender keeps track of which material was linked to the object and which to the mesh for the given 
    material index (slot). Changing link type will make corresponding material assigned to the slot.
    For example, if slot link is set to Object and material is linked and then link type is changed
    to Mesh, but no material is linked to mesh for the given slot index (i.e. is is None), 
    then executing this operator will restore slot link type back to Object, but will not unlink
    the material which was previously linked to the object for the given slot index.  
    """
    bl_idname = "object.blender_extra_link_all_materials_to_object"
    bl_label = "Link materials directly to the object"
    bl_description = "Link materials currently linked to the object's data directly to the object too"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        material_slots_which_link_material_to_mesh = [
            slot for obj in context.selected_objects for slot in obj.material_slots
            if obj.type == 'MESH' and len(obj.material_slots) > 0
            if slot.link == 'DATA'
        ]
        for material_slot in material_slots_which_link_material_to_mesh:
            material_linked_to_mesh = material_slot.material
            material_slot.link = 'OBJECT'
            # NOTE: setting slot material to None will unlink slot's linked material from the object
            if material_linked_to_mesh is not None:
                material_slot.material = material_linked_to_mesh

        return {'FINISHED'}


class OBJECT_BLENDER_EXTRA_OT_rename_to_match_object(bpy.types.Operator):
    """Renames all Mesh data-blocks with single linked object to match their linked object's name."""
    bl_idname = "object.blender_extra_rename_all_data_to_match_object"
    bl_label = "Rename all Mesh Data to match linked Object name"
    bl_description = "Rename all Mesh data-blocks with single linked object to match their linked object's name"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        meshes_with_nonmatching_obj_name = [
            (obj.data, obj.name) for obj in bpy.data.objects
            if obj.data is not None and obj.data.name != obj.name and obj.data.library is None
        ]

        if len(meshes_with_nonmatching_obj_name) > 0:
            def with_mesh_as_key(tuple): return tuple[0]
            for mesh, group in itertools.groupby(meshes_with_nonmatching_obj_name, with_mesh_as_key):
                mesh_to_object_name_tuples = list(group)
                print(f"{mesh.name_full}: {mesh_to_object_name_tuples}")

                if len(mesh_to_object_name_tuples) > 1:
                    continue

                mesh_single_object_tuple = mesh_to_object_name_tuples[0]
                obj_name = mesh_single_object_tuple[1]
                mesh.name = obj_name

        return {'FINISHED'}


def menu_object_rename_all_data_to_match_object(self, context):
    self.layout.separator()
    self.layout.operator(
        OBJECT_BLENDER_EXTRA_OT_rename_to_match_object.bl_idname)


def menu_object_link_all_materials_to_object(self, context):
    self.layout.separator()
    self.layout.operator(
        OBJECT_BLENDER_EXTRA_OT_link_all_materials_to_object.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_BLENDER_EXTRA_OT_rename_to_match_object)
    bpy.types.VIEW3D_MT_object.append(
        menu_object_rename_all_data_to_match_object)
    bpy.utils.register_class(
        OBJECT_BLENDER_EXTRA_OT_link_all_materials_to_object)
    bpy.types.VIEW3D_MT_make_links.append(
        menu_object_link_all_materials_to_object)


def unregister():
    bpy.utils.unregister_class(OBJECT_BLENDER_EXTRA_OT_rename_to_match_object)
    bpy.types.VIEW3D_MT_object.remove(
        menu_object_rename_all_data_to_match_object)
    bpy.utils.unregister_class(
        OBJECT_BLENDER_EXTRA_OT_link_all_materials_to_object)
    bpy.types.VIEW3D_MT_make_links.remove(
        menu_object_link_all_materials_to_object)


if __name__ == "__main__":
    register()
