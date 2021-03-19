# Blender Extra Tools Add-on
[Blender](https://www.blender.org/) Add-on with extra tools and features.

## Getting Started

### Installation

`Edit` > `Preferences` > `Add-ons` > `Install...`

### Usage

In 3D View / Object Mode:

* Select objects then `Object` > `Make Links` > `Link materials directly to the object`
* `Object` > `Rename all Mesh Data to match Object name`

## Development

Add-on source scripts are in the [blender_extra_tools](./blender_extra_tools) package. 

Optionally, install [fake-bpy-module-2.92](https://pypi.org/project/fake-bpy-module-2.92/) 
to remove Python linter warnings about missing `bpy` module.

### Debugging

Use [VS Code](https://code.visualstudio.com/) and 
[Blender Development extension][1] to install and debug the Add-on in Blender. 

Set the extension Workspace setting `Blender › Addon: Load Directory` to the 
Add-on [`blender_extra_tools`](./blender_extra_tools) package directory:

```
"blender.addon.loadDirectory": "blender_extra_tools",
```

### Running the tests

To avoid issues with module imports, test scripts are located in the [blender_extra_tools.tests](./blender_extra_tools/tests) 
sub-package. 

* To run all the tests which do not require Blender API (files matching `test*.py`)
execute the following command from the repository root:

    ```
    python -m unittest -v
    ```

* To run all the tests which use Blender API (files matching `bl_test*.py`) 
in Blender execute the following command from the repository root:

    ```
    blender -b -P scripts/run_bl_tests_in_blender.py
    ```

* To run tests from a single Blender test script file (file matching `bl_test*.py`) 
in Blender which has the Add-on installed already execute the following command from the repository root:

    ```
    blender -b -P tests/bl_test_<test name>.py
    ```

    Alternatively, to run tests from within VS Code first start debuggable
    Blender instance by executing `Blender: Start` command,
    open the test file and then execute [`Blender: Run Script`][2] command.

## Built With

* [VSCode](https://code.visualstudio.com/) / [Blender Development][1]
* [fake-bpy-module-2.92](https://pypi.org/project/fake-bpy-module-2.92/)
* [flake8](https://flake8.pycqa.org/en/latest/)

## License
[GPL-3.0 License](./LICENSE)

[1]: <https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development>
[2]: <https://github.com/JacquesLucke/blender_vscode#how-can-i-run-the-script-in-blender>
