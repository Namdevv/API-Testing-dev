ACTION_REGISTRY = {}


def register_action(name):
    def decorator(cls):
        ACTION_REGISTRY[name] = cls
        return cls

    return decorator


def scan_and_register_actions():
    from src.graph import actions  # noqa: F401
