"""
Represents an object
"""

# Determines the type of object
# text, image are mutually exclusive, text takes precedence
object_type = {
    "container" : False,
    "text" : False,
    "image" : False,
    "button" : False,
    "hover_activated" : False,
    "key_activated" : False
}
# The name of the container object that this object belongs to
# Must be the same as the container's file/class name (without .py)
# If the object is not contained within any others, choose None
container_name = None

# Class name must be the same as the file name (without .py)
class Commented_Object:
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
        self.img_dir = ""
        # Dictionary of keys that activate object ("[key_name]" : True/False) - KEY_ACTIVATED ONLY
        self.activation_keys = {}
        # Determines whether object is a scroll bar
        self.is_scroll_bar = False

        # List components are added together after calculations
        # [[pixels, percent of container's size], [pixels, percent of container's size]] -> [x, y]
        self.position_modifiers = [[0, 0.5], [0, 0.5]]
        # [[pixels, percent of container's size], [pixels, percent of container's size]] -> [x, y]
        self.size_modifiers = [[0, 1], [0, 1]]
        # [degrees, percent of container's rotation]
        self.rotation_modifiers = [0, 1]
        # [percentage opacity, percent of container's opacity]
        self.opacity_modifiers = [0, 1]

        # Determines the point on the object that the object's position_modifiers are moving
        # [percent of object size, percent of object size] -> [x, y]
        self.position_origin = [0.5, 0.5]

        # Content of the text - TEXT ONLY
        self.text = ""
        # If font does not exist, defaults to freesansbold
        self.text_font = ""
        # RGB -> (0 -> 255, 0 -> 255, 0 -> 255)
        self.text_colour = (0, 0, 0)
        self.text_bold = False
        self.text_italic = False

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

    # Called for each key in self.activation_keys that was pressed this frame, passes key name
    def key_input(self, key):
        pass
