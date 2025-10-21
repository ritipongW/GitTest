import bpy
import mathutils  # Import mathutils properly

class ResetViewOperator(bpy.types.Operator):
    """Focus view on the last imported object"""
    bl_idname = "view3d.reset_view"
    bl_label = "Reset View"
    
    def execute(self, context):
        # Get the last imported mesh object
        imported_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        
        if not imported_objects:
            self.report({'WARNING'}, "No imported object found to focus on")
            return {'CANCELLED'}

        # Select the last object that was added
        imported_object = imported_objects[-1]
        
        # Select and set it as active
        imported_object.select_set(True)
        context.view_layer.objects.active = imported_object
        
        # Check if we are in Edit Mode
        if imported_object.mode == 'EDIT':
            # Switch to Object Mode if needed
            bpy.ops.object.mode_set(mode='OBJECT')
        elif imported_object.mode == 'SCULPT':
            bpy.ops.object.mode_set(mode='OBJECT')
        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            
        # Deselect all objects first
        bpy.ops.object.select_all(action='DESELECT')

        # Select and set it as active
        imported_object.select_set(True)
        context.view_layer.objects.active = imported_object

        # Reset the view to focus on this object
        bpy.ops.view3d.view_selected()
        

        return {'FINISHED'}
    
class ClearViewOperator(bpy.types.Operator):
    """Clear all objects on scene"""
    bl_idname = "view3d.clear_view"
    bl_label = "Clear View"
    
    def execute(self, context):
        # Get all mesh objects in the scene
        imported_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        
        if not imported_objects:
            self.report({'WARNING'}, "No imported objects found")
            return {'CANCELLED'}

        # Delete all mesh objects
        for obj in imported_objects:
            bpy.data.objects.remove(obj, do_unlink=True)

        self.report({'INFO'}, "All mesh objects deleted")
        
        return {'FINISHED'}  # ✅ Ensure a valid return value
    
    
class ImportSTL(bpy.types.Operator):
    """Import an STL file"""
    bl_idname = "import.stl_file"
    bl_label = "Import STL"

    def execute(self, context):
        # Modify the path to your STL file
        file_path = "D:/3DProject/Blender_Test/jawhole.stl"
        # Import the STL file
        bpy.ops.wm.stl_import(filepath=file_path)
        # Get the last imported object
        imported_object = context.selected_objects[-1]
        
        # remane the object
        if imported_object.name != "mesh_example":
            imported_object.name = "mesh_example"
        
        # Ensure the object is in Object Mode before transformations
        bpy.ops.object.mode_set(mode='OBJECT')

        # Apply transformations to reset the origin to the bottom of the object
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        # Get the object's bounding box
        min_z = min((imported_object.matrix_world @ mathutils.Vector(v)).z for v in imported_object.bound_box)

        # Move the object so the bottom is at Z = 0
        imported_object.location.z -= min_z
        # Move the object so the bottom is at X = 0
        imported_object.location.x = 0
        # Move the object so the bottom is at Y = 0
        imported_object.location.y = 0
        
        # Auto-focus the view on the new object
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
        imported_object.select_set(True)  # Select the imported object
        context.view_layer.objects.active = imported_object  # Set it as the active object
        bpy.ops.view3d.view_selected()  # Focus the view on the object

        return {'FINISHED'}
    
class ExportSTL(bpy.types.Operator):
    """Export an STL file"""
    bl_idname = "export.stl_file"
    bl_label = "Export STL"
    
    

class SelectOperator(bpy.types.Operator):
    """Select mesh regions"""
    bl_idname = "mesh.select_circle"
    bl_label = "Select_Circle"
    
    def execute(self, context):
        # Get the last imported mesh object
        imported_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        if not imported_objects:
            self.report({'WARNING'}, "No imported object found to focus on")
            return {'CANCELLED'}
        
        imported_object = imported_objects[-1]
        
        # Make sure we're in OBJECT mode before selecting objects
        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
         # Make sure object is selected and active
        bpy.ops.object.select_all(action='DESELECT')
        imported_object.select_set(True)
        context.view_layer.objects.active = imported_object
        
        # Switch to Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')
        # Ensure Face Selection Mode is enabled
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
        
        # Get the user-defined circle size
        #circle_size = context.scene.circle_size
        circle_size = 10.0

        # Start Circle Select with specified size
        bpy.ops.view3d.select_circle('INVOKE_DEFAULT', radius=int(circle_size))
        
        return {'FINISHED'}
   
    
