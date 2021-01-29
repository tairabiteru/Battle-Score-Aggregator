import os
import sys
import toml


class Conf:
    """Define configuration to be used across modules."""

    BASE = {
        'host': 'localhost',
        'port': 8080,
        'rootDirectory': os.path.dirname(sys.modules['__main__'].__file__),
        'wwwDirectory': os.path.join(os.path.dirname(sys.modules['__main__'].__file__), "www"),
        'adminEnabled': True,
        'numberOfRounds': 7,
        'questionsPerRound': 8,
        'numberOfBonusRounds': 1,
        'questionsPerBonusRound': 7
    }

    def __init__(self):
        try:
            config = toml.load(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), "conf.toml"))
        except FileNotFoundError:
            with open("conf.toml", "w") as conf:
                toml.dump(Conf.BASE, conf)
            config = Conf.BASE

        config['templateDirectory'] = os.path.join(config['wwwDirectory'], "templates/")
        config['staticDirectory'] = os.path.join(config['wwwDirectory'], "static/")

        for key, value in config.items():
            setattr(self, key, value)


conf = Conf()
