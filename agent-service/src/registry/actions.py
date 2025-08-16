ACTION_REGISTRY = {}


def register_action(name):
    def decorator(cls):
        ACTION_REGISTRY[name] = cls
        return cls

    return decorator
