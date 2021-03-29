import os
import sys


ADDON = "blender_extra_tools"


def find_addon():
    addon_modules = [
        module for module in addon_utils.modules()
        if module.__name__ == ADDON
    ]
    return addon_modules[0] if len(addon_modules) > 0 else None


def addon_zip_and_install():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    zip_file_name = shutil.make_archive("addon-install", "zip", root_dir=root_dir, base_dir=ADDON)  # noqa E501
    path_addon_zip = os.path.abspath(
        os.path.join(root_dir, f"{zip_file_name}")
    )
    result = bpy.ops.preferences.addon_install(filepath=path_addon_zip)
    if 'FINISHED' in result:
        os.remove(path_addon_zip)
        return True
    return False


def addon_enable_if_not_loaded():
    _, is_loaded = addon_utils.check(ADDON)
    if not is_loaded:
        print("Enabling Add-on...", end="", flush=True)
        bpy.ops.preferences.addon_enable(module=ADDON)
        print("done")


def run_tests():
    try:
        argv = [__file__, "discover", "-p", "bl_test*.py"]
        unittest.main(module=None, argv=argv, verbosity=2)
    except SystemExit as ex:
        return ex.code


if os.path.basename(sys.argv[0]).startswith("blender"):
    import shutil
    import unittest

    import bpy
    import addon_utils

    addon_module = find_addon()
    print("Add-on:", addon_module or "not found")

    remove_addon_on_exit = False
    if not addon_module:
        remove_addon_on_exit = addon_zip_and_install()

        bpy.ops.preferences.addon_refresh()

        addon_module = find_addon()
        print("Installed Add-on:", addon_module or "not installed")

    bl_info = addon_utils.module_bl_info(addon_module)
    print("Version:", bl_info.get("version", (-1, -1, -1)))

    addon_enable_if_not_loaded()

    print("===== Tests =====")
    exitCode = run_tests()
    print("=== End Tests ===")

    if remove_addon_on_exit:
        print("Removing Add-on...", end="", flush=True)
        path_user_scripts_addons = bpy.utils.user_resource('SCRIPTS', "addons")  # noqa E501
        path_addon = os.path.abspath(
            os.path.join(path_user_scripts_addons, f"{ADDON}")
        )
        shutil.rmtree(path_addon)
        print("done")

    print(f"Exit code: {exitCode:d}")
    sys.exit(exitCode)
else:
    print(f"usage: blender -b -P {__file__}")
    sys.exit(1)
