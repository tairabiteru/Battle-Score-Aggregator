import sys
import os
from dash.core import Dash


def main():
    sys.path.append(os.path.abspath(os.path.join("..", "bsa")))
    Dash.run()


if __name__ == "__main__":
    main()
