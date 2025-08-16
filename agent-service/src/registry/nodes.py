NODE_REGISTRY = {}


def register_node(name):
    def decorator(cls):
        NODE_REGISTRY[name] = cls
        return cls

    return decorator
