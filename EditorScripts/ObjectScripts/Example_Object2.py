object_type = {
    "container" : True,
    "image" : True,
    "button" : True,
    "hover_activated" : False,
    "key_activated" : False
}
container_name = "Example_Object"

class Example_Object2:
    def __init__(self):
        self.update_priority = 0
        self.img_dir = "EditorTextures/pawn.png"
        self.activation_keys = {}

        self.position_modifiers = [[0, 0.5], [0, 0.5]]
        self.size_modifiers = [[0, 0.5], [0, 0.5]]
        self.rotation_modifiers = [30, 1]
        self.opacity_modifiers = [0, 1]

        self.animations = []

    def frame_update(self, time):
        pass

    def left_clicked(self):
        print("ping")

    def middle_clicked(self):
        pass

    def right_clicked(self):
        pass

    def hovered_over(self):
        pass
