docs_preprocessing_workflow = WORKFLOW_REGISTRY.get("docs_preprocessing")()
docs_preprocessing_graph = docs_preprocessing_workflow.get_graph()

simple_qa_workflow = WORKFLOW_REGISTRY.get("simple_qa")()
simple_qa_graph = simple_qa_workflow.get_graph()
