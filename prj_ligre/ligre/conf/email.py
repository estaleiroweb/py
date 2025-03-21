"""
Email config

Examples:
    email.json    
    ```json
    {
        "from": {
            "name": "localhost",
            "address": "root@localhost"
        },
        "smtp": {
            "server": "smtp.localhost.com.br",
            "port": 25,
            "user": null,
            "password": null,
            "use_tls": false,
            "use_ssl": false,
            "ssl_certfile": null,
            "ssl_keyfile": null,
            "timeout": null
        }
    }
    ```
"""

from_name: str = "localhost"
"""Display name to send emails"""

from_address: str = "root@localhost"
"""E-mail adrees to send one"""

class smtp:
    """SMPT configurations"""

    server: str = "smtp.localhost.com.br"
    """Valid server address to send emails"""

    port: int = 25
    """Port of comunication of the SMPT server address"""

    user: 'str|None' = None
    """Username if exists"""

    password: 'str|None' = None
    """Password if exists user"""

    use_tls: bool = False
    """Transport Layer Security"""

    use_ssl: bool = False
    """Secure Sockets Layer"""

    ssl_certfile: 'str|None' = None
    """SSL cer file"""

    ssl_keyfile: 'str|None' = None
    """SSL key file"""

    timeout: int = 0
    """Maximum downtime"""
