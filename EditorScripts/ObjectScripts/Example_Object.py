object_type = {
    "container" : True,
    "image" : True,
    "button" : False,
    "hover_activated" : False,
    "key_activated" : False
}
container_name = None

class Example_Object:
    def __init__(self):
        self.update_priority = 0
        self.img_dir = "EditorTextures/example_image.png"
        self.activation_keys = {}

        self.position_modifiers = [[0, 1], [0, 1]]
        self.size_modifiers = [[0, 1], [0, 1]]
        self.rotation_modifiers = [0, 1]
        self.opacity_modifiers = [0, 1]

        self.animations = []

        def frame_update(self, time):
            pass
