import bpy,json,time


def write_some_data(context, filepath):
    print("Running export HPandaClasses")
    d={} #{name:(class,x,y,z,rx,ry,rz,sx,sy,sz)}
    objects=bpy.context.selected_objects
    for object in objects:
        name=object.name
        _class=object['class']
        compose=object.matrix_world.decompose()
        x=compose[0][0]
        y=compose[0][1]
        z=compose[0][2]
        eulers=compose[1].to_euler()
        rx=eulers[0]
        ry=eulers[1]
        rz=eulers[2]
        sx=compose[2][0]
        sy=compose[2][1]
        sz=compose[2][2]
        d[name]=(_class,x,y,z,rx,ry,rz,sx,sy,sz)
    print(json.dumps(d))        
    f = open(filepath, 'w', encoding='utf-8')
    
    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportHPandaClasses(Operator, ExportHelper):
    """Export Objects,classes,and transforms"""
    bl_idname = "export_hpanda.classes"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export classes and transforms"

    # ExportHelper mixin class uses this
    filename_ext = ".hpanda"

    filter_glob = StringProperty(
            default="*.hpanda",
            options={'HIDDEN'},
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    
    def execute(self, context):
        return write_some_data(context, self.filepath)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportHPandaClasses.bl_idname, text="Export HPandaClasses")


def register():
    bpy.utils.register_class(ExportHPandaClasses)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportHPandaClasses)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    print(time.time())
    register()
    print ("REGISTERED")
