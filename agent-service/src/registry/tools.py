TOOL_REGISTRY = {}


def register_tool(name):
    def decorator(cls):
        TOOL_REGISTRY[name] = cls
        return cls

    return decorator


def scan_and_register_tools():
    from src.graph import tools  # noqa: F401
