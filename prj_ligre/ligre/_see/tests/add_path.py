import os
import sys

__dir_base__ = os.path.dirname(__file__)


def up(project: str) -> str:
    global __dir_base__
    while __dir_base__ and os.path.basename(__dir_base__) != project:
        __dir_base__ = os.path.dirname(__dir_base__)
    if __dir_base__:
        sys.path.append(os.path.dirname(__dir_base__))
    return __dir_base__
