object_type = {
    "container" : True,
    "text" : False,
    "image" : True,
    "button" : True,
    "hover_activated" : False,
    "key_activated" : True
}
container_name = "Example_Object"

class Example_Object2:
    def __init__(self):
        self.active = True
        self.update_priority = 0

        self.objects_visible_outside_container = False
        self.img_dir = "EditorTextures/pawn.png"
        self.activation_keys = {
            "SPACE" : True,
            "a" : True,
            "b" : False
        }
        self.is_scroll_bar = False

        self.position_modifiers = [[10, 0], [10, 0]]
        self.size_modifiers = [[0, 0.5], [0, 0.5]]
        self.rotation_modifiers = [0, 1]
        self.opacity_modifiers = [0, 1]

        self.position_origin = [0, 0]

        self.text = ""
        self.text_font = "Calibri"
        self.text_colour = (0, 0, 0)
        self.text_bold = False
        self.text_italic = False

        self.one_time = True

    def frame_update(self, global_scripts):
        if self.one_time:
            self.one_time = False
            self.create_animation(400, 1000, "posx", "x")
            self.create_animation(0, 1000, "rot", "x")

    def left_clicked(self, mouse_pos):
        pass

    def middle_clicked(self, mouse_pos):
        pass

    def right_clicked(self, mouse_pos):
        pass

    def hovered_over(self, mouse_pos):
        pass

    def key_input(self, key):
        print(key)
