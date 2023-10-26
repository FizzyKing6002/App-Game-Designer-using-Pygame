def Object(*args):
    container, image, button, hover_activated, key_activated, *args = args

    class Object(Container if container else None1,
                 Image if image else None2,
                 Button if button else None3,
                 Hover_Activated if hover_activated else None4,
                 Key_Activated if key_activated else None5):
        def __init__(self, *args):
            self.position = [0, 0]
            self.size = [0, 0]
            self.rotation = 0
            self.opacity = 1
            self.script_directory = args[0]

        def __call__(self, window, time,
                     con_pos, con_size, con_rot, con_opa,
                     mouse_pos, mouse_state, key_state):
            pass

        def animate(self, time):
            pass

        def calc_attr(self, con_pos, con_size, con_rot, con_opa):
            pass

    return Object(args)

class Container:
    def __init__(self):
        self.objects = []

    def call_objects(self, window, time,
                     mouse_pos, mouse_state, key_state):
        pass

class Image:
    def draw_self(self):
        pass

class Button:
    def call_clicked(self, mouse_pos, mouse_state):
        pass

class Hover_Activated:
    def call_hovered(self, mouse_pos):
        pass

class Key_Activated:
    def call_activated(self, key_state):
        pass

class None1:
    pass
class None2:
    pass
class None3:
    pass
class None4:
    pass
class None5:
    pass
