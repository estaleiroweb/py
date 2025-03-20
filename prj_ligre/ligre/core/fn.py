
dsnConfig = 'dsn.json'


def dsn(dsn: 'str|dict') -> dict:
    """
    Load every configs of database

    Args:
        dsn (str|dict): _description_
            - context of `dsn.json` (`dsnConfig`)
            - `mariadb://usuario:senha@exemplo.com:8080/caminho/para/recurso?param1=valor1&param2=valor2&a=1&a=2#fragmento`
            - `dict` like the return below
    Returns:
        dict: 
            ```python
            {
                'scheme': str,
                'host': str,
                'port': int,
                'user': str,
                'password': str,
                'database': str,
                'query': dict,
                'params': str,
                'fragment': str,
            }
            ```
    """
    def check(cfg: dict) -> dict:
        arr = {
            'type': 'scheme',
            'db': 'database',
            'username': 'user',
            'passwd': 'password',
            'pass': 'password',
        }
        cfg = {k.lower(): v for k, v in cfg.items()}
        for i in arr:
            if i in cfg and arr[i] not in cfg:
                cfg[arr[i]] = cfg[i]
                del (arr[i])
        return cfg

    def makeDSN(cfg: dict) -> str:
        strDsn = f'{cfg['scheme']}://' if cfg['scheme'] else ''
        strDsn += f'{cfg['username']}@' if cfg['username'] else ''
        port = f':{cfg['port']}' if cfg['port'] else ''
        strDsn += f'{cfg['hostname']}{port}' if cfg['hostname'] else ''
        strDsn += cfg['path'] if cfg['path'] else ''
        return strDsn

    if isinstance(dsn, str):
        if '://' in dsn:
            from urllib.parse import urlparse, parse_qs
            u = urlparse(dsn)
            cfg = {
                'scheme': u.scheme,
                'host': u.hostname,
                'port': u.port,
                'user': u.username,
                'password': u.password,
                'database': u.path.replace('/', '.').strip('.'),
                'query': simplify_lists(parse_qs(u.query)),
                'params': u.params,
                'fragment': u.fragment,
            }
            cfg['dsn'] = makeDSN(cfg)
        else:
            from ..core.conf import Conf
            obj = Conf(dsnConfig)
            cfg = obj()
            cfg = cfg[dsn] if isinstance(cfg, dict) and dsn in cfg else {}
            cfg['dsn'] = dsn
            return check(cfg)
    else:
        cfg = check(dsn)
        cfg['dsn'] = makeDSN(cfg)
    return cfg


def simplify_lists(data):
    """
    Transforma um dicionário onde os valores podem ser listas:
    - Se o valor for uma lista com um único elemento, substitui pelo próprio elemento
    - Se o valor for uma lista vazia, substitui por None
    - Outros valores são mantidos como estão
    - Aplica a transformação recursivamente para dicionários aninhados

    Args:
        data: Dicionário a ser transformado

    Returns:
        Dicionário transformado
    """
    if not isinstance(data, dict):
        return data

    result = {}
    for key, value in data.items():
        # Se o valor for um dicionário, processa recursivamente
        if isinstance(value, dict):
            result[key] = simplify_lists(value)
        # Se o valor for uma lista
        elif isinstance(value, list):
            # Lista com um elemento - substitui pelo elemento
            if len(value) == 1:
                # Se o elemento for um dicionário, processa recursivamente
                if isinstance(value[0], dict):
                    result[key] = simplify_lists(value[0])
                else:
                    result[key] = value[0]
            # Lista vazia - substitui por None
            elif len(value) == 0:
                result[key] = None
            # Lista com múltiplos elementos - processa cada elemento recursivamente
            else:
                result[key] = [simplify_lists(item) if isinstance(item, dict) else item
                               for item in value]
        # Outros tipos de valor mantém como estão
        else:
            result[key] = value

    return result


def merge_recursive(value1, value2):
    """Merge two dict recursive"""
    t1, t2 = type(value1), type(value2)
    if t1 != t2 or value1 == None:
        return value2
    if t2 is dict:
        out = {}
        keys = value1.keys() | value2.keys()
        for k in keys:
            if k in value1:
                if k in value2:
                    out[k] = merge_recursive(value1[k], value2[k])
                else:
                    out[k] = value1[k]
            else:
                out[k] = value2[k]
        return out
    elif t2 is set:
        return value1 | value2
    elif t2 in (list, tuple):
        return value1 + value2
    else:
        return value2


def anonymize(content):
    """
    Anonymizes sensitive data recursively.

    Rules:
    - Primitive types (str, int, float, bool) are kept as is
    - Dictionaries have their sensitive keys anonymized based on regex patterns
    - Lists and other iterable structures are processed recursively

    Args:
        content: The content to be anonymized

    Returns:
        Anonymized content maintaining the original structure
    """
    import re

    # Regex patterns for sensitive keys
    sensitive_patterns = [
        r'pass(w(or)?d)?|senha|pwd',
        r'cpf|cnpj|ssn|tax|id',
        r'rg|identity|document',
        r'email|e-mail',
        r'phone|tel(efone)?|tel|cel(ular)?|mobile',
        r'(credit_?)?card|cart[aã]o_?cr[eé]dito|cc_|card_?number',
        r'address|endereco|location',
        r'token|api_?key|secret|jwt',
        r'passport|passaporte',
        r'account|conta',
        r'birth|data_?(nasc|birth)',
        r'security|seguran[cç]a',
        r'credentials|credenciais',
        r'certificate|certificado',
        r'private|privado'
    ]

    # Compile the regex patterns for better performance
    compiled_patterns = [re.compile(pattern, re.IGNORECASE)
                         for pattern in sensitive_patterns]

    # Helper function to check if a key is sensitive
    def is_sensitive(key):
        key_str = str(key)
        return any(pattern.search(key_str) for pattern in compiled_patterns)

    # Function to process recursively
    def process(data):
        # Primitive types return as is
        if isinstance(data, (str, int, float, bool, type(None))):
            return data

        # Dictionaries
        elif isinstance(data, dict):
            result = {}
            for key, value in data.items():
                # If it's a sensitive key, anonymize the value
                if is_sensitive(key):
                    if isinstance(value, str):
                        result[key] = "********"
                    elif isinstance(value, (int, float)):
                        result[key] = 0
                    elif isinstance(value, bool):
                        result[key] = False
                    else:
                        # For complex types (lists, dictionaries, etc.)
                        result[key] = process(value)
                else:
                    # Process recursively for non-sensitive values
                    result[key] = process(value)
            return result

        # Lists and tuples
        elif isinstance(data, (list, tuple)):
            result = [process(item) for item in data]
            # Keep the same type (list or tuple)
            return type(data)(result)

        # Sets
        elif isinstance(data, set):
            return {process(item) for item in data}

        # For other types, return as is
        else:
            return data

    return process(content)
