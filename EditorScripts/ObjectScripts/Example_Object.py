object_type = {
    "container" : True,
    "text" : False,
    "image" : True,
    "button" : True,
    "hover_activated" : False,
    "key_activated" : False
}
container_name = None

class Example_Object:
    def __init__(self):
        self.active = True
        self.update_priority = 0

        self.img_dir = "EditorTextures/example_image.png"
        self.activation_keys = {}

        self.position_modifiers = [[0, 0.5], [0, 0.5]]
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

    def frame_update(self, global_scripts):
        global_scripts.active0 = self.active
        if global_scripts.active0 == global_scripts.active1:
            global_scripts.active1 = True
            self.update_priority += 2

    def left_clicked(self):
        self.active = False

    def middle_clicked(self):
        pass

    def right_clicked(self):
        pass

    def hovered_over(self):
        pass

    def key_input(self, key):
        pass