class ApplySelectOperator(bpy.types.Operator):
    """Confirm to select mesh regions"""
    bl_idname = "mesh.apply_select_mesh"
    bl_label = "Select_Mesh"
    
    def execute(self, context):
         # Get the last imported mesh object
        imported_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        
        if not imported_objects:
            self.report({'WARNING'}, "No imported object found to focus on")
            return {'CANCELLED'}
        
        
         # Select the last object that was added
        imported_object = imported_objects[-1]
        
        # Show selected mesh region that you want only
        bpy.ops.mesh.hide(unselected=True)
        # Separate the selected mesh from other regions
        bpy.ops.mesh.separate(type='SELECTED')
        
        # Define the index of the object you want to delete
        object_index = 0 
        
        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
            #deselect all objects
            bpy.ops.object.select_all(action='DESELECT')
            # select the object
            bpy.data.objects[object_index].select_set(True)
            # delete all selected objects
            bpy.ops.object.delete()
        
        # re-name 
        bpy.data.objects[object_index].name = "NT"   
        
        ############## Way two ####################################
        # Access object by index
        #object_to_delete = bpy.data.objects[object_index]
        # Ensure the object is not linked to any collection
        #bpy.data.objects.remove(object_to_delete, do_unlink=True)
        ###########################################################

        return {'FINISHED'}


class CropSelectOperator(bpy.types.Operator):
    bl_idname = "mesh.crop_select"
    bl_label = "Crop_Select"
    
    def execute(self, context):
        
         # Get the last imported mesh object
        imported_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        if not imported_objects:
            self.report({'WARNING'}, "No imported object found to focus on")
            return {'CANCELLED'}
        # Set Sculpt Mode
        bpy.ops.object.mode_set(mode='SCULPT')
        # Activate the Lasso Hide tool (region h
        bpy.ops.wm.tool_set_by_id(name="builtin.lasso_hide")
        
        # Set the tool manually
        #bpy.ops.sculpt.border_hide()
        
        return {'FINISHED'}

class ApplyCropSelectOperator(bpy.types.Operator):
    bl_idname = "mesh.apply_crop_select"
    bl_label = "Apply_Crop_Select"
    
    def execute(self, context):
        
         # Get the last imported mesh object
        imported_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        if not imported_objects:
            self.report({'WARNING'}, "No imported object found to focus on")
            return {'CANCELLED'}
        
        # Select the last object that was added
        imported_object = imported_objects[-1]
        
        # check if to swap to edit mode
        if bpy.context.object.mode == 'SCULPT':
            bpy.ops.object.mode_set(mode='EDIT')
            # Select all object
            bpy.ops.mesh.select_all(action='SELECT')
            # Separate the selected mesh from other regions
            bpy.ops.mesh.separate(type='SELECTED')
         
        # Define the index of the object you want to delete
        object_index = 0    
        
        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
            #deselect all objects
            bpy.ops.object.select_all(action='DESELECT')
            # select the object
            bpy.data.objects[object_index].select_set(True)
            # delete all selected objects
            bpy.ops.object.delete()
        
        # re-name 
        bpy.data.objects[object_index].name = "NT"
            
        
        return {'FINISHED'}

class CropDeleteOperator(bpy.types.Operator):
    bl_idname = "mesh.crop_delete"
    bl_label = "Crop_Delete"
    
    def execute(self, context):
        
        return {'FINISHED'}
    
class SmoothMeshOperator(bpy.types.Operator):
    """Smooth patial or whole object"""
    bl_idname = "mesh.smooth_mesh"
    bl_label = "Smooth_mesh"
    
    def execute(self, context):
        # Get the last imported mesh object
        imported_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        
        if not imported_objects:
            self.report({'WARNING'}, "No imported object found to focus on")
            return {'CANCELLED'}

        # Select the last object that was added
        imported_object = imported_objects[-1]
        
         # Check if we are in Edit Mode
        if imported_object.mode == 'EDIT':
            bpy.ops.mesh.faces_shade_smooth()
        else:
            bpy.ops.object.shade_smooth()
            
        return {'FINISHED'}


