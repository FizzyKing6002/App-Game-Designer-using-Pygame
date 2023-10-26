def Object(*args):
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

    container, image, button, hover_activated, key_activated, *args = args
    return Object(args)

class Container:
    pass

class Image:
    pass

class Button:
    pass

class Hover_Activated:
    pass

class Key_Activated:
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
