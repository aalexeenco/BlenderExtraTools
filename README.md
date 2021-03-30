# Blender Extra Tools Add-on
[![GitHub version](https://badge.fury.io/gh/aalexeenco%2FBlenderExtraTools.svg)](https://github.com/aalexeenco/BlenderExtraTools/releases/latest)
[![tests](https://github.com/aalexeenco/BlenderExtraTools/actions/workflows/test-addon.yml/badge.svg)](https://github.com/aalexeenco/BlenderExtraTools/actions/workflows/test-addon.yml)

[Blender](https://www.blender.org/) Add-on with extra tools and features.

## Getting Started

### Installation

Download the [latest](https://github.com/aalexeenco/BlenderExtraTools/releases/latest/download/addon_blender_extra_tools.zip) version and install in Blender menu
`Edit` > `Preferences` > `Add-ons` tab > click `Install...` button and select the downloaded zip file.

### Usage

In 3D View / Object Mode:

* Select objects then `Object` > `Make Links` > `Link materials directly to the object`
* `Object` > `Rename all Mesh Data to match linked Object name`

## Development

Add-on source scripts are located in the [blender_extra_tools](./blender_extra_tools) package. 

### Prerequisites

Install [fake-bpy-module-2.92](https://pypi.org/project/fake-bpy-module-2.92/) 
to remove Python errors about missing `bpy` module.

```
pip install -r requirements.txt
```

### Debugging

Use [VS Code](https://code.visualstudio.com/) and 
[Blender Development extension][1] to install and debug the Add-on in Blender. 

Set the extension Workspace setting `Blender › Addon: Load Directory` to the 
Add-on [`blender_extra_tools`](./blender_extra_tools) package directory:

```
"blender.addon.loadDirectory": "blender_extra_tools",
```

### Running the tests

Test scripts are located in the separate sibling [tests](./tests) package. 

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

    or using Docker containers, e.g.

    ```
    docker run -it --rm --workdir /work -v <path to repository root>:/work nytimes/blender:2.92-cpu-ubuntu18.04 blender -b -P scripts/run_bl_tests_in_blender.py
    ```

* To run tests from a single Blender test script file (file matching `bl_test*.py`) 
in Blender which has the Add-on installed already execute the following command from the repository root:

    ```
    blender -b -P tests/bl_test_<test suite>.py
    ```

    Alternatively, to run tests from within VS Code first start debuggable
    Blender instance by executing `Blender: Start` command,
    open the test file and then execute [`Blender: Run Script`][2] command.

## Built With

* [VSCode](https://code.visualstudio.com/) / [Blender Development][1]
* [fake-bpy-module-2.92](https://pypi.org/project/fake-bpy-module-2.92/)
* [flake8](https://flake8.pycqa.org/en/latest/)
* [rd-blender-docker](https://github.com/nytimes/rd-blender-docker)
* [Git Release](https://github.com/marketplace/actions/git-release) - A GitHub Action for creating a GitHub Release with Assets and Changelog

## License
[GPL-3.0 License](./LICENSE)

[1]: <https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development>
[2]: <https://github.com/JacquesLucke/blender_vscode#how-can-i-run-the-script-in-blender>
