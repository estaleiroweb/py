import re
import time
from abc import ABC, abstractmethod

DEBUG_NONE: int = 0
"""Debug nothing"""

DEBUG_PRIMARY: int = 1
"""Linked Expect._debug_primary method. Debug without LineFeed. Mainly used to shows output of terminal"""

DEBUG_INFO: int = 2
"""Linked Expect._debug_info method. Debug with LineFeed the informations steps of the job"""

DEBUG_CMD: int = 4
"""Linked Expect._debug_cmd method. Debug with LineFeed the send commands"""

DEBUG_WARNING: int = 8
"""Linked Expect._debug_warning method. Debug with LineFeed thwhen warning happens"""

DEBUG_ERROR: int = 16
"""Linked Expect._error method. Debug with LineFeed the fatal error"""

DEBUG_ALL: int = \
    DEBUG_PRIMARY + \
    DEBUG_INFO + \
    DEBUG_CMD + \
    DEBUG_WARNING + \
    DEBUG_ERROR
"""Debug everything. This is the union of before debugs"""

ret_dict: bool = False
"""When True, expect() returns dictionary instead of list for sequence inputs."""


class Main(ABC):
    verbose: int = DEBUG_NONE
    """
    Controls verbosity level for logging and debugging.

    Returns:
        bool|str: Verbosity setting
        - False: No verbose output (default)
        - True: Basic verbose output
        - 'all': Comprehensive verbose output
    """
    charset: str = 'utf-8'
    """Charset used in decode"""

    _prompts = {
        'linux': r'.*[\$#>] ?$',
        'bash': r'.*[\$#>] ?$',  # bash TCL {\n(-bash.*|\[[^\]]+\])[$#] *$} }
        # oracle TCL { set prompt {[\r\n](selection:|Save Changes \[y/n\]\?|((\e\[1m)?\*{1,2}(\e\[0m)?)?\w+(\([^\(\)]+\))?[>#])\s*} }
        'oracle': r'.*[\$#>] ?$',
        'juniper': r'.*[\$#>] ?$',  # TCL { set prompt {\n[^>]*> *$} }
        'alteon': r'.*[\$#>] ?$',  # TCL { set prompt {>>[^#]*# *$} }
        # cyclades TCL { set prompt {Select option ==> *$} }
        'cyclades': r'.*[\$#>] ?$',
        # cisco TCL { set prompt {\n[^>#]*[>#]( *\(enable\))? *$} }
        'cisco': r'.*[\$#>] ?$',
        'msc': r'.*[\$#>] ?$',  # TCL  set prompt {\n<|>} }
        'itl_vsc': r'.*[\$#>] ?$',  # TCL { set prompt {\n.*\d<} }
        # itl_nmm TCL { set prompt {\n(.*@.*:.*[$#] *|ITL>)$} }
        'itl_nmm': r'.*[\$#>] ?$',
        'hp': r'.*[\$#>] ?$',  # TCL  { set prompt {\n.*(>|\[Y/N\]:) *$} }
        'huawei': r'.*[\$#>] ?$',  # TCL { set prompt {[\n\r]+<[^>]+> *$} }
        # motorola TCL { set prompt {(#Enter Selection:|>) *$} }
        'motorola': r'.*[\$#>] ?$',
        # auto TCL { set prompt {[\n\r]+((-bash.*|\[[^\]]+\])[$#]|[^$>#]*([$>#]|\[Y/N\]:)( *\(enable\))?|>>[^#]*#|Select option ==>|#Enter Selection:) *$} }
        'auto': r'.*[\$#>] ?$',
    }
    """
    Collection of predefined command prompts for various systems.

    Contains regular expressions that match common shell prompts for different
    operating systems and devices.

    Returns:
        dict[str,str]: Mapping of system names to their respective prompt regex patterns
    """

    _mores = {
        'try_again': {'er': r'Please try again', 'exit': 10},
        'denied': {'er': r'Permission denied', 'exit': 10},
        'auth': {'er': r'authentication failures', 'exit': 10},
        'telnet': {'er': r'telnet sConnection closed by foreign host', 'exit': 50},
        'conn': {'er': r'Connection failed', 'exit': 10},
        'command': {'er': r'Unknown command.*[\n\r].*', 'exit': 40},
        'yesno': {'er': r'\[[yY]/[nN]\]\??: *$', 'send': 'n'},
        'user': {'er': r'(login|username|personal sshlogin \d+) *: *$', 'send': ''},
        'password': {'er': r'password *: *$', 'send': ''},
        'more': {'er': r'--more---', 'send': ' '},
    }
    """
    Collection of predefined patterns for handling common terminal interactions.

    Each entry defines a pattern to match and an action to take when encountered
    during command execution.

    Returns:
        dict[str, dict[str, str|int|callable]]: Dictionary of interaction handlers with:
            - 'er': Regular expression pattern to match
            - 'exit': Exit code to return (optional)
            - 'send': String to send in response (optional)
            - 'exec': Callback function to execute (optional)
    """

    _idErrors = {
        0: 'OK',
        1: 'End of connection',
        2: 'Unknown error',
        3: 'Command error',
        4: 'Connection error',
        5: 'Value error',
    }

    def __init__(self):
        self.__prompt: str = None
        self.__more: list = []
        self.__first: bool = True
        self.__timeout: int = 10

        self._conn = None
        """Conection of collect"""

        self._session = None
        """Session of connection"""

        self.welcome: str = None
        """Welcome content. It is the firts content after connection and before any command"""

        self.exit = 0
        """Exit code"""

        self.buffer: str = ''
        """Contains the full content received from the last command execution."""

        self.lf = '\n'
        """End of line used to send commands"""

        self.leaveInteractive: str = ':END:'
        """Command to leave the interactive mode"""

        self.sleep: float = 0
        """Time to sleep after send a command"""

    def __del__(self):
        """
        Destructor that ensures connections are properly closed.
        """
        self.close()

    def __call__(self,
                 command: 'str|list[str]|tuple[str]|dict[str,str]' = None
                 ) -> 'str|list[str]|dict[str,str]|bool|None':
        """
        Execute `self.command` in acoord of the type parameter command.

        Handles different input types:
        - str: Single command execution
        - list/tuple: Multiple commands executed sequentially
        - dict: Keys are command names, values are commands to execute

        Args:
            command (str|list|tuple|dict, optional): Command(s) to execute. Defaults to None.

        Returns:
            str|list|dict|None: Command output(s) in format matching the input type,
                                or None if connection is closed or error occurs
        """
        if not self._conn:
            return False
        if self.__first:
            self.buffer = ''
            self.welcome = self._expect()
            self.__first = False
        if not command:
            return
        self.exit = 0
        if type(command) == dict:
            out = {}
            for i in command.keys():
                out[i] = self.__call__(command[i])
            return out
        elif type(command) in (list, tuple):
            if ret_dict:
                out = {}
                for cmd in command:
                    out[cmd] = self.__call__(cmd)
            else:
                out = []
                for cmd in command:
                    out.append(self.__call__(cmd))
            return out
        else:
            try:
                if self.__send(command):
                    self.buffer = ''
                    return self._expect()
            except Exception as e:
                self._error(3, e)
                return

    @property
    def timeout(self):
        """
        Get or set the timeout of shell.

        Returns:
            int: Timeout of shell
                - Default=10
        """
        return self.__timeout

    @timeout.setter
    def timeout(self, value: int):
        if value < 0:
            self._debug_warning(f'Timeout must be greater than 0 ({value})')
        else:
            self._set_timeout(value)
            self.__timeout = value

    @timeout.deleter
    def timeout(self):
        self.timeout = 10

    @property
    def prompt(self):
        """
        Get or set the prompt pattern (regular expression) used for command response detection.

        Can be set using predefined keys from `self._prompts` or a custom regex pattern.

        Deleting this property resets it to 'auto'.

        Returns:
            str: Regular expression pattern for prompt detection
                - Default=auto
        """
        return self.__prompt

    @prompt.setter
    def prompt(self, value: str):
        if not value:
            value = 'auto'
        if value in self._prompts:
            self.__prompt = self._prompts[value]
        else:
            self.__prompt = value
        self._debug_info(f'Prompt: {self.__prompt}')

    @prompt.deleter
    def prompt(self):
        self.prompt = 'auto'

    @property
    def more(self) -> 'list[dict]':
        """
        Get or modify the list of patterns for handling interactive prompts.

        When setting:
        - String input is treated as a key to self._mores
        - Dict input adds a new pattern handler
        - List input processes each element recursively

        Deleting this property clears all handlers.

        Returns:
            list[dict]: List of pattern handlers with format:
                ```python
                {
                    'er': str,      # Regular expression to match (required)
                    'exit': int,    # Exit code to return (optional)
                    'send': str,    # String to send in response (optional)
                    # Function to call with self as argument (optional)
                    'exec': callable
                }
                ```
        """
        return self.__more

    @more.setter
    def more(self, value: 'str|list|dict'):
        if not value:
            return
        if isinstance(value, list):
            for i in value:
                self.more = i
            return
        if isinstance(value, str) and value in self._mores:
            value = self._mores[value]
        if not isinstance(value, dict):
            return self._error(5, f'This value is not dict: {value}')
        if 'er' not in value:
            return self._error(5, 'There is not `er` key')
        if not isinstance(value['er'], str):
            return self._error(5, 'The `er` key is not str')
        if 'exit' not in value and 'send' not in value and 'exec' not in value:
            return self._error(5, 'There is not `exit,send,exec` keys')
        if 'exit' in value and not isinstance(value['exit'], int):
            return self._error(5, 'The `exit` key is not int')
        if 'send' in value and not isinstance(value['send'], str):
            return self._error(5, 'The `send` key is not str')
        if 'exec' in value and not callable(value['exec']):
            return self._error(5, 'The `exec` key is not callable')

        self.__more.append(value)
        self._debug_info(f'Append more: {value}')

    @more.deleter
    def more(self):
        self.__more = []
        self._debug_info('Clear more')

    @property
    def backSpc(self) -> str:
        b = '\x08'*len(self.leaveInteractive)
        return b+self.lf

    @abstractmethod
    def _send(self, command: str):
        """
        Execute a single command.

        Handles different input types:
        - str: Single command execution

        Args:
            command (str): Command(s) to execute.
        """
        pass

    @abstractmethod
    def _recv(self) -> bytes:
        """
        Receive the output of the command.

        Args:
            prompt (str|list): Prompt of command if exists

        Returns:
            str: Terminal output
        """
        pass

    @abstractmethod
    def _set_timeout(self, value: int) -> bool:
        """Send the timeout value to connection class"""
        pass

    def __send(self, command: str) -> bool:
        """
        Execute a single command.

        Handles different input types:
        - str: Single command execution

        Args:
            command (str): Command(s) to execute.

        Returns:
            bool: True if successful, False otherwise.
        """
        if command and type(command) == str and self.isConnected():
            self._debug_cmd(command)
            self._send((command + self.lf).encode(self.charset))
            return True
        return False

    def _debug_primary(self, text):
        """
        Output debug information based on verbosity settings.

        Args:
            text (str): The text to output
        """
        if self.verbose & DEBUG_PRIMARY:
            print(f'{text}', end='')

    def _debug_info(self, text):
        """
        Output debug information based on verbosity settings.

        Args:
            text (str): The text to output
        """
        if self.verbose & DEBUG_INFO:
            print(f'# {text}')

    def _debug_cmd(self, text):
        """
        Output debug information based on verbosity settings.

        Args:
            text (str): The text to output
        """
        if self.verbose & DEBUG_CMD:
            print(f'>>>>>>>>>>>>>>> {text}')

    def _debug_warning(self, text):
        """
        Output debug information based on verbosity settings.

        Args:
            text (str): The text to output
        """
        if self.verbose & DEBUG_WARNING:
            print(f'### WARNING: {text}')

    def _error(self, idError: int = 0, content=None) -> bool:
        """
        Output error messages and return False.

        Args:
            text (str): The error message to output

        Returns:
            bool: Always returns False
        """
        self.exit = idError
        if self.verbose & DEBUG_ERROR:
            if idError in self._idErrors:
                print(f'### ERROR[{idError}]:', self._idErrors[idError])
            if content:
                print(f'{content}')
        return False if idError else True

    def _action(self, action: dict) -> bool:
        """
        Execute an action based on the provided pattern.

        Actions can include sending a response, executing a function, or setting an exit code.

        Args:
            action (dict): Action to execute

        Returns:
            bool: True if script is the end, False otherwise
        """
        if 'send' in action:
            self._send(action['send'])
        if 'exec' in action and callable(action['exec']):
            if action['exec'](self):
                return True
        if 'exit' in action:
            self.exit = action['exit']
            return True
        return False

    def _checkMore(self, recv: str) -> bool:
        """
        Check if the received content matches any of the defined patterns.

        Args:
            recv (str): Received content to check

        Returns:
            bool: True if a pattern is matched, False otherwise
        """
        for action in self.more:
            if 'er' in action and re.search(action['er'], recv):
                if self._action(action):
                    return True
        return False

    def _checkPrompt(self) -> bool:
        """
        Check if the received content matches the prompt pattern.

        Returns:
            bool: True if prompt is matched, False otherwise
        """
        prompt = self.prompt
        if not prompt:
            return True
        if re.search(prompt, self.buffer):
            return self._stripPrompt()
        return False

    def _stripPrompt(self) -> bool:
        """
        Remove the prompt pattern from the content.

        Args:
            content (str): Content to strip

        Returns:
            bool: every True
        """
        prompt = self.prompt
        if prompt:
            self.buffer = re.sub(prompt, '', self.buffer)
        return True

    def _get_session(self):
        """Get the session of connection"""
        return self._session

    def _expect(self) -> 'str|None':
        """
        Wait for prompt or defined patterns.

        Detects connection closure, prompts, and interactive patterns.

        Returns:
            str|None: Command output in format matching the input type,
                or None if connection is closed or error occurs
        """
        start_time = time.time()
        timeout = self.timeout

        def checkTime():
            if timeout == 0:
                return True
            return (time.time() - start_time) < timeout

        while self.isConnected() and checkTime():
            try:
                recv = self._recv().decode(self.charset)
                if not recv:
                    self._debug_warning("Connection closed")
                    self.exit = 0
                    break
                self._debug_primary(recv)
                self.buffer += recv
            except:
                # self._error(2)
                break
            if self._checkPrompt() or self._checkMore(self.buffer):
                break
            if self.sleep:
                time.sleep(self.sleep)

        return self.buffer

    def isConnected(self) -> bool:
        """Check if connection is activated"""
        return bool(self._conn)

    def close(self) -> bool:
        """
        Close connection.

        Attempts to close both the channel and SSH client,
        suppressing any exceptions that might occur during closure.
        """
        try:
            if self._conn:
                self._conn.close()
                self._conn = None
                return True
        except Exception as e:
            pass
        return False

    def show(self, content):
        """
        Output the expect content in the basic format.

        Args:
            content (list|dict): The object to output
        """
        if not content:
            return
        t = type(content)
        if t in (list, tuple, set, dict):
            isDict = t == dict
            c = 0
            for i in content:
                if isDict:
                    print(f'{" "+i+" ":#^100}')
                    print(content[i])
                else:
                    print(f'{f" {c} ":-^100}')
                    print(i)
                    c += 1
        else:
            print(content)

    def _interactiveRecv(self, rlist: list = None) -> 'bool|list':
        """
        Receive terminal output and handle interactive sessions.

        Returns:
            bool|list: True if connection is closed, list otherwise
        """
        import sys
        import socket
        import select

        r, w, e = select.select(rlist, [], [])
        # r, w, e = select.select(rlist, [], [], self.timeout)

        if self._get_session() in r:
            try:
                recv = self._recv().decode(self.charset)
                if recv:
                    self.buffer += recv
                    sys.stdout.write(recv)
                    sys.stdout.flush()
            except EOFError:
                self._debug_warning("Connection closed")
                self.exit = 1
                return True
            except socket.timeout:
                pass
            except OSError:
                # Process closed the pipe
                return True
        return r

    def interactive(self):
        """
        Enter in the interactive mode.

        The user will be control of session.

        Type self.leaveInteractive value or exit of terminal to leave the interactive mode.

        After leave interactive mode, the script came back.
        """
        if not self.isConnected():
            return
        import os
        import sys
        import termios
        import tty

        # Obter os atributos do terminal
        oldtty = termios.tcgetattr(sys.stdin)
        try:
            # Configurar modo raw
            tty.setraw(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())

            self.buffer = ''
            input_buffer = ''
            rlist = [sys.stdin]
            if self._get_session():
                rlist.insert(0, self._get_session())

            while self.isConnected():
                r = self._interactiveRecv(rlist)
                if isinstance(r, list) and sys.stdin in r:
                    available = os.read(sys.stdin.fileno(), 65535)
                    if len(available) == 0:
                        break
                    input_buffer += available.decode(self.charset)
                    if self.leaveInteractive in input_buffer:
                        self._send(self.backSpc)
                        break
                    self._send(available)
                elif r == True:
                    break
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
            print()


