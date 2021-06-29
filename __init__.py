bl_info = {
    "name": "Tween Machine",
    "author": "Fabien Collet",
    "version": (0, 1, 0),
    "blender": (2, 90, 0),
    "location": "Object > Animation > Tween Machine",
    "description": "Insert Breakdown Keyframes",
    "warning": "",
    "doc_url": "https://github.com/fabiencollet/blender-tweenMachine",
    "category": "Animation",
}

import bpy

from .core import tween

# --------------------------------------------------------------
# To-Do
# --------------------------------------------------------------

# --------------------------------------------------------------
# Globals
# --------------------------------------------------------------

# --------------------------------------------------------------
# Operators
# --------------------------------------------------------------

class ANIM_OT_tween_10(bpy.types.Operator):
    """Tween Machine 10%"""
    bl_idname = "anim.tween_machine_10"
    bl_label = "10%"
    bl_options = {'REGISTER', 'UNDO'}
    bl_context = ['objectmode', 'posemode']

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if tween(self, context, 0.10):
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class ANIM_OT_tween_25(bpy.types.Operator):
    """Tween Machine 25%"""
    bl_idname = "anim.tween_machine_25"
    bl_label = "25%"
    bl_options = {'REGISTER', 'UNDO'}
    bl_context = ['objectmode', 'posemode']

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if tween(self, context, 0.25):
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class ANIM_OT_tween_50(bpy.types.Operator):
    """Tween Machine 50%"""
    bl_idname = "anim.tween_machine_50"
    bl_label = "50%"
    bl_options = {'REGISTER', 'UNDO'}
    bl_context = ['objectmode', 'posemode']

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if tween(self, context, 0.50):
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class ANIM_OT_tween_75(bpy.types.Operator):
    """Tween Machine 75%"""
    bl_idname = "anim.tween_machine_75"
    bl_label = "75%"
    bl_options = {'REGISTER', 'UNDO'}
    bl_context = ['objectmode', 'posemode']

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if tween(self, context, 0.75):
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class ANIM_OT_tween_90(bpy.types.Operator):
    """Tween Machine 90%"""
    bl_idname = "anim.tween_machine_90"
    bl_label = "90%"
    bl_options = {'REGISTER', 'UNDO'}
    bl_context = ['objectmode', 'posemode']

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if tween(self, context, 0.90):
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class VIEW_3D_PT_tweenMachine(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_category = "Tween Machine"
    bl_label = "Tween Machine"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):

        layout = self.layout

        # Add the property slider Tween Mix
        row = layout.row()
        row.prop(context.scene, "tween_mix")

        # Add all operators Tween Machine
        row = layout.row()
        row.operator(ANIM_OT_tween_10.bl_idname)
        row.operator(ANIM_OT_tween_25.bl_idname)
        row.operator(ANIM_OT_tween_50.bl_idname)
        row.operator(ANIM_OT_tween_75.bl_idname)
        row.operator(ANIM_OT_tween_90.bl_idname)


def add_tween_menu_draw(self, context):
    """Creates a Menu inside Object > Animation"""
    self.layout.separator()

    self.layout.operator(
        ANIM_OT_tween_10.bl_idname,
        text="Tween Machine 10%")

    self.layout.operator(
        ANIM_OT_tween_25.bl_idname,
        text="Tween Machine 25%")

    self.layout.operator(
        ANIM_OT_tween_50.bl_idname,
        text="Tween Machine 50%")

    self.layout.operator(
        ANIM_OT_tween_75.bl_idname,
        text="Tween Machine 75%")

    self.layout.operator(
        ANIM_OT_tween_90.bl_idname,
        text="Tween Machine 90%")


def register():
    # Register Operators
    bpy.utils.register_class(ANIM_OT_tween_10)
    bpy.utils.register_class(ANIM_OT_tween_25)
    bpy.utils.register_class(ANIM_OT_tween_50)
    bpy.utils.register_class(ANIM_OT_tween_75)
    bpy.utils.register_class(ANIM_OT_tween_90)

    # Register Panel
    bpy.utils.register_class(VIEW_3D_PT_tweenMachine)

    # Register Menu
    bpy.types.VIEW3D_MT_object_animation.append(add_tween_menu_draw)


def unregister():
    # Unregister Operators
    bpy.utils.unregister_class(ANIM_OT_tween_10)
    bpy.utils.unregister_class(ANIM_OT_tween_25)
    bpy.utils.unregister_class(ANIM_OT_tween_50)
    bpy.utils.unregister_class(ANIM_OT_tween_75)
    bpy.utils.unregister_class(ANIM_OT_tween_90)

    # Unregister Panel
    bpy.utils.unregister_class(VIEW_3D_PT_tweenMachine)

    # Unregister Menu
    bpy.types.VIEW3D_MT_object_animation.remove(add_tween_menu_draw)


if __name__ == "__main__":
    register()
