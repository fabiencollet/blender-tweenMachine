import bpy

# --------------------------------------------------------------
# Globals
# --------------------------------------------------------------

ROTATION_LIST = ["rotation", "rotation_euler", "rotation_quaternion"]

# --------------------------------------------------------------
# Functions
# --------------------------------------------------------------


def resolve_property(object: bpy.types.Object, data_path: str) -> tuple[str, str]:
    """
    Resolve path property

    :param object: Blender Object
    :type object: bpy.types.Object
    :param data_path: The data path, (location, rotation, scale, and custom attributes)
    :type data_path: str
    :return: A tuple of the resolved property and is path
    :rtype: tuple[str, str]
    """
    if "." in data_path:
        custom_attr = data_path.split('["')

        if len(custom_attr) > 2:
            path_property, attribute = data_path.rsplit('["', 1)
        else:
            path_property, path_attribute = data_path.rsplit(".", 1)

        property = object.path_resolve(path_property)

    else:
        property = object

    return (property, path_property)


def get_closest_keyframe(object: bpy.types.Object, current_frame: int, bone_list: list = []) -> dict:
    """
    Get the closest Keyframe

    :param object: Blender Object
    :type object: bpy.types.Object
    :param current_frame: The current frame
    :type current_frame: int
    :param bone_list: Bone list, defaults to []
    :type bone_list: list, optional
    :return: The closest keyframe dict dict_keyframes[data_path] = {"value_before": value_before, "value_after": value_after}
    :rtype: dict
    """
    dict_keyframes = {}

    try:
        fcurves = object.animation_data.action.fcurves
    except:
        return dict_keyframes

    for curve in fcurves:
        # Get All Keyframes fron the curve
        keyframes = curve.keyframe_points

        data_path = curve.data_path
        index = curve.array_index

        # Check If the bone is selected
        if bpy.context.mode == "POSE":
            property, _ = resolve_property(object=object, data_path=data_path)

            if property not in bone_list:
                continue

        if not data_path in dict_keyframes:
            dict_keyframes[data_path] = {}

        # Get Closest Frames
        # Get the range of the animation curve
        range = curve.range()

        # Init Frames Variables
        frame_before = range[0]
        frame_after = range[1]

        if current_frame < range[0]:
            frame_after = range[0]
        elif current_frame > range[1]:
            frame_before = range[1]
        else:
            list_frames = []

            for keyframe in keyframes:
                frame, value = keyframe.co

                if frame < current_frame and frame > frame_before:
                    frame_before = frame
                elif frame > current_frame and frame < frame_after:
                    frame_after = frame

                list_frames.append(frame)

        # Init Values Variables
        value_before = 0.0
        value_after = 0.0

        # Get Values From Closest Frame
        for keyframe in keyframes:

            frame, value = keyframe.co

            if frame == frame_before:
                value_before = value
            elif frame == frame_after:
                value_after = value

        dict_index = {}

        dict_index[index] = {"value_before": value_before,
                             "value_after": value_after}

        dict_keyframes[data_path].update(dict_index)

    return dict_keyframes