class SSH(Main):
    """
    SSH client wrapper for executing commands and handling interactive sessions.

    Extends the Main class for prompt and pattern handling functionality while
    providing SSH connection management through the Paramiko library.
    """

    def __init__(self,
                 hostname,
                 username: str = None,
                 password: str = None,
                 port: int = 22,
                 timeout: float = 60,
                 prompt: str = None,
                 more: list = [],
                 paramiko_conf: dict = {
                     # pkey: PKey | None = None,
                     # key_filename: str | None = None,
                     # allow_agent: bool = True,
                     # look_for_keys: bool = True,
                     # compress: bool = False,
                     # sock: _SocketLike | None = None,
                     # gss_auth: bool = False,
                     # gss_kex: bool = False,
                     # gss_deleg_creds: bool = True,
                     # gss_host: str | None = None,
                     # banner_timeout: float | None = None,
                     # auth_timeout: float | None = None,
                     # channel_timeout: float | None = None,
                     # gss_trust_dns: bool = True,
                     # passphrase: str | None = None,
                     # disabled_algorithms: Mapping[str, Iterable[str]] | None = None,
                     # transport_factory: _TransportFactory | None = None,
                     # auth_strategy: AuthStrategy | None = None,
                 }
                 ):
        """
        Initialize SSH connection and setup session parameters.

        Args:
            hostname (str): Target host to connect to
            username (str, optional): SSH username. Defaults to None.
            password (str, optional): SSH password. Defaults to None.
            port (int, optional): SSH port. Defaults to 22.
            prompt (str, optional): Prompt pattern or key. Defaults to None.
            timeout (float, optional): Connection timeout. Defaults to 60.
            more (list, optional): List of interaction patterns. Defaults to [].
            paramiko_conf (dict, optional): Additional Paramiko parameters. Defaults to {}.
        """

        super().__init__()
        import paramiko

        self.prompt = prompt
        self.more = more
        self.timeout = timeout

        self._conn: paramiko.SSHClient = paramiko.SSHClient()
        """Conection SSH of collect"""

        self._session: paramiko.Channel = None
        """Session of SSH connection"""

        try:
            self._debug_info(
                f'SSH Connecting: {username}@{hostname}:{port}')
            self._conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._conn.connect(hostname=hostname,
                               port=port,
                               username=username,
                               password=password,
                               timeout=timeout,
                               **paramiko_conf)
            self._debug_info('SSH Connected')
            # print(self._conn)
            self._session = self._conn.invoke_shell()
            self._session.settimeout(self.timeout)
        except Exception as e:
            self.conn = None
            self._error(4, e)

    def isConnected(self) -> bool:
        if not self._conn or not self._session:
            return False
        return not self._session.closed

    def _set_timeout(self, value: int) -> bool:
        if self.isConnected():
            self._session.settimeout(self.timeout)
            return True
        return False

    def close(self) -> bool:
        try:
            if self._session:
                self._session.close()
            if self._conn:
                self._conn.close()
            return True
        except Exception as e:
            pass
        return False

    def _send(self, command: str):
        self._session.send(command)

    def _recv(self) -> bytes:
        return self._session.recv(65535)