class DeleteMeshOperator(bpy.types.Operator):
    """Select region before delete mesh"""
    bl_idname = "mesh.delete_mesh"
    bl_label = "Delete_Mesh"  
    
    def execute(self, context):
        # Get the last imported mesh object
        imported_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        
        # Select the last object that was added
        imported_object = imported_objects[-1]
        
        if not imported_objects:
            self.report({'WARNING'}, "No imported object found to focus on")
            return {'CANCELLED'}
        
        if imported_object.mode == 'OBJECT':
            self.report({'WARNING'}, "Please use select mesh before.")
            return {'CANCELLED'}

        # Select the last object that was added
        imported_object = imported_objects[-1]
        
        #bpy.ops.mesh.delete(type='EDGE_FACE')
        bpy.ops.mesh.delete(type='FACE')
        
        
        return {'FINISHED'}
    
class FillHolesOperator(bpy.types.Operator):
    bl_idname = "mesh.fill_mesh"
    bl_label = "Fill_Mesh"    
    

class TestPanel(bpy.types.Panel):
    bl_label = "3D Manipulation"
    bl_idname = "PT_TestPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = 'My Tools'

    def draw(self, context):
        layout = self.layout
        
        layout.label(text='Load & save object', icon="IMPORT")
        row = layout.row()
        row.operator('import.stl_file', text="Reload STL")
        row.operator('export.stl_file', text="Save STL")
        row = layout.row()
        row.operator('view3d.reset_view', text="Preview")
        row.operator('view3d.clear_view', text="Clear all")
        
        #
        
        #Edit Tools
        row = layout.row()
        row = layout.row()
        row.label(text='Edit mesh', icon="EDITMODE_HLT")
        row = layout.row()
        row.operator('mesh.select_circle', text="Select mesh")
        row.operator('mesh.apply_select_mesh', text="Apply")
        row = layout.row()
        row.operator('mesh.crop_select', text="Crop to select")
        row.operator('mesh.apply_crop_select', text="Apply")
        row = layout.row()
        row.operator('mesh.crop_delete', text="Crop to delete")
        row = layout.row()
        row.operator('mesh.smooth_mesh', text="Smooth mesh")
        row = layout.row()
        row.operator('mesh.delete_mesh', text="Delete mesh")
        row = layout.row()
        row.operator('mesh.fill_mesh', text="Fill holes")
        row = layout.row()
        row.label(text='Sculpt mesh', icon="SCULPTMODE_HLT")
        row = layout.row()
        row.operator('mesh.fill_mesh', text="Brush up")
        row = layout.row()
        row.operator('mesh.fill_mesh', text="Brush down")
        

def register():
    bpy.utils.register_class(TestPanel)
    bpy.utils.register_class(ImportSTL)
    bpy.utils.register_class(ExportSTL)
    bpy.utils.register_class(ResetViewOperator)
    bpy.utils.register_class(ClearViewOperator)
    bpy.utils.register_class(SelectOperator)
    bpy.utils.register_class(ApplySelectOperator)
    bpy.utils.register_class(CropSelectOperator)
    bpy.utils.register_class(ApplyCropSelectOperator)
    bpy.utils.register_class(CropDeleteOperator)
    bpy.utils.register_class(SmoothMeshOperator)
    bpy.utils.register_class(DeleteMeshOperator)
    bpy.utils.register_class(FillHolesOperator)


def unregister():
    bpy.utils.unregister_class(TestPanel)
    bpy.utils.unregister_class(ImportSTL)
    bpy.utils.unregister_class(ExportSTL)
    bpy.utils.unregister_class(ResetViewOperator)
    bpy.utils.unregister_class(ClearViewOperator)
    bpy.utils.unregister_class(SelectOperator)
    bpy.utils.unregister_class(ApplySelectOperator)
    bpy.utils.unregister_class(CropSelectOperator)
    bpy.utils.unregister_class(ApplyCropSelectOperator)
    bpy.utils.unregister_class(CropDeleteOperator)
    bpy.utils.unregister_class(SmoothMeshOperator)
    bpy.utils.unregister_class(CropDeleteOperator)
    bpy.utils.unregister_class(FillHolesOperator)

if __name__ == "__main__":
    register()
