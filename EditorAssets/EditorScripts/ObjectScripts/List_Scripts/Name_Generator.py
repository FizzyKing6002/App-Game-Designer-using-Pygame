"""
Represents a single line Text Box
"""


# Text box must have text, a background image, must be selectable and react to user keyboard input
object_type = {
    "container" : True,
    "text" : True,
    "image" : True,
    "button" : True,
    "hover_activated" : True,
    "key_activated" : True
}
container_name = "None"

# Class in which methods and attributes are used - DO NOT RENAME
class Main:
    def __init__(self):
        self.active = True
        self.update_priority = 0
        self.generated_value = None

        # [[pixels, percent of container's size], [pixels, percent of container's size]] -> [x, y]
        self.position_modifiers = [[0, 0.15], [0, 0.5]]
        # [[pixels, percent of container's size], [pixels, percent of container's size]] -> [x, y]
        self.size_modifiers = [[0, 0.7], [0, 0.75]]
        # [degrees, percent of container's rotation]
        self.rotation_modifiers = [0, 1]
        # [percentage opacity, percent of container's opacity]
        self.opacity_modifiers = [0, 1]

        # Aligns text within the text box and alters position
        # [percent of object size, percent of object size] -> [x, y]
        self.position_origin = [0, 0.5]
        self.min_max_size = [[None, None], [None, None]]

        self.objects_visible_outside_container = True
        self.objects_are_lame = False
        # Background image for text box - most use a colour rather than image
        self.img_dir = ""
        # RGB -> (0 -> 255, 0 -> 255, 0 -> 255),
        # used for background colour of text box
        self.object_colour = (175, 179, 189)
        # Text box needs backspace key and return key
        self.activation_keys = {
            "BACKSPACE" : True,
            "RETURN" : True
        }
        # Requires text input from the user
        self.uses_text_input = True
        self.is_scroll_bar = False

        # Content of the text
        self.text = " "
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
        self.selected = False

        self.one_time = True
        self.object_path = None
        self.file_name = ""
        self.object_index = 0
        self.homeless = False

        self.rename = False


    def frame_update(self, global_scripts):
        if self.one_time:
            self.one_time = False

            self.object_path = self.generated_value[0]
            self.file_name = self.object_path.split("/")[-1][:-3]
            self.object_index = self.generated_value[1]
            self.text += "| " * self.generated_value[2]
            self.text += self.file_name
            self.homeless = self.generated_value[3]
            self.generate_object(global_scripts, "List_Text_Edit")

        if global_scripts.menu_state != 0:
            self.activated = False

        if self.objects[0].activated:
            self.activated = True
            self.objects[0].activated = False

        # If the mouse has been released on the text box meaning it has been clicked
        if not self.clicked and self.prev_clicked and self.hovered:
            global_scripts.current_path = self.object_path
            global_scripts.current_index = self.object_index

            if self.homeless:
                global_scripts.project_global_scripts.__editor_attr__selected_size__ = [0, 0]
                global_scripts.project_global_scripts.__editor_attr__container_name__ = "Error"
                global_scripts.project_global_scripts.__editor_attr__selected_pos_mod__ \
                    = [[0, 0], [0, 0]]
                global_scripts.project_global_scripts.__editor_attr__selected_size_mod__ \
                    = [[0, 0], [0, 0]]
                global_scripts.project_global_scripts.__editor_attr__selected_rot_mod__ = [0, 0]
                global_scripts.project_global_scripts.__editor_attr__selected_opa_mod__ = [0, 0]

            self.selected = True

        # If the user clicks off of the text box
        elif global_scripts.mouse_state[0] and not self.hovered and self.activated:
            self.activated = False
            self.rename = True

        if self.rename:
            self.rename = False
            global_scripts.rename_file(self.object_path,
                                       self.text[1 + 2 * self.generated_value[2]:])

        if self.hovered:
            self.object_colour = (149, 152, 161)
        elif global_scripts.current_path == self.object_path:
            global_scripts.current_index = self.object_index
            self.object_colour = (160, 164, 174)
        else:
            self.object_colour = (175, 179, 189)

        # Reset variables
        if self.clicked:
            self.prev_clicked = True
            self.clicked = False
        else:
            self.prev_clicked = False
        self.hovered = False

    def left_clicked(self):
        self.clicked = True

    def middle_clicked(self):
        pass

    def right_clicked(self):
        pass

    def hovered_over(self):
        self.hovered = True

    def key_input(self, keys):
        # Text input only occurs once the text box has been clicked on
        if self.activated:
            if "BACKSPACE" in keys:
                if not self.prev_backspace:
                    if len(self.text) >= 2:
                        # Removes one character
                        self.text = self.text[:-1]
                        self.prev_backspace = True
            else:
                self.prev_backspace = False

                if "RETURN" in keys:
                    # The text has been entered and so the text box should not be active anymore
                    self.activated = False
                    self.rename = True
                else:
                    # Add the text input from the user to the text
                    self.text += keys[0]
        else:
            self.prev_backspace = False
