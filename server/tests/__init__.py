import sys
from pathlib import Path

path = Path(__file__)
path_string = path.parent.parent.absolute().__str__()

sys.path.append(path_string)
