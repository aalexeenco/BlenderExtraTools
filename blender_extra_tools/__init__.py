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


from . import blender_extra_ops

bl_info = {
    "name": "Blender Extra Tools",
    "author": "aalexeenco",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "description": "Extra tools and features.",
    "warning": "",
    "doc_url": "https://aalexeenco.github.io/BlenderExtraTools/v1.0.0/",
    "category": "Object",
}


def register():
    blender_extra_ops.register()


def unregister():
    blender_extra_ops.unregister()
