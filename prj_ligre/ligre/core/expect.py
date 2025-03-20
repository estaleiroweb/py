import re
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

        self.welcome: str = None
        """Welcome content. It is the firts content after connection and before any command"""

        self.exit = 0
        """Exit code"""

        self.buffer: str = ''
        """Contains the full content received from the last command execution."""

        self.lf = '\n'
        """End of line used to send commands"""

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
                if self._send(command):
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
                    'exec': callable # Function to call with self as argument (optional)
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

    @abstractmethod
    def _send(self, command: str) -> bool:
        """
        Execute a single command.

        Handles different input types:
        - str: Single command execution

        Args:
            command (str): Command(s) to execute.

        Returns:
            bool: True if successful, False otherwise.
        """
        pass

    @abstractmethod
    def _expect(self) -> 'str|None':
        """
        Wait for prompt or defined patterns.

        Detects connection closure, prompts, and interactive patterns.

        Returns:
            str|None: Command output in format matching the input type, 
                or None if connection is closed or error occurs
        """
        pass

    @abstractmethod
    def _set_timeout(self, value: int) -> bool:
        """Send the timeout value to connection class"""
        pass

    @abstractmethod
    def interactive(self):
        """
        Enter in the interactive mode.

        The user will be control of session.

        Type :END: or exit of terminal to leave the interactive mode.

        After leave interactive mode, the script came back.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Close connection.

        Attempts to close both the channel and SSH client,
        suppressing any exceptions that might occur during closure.
        """
        pass

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

        self._conn = paramiko.SSHClient()
        """Conection SSH of collect"""

        self._session: paramiko.Channel = None
        """Session of SSH connection"""

        try:
            self._debug_info('Connecting')
            self._conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._conn.connect(
                hostname=hostname,
                port=port,
                username=username,
                password=password,
                timeout=timeout,
                **paramiko_conf
            )
            self._debug_info('Connected')
            # print(self._conn)
            self._session = self._conn.invoke_shell()
            self._session.settimeout(self.timeout)
        except Exception as e:
            self.conn = None
            self._error(4, e)

    def _set_timeout(self, value: int) -> bool:
        if not self._session or self._session.closed:
            return False
        self._session.settimeout(self.timeout)
        return True

    def _send(self, command: str) -> bool:
        if not self._session or self._session.closed:
            return False
        if command and type(command) == str:
            self._debug_cmd(command)
            self._session.send(command + self.lf)
        return True

    def _expect(self) -> 'str|None':
        if not self._session or self._session.closed:
            return
        self.buffer = ''
        more: list = self.more
        prompt: str = self.prompt
        while True:
            try:
                recv = self._session.recv(65535).decode(self.charset)
                if len(recv) == 0:
                    self._debug_warning("Connection closed by server")
                    self.exit = 0
                    break
                self._debug_primary(recv)
                self.buffer += recv
            except:
                # self._error(2)
                break
            if re.search(prompt, self.buffer):
                self.buffer = re.sub(
                    prompt,
                    '',
                    self.buffer)
                break
            for i in more:
                if re.search(i['er'], self.buffer):
                    if 'send' in i:
                        self._session.send(i['send'])
                    if 'exec' in i and callable(i['exec']):
                        i['exec'](self)
                    if 'exit' in i:
                        self.exit = i['exit']
                        return self.buffer
        return self.buffer

    def interactive(self):
        import os
        import sys
        import termios
        import select
        import socket
        import tty

        # Obter os atributos do terminal
        oldtty = termios.tcgetattr(sys.stdin)
        try:
            # Configurar modo raw
            tty.setraw(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())

            self.buffer = ''
            input_buffer = ''
            # Enquanto o canal estiver aberto
            while True:
                r, w, e = select.select([self._session, sys.stdin], [], [])
                if self._session in r:
                    try:
                        recv = self._session.recv(1024).decode(self.charset)
                        if len(recv) == 0:
                            self._debug_warning("Connection closed")
                            self.exit = 0
                            break
                        self.buffer += recv
                        sys.stdout.write(recv)
                        sys.stdout.flush()
                    except socket.timeout:
                        pass
                if sys.stdin in r:
                    available = os.read(sys.stdin.fileno(), 65535)
                    if len(available) == 0:
                        break
                    input_buffer += available.decode(self.charset)
                    if ":END:" in input_buffer:
                        self._session.send(('\x08'*4)+self.lf)
                        break

                    self._session.send(available)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
            print()

    def close(self):
        try:
            if self._session:
                self._session.close()
            if self._conn:
                self._conn.close()
        except Exception as e:
            pass


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
                 timeout: float = 10,
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

        try:
            self._debug_info('Connecting via Telnet')
            self._conn: telnetlib.Telnet = telnetlib.Telnet(
                hostname, port, timeout)
            self._debug_info('Connected')

            # Handle login if credentials provided
            if username:
                # Wait for username prompt
                self._conn.read_until(b"login: ", timeout)
                self._conn.write(username.encode(self.charset) + b"\n")

                if password:
                    # Wait for password prompt
                    self._conn.read_until(b"Password: ", timeout)
                    self._conn.write(password.encode(self.charset) + b"\n")

            # Initial read to get welcome message
            self._debug_info('Reading initial output')
        except Exception as e:
            self._conn = None
            self._error(4, e)

    def __del__(self):
        """
        Destructor that ensures Telnet connections are properly closed.
        """
        self.close()

    def _set_timeout(self, value: int) -> bool:
        """
        Set the timeout value for the Telnet connection.

        Args:
            value (int): Timeout value in seconds.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self._conn:
            return False
        self._conn.timeout = value
        return True

    def _send(self, command: str) -> bool:
        """
        Send a command to the Telnet session.

        Args:
            command (str): Command to send.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self._conn:
            return False
        if command and type(command) == str:
            self._debug_cmd(command)
            self._conn.write((command + self.lf).encode(self.charset))
        return True

    def _expect(self) -> 'str|None':
        """
        Wait for prompt or defined patterns on the Telnet connection.

        Detects connection closure, prompts, and interactive patterns.

        Returns:
            str|None: Command output, or None if connection is closed or error occurs
        """
        if not self._conn:
            return

        self.buffer = ''
        more = self.more
        prompt_pattern = self.prompt.encode(
            self.charset) if self.prompt else None

        import re

        try:
            # Create list of regex patterns from more handlers
            patterns = []
            for pattern in more:
                if 'er' in pattern:
                    patterns.append(pattern['er'].encode(self.charset))

            if prompt_pattern:
                patterns.append(prompt_pattern)

            # Wait for a pattern match
            index, match, data = self._conn.expect(patterns, self.timeout)

            # Process data
            if data:
                decoded_data = data.decode(self.charset)
                self._debug_primary(decoded_data)
                self.buffer += decoded_data

                # Handle more patterns
                for i, pattern in enumerate(more):
                    if i == index:  # This pattern matched
                        if 'send' in pattern:
                            self._conn.write(
                                pattern['send'].encode(self.charset))
                        if 'exec' in pattern and callable(pattern['exec']):
                            pattern['exec'](self)
                        if 'exit' in pattern:
                            self.exit = pattern['exit']
                            return self.buffer

            # Remove prompt from output if it's included
            if prompt_pattern and re.search(self.prompt, self.buffer):
                self.buffer = re.sub(self.prompt, '', self.buffer)

            return self.buffer

        except EOFError:
            self._debug_warning("Connection closed by remote host")
            self.exit = 1
            return self.buffer
        except Exception as e:
            self._error(2, e)
            return self.buffer

    def close(self):
        try:
            if self._conn:
                self._conn.close()
                self._conn = None
        except Exception as e:
            pass

    def interactive(self):
        """
        Enter in the interactive mode for Telnet.

        The user will be in control of the session.

        Type :END: or exit the terminal to leave the interactive mode.

        After leaving interactive mode, the script comes back.
        """
        import os
        import sys
        import termios
        import select
        import tty

        # Get terminal attributes
        oldtty = termios.tcgetattr(sys.stdin)
        try:
            # Configure raw mode
            tty.setraw(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())

            self.buffer = ''
            input_buffer = ''

            # While connected
            while True:
                r, w, e = select.select(
                    [self._conn.get_socket(), sys.stdin], [], [])

                if self._conn.get_socket() in r:
                    try:
                        data = self._conn.read_eager()
                        if not data:
                            continue
                        recv = data.decode(self.charset)
                        self.buffer += recv
                        sys.stdout.write(recv)
                        sys.stdout.flush()
                    except EOFError:
                        self._debug_warning("Connection closed")
                        self.exit = 1
                        break

                if sys.stdin in r:
                    available = os.read(sys.stdin.fileno(), 65535)
                    if len(available) == 0:
                        break
                    input_buffer += available.decode(self.charset)
                    if ":END:" in input_buffer:
                        # Send backspaces to remove :END: from the terminal
                        self._conn.write(
                            ('\x08'*4+self.lf).encode(self.charset))
                        break

                    self._conn.write(available)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
            print()


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

        try:
            self._debug_info(f'Connecting to socket {hostname}:{port}')
            self._conn: socket.socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            )
            self._conn.settimeout(timeout)
            self._conn.connect((hostname, port))
            self._debug_info('Connected')
        except Exception as e:
            self._conn = None
            self._error(4, e)

    def __del__(self):
        """
        Destructor that ensures socket connections are properly closed.
        """
        self.close()

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

    def _send(self, command: str) -> bool:
        """
        Send a command to the socket.

        Args:
            command (str): Command to send.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self._conn:
            return False
        if command and type(command) == str:
            self._debug_cmd(command)
            self._conn.sendall((command + self.lf).encode(self.charset))
        return True

    def _expect(self) -> 'str|None':
        """
        Wait for prompt or defined patterns on the socket connection.

        Detects connection closure, prompts, and interactive patterns.

        Returns:
            str|None: Command output, or None if connection is closed or error occurs
        """
        if not self._conn:
            return

        import re
        import socket

        self.buffer = ''
        more = self.more
        prompt = self.prompt

        while True:
            try:
                # Receive data in chunks
                chunk = self._conn.recv(4096)
                if not chunk:
                    self._debug_warning("Connection closed by server")
                    self.exit = 1
                    break

                recv = chunk.decode(self.charset)
                self._debug_primary(recv)
                self.buffer += recv

                # Check for prompt match
                if prompt and re.search(prompt, self.buffer):
                    self.buffer = re.sub(prompt, '', self.buffer)
                    break

                # Check for more patterns
                for i in more:
                    if re.search(i['er'], self.buffer):
                        if 'send' in i:
                            self._conn.sendall(i['send'].encode(self.charset))
                        if 'exec' in i and callable(i['exec']):
                            i['exec'](self)
                        if 'exit' in i:
                            self.exit = i['exit']
                            return self.buffer

            except socket.timeout:
                # Timeout might be expected behavior
                break
            except Exception as e:
                self._error(2, e)
                break

        return self.buffer

    def close(self):
        """
        Close the socket connection safely.

        Attempts to close the socket connection,
        suppressing any exceptions that might occur during closure.
        """
        try:
            if self._conn:
                self._conn.close()
                self._conn = None
        except Exception as e:
            pass

    def interactive(self):
        """
        Enter in the interactive mode for socket.

        The user will be in control of the session.

        Type :END: or exit the terminal to leave the interactive mode.

        After leaving interactive mode, the script comes back.
        """
        import os
        import sys
        import termios
        import select
        import tty

        # Get terminal attributes
        oldtty = termios.tcgetattr(sys.stdin)
        try:
            # Configure raw mode
            tty.setraw(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())

            self.buffer = ''
            input_buffer = ''

            # While connected
            while True:
                r, w, e = select.select([self._conn, sys.stdin], [], [], 0.1)

                if self._conn in r:
                    try:
                        data = self._conn.recv(1024)
                        if not data:
                            self._debug_warning("Connection closed")
                            self.exit = 1
                            break

                        recv = data.decode(self.charset)
                        self.buffer += recv
                        sys.stdout.write(recv)
                        sys.stdout.flush()
                    except Exception as e:
                        self._error(2, e)
                        break

                if sys.stdin in r:
                    available = os.read(sys.stdin.fileno(), 65535)
                    if len(available) == 0:
                        break

                    input_buffer += available.decode(self.charset)
                    if ":END:" in input_buffer:
                        # Send backspaces to remove :END: from the terminal
                        self._conn.sendall(
                            ('\x08'*4+self.lf).encode(self.charset))
                        break

                    self._conn.sendall(available)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
            print()


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
        try:
            import serial
        except ImportError:
            self._error(
                4, "pyserial library not installed. Install with 'pip install pyserial'")
            return

        self.prompt = prompt
        self.more = more
        self.timeout = timeout

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

    def __del__(self):
        """
        Destructor that ensures serial port connections are properly closed.
        """
        self.close()

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

    def _send(self, command: str) -> bool:
        """
        Send a command to the serial port.

        Args:
            command (str): Command to send.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self._conn or not self._conn.is_open:
            return False
        if command and type(command) == str:
            self._debug_cmd(command)
            self._conn.write((command + self.lf).encode(self.charset))
            self._conn.flush()
        return True

    def _expect(self) -> 'str|None':
        """
        Wait for prompt or defined patterns on the serial connection.

        Detects connection closure, prompts, and interactive patterns.

        Returns:
            str|None: Command output, or None if connection is closed or error occurs
        """
        if not self._conn or not self._conn.is_open:
            return

        import re
        import time

        self.buffer = ''
        more = self.more
        prompt = self.prompt

        start_time = time.time()
        timeout = self.timeout

        while (time.time() - start_time) < timeout:
            # Check if data is available
            if self._conn.in_waiting:
                chunk = self._conn.read(self._conn.in_waiting)
                if chunk:
                    recv = chunk.decode(self.charset)
                    self._debug_primary(recv)
                    self.buffer += recv

                    # Check for prompt match
                    if prompt and re.search(prompt, self.buffer):
                        self.buffer = re.sub(prompt, '', self.buffer)
                        break

                    # Check for more patterns
                    for i in more:
                        if re.search(i['er'], self.buffer):
                            if 'send' in i:
                                self._conn.write(
                                    i['send'].encode(self.charset))
                                self._conn.flush()
                            if 'exec' in i and callable(i['exec']):
                                i['exec'](self)
                            if 'exit' in i:
                                self.exit = i['exit']
                                return self.buffer
            else:
                # Sleep briefly to avoid CPU spinning
                time.sleep(0.01)

        return self.buffer

    def close(self):
        """
        Close the serial port connection safely.

        Attempts to close the serial port,
        suppressing any exceptions that might occur during closure.
        """
        try:
            if self._conn and self._conn.is_open:
                self._conn.close()
                self._conn = None
        except Exception as e:
            pass

    def interactive(self):
        """
        Enter in the interactive mode for serial port.

        The user will be in control of the session.

        Type :END: or exit the terminal to leave the interactive mode.

        After leaving interactive mode, the script comes back.
        """
        import os
        import sys
        import termios
        import select
        import tty

        # Get terminal attributes
        oldtty = termios.tcgetattr(sys.stdin)
        try:
            # Configure raw mode
            tty.setraw(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())

            self.buffer = ''
            input_buffer = ''

            # While connected
            while self._conn and self._conn.is_open:
                # Use select to check for input from terminal or serial port
                rlist = [sys.stdin]
                if self._conn.in_waiting:
                    # Data available from serial port
                    data = self._conn.read(self._conn.in_waiting)
                    if data:
                        recv = data.decode(self.charset)
                        self.buffer += recv
                        sys.stdout.write(recv)
                        sys.stdout.flush()

                # Check for keyboard input
                r, w, e = select.select([sys.stdin], [], [], 0.1)
                if sys.stdin in r:
                    available = os.read(sys.stdin.fileno(), 65535)
                    if len(available) == 0:
                        break

                    input_buffer += available.decode(self.charset)
                    if ":END:" in input_buffer:
                        # Send backspaces to remove :END: from the terminal
                        self._conn.write(
                            ('\x08'*4+self.lf).encode(self.charset))
                        self._conn.flush()
                        break

                    self._conn.write(available)
                    self._conn.flush()
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
            print()


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

        self.prompt = prompt
        self.more = more
        self.timeout = timeout

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
            self._process:subprocess.Popen = subprocess.Popen(
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
            self._master_fd = master
            os.close(slave)

            self._debug_info('Process spawned')
        except Exception as e:
            self._conn = None
            self._error(4, e)

    def __del__(self):
        """
        Destructor that ensures spawned processes are properly terminated.
        """
        self.close()

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

    def _send(self, command: str) -> bool:
        """
        Send a command to the spawned process.

        Args:
            command (str): Command to send.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self._conn or self._process.poll() is not None:
            return False
        if command and type(command) == str:
            self._debug_cmd(command)
            self._conn.write((command + self.lf).encode(self.charset))
        return True

    def _expect(self) -> 'str|None':
        """
        Wait for prompt or defined patterns from the spawned process.

        Detects process termination, prompts, and interactive patterns.

        Returns:
            str|None: Command output, or None if process terminated or error occurs
        """
        if not self._conn or self._process.poll() is not None:
            return

        import os
        import re
        import select
        import time

        self.buffer = ''
        more = self.more
        prompt = self.prompt

        start_time = time.time()
        timeout = self.timeout

        while (time.time() - start_time) < timeout:
            # Check if the process is still running
            if self._process.poll() is not None:
                self._debug_warning(
                    f"Process terminated with exit code {self._process.returncode}")
                self.exit = self._process.returncode
                break

            # Check for data from the process
            r, w, e = select.select([self._master_fd], [], [], 0.1)
            if self._master_fd in r:
                try:
                    chunk = os.read(self._master_fd, 4096)
                    if not chunk:
                        continue

                    recv = chunk.decode(self.charset)
                    self._debug_primary(recv)
                    self.buffer += recv

                    # Check for prompt match
                    if prompt and re.search(prompt, self.buffer):
                        self.buffer = re.sub(prompt, '', self.buffer)
                        break

                    # Check for more patterns
                    for i in more:
                        if re.search(i['er'], self.buffer):
                            if 'send' in i:
                                os.write(self._master_fd,
                                         i['send'].encode(self.charset))
                            if 'exec' in i and callable(i['exec']):
                                i['exec'](self)
                            if 'exit' in i:
                                self.exit = i['exit']
                                return self.buffer
                except OSError:
                    # Process closed the pipe
                    break

        return self.buffer

    def close(self):
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
                    import time
                    time.sleep(0.5)

                    # Force kill if still running
                    if self._process.poll() is None:
                        self._process.kill()

                self._process = None
        except Exception as e:
            pass

    def interactive(self):
        """
        Enter in the interactive mode for the spawned process.

        The user will be in control of the session.

        Type :END: or exit the terminal to leave the interactive mode.

        After leaving interactive mode, the script comes back.
        """
        import os
        import sys
        import termios
        import select
        import tty

        # Get terminal attributes
        oldtty = termios.tcgetattr(sys.stdin)
        try:
            # Configure raw mode
            tty.setraw(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())

            self.buffer = ''
            input_buffer = ''

            # While process is running
            while self._process.poll() is None:
                r, w, e = select.select(
                    [self._master_fd, sys.stdin], [], [], 0.1)

                if self._master_fd in r:
                    try:
                        data = os.read(self._master_fd, 4096)
                        if not data:
                            continue

                        recv = data.decode(self.charset)
                        self.buffer += recv
                        sys.stdout.write(recv)
                        sys.stdout.flush()
                    except OSError:
                        # Process closed the pipe
                        break

                if sys.stdin in r:
                    available = os.read(sys.stdin.fileno(), 65535)
                    if len(available) == 0:
                        break

                    input_buffer += available.decode(self.charset)
                    if ":END:" in input_buffer:
                        # Send backspaces to remove :END: from the terminal
                        os.write(self._master_fd, ('\x08'*4 +
                                 self.lf).encode(self.charset))
                        break

                    os.write(self._master_fd, available)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
            print()
