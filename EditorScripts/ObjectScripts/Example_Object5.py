object_type = {
    "container" : False,
    "text" : False,
    "image" : False,
    "button" : False,
    "hover_activated" : False,
    "key_activated" : False
}
container_name = "Example_Object2"

class Example_Object5:
    def __init__(self):
        self.active = True

        self.update_priority = 0
        self.img_dir = None
        self.activation_keys = {}

        self.position_modifiers = [[0, 1], [0, 1]]
        self.size_modifiers = [[0, 1], [0, 1]]
        self.rotation_modifiers = [0, 1]
        self.opacity_modifiers = [0, 1]

        self.position_origin = [0.5, 0.5]
        self.animations = []

        self.text = ""
        self.text_font = "Calibri"
        self.text_colour = (0, 0, 0)
        self.text_bold = False
        self.text_italic = False

    def frame_update(self, time):
        pass

    def left_clicked(self):
        pass

    def middle_clicked(self):
        pass

    def right_clicked(self):
        pass

    def hovered_over(self):
        pass

    def key_input(self, key):
        pass
