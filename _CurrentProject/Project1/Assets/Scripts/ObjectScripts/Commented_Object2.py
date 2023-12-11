"""
Represents an object
"""


# Determines the type of object
object_type = {
    "container" : False,
    "text" : False,
    "image" : True,
    "button" : False,
    "hover_activated" : False,
    "key_activated" : False
}
# The name of the container object that this object belongs to -> string
# Must be the same as the container's file name (without .py and without any folder path)
# If the object is not contained within any others, choose None
# If the object belongs to multiple containers, a list can be used
container_name = None

# Class in which methods and attributes are used - DO NOT RENAME
class Main:
    def __init__(self):
        # Determines if object is evaluated
        # Only functionality of inactive objects is the frame_update function which is still called
        self.active = True
        # Determines the order that objects within a container are evaluated from low to high
        # Objects evaluated later will be drawn over others that are evaluated sooner
        self.update_priority = 0
        # If this object has been generated using the generate_object method,
        # this value can be changed to identify or pass values to this object
        self.generated_value = None

        # List components are added together after calculations
        # [[pixels, percent of container's size], [pixels, percent of container's size]] -> [x, y]
        self.position_modifiers = [[0, 0.443359375], [0, 0.22841112846318462]]
        # [[pixels, percent of container's size], [pixels, percent of container's size]] -> [x, y]
        self.size_modifiers = [[0, 0.15], [0, 0.15]]
        # [degrees, percent of container's rotation]
        self.rotation_modifiers = [0, 1]
        # [percentage opacity, percent of container's opacity]
        self.opacity_modifiers = [0, 1]

        # Determines the point on the object that the object's position_modifiers are moving
        # [percent of object size, percent of object size] -> [x, y]
        # e.g. [0, 0] allows the object's top left corner to be aligned no matter the object's size
        self.position_origin = [0.5, 0.5]
        # limits x and y size to a percentage of each other
        # [[min percent of y, max percent of y], [min percent of x, max percent of x]]
        # e.g. [[None, 1], [None, 1]] ensures object is square
        self.min_max_size = [[None, None], [None, None]]

        # Determines whether objects that protrude from this container are shown - CONTAINER ONLY
        # For rotated containers and containers that have a scroll bar, this becomes False
        self.objects_visible_outside_container = True
        # Determines whether objects belonging to this container are lame - CONTAINER ONLY
        # Lame objects cannot be clicked or hovered over, do not react to key input,
        # and do not get their frame_update method called
        self.objects_are_lame = False
        # Image directory for this object (path from main.py) - IMAGE ONLY
        # If image does not exist, defaults to black rectangle
        self.img_dir = ""
        # RGB -> (0 -> 255, 0 -> 255, 0 -> 255),
        # colour is used if the object's image does not exist - IMAGE ONLY
        self.object_colour = (227, 248, 40)
        # Dictionary of keys that activate object ("key_name" : True/False) - KEY_ACTIVATED ONLY
        self.activation_keys = {}
        # Passes the unicode text input as first item in keys list in key_input method
        # KEY_ACTIVATED ONLY
        self.uses_text_input = False
        # Determines whether object is a scroll bar
        self.is_scroll_bar = False

        # Content of the text - TEXT ONLY
        self.text = ""
        # If font does not exist, defaults to freesansbold
        self.text_font = ""
        # RGB -> (0 -> 255, 0 -> 255, 0 -> 255)
        self.text_colour = (0, 0, 0)
        self.text_bold = False
        self.text_italic = False

        # Additional attributes:


    # Called every frame, passes the object of globalScripts.py class
    def frame_update(self, global_scripts):
        pass

    # Called if the object was left-clicked this frame, passes mouse position -> [x, y]
    def left_clicked(self, mouse_pos):
        pass

    # Called if the object was middle-clicked this frame, passes mouse position -> [x, y]
    def middle_clicked(self, mouse_pos):
        pass

    # Called if the object was right-clicked this frame, passes mouse position -> [x, y]
    def right_clicked(self, mouse_pos):
        pass

    # Called if the mouse was over the object this frame, passes mouse position -> [x, y]
    def hovered_over(self, mouse_pos):
        pass

    # Called if a key in activation_keys was pressed this frame,
    # passes list of all pressed keys in activation_keys
    def key_input(self, keys):
        pass

    # Additional methods:


"""
To dynamically create an object (ONLY FOR CONTAINERS):
Call self.generate_object(global_scripts, n[, m])
    global_scripts -> this is already passed into the frame_update method,
        therefore this method must be called from frame_update
    n -> string -> name of the object that is to be created
    m -> variable -> value that is passed to the generated object,
        can be ignored (therefore shown in square braces)

To create an animation:
Call self.create_animation(x, y, z[, a, b])
    x -> float -> final value of the animation (initial value is always zero)
    y -> int -> total time for the animation to take place over in milliseconds
    z -> string -> type of animation ->
        include pos (position), size, rot (rotation) or opa (opacity)
        include x, y or neither for position and size animations
            if neither, its assumed the animation is in both x and y directions
            if neither, a list can be used for x and a
        include % if the animation controls the percentage modifiers
    a -> this parameter can be ignored (therefore is shown in square braces) ->
        string -> easing function for animation -> use "x" as the subject of the function ->
        if none given, defaults to linear easing function (simply "y = x")
    b -> this parameter can be ignored (therefore is shown in square braces) ->
        string -> name of the animation -> used to manipulate the animation
e.g. self.create_animation(500, 5000, "posx") ->
    moves object 500 pixels to the right over 5 seconds
e.g. self.create_animation([0.5, 0.1], 2000, "size%", ["x", "x**3"], "resize_me") ->
    resizes the object in both x and y by percentages of their container over 2 seconds
Remember to only create the animation once as animations stack with each other

To check if an animation is completed:
Call self.get_complete_animation(b)
    b -> string -> name of animation used to locate the correct animation
Returns true or false

To instantly complete an animation:
Call self.complete_animation(b)
    b -> string -> name of animation used to locate the correct animation

To delete an animation (moves the object back to where it was before):
Call self.delete_animation(b)
    b -> string -> name of animation used to locate the correct animation

To progress an animation (moves the animation forwards by an amount of time):
Call self.progress_animation(b, c)
    b -> string -> name of animation used to locate the correct animation
    c -> integer -> milliseconds to move the animation forward by

To reverse an animation (makes the animation progress backwards):
Call self.reverse_animation(b[, d])
    b -> string -> name of animation used to locate the correct animation
    d -> this parameter can be ignored if the state of reversal wants to be switched ->
        specifies either reversed or not -> boolean -> True = reversed, False = not reversed
"""
