def singleton(byId=False):
    instances = {}

    def decorador(cls):
        def wrapper(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            # print(instances)
            return instances[cls]
        return wrapper

    def decorador_id(cls):
        def wrapper(*args, **kwargs):
            id = args[0] if args else kwargs.get("id", '')
            k = f'{cls}#{id}'
            if k not in instances:
                instances[k] = cls(*args, **kwargs)
            # print(k)
            # print(instances)
            return instances[k]
        return wrapper
    return decorador_id if byId else decorador
