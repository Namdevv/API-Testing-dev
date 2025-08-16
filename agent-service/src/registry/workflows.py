WORKFLOW_REGISTRY = {}


def register_workflow(name):
    def decorator(cls):
        WORKFLOW_REGISTRY[name] = cls
        return cls

    return decorator
