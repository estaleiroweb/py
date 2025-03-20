import os
import time
import pickle
from typing import Any
from ..decorator.singleton import singleton


@singleton(True)
class Session:
    dir = "/sessions"  # Pasta para armazenar sessões
    expire: int = 0  # seconds

    def __init__(self, id: str = None):
        self.__id: str = self.__get_id(id)
        self.__target: str = ''
        self.__data: dict = {}

        self.__target = self.target()
        self.__remove_on_expire()
        self.__data = self.load()
        # print(self.__repr__())

    def __str__(self) -> str:
        """Get id of session."""
        return self.__id

    def __call__(self, arg=None) -> dict | Any:
        """Get data of session. All or only `arg`."""
        return self.__data if arg == None else self.__data.get(arg)

    def __getattr__(self, name):
        print('get:', name)
        try:
            if name.startswith(f"_{self.__class__.__name__}__"):
                return object.__getattribute__(self, name)
            data = object.__getattribute__(
                self,
                f"_{self.__class__.__name__}__data"
            )
            return data.get(name)
        except AttributeError:
            return None  # ou levante uma exceção, dependendo do que você precisa

    def __setattr__(self, name, value):
        if name.startswith(f"_{self.__class__.__name__}__"):
            object.__setattr__(self, name, value)
        else:
            self.__data[name] = value
            self.save()

    def __repr__(self):
        return \
            f'{self.__class__.__name__}(' +\
            f'id={self.__id}, ' +\
            f'target={self.__target}, ' +\
            f'data={self.__data})'

    def __get_id(self, id) -> str:
        if id == None:
            import uuid
            id = uuid.uuid4()
        return str(id)

    def target(self) -> str:
        """Target of session"""
        if not self.__target:
            file = os.path.join(self.dir, self.__id)
            self.__target = os.path.abspath(file)
        return self.__target

    def reset(self):
        """Reset data value"""
        self.__data = {}

    def load(self) -> dict:
        """Load user data session from target"""
        self.__data = {}
        if os.path.exists(self.__target):
            with open(self.__target, "rb") as f:
                self.__data = pickle.load(f)
                # print('load', self.__data)
        return self.__data

    def save(self, data: dict = None):
        """Save user data session to target"""
        if data != None:
            self.__data = data
        # Create directory if not exists
        os.makedirs(self.dir, exist_ok=True)
        with open(self.__target, "wb") as f:
            # print('save: ',self.__data)
            pickle.dump(self.__data, f)

    def remove(self):
        """Remove user data session from target"""
        try:
            os.remove(self.__target)
        except FileNotFoundError:
            ...
        except IsADirectoryError:
            ...
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    def __remove_on_expire(self):
        """
        Verifica se um arquivo foi atualizado há mais de um determinado número de segundos.

        Args:
            caminho_arquivo (str): O caminho do arquivo a ser verificado.
            segundos (int): O número de segundos a comparar.

        Returns:
            bool: True se o arquivo foi atualizado há mais de 'segundos' segundos, False caso contrário.
            None: Caso o arquivo não exista.
        """
        if self.expire:
            try:
                # Obtém a hora da última modificação do arquivo (em segundos desde a época)
                last_update = os.path.getmtime(self.__target)

                delta_time = time.time() - last_update
                if delta_time > self.expire:
                    self.remove()
            except FileNotFoundError:
                # print(f"Erro: Arquivo '{self.__target}' não encontrado.")
                ...
            except Exception as e:
                print(f"Ocorreu um erro inesperado: {e}")
                ...
