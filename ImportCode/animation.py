"""
Handles animations for window objects

Methods:
    create_animation(val, time, anim_type, *args):
        Creates an animation (list) in the format required to carry out animations
    animate(anim, time):
        Resposible for progressing animations passed to it based upon how much time has passed
"""


def create_animation(val, time, anim_type, *args):
    # Args describes the easing function for the animation which is not required
    args = list(args)
    if len(args) == 0:
        # Default easing function is linear
        args = "x"
    else:
        # If multiple easing functions are given
        if isinstance(args[0], list):
            # Rewrite easing functions in terms of time_ratio
            for function in args[0]:
                function = function.replace("x", "time_ratio")
                function = function.replace("y", "")
                function = function.replace("=", "")
        else:
            # Rewrite easing function in terms of time_ratio
            args[0] = args[0].replace("x", "time_ratio")
            args[0] = args[0].replace("y", "")
            args[0] = args[0].replace("=", "")

    # If the animation is 2-Dimensional
    if isinstance(val, list):
        # Create 2-Dimensional animation
        return [False, [0, 0], val, 0, time, anim_type, args[0]]
    # Create 1-Dimensional animation
    return [False, 0, val, 0, time, anim_type, args[0]]

def animate(anim, time):
    # Increase the elapsed animation time by the time since the last frame
    anim[3] += time

    # If the target animation time is valid
    if anim[4] > 0:
        # Find the percentage of the animation that should be completed
        time_ratio = min(anim[3] / anim[4], 1)
    else:
        # Assume the animation is completed
        time_ratio = 1

    # If the animation is completed, flag it as completed
    if time_ratio == 1:
        anim[0] = True

    # If the animation is 2-Dimensional
    if isinstance(anim[1], list):
        # Interpolate the new values for the animation
        for i in range(len(anim[1])):
            if isinstance(anim[-1], list):
                exec(f"anim[1][i] = ({anim[-1][i]}) * anim[2][i]",
                     locals(), globals())
            else:
                exec(f"anim[1][i] = ({anim[-1]}) * anim[2][i]",
                     locals(), globals())
    else:
        # Interpolate the new value for the animation
        exec(f"anim[1] = ({anim[-1]}) * anim[2]",
             locals(), globals())

    return anim
