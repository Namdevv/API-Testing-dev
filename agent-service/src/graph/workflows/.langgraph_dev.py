from src.registry.actions import scan_and_register_actions
from src.registry.nodes import scan_and_register_nodes
from src.registry.tools import scan_and_register_tools
from src.registry.workflows import WORKFLOW_REGISTRY, scan_and_register_workflows

scan_and_register_tools()
scan_and_register_actions()
scan_and_register_nodes()
scan_and_register_workflows()

docs_preprocessing_workflow = WORKFLOW_REGISTRY.get("docs_preprocessing")()
docs_preprocessing_graph = docs_preprocessing_workflow.get_graph()

simple_qa_workflow = WORKFLOW_REGISTRY.get("simple_qa")()
simple_qa_graph = simple_qa_workflow.get_graph()
