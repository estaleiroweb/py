import os
import json
import sys
import configparser
import jsonpath_ng as j
# from typing import Union
from .fn import merge_recursive


class Conf:
    """
    Class to load and access configurations from JSON and INI files.

    Allows loading multiple configuration files, merging them, and accessing values
    using JSONPath. Also supports loading INI files.
    """

    subdir = 'conf'
    """Subfolder that has configurations"""

    path: 'dict[str,list[str]]' = {}
    """Collection of list of directories where configuration files are searched."""

    cache: dict = {}
    """Cache to store already loaded configurations."""

    debug: bool = False
    """Flag to enable debug message display."""

    def __init__(self, file: str, encoding: str = "utf-8", merge: bool = False):
        """
        Initializes a Conf class instance.

        Args:
            file: Configuration file name to load.
            encoding: Configuration file encoding.
        """
        if Conf.subdir not in Conf.path:
            Conf.path[Conf.subdir] = []
            Conf.__checkDir(sys.path[0])
            d, dOld = __file__, ''
            while d and d != dOld:
                dOld, d = d, os.path.dirname(d)
                Conf.__checkDir(d)

        self.__subdir: str = self.subdir
        self.__dir: list = []
        self.__file: str = file
        self.__encoding: str = encoding
        self.__load(merge)

    def __str__(self) -> str:
        """Returns the configuration file name."""
        return self.__file

    def __call__(self, jsonPath: str = None) -> 'dict|list|str|int|float|bool|None':
        """
        Accesses configuration values using JSONPath.

        Args:
            jsonPath: JSONPath expression to access values.

        Returns:
            The found value(s), or the entire configuration dictionary if jsonPath is None.
        """
        conf = Conf.cache[self.key]['conf']
        if jsonPath is not None:
            jsonpath_expr = j.parse(jsonPath)
            out = [match.value for match in jsonpath_expr.find(conf)]
            return out[0] if len(out) == 1 else out
        return conf

    @classmethod
    def __checkDir(cls, dir: str):
        dir = os.path.join(dir, cls.subdir)
        if os.path.isdir(dir):
            cls.path[cls.subdir].append(os.path.realpath(dir))

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

    def __load(self, merge: bool = False):
        """Loads the configuration file (JSON or INI) and stores it in cache."""
        key = self.key
        if key in Conf.cache:
            return
        Conf.cache[key] = {
            'dir': [],
            'conf': None,
        }
        for dir in self.path[self.subdir]:
            fullfile = os.path.join(dir, self.__file)
            if not os.path.isfile(fullfile):
                continue
            self.__show(f'Conf Load {fullfile}')
            Conf.cache[key]['dir'].append(dir)
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
            if merge:
                Conf.cache[key]['conf'] = merge_recursive(
                    Conf.cache[key]['conf'],
                    conf
                )
            else:
                Conf.cache[key]['conf'] = conf
                break
        self.__dir = Conf.cache[key]['dir']

    @property
    def key(self):
        """Key of cache"""
        return self.__file
        return f'{self.__subdir}/{self.__file}'

    def __show(self, text):
        """Displays debug messages if debug mode is enabled."""
        if self.debug:
            print(text)
