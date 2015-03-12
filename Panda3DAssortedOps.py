import bpy

def write(context, filepath):
    name=filepath
    file=open(name,"w")
    for o in context.selected_objects:
        s=(o.name,o.location[0],o.location[1],o.location[2])
        file.write(repr(s)+"\n")
    file.close()
    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportObjAndPos(Operator, ExportHelper):
    """Write selected objects names and position"""
    bl_idname = "object.obj_pos_to_file"
    bl_label = "Write select objects position to a file"

    # ExportHelper mixin class uses this
    filename_ext = ".txt"

    filter_glob = StringProperty(
            default="*.txt",
            options={'HIDDEN'},
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    
    def execute(self, context):
        return write(context, self.filepath)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportObjAndPos.bl_idname, text="Export Obj name and position")


def register():
    bpy.utils.register_class(ExportObjAndPos)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportObjAndPos)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    
    
    
    
