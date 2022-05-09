from time import time


def time_calc(start, now):
    sekunden = now - round(time() - start)
    if sekunden < 60:
        return str(sekunden) + " seconds"
    elif sekunden < 3600:
        minutes = sekunden // 60
        seconds = sekunden - 60 * minutes
        return str(minutes) + " minutes and " + str(seconds) + " seconds"
    else:
        hours = sekunden // 3600
        minutes = (sekunden - 3600 * hours) // 60
        seconds = sekunden - 3600 * hours - 60 * minutes
        return str(hours) + " hours, " + str(minutes) + " minutes and " + str(seconds) + " seconds"
