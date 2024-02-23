"""
Handles animations for window objects

Methods:
    create_animation(val, time, anim_type, *args):
        Creates an animation (list) in the format required to carry out animations
    animate(anim, time):
        Resposible for progressing animations passed to it based upon how much time has passed
"""


import math


def create_animation(val, time, anim_type, *args):
    # Args describes the easing function for the animation which is not required
    args = list(args)
    if len(args) == 0:
        # Default easing function is linear
        args = ["time_ratio"]
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

    # Gives the animation the default name of nothing
    if len(args) == 1:
        args.append("")

    # If the animation is 2-Dimensional
    if isinstance(val, list):
        # Create 2-Dimensional animation
        return [0, [0, 0], val, 0, time, anim_type, args[0], args[1], False]
    # Create 1-Dimensional animation
    return [0, 0, val, 0, time, anim_type, args[0], args[1], False]

def animate(anim, time):
    # If the animation is reversed, time goes backwards
    if anim[8]:
        time = -time

    # Increase the elapsed animation time by the time since the last frame
    anim[3] += time

    # If the target animation time is valid
    if anim[4] > 0:
        # Find the percentage of the animation that should be completed
        time_ratio = max(min(anim[3] / anim[4], 1), 0)
    else:
        # Assume the animation is completed
        time_ratio = 1

    # If the animation is completed, flag it as completed
    if time_ratio == 1:
        anim[0] = 2
    # If the animation is at the beginning, flag it that way
    elif time_ratio == 0:
        anim[0] = 0
    # If the animation is in progress, flag it that way
    else:
        anim[0] = 1

    # If the animation is 2-Dimensional
    if isinstance(anim[1], list):
        # Interpolate the new values for the animation
        for i in range(len(anim[1])):
            if isinstance(anim[6], list):
                exec(f"anim[1][i] = ({anim[6][i]}) * anim[2][i]",
                     locals(), globals())
            else:
                exec(f"anim[1][i] = ({anim[6]}) * anim[2][i]",
                     locals(), globals())
    else:
        # Interpolate the new value for the animation
        exec(f"anim[1] = ({anim[6]}) * anim[2]",
             locals(), globals())

    return anim
