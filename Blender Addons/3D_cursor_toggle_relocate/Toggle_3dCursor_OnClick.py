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
#Copyright 2014 Ryan Sweeney

bl_info = {
    "name": "Cookie Rig UI",
    "author": "Ryan Sweeney",
    "version": (1, 0),
    "blender": (2, 71, 0),
    "location": "View3D > Properties Panel > 3D Cursor",
    "description": "Adds a toggle to the 3D Cursor in the properties tab.",
    "warning": "",
    "wiki_url": "http://sweenist.wordpress.com",
    "category": "3D View"}

import bpy

class VIEW3D_PT_view3d_cursor_toggle(VIEW3D_PT_view3d_cursor):
    """Turns Mouse Action on/off for placing 3D Cursor"""
       
    def draw(self, context):
        keymaps = context.window_manager.keyconfigs['Blender User'].keymaps['3D View'].keymap_items
        cursor_key = keymaps['view3d.cursor3d'].active
        
        
    