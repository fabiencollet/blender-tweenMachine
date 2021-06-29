import bpy

# --------------------------------------------------------------
# TO-DO
# --------------------------------------------------------------

# 1. Adding abilities to tween specific properties
#    (location, rotation, scale and customs properties)

# --------------------------------------------------------------
# Globals
# --------------------------------------------------------------

# --------------------------------------------------------------
# Functions
# --------------------------------------------------------------


def resolveProperty(obj, data_path):
    # resolve property path
    if "." in data_path:
        custom_attr = data_path.split('["')

        if len(custom_attr) > 2:
            path_prop, attr = data_path.rsplit('["', 1)
            path_attr = '["' + attr
        else:
            path_prop, path_attr = data_path.rsplit(".", 1)

        prop = obj.path_resolve(path_prop)

    else:
        prop = obj
        # single attribute such as name, location... etc
        path_attr = data_path

    return prop, path_attr


def setValue(obj, path, value):
    # resolve property path
    prop, path_attr = resolveProperty(obj, path)

    # Set value
    if len(value) == 1:
        setattr(prop, path_attr, value[0])
    else:
        setattr(prop, path_attr, value)


def getClosestKeyFrame(obj, current_frame, list_bones=[]):
    dict_keyframes = {}

    # pprint(list_bones)

    try:
        fcurves = obj.animation_data.action.fcurves
    except:
        return False

    for curve in fcurves:

        # Get All Keyframes fron the curve
        keyframes = curve.keyframe_points

        data = curve.data_path
        index = curve.array_index

        # Check If the bone is selected
        if bpy.context.mode == "POSE":
            prop, attr = resolveProperty(obj, data)

            if prop not in list_bones:
                continue

        if not data in dict_keyframes:
            dict_keyframes[data] = {}

        # print(f"ATTRIBUTE : {data} | {index}")

        # Get Closest Frames
        # Get the range of the animation curve
        range = curve.range()
        # print(f"RANGE : {range}")

        # Init Frames Variables
        f_before = range[0]
        f_after = range[1]

        if current_frame < range[0]:
            f_after = range[0]

        elif current_frame > range[1]:
            f_before = range[1]

        else:
            list_frames = []

            for keyframe in keyframes:

                frame, value = keyframe.co

                if frame < current_frame and frame > f_before:
                    f_before = frame

                if frame > current_frame and frame < f_after:
                    f_after = frame

                list_frames.append(frame)

        # Init Values Variables
        v_before = 0.0
        v_after = 0.0

        # Get Values From Closest Frame
        for keyframe in keyframes:

            frame, value = keyframe.co

            if frame == f_before:
                v_before = value

            if frame == f_after:
                v_after = value

        dict_index = {}

        dict_index[index] = {"v_before": v_before,
                             "v_after": v_after}

        dict_keyframes[data].update(dict_index)

    return dict_keyframes


def insertKeyframe(dict_objects, mix):
    # pprint(dict_objects)

    for obj in dict_objects:

        for data in dict_objects[obj]:

            list_data = []

            for index in dict_objects[obj][data]:
                # Calculate the new value
                v_before = dict_objects[obj][data][index]["v_before"]
                v_after = dict_objects[obj][data][index]["v_after"]

                v_distance = v_after - v_before
                v_mix = v_before + (v_distance * mix)

                list_data.append(v_mix)

            # Set New Data
            setValue(obj, data, list_data)

            # Insert Keyframe
            obj.keyframe_insert(data_path=data)


def tweenMachine(scene, context):
    # Get mix value from the scene property slider
    mix = scene.tween_mix

    tween(scene, context, mix)


def tween(scene, context, mix):

    # Get the current frame
    current_frame = context.scene.frame_current

    # List selected Objects or Pose Bones
    objects = None
    # init Armature variable:
    armature = None

    if context.mode == "POSE":
        # List selected bones
        armature = context.active_object
        objects = list(context.selected_pose_bones)

    elif context.mode == "OBJECT":
        # List selected objects
        objects = list(context.selected_objects)

    if not objects:
        return None

    dict_objects = {}

    for obj in objects:

        # print(obj.name)

        # Find the closest keyframes (one before and one after)
        # if not found copy values of the closest
        # Store keyframes values of previous and next keyframe found
        if context.mode == "POSE":
            dict_objects[armature] = getClosestKeyFrame(armature,
                                                        current_frame,
                                                        objects)
        else:
            dict_objects[obj] = getClosestKeyFrame(obj, current_frame)

        # Insert a keyframe at the current frame
        # based on a mix(%) of the previous and the next keyframe value

        insertKeyframe(dict_objects, mix)

    return None


# --------------------------------------------------------------
# Properties
# --------------------------------------------------------------

bpy.types.Scene.tween_mix = bpy.props.FloatProperty(name="Tween Mix",
                                                    min=0,
                                                    default=0.5,
                                                    max=1,
                                                    update=tweenMachine)