class Telnet(Main):
    """
    Telnet client wrapper for executing commands and handling interactive sessions.

    Extends the Main class for prompt and pattern handling functionality while
    providing Telnet connection management through the telnetlib library.
    """

    def __init__(self,
                 hostname: str,
                 username: str = None,
                 password: str = None,
                 port: int = 23,
                 timeout: float = 60,
                 prompt: str = None,
                 more: list = []
                 ):
        """
        Initialize Telnet connection and setup session parameters.

        Args:
            hostname (str): Target host to connect to
            username (str, optional): Telnet username. Defaults to None.
            password (str, optional): Telnet password. Defaults to None.
            port (int, optional): Telnet port. Defaults to 23.
            timeout (float, optional): Connection timeout. Defaults to 10.
            prompt (str, optional): Prompt pattern or key. Defaults to None.
            more (list, optional): List of interaction patterns. Defaults to [].
        """
        super().__init__()
        import telnetlib

        self.prompt = prompt
        self.more = more
        self.timeout = timeout

        self._conn: telnetlib.Telnet = None
        """Conection Telnet of collect"""

        try:
            self._debug_info(
                f'Telnet Connecting: {username}@{hostname}:{port}')
            self._conn = telnetlib.Telnet(hostname,
                                          port,
                                          timeout)
            self._debug_info('Telnet Connected')
            self.__login(username, password)
            # Initial read to get welcome message
        except Exception as e:
            self._conn = None
            self._error(4, e)

    def __login(self, username: str, password: str) -> bool:
        """
        Handle login process for Telnet connection.

        Args:
            username (str): Telnet username
            password (str): Telnet password

        Returns:
            bool: True if successful, False otherwise
        """
        if not username:
            return True
        if self.isConnected():
            self._conn.read_until(b"login: ", self.timeout)
            self._conn.write(username.encode(self.charset) + b"\n")
            if password:
                self._conn.read_until(b"Password: ", self.timeout)
                self._conn.write(password.encode(self.charset) + b"\n")
            return True
        return False

    def _set_timeout(self, value: int) -> bool:
        """
        Set the timeout value for the Telnet connection.

        Args:
            value (int): Timeout value in seconds.

        Returns:
            bool: True if successful, False otherwise.
        """
        if self.isConnected():
            self._conn.timeout = value
            return True
        return False

    def _send(self, command: str):
        self._conn.write(command)

    def _recv(self) -> bytes:
        return self._conn.read_eager()

    def _expect(self) -> 'str|None':
        more: list = self.more
        patterns = [self.prompt]
        for pattern in more:
            if 'er' in pattern:
                patterns.append(pattern['er'])
        while self.isConnected():
            try:
                index, _, recv = self._conn.expect(patterns, self.timeout)
                if recv:
                    recv = recv.decode(self.charset)
                    self._debug_primary(recv)
                    self.buffer += recv

                if index == 0:  # Prompt match
                    self._stripPrompt()
                elif index < 0:  # Timeout
                    self._debug_warning("Connection timeout")  # TODO Check it
                    self.exit = 1  # TODO Check it
                elif not self._action(more[index-1]):  # Prompt more
                    if self.sleep:
                        time.sleep(self.sleep)
                    continue
                break
            except EOFError:
                self._debug_warning("Connection closed by remote host")
                self.exit = 1
                break
            except Exception as e:
                self._error(2, e)
                break
        return self.buffer

    def _get_session(self):
        return self._conn.get_socket()


