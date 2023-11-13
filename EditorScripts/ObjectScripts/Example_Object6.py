object_type = {
    "container" : False,
    "text" : False,
    "image" : True,
    "button" : True,
    "hover_activated" : False,
    "key_activated" : False
}
container_name = "Example_Object2"

class Example_Object6:
    def __init__(self):
        self.active = True
        self.update_priority = 1000

        self.objects_visible_outside_container = True
        self.img_dir = "EditorTextures/box.png"
        self.activation_keys = {
            "MOUSEWHEEL" : True
        }
        self.is_scroll_bar = True

        self.position_modifiers = [[0, 0.975], [0, 0.5]]
        self.size_modifiers = [[0, 0.05], [0, 1]]
        self.rotation_modifiers = [0, 1]
        self.opacity_modifiers = [0, 1]

        self.position_origin = [0.5, 0.5]

        self.text = ""
        self.text_font = "Calibri"
        self.text_colour = (0, 0, 0)
        self.text_bold = False
        self.text_italic = False

        self.clicked = False
        self.init_mouse_pos = None
        self.mouse_pos_diff = 0
        self.scroll_bar_limit = 0

    def frame_update(self, global_scripts):
        self.pos[1] += self.mouse_pos_diff

        if not self.clicked and self.init_mouse_pos is not None:
            self.init_mouse_pos = None

            self.position_modifiers[1][0] += self.mouse_pos_diff
            self.mouse_pos_diff = 0

        self.clicked = False

    def left_clicked(self, mouse_pos):
        self.clicked = True
        if self.init_mouse_pos is None:
            self.init_mouse_pos = mouse_pos[1]
        self.mouse_pos_diff = mouse_pos[1] - self.init_mouse_pos

        total_diff = self.mouse_pos_diff + self.position_modifiers[1][0]

        if total_diff > self.scroll_bar_limit:
            self.mouse_pos_diff = self.scroll_bar_limit - self.position_modifiers[1][0]
        elif total_diff < 0:
            self.mouse_pos_diff = 0 - self.position_modifiers[1][0]

    def middle_clicked(self, mouse_pos):
        pass

    def right_clicked(self, mouse_pos):
        pass

    def hovered_over(self, mouse_pos):
        pass

    def key_input(self, key):
        print(key)
