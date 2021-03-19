import os
import sys


ADDON = "blender_extra_tools"


def find_my_addon():
    addon_modules = [
        module for module in addon_utils.modules()
        if module.__name__ == ADDON
    ]
    return addon_modules[0] if len(addon_modules) > 0 else None


if os.path.basename(sys.argv[0]).startswith("blender"):
    import shutil
    import unittest

    import bpy
    import addon_utils

    addon_module = find_my_addon()
    print("Add-on:", addon_module or "not found")

    path_dest_addon = None
    if not addon_module:
        path_user_scripts_addons = bpy.utils.user_resource('SCRIPTS', "addons", create=True)  # noqa E501
        print(f"Add-ons load dir: '{path_user_scripts_addons}'")
        path_src_addon = os.path.abspath(
            os.path.join(os.path.dirname(__file__), f"../{ADDON}")
        )
        path_dest_addon = os.path.abspath(
            os.path.join(path_user_scripts_addons, f"{ADDON}")
        )
        print(f"Copying Add-on from '{path_src_addon}'")
        all_non_py = shutil.ignore_patterns("__pycache__")
        shutil.copytree(path_src_addon, path_dest_addon, ignore=all_non_py)
        print(f"Add-on copied to '{path_dest_addon}'")
        addon_utils.modules_refresh()
        addon_module = find_my_addon()

    bl_info = addon_utils.module_bl_info(addon_module)
    print("Version:", bl_info.get("version", (-1, -1, -1)))

    _, is_loaded = addon_utils.check(ADDON)
    if not is_loaded:
        print("Enabling Add-on...", end="")
        addon_utils.enable(ADDON)
        print("done")

    try:
        print("=== Tests ===")
        argv = [__file__, "discover", "-p", "bl_test*.py"]
        unittest.main(module=None, argv=argv, verbosity=2)
    except SystemExit as ex:
        print("=============")
        if path_dest_addon:
            print(f"Removing Add-on at '{path_dest_addon}'")
            shutil.rmtree(path_dest_addon)
            print("Add-on removed")

        print(f"Exit code: {ex.code:d}")
        sys.exit(ex.code)
else:
    print(f"usage: blender -b -P {__file__}")
    sys.exit(1)
