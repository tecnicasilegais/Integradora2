from datetime import datetime


def make_filename(name):
    return "%s%s" % (datetime.now().strftime("%d_%H-%M-%S_"), name)
