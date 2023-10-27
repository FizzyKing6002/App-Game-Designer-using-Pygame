object_type = {
    "container" : False,
    "image" : False,
    "button" : False,
    "hover_activated" : False,
    "key_activated" : False
}
container_name = "xd"

class Example_Object:
    def __init__(self):
        self.update_priority = 0
        self.img_dir = ""
        self.activation_keys = {}

        self.position_modifiers = [[0, 1], [0, 1]]
        self.size_modifiers = [[0, 1], [0, 1]]
        self.rotation_modifiers = [0, 1]
        self.opacity_modifiers = [0, 1]

        self.animations = []

        def frame_update(self, time):
            pass