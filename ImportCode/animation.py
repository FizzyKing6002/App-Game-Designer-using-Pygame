def animate(anim, time):
    anim[3] += time

    if anim[4] != 0:
        time_ratio = min(anim[3] / anim[4], 1)
    else:
        time_ratio = 1

    if time_ratio == 1:
        anim[0] = True

    if isinstance(anim[-1], list):
        for function in anim[-1]:
            function = function.replace("x", "time_ratio")
            function = function.replace("y", "")
            function = function.replace("=", "")
    else:
        anim[-1] = anim[-1].replace("x", "time_ratio")
        anim[-1] = anim[-1].replace("y", "")
        anim[-1] = anim[-1].replace("=", "")

    if isinstance(anim[1], list):
        for i in range(len(anim[1])):
            if isinstance(anim[-1], list):
                exec(f"anim[1][i] = ({anim[-1][i]}) * anim[2][i]",
                     locals(), globals())
            else:
                exec(f"anim[1][i] = ({anim[-1]}) * anim[2][i]",
                     locals(), globals())
    else:
        exec(f"anim[1] = ({anim[-1]}) * anim[2]",
             locals(), globals())

    return anim
