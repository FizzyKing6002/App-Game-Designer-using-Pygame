"""
Represents a single line Text Box
"""


# Text box must have text, a background image, must be selectable and react to user keyboard input
object_type = {
    "container" : False,
    "text" : True,
    "image" : True,
    "button" : True,
    "hover_activated" : True,
    "key_activated" : True
}
container_name = None

# Class in which methods and attributes are used - DO NOT RENAME
class Main:
    def __init__(self):
        self.active = True
        self.update_priority = 0
        self.generated_value = None

        # [[pixels, percent of container's size], [pixels, percent of container's size]] -> [x, y]
        self.position_modifiers = [[0, 0.5], [0, 0.5]]
        # [[pixels, percent of container's size], [pixels, percent of container's size]] -> [x, y]
        self.size_modifiers = [[0, 0.15], [0, 0.15]]
        # [degrees, percent of container's rotation]
        self.rotation_modifiers = [0, 1]
        # [percentage opacity, percent of container's opacity]
        self.opacity_modifiers = [0, 1]

        # Aligns text within the text box and alters position
        # [percent of object size, percent of object size] -> [x, y]
        self.position_origin = [0.5, 0.5]
        self.min_max_size = [[None, None], [None, None]]

        self.objects_visible_outside_container = True
        self.objects_are_lame = False
        # Background image for text box - most use a colour rather than image
        self.img_dir = ""
        # RGB -> (0 -> 255, 0 -> 255, 0 -> 255),
        # used for background colour of text box
        self.object_colour = (255, 255, 255)
        # Text box needs backspace key and return key
        self.activation_keys = {
            "BACKSPACE" : True,
            "RETURN" : True
        }
        # Requires text input from the user
        self.uses_text_input = True
        self.is_scroll_bar = False

        # Content of the text
        self.text = "Text"
        # Text box font
        self.text_font = ""
        # RGB -> (0 -> 255, 0 -> 255, 0 -> 255)
        self.text_colour = (0, 0, 0)
        self.text_bold = False
        self.text_italic = False

        # Text box variable definitions:
        # The text box has been clicked on and can be written in
        self.activated = False
        self.clicked = False
        self.prev_clicked = False
        self.hovered = False
        # Ensures multiple backspaces cannot be done in one click
        self.prev_backspace = False


    def frame_update(self, global_scripts):
        # If the mouse has been released on the text box meaning it has been clicked
        if not self.clicked and self.prev_clicked and self.hovered:
            self.activated = True
        # If the user clicks off of the text box
        elif global_scripts.mouse_state[0] and not self.hovered and self.activated:
            self.activated = False

        # Reset variables
        if self.clicked:
            self.prev_clicked = True
            self.clicked = False
        else:
            self.prev_clicked = False
        self.hovered = False

    def left_clicked(self, mouse_pos):
        self.clicked = True

    def middle_clicked(self, mouse_pos):
        pass

    def right_clicked(self, mouse_pos):
        pass

    def hovered_over(self, mouse_pos):
        self.hovered = True

    def key_input(self, keys):
        # Text input only occurs once the text box has been clicked on
        if self.activated:
            if "BACKSPACE" in keys:
                if not self.prev_backspace:
                    # Removes one character
                    self.text = self.text[:-1]
                    self.prev_backspace = True
            else:
                self.prev_backspace = False

                if "RETURN" in keys:
                    # The text has been entered and so the text box should not be active anymore
                    self.activated = False
                else:
                    # Add the text input from the user to the text
                    self.text += keys[0]
        else:
            self.prev_backspace = False
