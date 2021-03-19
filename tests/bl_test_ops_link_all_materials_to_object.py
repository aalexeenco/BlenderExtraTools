import bpy
import sys
import unittest


is_run_as_script = __name__ in ["__main__", "<run_path>"]
_initial_sys_path = None
if is_run_as_script and not __package__:
    __package__ = "tests"

    import os
    import importlib

    for key, mod in sys.modules.items():
        if key != __name__ and getattr(mod, "__package__", "") == __package__:
            print("Reload", mod)
            importlib.reload(mod)

    path_run = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    _initial_sys_path = sys.path
    sys.path.insert(0, path_run)


from . import blender_utils as bl  # noqa E407


if _initial_sys_path:
    sys.path = _initial_sys_path


def setUpModule():
    bl.cleanup_blender_data()


class LinkMaterialsToObjectTests(unittest.TestCase):
    def tearDown(self):
        bl.cleanup_blender_data()

    def test_operator_menu_is_enabled_if_one_or_more_objects_with_mesh_materials_are_selected(self):  # noqa E501
        obj1 = bl.mesh_object_add("Box")
        with_mesh_materials(obj1, ["Material1", "Material2"])
        selected_objects = [obj1]
        self.assertTrue(self._poll_operator_for(selected_objects))

        obj2 = bl.mesh_object_add("Cube")
        selected_objects = [obj1, obj2]
        self.assertTrue(self._poll_operator_for(selected_objects))

        with_mesh_materials(obj2, ["Material1", "Material2"])
        self.assertTrue(self._poll_operator_for(selected_objects))

    def test_operator_menu_is_disabled_if_no_objects_with_mesh_materials_are_selected(self):  # noqa E501
        selected_objects = []
        self.assertFalse(self._poll_operator_for(selected_objects))

        selected_objects = [bl.mesh_object_add("Cube")]
        self.assertFalse(self._poll_operator_for(selected_objects))

    def test_Given_selected_objects_with_materials_linked_to_mesh_data_Then_same_materials_are_linked_to_object_at_corresponding_slots(self):  # noqa E501
        obj1 = bl.mesh_object_add("Cube1")
        with_mesh_materials(obj1, ["Mesh_Mat_1", "Mesh_Mat_2"])
        obj2 = bl.mesh_object_add("Cube2")
        with_mesh_materials(obj2, ["Mesh_Mat_1", "Mesh_Mat_2"])

        selected_objects = [obj1, obj2]
        self._execute_operator_for(selected_objects)

        for obj in selected_objects:
            for i, slot in enumerate(obj.material_slots):
                with self.subTest(obj=obj.name, material_slot=slot.name, link=slot.link):  # noqa E501
                    self.assertEqual(slot.link, 'OBJECT')
                    self.assertEqual(slot.material, obj.data.materials[i])

    def test_Given_selected_objects_without_any_materials_linked_Then_material_links_are_not_created(self):  # noqa E501
        selected_objects = [
            bl.mesh_object_add("Cube1"),
            bl.mesh_object_add("Cube2")
        ]

        self.assertRaisesRegex(
            RuntimeError,
            "Operator .*\\.poll\\(\\) failed, context is incorrect",
            self._execute_operator_for, selected_objects
        )

        for obj in selected_objects:
            self.assertEqual(len(obj.material_slots), 0)

    def test_unselected_objects_are_unaffected(self):
        for name in ["Cube1", "Cube2", "Cube3"]:
            with_mesh_materials(
                bl.mesh_object_add(name), ["Mesh_Mat_1", "Mesh_Mat_2"])

        selected_objects = [bpy.data.objects["Cube2"]]
        self._execute_operator_for(selected_objects)

        unselected_objects = [
            obj for obj in bpy.data.objects if obj not in selected_objects
        ]
        for obj in unselected_objects:
            for slot in obj.material_slots:
                with self.subTest(obj=obj.name, material_slot=slot.name, link=slot.link):  # noqa E501
                    self.assertNotEqual(slot.link, 'OBJECT')

    def test_material_slots_with_link_type_object_are_unaffected(self):
        obj = bl.mesh_object_add("Cube")
        with_mesh_materials(obj, ["Mesh_Mat_1", "Mesh_Mat_2"])
        obj_materials = with_obj_materials(obj, [None, "Obj_Mat_2"])
        _set_material_links(obj, ['OBJECT', 'OBJECT'])

        self._execute_operator_for([obj])

        for slot, obj_material in zip(obj.material_slots, obj_materials):
            self.assertEqual(slot.link, 'OBJECT')
            self.assertEqual(slot.material, obj_material)

    def test_materials_already_linked_to_the_object_take_precedence_when_changing_link_type(self):  # noqa E501
        obj = bl.mesh_object_add("Cube")
        with_mesh_materials(obj, [None, "Mesh_Mat_2"])
        obj_materials = with_obj_materials(obj, ["Obj_Mat_1", "Obj_Mat_2"])
        _set_material_links(obj, ['DATA', 'DATA'])

        self._execute_operator_for([obj])

        for slot, obj_material in zip(obj.material_slots, obj_materials):
            self.assertEqual(slot.link, 'OBJECT')
            self.assertEqual(slot.material, obj_material)

    def _execute_operator_for(self, selected_objects):
        result = bpy.ops.object.link_all_materials_to_object(
            _context_copy(selected_objects=selected_objects))
        self.assertIn('FINISHED', result)

    def _poll_operator_for(self, selected_objects):
        return bpy.ops.object.link_all_materials_to_object.poll(
            _context_copy(selected_objects=selected_objects))


def material_new(name):
    return bpy.data.materials.new(name)


def with_mesh_materials(obj, mesh_material_names: list):
    mesh_materials = []
    obj.data.materials.clear()
    for name in mesh_material_names:
        material = None if name is None \
            else material_new(name) if bpy.data.materials.get(name) is None \
            else bpy.data.materials[name]
        obj.data.materials.append(material)
        mesh_materials.append(material)
    return mesh_materials


def with_obj_materials(obj, obj_material_names: list):
    obj_materials = []
    for slot, name in zip(obj.material_slots, obj_material_names):
        current_link = slot.link
        slot.link = 'OBJECT'
        material = None if name is None else material_new(name)
        slot.material = material
        obj_materials.append(material)
        slot.link = current_link
    return obj_materials


def _context_copy(selected_objects):
    ctx = bpy.context.copy()
    ctx["selected_objects"] = selected_objects
    return ctx


def _set_material_links(obj, links: list):
    for slot, link in zip(obj.material_slots, links):
        slot.link = link


if is_run_as_script:
    argv = [__file__]
    unittest.main(module=__name__, argv=argv, exit=False, verbosity=2)
