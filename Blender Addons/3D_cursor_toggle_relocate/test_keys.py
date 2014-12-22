# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>
bl_info = {
    "name": "3D Cursor Replacement",
    "author": "Ryan Sweeney",
    "version": (1, 0),
    "blender": (2, 7, 2),
    "location": "3d View > Tools",
    "description": "Toggle the left mouse click for cursor placement",
    "warning": "",
    "category": "3D View"}
    
import bpy
from bpy.props import BoolProperty
from bpy.types import Panel


class TEST_VIEW3D_toggle_cursor_click(Panel):
    """Turns the Cursor placement with LMB on and off """
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "3D Cursor Toggle"
    bl_options = {'DEFAULT_CLOSED'}
    #bl_idname = "VIEW3D_PT_view3d_cursor_toggle"
    
    place_by_click = BoolProperty(name="toggle_3d_lmb", description="") 
    
    @classmethod
    def poll(cls, context):
        view = context.space_data
        return (view is not None)
    
    def draw(self, context):
        layout = self.layout
        
        view = context.space_data
        
        layout.column.prop(view, "cursor_location", text="location")
        layout.row.prop(view, "place_by_click", text="Toggle Click on/off",toggle=True)
                
    def execute(self, context):
        wm = context.window_manager
        wm.keyconfigs.user.keymaps['3D View'].keymap_items['view3d.cursor3d'].active = place_by_click
        
def register():
    bpy.utils.register_module(__name__)
    #bpy.utils.register_class(TEST_VIEW3D_toggle_cursor_click)
def unregister():
    #bpy.utils.unregister_class(TEST_VIEW3D_toggle_cursor_click)
    bpy.utils.unregister_module(__name__)