def insert_keyframe(object_dict: dict, mix: float):
    """
    Insert a keyframe based on the mix value

    :param object_dict: The Object dict
    :type object_dict: dict
    :param mix: The mix value
    :type mix: float
    """
    t_location = bpy.context.scene.tween_location
    t_rotation = bpy.context.scene.tween_rotation
    t_scale = bpy.context.scene.tween_scale
    t_custom = bpy.context.scene.tween_custom

    for object in object_dict:

        for data_path in object_dict[object]:

            list_data = []

            property, data_path = resolve_property(object=object, data_path=data_path)

            if data_path == "location":
                if not t_location:
                    continue

            elif data_path in ROTATION_LIST:
                if not t_rotation:
                    continue

            elif data_path == "scale":
                if not t_scale:
                    continue

            else:
                if not t_custom:
                    continue

            # Resolve the property
            object_to_resolve, attr_to_resolve = resolve_property(object=object, data_path=data_path)
            property_resolved = object_to_resolve.path_resolve(attr_to_resolve)
            if not isinstance(property_resolved, (int, float, str)):
                property_length = len(property_resolved)
            else:
                property_length = 1

            for i in range(property_length):

                if i not in object_dict[object][data_path]:
                    continue
                else:
                    # Calculate the new value
                    value_before = object_dict[object][data_path][i]["value_before"]
                    value_after = object_dict[object][data_path][i]["value_after"]

                    v_distance = value_after - value_before
                    v_mix = value_before + (v_distance * mix)

                list_data.append(v_mix)

                # Set New data_path and insert Keyframe
                if property_length == 1:
                    # property_resolved = v_mix
                    setattr(object_to_resolve, attr_to_resolve, v_mix)
                    object.keyframe_insert(data_path=data_path)
                else:
                    property_resolved[i] = v_mix
                    object.keyframe_insert(data_path=data_path, index=i)


def tween_machine(scene: bpy.types.Scene, context: bpy.types.Context):
    """
    Tween Machine operator

    :param scene: Blender scene
    :type scene: bpy.types.Scene
    :param context: Blender context, (OBJECT, POSE, etc..)
    :type context: bpy.types.Context
    """
    # Get mix value from the scene property slider
    mix = scene.tween_mix
    tween(scene=scene, context=context, mix=mix)


def tween(scene: bpy.types.Scene, context: bpy.types.Context, mix: float):
    """
    
    Tween machine main function

    :param scene: Blender scene
    :type scene: bpy.types.Scene
    :param context: Blender context, (OBJECT, POSE, etc..)
    :type context: bpy.types.Context
    :param mix: The mix value
    :type mix: float
    """
    # Get the current frame
    current_frame = context.scene.frame_current

    # init variables:
    object_list = None
    armature = None

    # List selected object_list or Pose Bones
    if context.mode == "POSE":
        # List selected bones
        armature = context.active_object
        object_list = list(context.selected_pose_bones)

    elif context.mode == "OBJECT":
        object_list = []
        # List selected object_list
        selected_objects_list = list(context.selected_objects_list)
        for object in selected_objects_list:
            # Get subtype object(Mesh, Light, Camera, etc...)
            obj_subtype = object.data
            object_list.append(object)
            object_list.append(obj_subtype)

    if not object_list:
        return

    object_dict = {}

    for object in object_list:
        # Find the closest keyframes (one before and one after)
        # if not found copy values of the closest
        # Store keyframes values of previous and next keyframe found
        closest_key = None
        object_to_add = None

        if context.mode == "POSE" and armature:
            closest_key = get_closest_keyframe(object=armature,
                                               current_frame=current_frame,
                                               object_list=object_list)
            object_to_add = armature

        else:
            closest_key = get_closest_keyframe(object=armature,
                                               current_frame=current_frame)
            object_to_add = object

        if not closest_key:
            continue

        object_dict[object_to_add] = closest_key

    # Insert a keyframe at the current frame
    # based on a mix(%) of the previous and the next keyframe value
    insert_keyframe(object_dict=object_dict, mix=mix)

    return


# --------------------------------------------------------------
# Properties
# --------------------------------------------------------------
# Mix Property
bpy.types.Scene.tween_mix = bpy.props.FloatProperty(name="Tween Mix",
                                                    min=0,
                                                    default=0.5,
                                                    max=1,
                                                    update=tween_machine)

# Enables Properties
bpy.types.Scene.tween_location = bpy.props.BoolProperty(name="Tween Location",
                                                        default=True)

bpy.types.Scene.tween_rotation = bpy.props.BoolProperty(name="Tween Rotation",
                                                        default=True)

bpy.types.Scene.tween_scale = bpy.props.BoolProperty(name="Tween Scale",
                                                     default=True)

bpy.types.Scene.tween_custom = bpy.props.BoolProperty(name="Tween Custom",
                                                      default=True)
