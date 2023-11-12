object_type = {
    "container" : False,
    "text" : True,
    "image" : True,
    "button" : False,
    "hover_activated" : False,
    "key_activated" : False
}
container_name = "Example_Object2"

class Example_Object5:
    def __init__(self):
        self.active = True
        self.update_priority = 1

        self.objects_visible_outside_container = True
        self.img_dir = ""
        self.activation_keys = {}
        self.is_scroll_bar = False

        self.position_modifiers = [[0, 0.5], [0, 0.5]]
        self.size_modifiers = [[0, 0.1], [0, 2]]
        self.rotation_modifiers = [0, 1]
        self.opacity_modifiers = [0, 1]

        self.position_origin = [0.5, 0.5]

        self.text = "T"
        self.text_font = "Calibri"
        self.text_colour = (100, 0, 0)
        self.text_bold = True
        self.text_italic = True

    def frame_update(self, global_scripts):
        pass

    def left_clicked(self, mouse_pos):
        pass

    def middle_clicked(self, mouse_pos):
        pass

    def right_clicked(self, mouse_pos):
        pass

    def hovered_over(self, mouse_pos):
        pass

    def key_input(self, key):
        pass
