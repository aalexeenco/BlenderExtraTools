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


class RenameAllMeshDataToMatchSingleLinkedObjectTests(unittest.TestCase):
    def tearDown(self):
        bl.cleanup_blender_data()

    def test_operator_menu_is_enabled_if_there_are_meshes_linked_to_single_obj_with_mismatched_name(self):  # noqa E501
        obj = bl.mesh_object_add("Suzanne")
        obj.data.name = "Monkey"

        self.assertTrue(self._poll_operator())

    def test_operator_menu_is_disabled_if_there_are_no_meshes_linked_to_single_obj_with_mismatched_name(self):  # noqa E501
        bl.mesh_object_add("Plane")
        bl.mesh_object_add("Cube")
        bpy.ops.object.add_named(name="Cube", linked=True)
        obj = bl.mesh_object_add("Suzanne")
        obj.data.name = "Monkey"
        bpy.ops.object.add_named(name="Suzanne", linked=True)
        bpy.data.objects["Suzanne.001"].name = obj.data.name

        self.assertFalse(self._poll_operator())

    def test_all_meshes_each_linked_to_single_object_with_mismatched_name_are_renamed(self):  # noqa E501
        obj = bl.mesh_object_add("Suzanne")
        obj.data.name = "Monkey"
        prev_mesh_name = obj.data.name

        self._execute_operator()

        self.assertEqual(obj.data.name, obj.name)
        self.assertIsNone(bpy.data.meshes.get(prev_mesh_name))

    def test_all_meshes_each_linked_to_more_than_one_object_are_not_renamed(self):  # noqa E501
        test_data = [
            ("Cube", "Cube", 5),
            ("Suzanne", "Monkey", 2),
            ("Donut", "Donut", 2)
        ]
        for obj_name, mesh_name, count in test_data:
            obj_required_for_op_to_be_enabled = bl.mesh_object_add(f"Test_{obj_name}")  # noqa E501
            obj_required_for_op_to_be_enabled.data.name = f"Mesh_{obj_name}"

            obj = bl.mesh_object_add(obj_name)
            obj.data.name = mesh_name
            obj_copy_range = range(1, count)
            for i in obj_copy_range:
                bpy.ops.object.add_named(name=obj.name, linked=True)

            self._execute_operator()

            obj_copies = [
                bpy.data.objects[f"{obj.name}.00{i}"] for i in obj_copy_range  # noqa E501
            ]
            for test_obj in [obj, *obj_copies]:
                with self.subTest(obj=test_obj.name, mesh=test_obj.data.name, expected_mesh=mesh_name):  # noqa E501
                    self.assertEqual(test_obj.data.name, mesh_name)

    def test_all_meshes_each_linked_to_single_object_with_matching_name_are_ignored(self):  # noqa E501
        obj = bl.mesh_object_add("Suzanne")
        obj.data.name = "Monkey"

        ignored_obj = bl.mesh_object_add("IgnoredObject")

        self._execute_operator()

        self.assertEqual(ignored_obj.data.name, ignored_obj.name)

    def _execute_operator(self):
        result = bpy.ops.object.rename_all_meshes_to_match_linked_object()
        self.assertIn('FINISHED', result)

    def _poll_operator(self):
        return bpy.ops.object.rename_all_meshes_to_match_linked_object.poll()


if is_run_as_script:
    argv = [__file__]
    unittest.main(module=__name__, argv=argv, exit=False, verbosity=2)
