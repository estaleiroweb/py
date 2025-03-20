import os
import json
import sys
import configparser
import jsonpath_ng as j
from .fn import merge_recursive


class Conf:
    """
    Class to load and access configurations from JSON and INI files.

    Allows loading multiple configuration files, merging them, and accessing values
    using JSONPath. Also supports loading INI files.
    """

    path: list = []
    """List of directories where configuration files are searched."""

    cache: dict = {}
    """Cache to store already loaded configurations."""

    debug: bool = False
    """Flag to enable debug message display."""

    def __new__(cls, *args, encoding: str = "utf-8", returnDict: bool = False) -> 'dict[str,Conf]|list[Conf]|Conf|None':
        """
        Creates a new instance or list of instances of the Conf class.

        Args:
            *args: Configuration file names to load.
            encoding: Configuration file encoding.
            returnDict: If True, returns a dictionary of instances instead of a list.

        Returns:
            A Conf instance, a list of Conf instances, a dictionary of Conf instances, or None.
        """
        op = os.path
        if not cls.path:
            cls.path = [
                op.realpath(op.join(op.dirname(__file__), '..', 'conf')),
                op.realpath(op.join(sys.path[0], 'conf')),
            ]
        if len(args) > 1:
            if returnDict:
                return {file: cls(file, encoding=encoding) for file in args}
            else:
                return [cls(file, encoding=encoding) for file in args]
        else:
            return super().__new__(cls)

    def __init__(self, file: str, *, encoding: str = "utf-8"):
        """
        Initializes a Conf class instance.

        Args:
            file: Configuration file name to load.
            encoding: Configuration file encoding.
        """
        self.__dir: list = []
        self.__file: str = file
        self.__encoding: str = encoding
        self.__load()

    def __str__(self) -> str:
        """Returns the configuration file name."""
        return self.__file

    def __call__(self, jsonPath: str = None) -> dict | list | str | int | float | bool | None:
        """
        Accesses configuration values using JSONPath.

        Args:
            jsonPath: JSONPath expression to access values.

        Returns:
            The found value(s), or the entire configuration dictionary if jsonPath is None.
        """
        conf = Conf.cache[self.__file]['conf']
        if jsonPath is not None:
            jsonpath_expr = j.parse(jsonPath)
            out = [match.value for match in jsonpath_expr.find(conf)]
            return out[0] if len(out) == 1 else out
        return conf

    @property
    def dir(self) -> list:
        """Directories where the configuration file was found."""
        return self.__dir

    @property
    def file(self) -> str:
        """Configuration file name."""
        return self.__file

    @property
    def encoding(self) -> str:
        """Configuration file encoding."""
        return self.__encoding

    def __load(self):
        """Loads the configuration file (JSON or INI) and stores it in cache."""
        if self.__file not in Conf.cache:
            Conf.cache[self.__file] = {
                'dir': [],
                'conf': None,
            }
        self.__dir = []
        for dir in self.path:
            fullfile = os.path.join(dir, self.__file)
            if not os.path.isfile(fullfile):
                continue
            self.__show(f'Conf Load {fullfile}')
            self.__dir.append(dir)
            conf = None
            if self.__file.endswith('.json'):
                with open(fullfile, "r", encoding=self.__encoding) as f:
                    conf = json.load(f)
            elif self.__file.endswith('.ini'):
                config = configparser.ConfigParser()
                config.read(fullfile)
                conf = {
                    s: dict(config.items(s)) for s in config.sections()
                }
            else:
                continue
            Conf.cache[self.__file]['conf'] = merge_recursive(
                Conf.cache[self.__file]['conf'],
                conf
            )
        Conf.cache[self.__file]['dir'] = self.__dir
        self.__dir = Conf.cache[self.__file]['dir']

    def __show(self, text):
        """Displays debug messages if debug mode is enabled."""
        if self.debug:
            print(text)
