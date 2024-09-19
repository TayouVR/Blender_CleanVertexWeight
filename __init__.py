#!/usr/bin/env python
# SPDX-License-Identifier: GPL-3.0-only
#
# Copyright (C) 2024 Tayou <tayou@gmx.net>
#
# This file is part of the Blender Plugin "Vertex Weight Cleanup" by Tayou.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; If not, see <https://www.gnu.org/licenses/>.

import bpy

bl_info = {
    "name": "Vertex Weight Cleanup",
    "category": "Mesh",
    "author": "Tayou",
    "location": "Mesh > Context Menu > cleanup vertex weights",
    "description": "Cleans up the actively selected mesh by removing all 0-weight vertices from all vertex groups.",
    "version": (1, 0, 0),
    "blender": (3, 4, 1),
    "tracker_url": 'https://github.com/TayouVR/Blender_merge-bones/issues',
    "doc_url": "https://github.com/TayouVR/Blender_merge-bones",
    "wiki_url": 'https://github.com/TayouVR/Blender_merge-bones',
    'warning': '',
}


# --------------------------------------------
# look at TODOs you idiot!
# --------------------------------------------

class CleanVertexWeights(bpy.types.Operator):
    """Merge Selected Bones into Active"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "mesh.cleanup_vert_weights"  # Unique identifier for buttons and menu items to reference.
    bl_label = "cleanup vertex weights"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):
        print("Starting vertex weight cleanup!!!")

        # Get the active mesh object
        obj = bpy.context.object
        if obj is None or obj.type != 'MESH':
            print("No mesh object selected.")
        else:
            # iterate over each vertex group
            for vgroup in obj.vertex_groups:

                # iterate over each vertex in the mesh
                for vert in obj.data.vertices:

                    try:  # this will throw an error if the vertex is not part of the group
                        weight = vgroup.weight(vert.index)

                        # if the weight is 0, remove it from the group
                        if weight == 0:
                            vgroup.remove([vert.index])
                    except RuntimeError:
                        pass

        print("vertex weight cleanup Done!!!")
        return {'FINISHED'}  # Lets Blender know the operator finished successfully.


def draw_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(CleanVertexWeights.bl_idname)


def register():
    bpy.utils.register_class(CleanVertexWeights)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_menu)


def unregister():
    bpy.utils.unregister_class(CleanVertexWeights)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_menu)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    print("Test executing plugin, registering menu")
    register()
