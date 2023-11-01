object_type = {
    "container" : True,
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
        self.img_dir = "EditorTextures/pawn.png"
        self.activation_keys = {
            "SPACE" : True,
            "a" : True,
            "b" : False
        }

        self.position_modifiers = [[10, 0], [10, 0]]
        self.size_modifiers = [[0, 0.5], [0, 0.5]]
        self.rotation_modifiers = [0, 1]
        self.opacity_modifiers = [0, 1]

        self.position_origin = [0, 0]
        self.animations = [[False, [0, 0], [200, 200], 0, 5000, "move", "x"]]

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
