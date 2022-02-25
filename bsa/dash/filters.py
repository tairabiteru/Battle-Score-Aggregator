jinjafilters = []


def jinjafilter(func):
    """Decorate a function to automagically make it a jinja filter!"""
    jinjafilters.append(func)
    return func
