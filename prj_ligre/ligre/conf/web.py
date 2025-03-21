"""
web.json
Returns:
    web.json
    ```
    {
        "cookie": {
            "name": "project",
            "age": null,
            "domain": null,
            "path": "/",
            "secure": false,
            "httponly": false,
            "samesite": null
        }
        "log": {
            "error": {},
            "info": {
                "format": "",
                "type": []
            }
        }
        "file_upload": {
            "max_memory_size": 2621440,
            "temp_dir": null,
            "permissions": 644,
            "directory_permissions": null
        }
    }
    ```
"""

webserver: dict = {}
"""
Webserver configurations

Returns:
    web.json (part)
    ```
    "webserver": {
        ":443": {
            "bind": "",
            "port": 443,
            "https": true,
            "keyfile": "/cer/key.pem",
            "certfile": "/cer/cert.pem",
            "router": ".roter.main"
        },
        ":80": {
            "bind": "",
            "port": 80,
            "redirect": ":443"
        }
    }
    ```
"""

tr_url: list = []
"""
Regular expression to translate URLs before check permition

Returns:
    web.json (part)
    ```
    "tr_url": [
        ["^https?://","/"],
        ["#.*?$",""],
    ]
    ```
"""


class log:
    """
    Returns:
        web.json (part)
        ```
        "log": {
            "error": {
                "format": "",
                "type": []
            },
            "info": {
                "format": "",
                "type": []
            }
        }
        ```
    """
    error: dict = {}
    info: dict = {}


class file_upload:
    """
    Returns:
        web.json (part)
        ```
        "file_upload": {
            "max_memory_size": 2621440,
            "temp_dir": null,
            "permissions": 644,
            "directory_permissions": null
        }
        ```
    """
    max_size: int = 2621440
    temp_dir: 'str|None' = None
    permissions: int = 644
    directory_permissions: int = 755


class cookie:
    """
    Cookie settings

    Returns:
        web.json
        ```
        "cookie": {
            "name": "project",
            "age": null,
            "domain": null,
            "path": "/",
            "secure": false,
            "httponly": false,
            "samesite": null
        }
        ```
    """
    name: str = "project"
    age: int = 0
    domain: 'str|None' = None
    path: str = "/"
    secure: bool = False
    httponly: bool = False
    samesite: 'str|None' = None
