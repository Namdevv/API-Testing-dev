# src/registry/nodes.py
NODE_REGISTRY = {}


def register_node(name):
    def decorator(cls):
        NODE_REGISTRY[name] = cls
        return cls

    return decorator


def scan_and_register_nodes():
    from src.graph import nodes  # noqa: F401
