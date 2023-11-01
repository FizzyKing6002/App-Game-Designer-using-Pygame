def __call__(anim):
    pass

def create_animation(val, time, anim_type):
    if isinstance(val, list):
        return [[0, 0], val, 0, time, anim_type]
    else:
        return [0, val, 0, time, anim_type]