class Socket(Main):
    """
    Socket client wrapper for executing commands and handling interactive sessions.

    Extends the Main class for prompt and pattern handling functionality while
    providing raw socket connection management through the socket library.
    """

    def __init__(self,
                 hostname: str,
                 port: int,
                 timeout: float = 10,
                 prompt: str = None,
                 more: list = []
                 ):
        """
        Initialize socket connection and setup session parameters.

        Args:
            hostname (str): Target host to connect to
            port (int): Socket port to connect to
            timeout (float, optional): Connection timeout. Defaults to 10.
            prompt (str, optional): Prompt pattern or key. Defaults to None.
            more (list, optional): List of interaction patterns. Defaults to [].
        """
        super().__init__()
        import socket

        self.prompt = prompt
        self.more = more
        self.timeout = timeout
        self._conn: socket.socket = None

        try:
            self._debug_info(f'Connecting to socket {hostname}:{port}')
            self._conn = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            )
            self._conn.settimeout(timeout)
            self._conn.connect((hostname, port))
            self._debug_info('Connected')
        except Exception as e:
            self._conn = None
            self._error(4, e)

    def _set_timeout(self, value: int) -> bool:
        """
        Set the timeout value for the socket connection.

        Args:
            value (int): Timeout value in seconds.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self._conn:
            return False
        self._conn.settimeout(value)
        return True

    def _send(self, command: str):
        self._conn.sendall(command)

    def _recv(self) -> bytes:
        return self._conn.recv(1024)

    def _get_session(self):
        return self._conn


class Serial(Main):
    """
    Serial port wrapper for executing commands and handling interactive sessions.

    Extends the Main class for prompt and pattern handling functionality while
    providing serial port communication through the pyserial library.
    """

    def __init__(self,
                 port: str,
                 baudrate: int = 9600,
                 bytesize: int = 8,
                 parity: str = 'N',
                 stopbits: float = 1,
                 timeout: float = 10,
                 prompt: str = None,
                 more: list = []
                 ):
        """
        Initialize serial port connection and setup session parameters.

        Args:
            port (str): Serial port device (e.g., '/dev/ttyS0', 'COM1')
            baudrate (int, optional): Baud rate. Defaults to 9600.
            bytesize (int, optional): Number of data bits. Defaults to 8.
            parity (str, optional): Parity check ('N', 'E', 'O', 'M', 'S'). Defaults to 'N'.
            stopbits (float, optional): Number of stop bits. Defaults to 1.
            timeout (float, optional): Read timeout. Defaults to 10.
            prompt (str, optional): Prompt pattern or key. Defaults to None.
            more (list, optional): List of interaction patterns. Defaults to [].
        """
        super().__init__()
        import serial

        self.prompt = prompt
        self.more = more
        self.timeout = timeout
        self._conn: serial.Serial = None

        try:
            self._debug_info(f'Opening serial port {port} at {baudrate} baud')
            self._conn = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=bytesize,
                parity=parity,
                stopbits=stopbits,
                timeout=timeout
            )
            self._debug_info('Serial port opened')
        except Exception as e:
            self._conn = None
            self._error(4, e)

    def isConnected(self) -> bool:
        return True if self._conn and self._conn.is_open else False

    def _set_timeout(self, value: int) -> bool:
        """
        Set the timeout value for the serial connection.

        Args:
            value (int): Timeout value in seconds.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self._conn or not self._conn.is_open:
            return False
        self._conn.timeout = value
        return True

    def _send(self, command: str):
        self._conn.write(command)
        self._conn.flush()

    def _recv(self) -> bytes:
        return self._conn.read(self._conn.in_waiting) if self._conn.in_waiting else b''

    def close(self) -> bool:
        """
        Close the serial port connection safely.

        Attempts to close the serial port,
        suppressing any exceptions that might occur during closure.
        """
        try:
            if self._conn:
                if self._conn.is_open:
                    self._conn.close()
                self._conn = None
                return True
        except Exception as e:
            pass
        return False

    def _get_session(self):
        return self._conn

    def _interactiveRecv(self, rlist: list = None) -> 'bool|list':
        """
        Receive terminal output and handle interactive sessions.

        Returns:
            bool|list: True if connection is closed, list otherwise
        """
        import sys
        import select

        rlist = [sys.stdin]
        if self._conn.in_waiting:
            # Data available from serial port
            recv = self._recv().decode(self.charset)
            if recv:
                self.buffer += recv
                sys.stdout.write(recv)
                sys.stdout.flush()

        # Check for keyboard input
        r, w, e = select.select(rlist, [], [], 0.1)
        return r


