from src.graph.workflows.docs_preprocessing import DocsPreprocessingWorkflow
from src.registry.nodes import NODE_REGISTRY, scan_and_register_nodes

scan_and_register_nodes()
agent = DocsPreprocessingWorkflow(
    collection_name="test",
    llm_temperature=0.1,
)
graph = agent.get_graph()
print("Graph initialized:", graph is not None)
