WORKFLOW_REGISTRY = {}


def register_workflow(name):
    def decorator(cls):
        WORKFLOW_REGISTRY[name] = cls
        return cls

    return decorator


def scan_and_register_workflows():
    from src.graph import workflows  # noqa: F401