class Spawn(Main):
    """
    Process spawning wrapper for executing commands in a subprocess.

    Extends the Main class for prompt and pattern handling functionality while
    providing process control through the subprocess module, similar to Expect/TCL's spawn.
    """

    def __init__(self,
                 command: 'str|list',
                 timeout: float = 10,
                 prompt: str = None,
                 more: list = [],
                 env: dict = None,
                 cwd: str = None
                 ):
        """
        Initialize a spawned process and setup session parameters.

        Args:
            command (str|list): Command to execute as string or list of arguments
            timeout (float, optional): Command timeout. Defaults to 10.
            prompt (str, optional): Prompt pattern or key. Defaults to None.
            more (list, optional): List of interaction patterns. Defaults to [].
            env (dict, optional): Environment variables for the process. Defaults to None.
            cwd (str, optional): Working directory for the process. Defaults to None.
        """
        super().__init__()
        import subprocess
        import pty
        import os
        import io

        self.prompt = prompt
        self.more = more
        self.timeout = timeout

        self._os = os
        self._conn: io.FileIO = None
        self._process: subprocess.Popen = None
        try:
            self._debug_info(f'Spawning process: {command}')

            # Create a pseudo-terminal for interactive processes
            master, slave = pty.openpty()

            # Convert command to list if it's a string
            if isinstance(command, str):
                cmd_args = command.split()
            else:
                cmd_args = command

            # Start the process
            self._process = subprocess.Popen(
                cmd_args,
                stdin=slave,
                stdout=slave,
                stderr=slave,
                universal_newlines=False,
                env=env,
                cwd=cwd,
                start_new_session=True
            )

            # Store the master fd for communication
            self._conn = os.fdopen(master, 'wb+', buffering=0)
            self._session = master
            os.close(slave)

            self._debug_info('Process spawned')
        except Exception as e:
            self._conn = None
            self._error(4, e)

    def isConnected(self) -> bool:
        if not self._conn or self._process.poll() is not None:
            return False
        return True

    def _set_timeout(self, value: int) -> bool:
        """
        Set the timeout value for the spawned process.

        Args:
            value (int): Timeout value in seconds.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self._conn:
            return False
        # Just store the timeout value, used in _expect
        return True

    def _send(self, command: str):
        self._conn.write(command)
        # self._os.write(command)

    def _recv(self) -> bytes:
        return self._os.read(self._session, 4096)

    def close(self) -> bool:
        """
        Terminate the spawned process and close file descriptors.

        Attempts to gracefully terminate the process,
        suppressing any exceptions that might occur during closure.
        """
        try:
            if self._conn:
                self._conn.close()

            if hasattr(self, '_process') and self._process:
                # Check if process is still running
                if self._process.poll() is None:
                    # Try to terminate gracefully
                    self._process.terminate()

                    # Give it a moment to terminate
                    time.sleep(0.5)

                    # Force kill if still running
                    if self._process.poll() is None:
                        self._process.kill()

                self._process = None
            return True
        except Exception as e:
            pass
        return False
