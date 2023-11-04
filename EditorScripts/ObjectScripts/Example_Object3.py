object_type = {
    "container" : False,
    "text" : True,
    "image" : False,
    "button" : False,
    "hover_activated" : False,
    "key_activated" : False
}
container_name = "Example_Object2"

class Example_Object3:
    def __init__(self):
        self.active = True
        self.update_priority = 2

        self.objects_visible_outside_container = True
        self.img_dir = None
        self.activation_keys = {}

        self.position_modifiers = [[0, 0.5], [0, 0.5]]
        self.size_modifiers = [[0, 1], [0, 0.3]]
        self.rotation_modifiers = [0, 1]
        self.opacity_modifiers = [0, 1]

        self.position_origin = [0.5, 0.5]
        self.animations = []

        self.text = "Hello World"
        self.text_font = "Calibri"
        self.text_colour = (0, 100, 0)
        self.text_bold = True
        self.text_italic = True

        self.one_time = True

    def frame_update(self, global_scripts):
        if self.one_time:
            self.one_time = False
            self.create_animation(237, 11000, "rot", "x**3")

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
