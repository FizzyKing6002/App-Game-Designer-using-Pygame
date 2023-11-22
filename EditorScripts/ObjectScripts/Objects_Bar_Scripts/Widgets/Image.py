"""
Represents an object
"""


# Determines the type of object
# text, image are mutually exclusive, text takes precedence
object_type = {
    "container" : False,
    "text" : False,
    "image" : True,
    "button" : True,
    "hover_activated" : True,
    "key_activated" : True
}
# The name of the container object that this object belongs to -> string
# Must be the same as the container's file/class name (without .py)
# If the object is not contained within any others, choose None
container_name = "Objects_Bar"

# Class in which methods and attributes are used - DO NOT RENAME
class Main:
    def __init__(self):
        # Determines if object is evaluated
        # Only functionality of inactive objects is the frame_update function which is still called
        self.active = True
        # Determines the order that objects within a container are evaluated from low to high
        # Objects evaluated later will be drawn over others that are evaluated sooner
        self.update_priority = 0

        # Determines whether objects that protrude from this container are shown - CONTAINER ONLY
        # For rotated containers and containers that have a scroll bar, this becomes False
        self.objects_visible_outside_container = True
        # Image directory for this object (path from main.py) - IMAGE ONLY
        # If image does not exist, defaults to black rectangle
        self.img_dir = "EditorTextures/Objects_Icons/insert-picture-icon.png"
        # Dictionary of keys that activate object ("[key_name]" : True/False) - KEY_ACTIVATED ONLY
        self.activation_keys = {
            "LCTRL" : True,
            "RCTRL" : True,
            "LSHIFT" : True,
            "RSHIFT" : True,
            "i" : True
        }
        # Determines whether object is a scroll bar
        self.is_scroll_bar = False

        # List components are added together after calculations
        # [[pixels, percent of container's size], [pixels, percent of container's size]] -> [x, y]
        self.position_modifiers = [[0, 0.09 + 5*0.76/14], [0, 0.4]]
        # [[pixels, percent of container's size], [pixels, percent of container's size]] -> [x, y]
        self.size_modifiers = [[0, 0.76/7], [0, 0.6]]
        # [degrees, percent of container's rotation]
        self.rotation_modifiers = [0, 1]
        # [percentage opacity, percent of container's opacity]
        self.opacity_modifiers = [0, 1]

        # RGB -> (0 -> 255, 0 -> 255, 0 -> 255),
        # colour is used for text and if the object's image does not exist
        self.object_colour = (0, 0, 0)
        # Determines the point on the object that the object's position_modifiers are moving
        # [percent of object size, percent of object size] -> [x, y]
        self.position_origin = [0.5, 0.5]

        # Content of the text - TEXT ONLY
        self.text = ""
        # If font does not exist, defaults to freesansbold
        self.text_font = ""
        self.text_bold = False
        self.text_italic = False

        # Additional attributes:
        self.clicked = False
        self.key_clicked = False
        self.hovered = False

    # Called every frame, passes the object of globalScripts.py class
    def frame_update(self, global_scripts):
        if self.hovered:
            self.opacity_modifiers[1] = 0.5
            self.hovered = False
        else:
            self.opacity_modifiers[1] = 1

        if self.key_clicked:
            global_scripts.key_dragging = True
            self.key_clicked = False

        elif self.clicked:
            global_scripts.dragging = True
            self.clicked = False

    # Called if the object was left-clicked this frame, passes mouse position -> [x, y]
    def left_clicked(self, mouse_pos):
        self.clicked = True

    # Called if the object was middle-clicked this frame, passes mouse position -> [x, y]
    def middle_clicked(self, mouse_pos):
        pass

    # Called if the object was right-clicked this frame, passes mouse position -> [x, y]
    def right_clicked(self, mouse_pos):
        pass

    # Called if the mouse was over the object this frame, passes mouse position -> [x, y]
    def hovered_over(self, mouse_pos):
        self.hovered = True

    # Called for each key in self.activation_keys that was pressed this frame, passes key name
    def key_input(self, keys):
        if "i" in keys \
            and ("LCTRL" in keys or "RCTRL" in keys) \
                and ("LSHIFT" in keys or "RSHIFT" in keys):
            self.key_clicked = True

    # Additional methods:


"""
To create an animation:
Call self.create_animation(x, y, z{, a})
    x -> float -> final value of the animation (initial value is always zero)
    y -> int -> total time for the animation to take place over in milliseconds
    z -> string -> type of animation ->
        include pos (position), size, rot (rotation) or opa (opacity)
        include x, y or neither for position and size animations
            if neither, its assumed the animation is in both x and y directions
            if neither, a list can be used for x and a
        include % if the animation controls the percentage modifiers
    a -> this parameter can be ignored (therefore is shown in curly braces) ->
        string -> easing function for animation -> use "x" as the subject of the function
        if none given, defaults to linear easing function
e.g. self.create_animation(500, 5000, "posx") ->
    moves object 500 pixels to the right over 5 seconds
e.g. self.create_animation([0.5, 0.1], 2000, "size%", ["x", "x**3"]) ->
    resizes the object in both x and y by percentages of their container over 2 seconds
Remember to only create the animation once as animations stack with each other
"""
