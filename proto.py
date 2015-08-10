bl_info = {
    "name": "LuthiTool",
    "author": "Ryan Sweeney",
    "version": (0, 1),
    "blender": (2, 72, 0),
    "location": "View3D > Add > Mesh > PieChart",
    "description": "Adds a pie graph to represent data",
    "warning": "Prototype",
    "wiki_url": "http://sweenist.wordpress.com/",
    "category": "Add Mesh"
}

import bpy

from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import FloatProperty, BoolProperty, IntProperty, EnumProperty, StringProperty, CollectionProperty, PointerProperty

class View3DPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"    

class BlendChartsPiePanel(View3DPanel, Panel):
    bl_category = "BlendData"    
    bl_context = "objectmode"
    bl_label = "Data"
    
    @classmethod
    def poll(cls, context):
        return (context.mode == 'OBJECT')
        
    def draw(self, context):
        wm = context.window_manager
        props = wm.blendcharts
        layout = self.layout
        if props:
            layout.label("Data Segments:")
            for prop in props:
                box = layout.box()
                row = box.row()
                row.prop(prop, "name")
                
                row = box.row()
                row.prop(prop, "value")
                
                row = box.row()
                row.alignment = 'RIGHT'
                row.label(("%.1f" % prop.percentage) + "%")
                
        else:
            box = layout.box()
            box.label("Please add a data input by clicking")
            box.label("[Add New Data] button below.")
        
class BlendChartsDataPanel(View3DPanel,Panel):
    bl_category = "BlendData"
    bl_space_type = "VIEW_3D"
    bl_context = "objectmode"
    bl_label = "Add Data"
    
    @classmethod
    def poll(cls, context):
        return (context.mode == 'OBJECT')
        
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator('wm.blendcharts_add_sample', text="Add New Data")
        
        row = layout.row()
        row.operator('wm.blendcharts_clear_samples', text="Clear Data Points")
        
        
class BlendChartsMeshPropertyGroup(PropertyGroup):
    radius = FloatProperty(
            name="Radius",
            description="Length from center to outer edge",
            default=1.0
            )
    thickness = FloatProperty(
            name="Thickness",
            description="Thickness of pie chart",
            default=0.25
            )
    hole = BoolProperty(
            name="center hole",
            description="Insert a hole in middle of pie. Uses Inner Radius",
            default=False
            )
    inner_radius = FloatProperty(
            name="Inner Radius",
            default=0.1,
            description="when center hole is selected this vlue determines percentage of gap from center",
            min=0.1,
            max=99.9
            )
            

class BlendChartsPropertyGroup(PropertyGroup):
    name = StringProperty(
            name="Name",
            description="Name of the represented Data",
            default="(none)")
    value = FloatProperty(
            name="Amount",
            description="Numeric Value of data in units",
            default=1.0
            )
    percentage = FloatProperty(
            name="Percentage",
            description="calculated percentage of representation",
            default=0
            )
            
class BlendCharts_OT_AddSample(Operator):
    bl_idname = "wm.blendcharts_add_sample"
    bl_label = "Click to add a new data sample"
    
    def invoke(self, context, event):
        wm = context.window_manager
        
        percentage = 100
        if(wm.blendcharts):
            amt = 1.0
            for bc in wm.blendcharts:
                amt += bc.value
            for bc in wm.blendcharts:
                bc.percentage = bc.value / amt * 100.0
            percentage = 100.0 / amt 
        else:
            bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=0.5)
        
        item = wm.blendcharts.add()
        item.value = 1.0
        item.name = "(none)"
        item.percentage = percentage
        
        print("invoked")
        print(event.value)
        return {'FINISHED'}
    
    def model(self):
        verts = []
        faces = []
        
        

class BlendCharts_OT_ClearSamples(Operator):
    bl_idname = "wm.blendcharts_clear_samples"
    bl_label = "Click to clear all data samples"
    
    def execute(self, context):
        wm = context.window_manager
        wm.blendcharts.clear()
        return {'FINISHED'}

class INFO_MT_blendchart_add(bpy.types.Menu):
    bl_idname = "INFO_MT_blendchart_add"
    bl_label = "Data Models"
    
    def draw(self, content):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("wm.blendcharts_add_sample", text="Pie Chart", icon="COLOR")

def menu_function(self, context):
    self.layout.separator()
    self.layout.menu("INFO_MT_blendchart_add", text="Pie Chart", icon="COLOR")

def register():
    bpy.utils.register_class(BlendChartsPiePanel)
    bpy.utils.register_class(BlendChartsDataPanel)
    bpy.utils.register_class(BlendChartsPropertyGroup)
    bpy.utils.register_class(BlendChartsMeshPropertyGroup)
    bpy.utils.register_class(BlendCharts_OT_AddSample)
    bpy.utils.register_class(BlendCharts_OT_ClearSamples)    
    
    bpy.types.WindowManager.blendcharts = CollectionProperty(type=BlendChartsPropertyGroup)
    bpy.types.Mesh.blendchart_pie = PointerProperty(type=BlendChartsMeshPropertyGroup)
    bpy.types.INFO_MT_mesh_add.append(menu_function)

if __name__=="__main__":
    register()