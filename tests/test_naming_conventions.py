import inspect
import typing
import unittest

from blender_extra_tools import blender_extra_ops


def operator_bl_idname_by_convention(clazz: typing.Type[typing.Any]) -> str:
    return clazz.__name__.replace("_OT_", ".").lower()


class BlenderNamingConventionTests(unittest.TestCase):
    def test_all_operator_classes_have_valid_bl_idname(self):
        operator_classes = [
            m[1] for m
            in inspect.getmembers(blender_extra_ops, inspect.isclass)
            if m[1].__module__ == blender_extra_ops.__name__
        ]
        for operator_class in operator_classes:
            with self.subTest(
                className=operator_class.__name__,
                bl_idname=operator_class.bl_idname
            ):
                self.assertEqual(
                    operator_class.bl_idname,
                    operator_bl_idname_by_convention(operator_class)
                )
