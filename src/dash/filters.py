filters = []


def filter(func):
    """Decorate a function to automagically make it a jinja filter!"""
    filters.append(func)
    return func
