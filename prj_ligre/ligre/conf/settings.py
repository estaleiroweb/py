secret = None
"""Secret key to crypt sensible data"""

debug = False
"""True only to development"""

charset = "utf-8"
"""Default charset to use"""

language = "pt_br"
"""Language of system <http://www.i18nguy.com/unicode/language-identifiers.html>"""

time_zone = "America/Chicago"
"""Local time zone <https://en.wikipedia.org/wiki/List_of_tz_zones_by_name>"""

tz = True
"""Show or not timezone"""

formats = {
    "date": "N j, Y",
    "datetime": "N j, Y, P",
    "time": "P",
    "year_month": "F Y",
    "month_day": "F j",
    "short_date": "m/d/Y",
    "short_datetime": "m/d/Y P",
    "number": {
        "separator": {
            "decimal": ".",
            "thousand": ",",
            "group": 0
        }
    },
    "week": {
        "first_day": 0
    },
    "input": {
        "date": {
            "%Y-%m-%d": "2006-10-25",
            "%m/%d/%Y": "10/25/2006",
            "%m/%d/%y": "10/25/06",
            "%b %d %Y": "Oct 25 2006",
            "%b %d, %Y": "Oct 25, 2006",
            "%d %b %Y": "25 Oct 2006",
            "%d %b, %Y": "25 Oct, 2006",
            "%B %d %Y": "October 25 2006",
            "%B %d, %Y": "October 25, 2006",
            "%d %B %Y": "25 October 2006",
            "%d %B, %Y": "25 October, 2006"
        },
        "time": {
            "%H:%M:%S": "14:30:59",
            "%H:%M:%S.%f": "14:30:59.000200",
            "%H:%M": "14:30"
        }
    }
}
"""<https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date> <https://docs.python.org/library/datetime.html#strftime-behavior>"""

contact: list[dict] = []
"""
List of contacts of project.

Returns:
    settings.json (part)
    ```json
    "contact": [
        {
            "name": "Full name",
            "e_mail": [
                "email@example.com"
            ],
            "phones": [
                "+55 31 99999-1234"
            ]
        }
    ]
    ```
"""


"""

# SETTINGS Documentation


- Cache to store session data if using the cache session backend

SESSION_CACHE_ALIAS = "default"

- Cookie name. This can be whatever you want

SESSION_COOKIE_NAME = "sessionid"

- Age of cookie, in seconds (default: 2 weeks)

SESSION_COOKIE_AGE = 60 *60* 24 *7* 2

- A string like "example.com", or None for standard domain cookie

SESSION_COOKIE_DOMAIN = None

- Whether the session cookie should be secure (https:// only)

SESSION_COOKIE_SECURE = false

- The path of the session cookie

SESSION_COOKIE_PATH = "/"

- Whether to use the HttpOnly flag

SESSION_COOKIE_HTTPONLY = True

- Whether to set the flag restricting cookie leaks on cross-site requests

- This can be "Lax", "Strict", "None", or false to disable the flag

SESSION_COOKIE_SAMESITE = "Lax"

- Whether to save the session data on every request

SESSION_SAVE_EVERY_REQUEST = false

- Whether a user"s session cookie expires when the web browser is closed

SESSION_EXPIRE_AT_BROWSER_CLOSE = false

- The module to store session data

SESSION_ENGINE = "django.contrib.sessions.backends.db"

- Directory to store session files if using the file session module. If None

- the backend will use a sensible default

SESSION_FILE_PATH = None

- class to serialize session data

SESSION_SERIALIZER = "django.contrib.sessions.serializers.JSONSerializer"

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
SECURE_HSTS_INCLUDE_SUBDOMAINS = false
SECURE_HSTS_PRELOAD = false
SECURE_HSTS_SECONDS = 0
SECURE_REDIRECT_EXEMPT = []
SECURE_REFERRER_POLICY = "same-origin"
SECURE_SSL_HOST = None
SECURE_SSL_REDIRECT = false
"""
