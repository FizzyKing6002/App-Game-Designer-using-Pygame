object_type = {
    "container" : False,
    "text" : False,
    "image" : True,
    "button" : True,
    "hover_activated" : False,
    "key_activated" : False
}
container_name = None

class Example_Object4:
    def __init__(self):
        self.active = False
        self.update_priority = 1

        self.objects_visible_outside_container = True
        self.img_dir = "EditorTextures/palms.png"
        self.activation_keys = {}
        self.is_scroll_bar = False

        self.position_modifiers = [[0, 0.5], [0, 0.5]]
        self.size_modifiers = [[0, 1], [0, 1]]
        self.rotation_modifiers = [0, 1]
        self.opacity_modifiers = [0, 1]

        self.position_origin = [0.5, 0.5]

        self.text = ""
        self.text_font = "Calibri"
        self.text_colour = (0, 0, 0)
        self.text_bold = False
        self.text_italic = False

        self.triggered = False

    def frame_update(self, global_scripts):
        if self.triggered:
            self.triggered = False
            if not global_scripts.mousedown:
                self.active = False
                global_scripts.state = 0
                global_scripts.mousedown = True
                self.update_priority += 2
        else:
            if global_scripts.mousedown and self.active:
                global_scripts.mousedown = False

        if not self.active and global_scripts.state == 1:
            self.active = True


    def left_clicked(self, mouse_pos):
        self.triggered = True

    def middle_clicked(self, mouse_pos):
        pass

    def right_clicked(self, mouse_pos):
        pass

    def hovered_over(self, mouse_pos):
        pass

    def key_input(self, key):
        pass
