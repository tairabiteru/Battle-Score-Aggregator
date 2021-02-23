"""
This module defines the configuration used by the BSA.

It contains the default configuration which is generated when the program is
first run, as well as the code responsible for the serialization and
deserialization of the config file itself. The config file is stored using
the TOML format.
"""

import os
import sys
import toml


class Conf:
    """
    Define configuration to be used across modules.

    This class serializes the config, (or creates a new one) then places the
    configuration itself into attributes for easy access. When instantiated,
    it creates a config object which is used across the program to access
    settings.
    """

    # Base configuration
    BASE = {
        'host': 'localhost',
        'port': 8080,
        # Resolves to the directory that main.py is located in
        'rootDirectory': os.path.dirname(sys.modules['__main__'].__file__),
        'wwwDirectory': os.path.join(os.path.dirname(sys.modules['__main__'].__file__), "www"),
        'loginTimeout': 10,
        'adminEnabled': True,
        'numberOfRounds': 7,
        'questionsPerRound': 8,
        'numberOfBonusRounds': 1,
        'questionsPerBonusRound': 7
    }

    def __init__(self):
        # Try loading config from file. If it doesn't exist, use the base conf.
        try:
            config = toml.load(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), "conf.toml"))
        except FileNotFoundError:
            with open("conf.toml", "w") as conf:
                toml.dump(Conf.BASE, conf)
            config = Conf.BASE

        # These are 'internal' settings. They're here for easy access,
        # but they do not get written to the config file, as their value
        # is based upon the rest of the settings.
        config['templateDirectory'] = os.path.join(config['wwwDirectory'], "templates/")
        config['staticDirectory'] = os.path.join(config['wwwDirectory'], "static/")

        # Set config as attributes.
        for key, value in config.items():
            setattr(self, key, value)

# Instantiate config. This variable is the item that gets
# imported by everything else.
conf = Conf()
