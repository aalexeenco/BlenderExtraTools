# Blender Extra Tools - Blender Add-on with extra tools.
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


class OBJECT_OT_link_all_materials_to_object(bpy.types.Operator):
    """
    Links all the materials currently linked to the object's Mesh data directly
    to the Object data-block.

    Blender keeps track of which material was linked to the object and which
    to the mesh for the given material index (slot). Changing link type will
    make corresponding material assigned to the slot.
    For example, if slot link is set to Object and material is linked and then
    link type is changed to Mesh, but no material is linked to mesh for
    the given slot index (i.e. iт is None), then executing this operator will
    restore slot link type back to Object, but will not unlink the material
    which was previously linked to the object for the given slot index.
    """

    bl_idname = "object.link_all_materials_to_object"
    """Operator id used to register it in `bpy.ops`"""

    bl_label = "Link materials directly to the object"
    bl_description = """Link materials currently linked to the object's data
    directly to the object too"""
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return any(obj for obj in context.selected_objects if len(obj.data.materials) > 0)  # noqa E501

    def execute(self, context):
        material_slots_which_link_material_to_mesh = [
            slot for obj in context.selected_objects
            for slot in obj.material_slots
            if obj.type == 'MESH' and len(obj.material_slots) > 0
            if slot.link == 'DATA'
        ]
        for material_slot in material_slots_which_link_material_to_mesh:
            material_linked_to_mesh = material_slot.material
            material_slot.link = 'OBJECT'
            if material_slot.material is None:
                material_slot.material = material_linked_to_mesh

        return {'FINISHED'}


class OBJECT_OT_rename_all_meshes_to_match_linked_object(bpy.types.Operator):
    """
    Renames all Mesh data-blocks to match their single linked object's name.
    """

    bl_idname = "object.rename_all_meshes_to_match_linked_object"
    """Operator id used to register it in `bpy.ops`"""

    bl_label = "Rename all Mesh Data to match linked Object name"
    bl_description = """Rename each Mesh data-block linked to a single object
    with mismatched name to match the linked object's name"""
    bl_options = {'REGISTER', 'UNDO'}

    @staticmethod
    def _all_objects_linked_to_single_user_mesh_with_mismatched_name():
        def is_obj_linked_to_single_nonlib_mesh_with_mismatched_name(obj):
            return obj.data and not obj.data.library \
                and obj.data.users == 1 \
                and obj.name != obj.data.name
        return filter(
            is_obj_linked_to_single_nonlib_mesh_with_mismatched_name,
            bpy.data.objects
        )

    @classmethod
    def poll(cls, context):
        return any(cls._all_objects_linked_to_single_user_mesh_with_mismatched_name())  # noqa E501

    def execute(self, context):
        for obj in self._all_objects_linked_to_single_user_mesh_with_mismatched_name():  # noqa E501
            obj.data.name = obj.name

        return {'FINISHED'}


def menu_rename_all_meshes_to_match_linked_object(self, context):
    self.layout.separator()
    self.layout.operator(
        OBJECT_OT_rename_all_meshes_to_match_linked_object.bl_idname)


def menu_link_all_materials_to_object(self, context):
    self.layout.separator()
    self.layout.operator(OBJECT_OT_link_all_materials_to_object.bl_idname)


def register():
    bpy.utils.register_class(
        OBJECT_OT_rename_all_meshes_to_match_linked_object)
    bpy.types.VIEW3D_MT_object.append(
        menu_rename_all_meshes_to_match_linked_object)
    bpy.utils.register_class(OBJECT_OT_link_all_materials_to_object)
    bpy.types.VIEW3D_MT_make_links.append(menu_link_all_materials_to_object)


def unregister():
    bpy.utils.unregister_class(
        OBJECT_OT_rename_all_meshes_to_match_linked_object)
    bpy.types.VIEW3D_MT_object.remove(
        menu_rename_all_meshes_to_match_linked_object)
    bpy.utils.unregister_class(OBJECT_OT_link_all_materials_to_object)
    bpy.types.VIEW3D_MT_make_links.remove(menu_link_all_materials_to_object)
