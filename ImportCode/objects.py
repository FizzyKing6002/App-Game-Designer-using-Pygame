def Object(*args):
    container, image, button, hover_activated, key_activated, object_class, *args = args

    class Object(Container if container else None1,
                 Image if image else None2,
                 Button if button else None3,
                 Hover_Activated if hover_activated else None4,
                 Key_Activated if key_activated else None5,
                 object_class):
        def __init__(self, *args):
            self.pos = [0, 0]
            self.size = [0, 0]
            self.rot = 0
            self.opa = 1

            if container:
                Container.__init__(self)

            object_class.__init__(self)

        def __call__(self, window, time,
                     con_pos, con_size, con_rot, con_opa,
                     mouse_pos, mouse_state, key_state):
            print("pong")
            self.call_clicked = getattr(self, "call_clicked", None)
            if callable(self.call_clicked):
                self.call_clicked(mouse_pos, mouse_state)

            self.call_hovered = getattr(self, "call_hovered", None)
            if callable(self.call_hovered):
                self.call_hovered(mouse_pos)

            self.call_activated = getattr(self, "call_activated", None)
            if callable(self.call_activated):
                self.call_activated(key_state)

            self.animate(time)
            self.calc_attr(con_pos, con_size, con_rot, con_opa)

            self.draw_self = getattr(self, "draw_self", None)
            if callable(self.draw_self):
                self.draw_self()

            self.call_objects = getattr(self, "call_objects", None)
            if callable(self.call_objects):
                self.call_objects(window, time,
                                  mouse_pos, mouse_state, key_state)

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
        for obj in self.objects:
            obj(window, time,
                self.pos, self.size, self.rot, self.opa,
                mouse_pos, mouse_state, key_state)

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
