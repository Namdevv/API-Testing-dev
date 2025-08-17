from src.registry.nodes import NODE_REGISTRY


def test_text_extractor_vn():
    source = "assents/test_extractor/test_vn.pdf"

    extractor = NODE_REGISTRY.get("docs_preprocessing.text_extractor")()
    result = extractor(type("State", (object,), {"data": source, "lang": "vi"})())

    assert "Trường" in result["messages"][0]


def test_text_extractor_en():
    source = "assents/test_extractor/test_en.pdf"

    extractor = NODE_REGISTRY.get("docs_preprocessing.text_extractor")()
    result = extractor(type("State", (object,), {"data": source, "lang": "en"})())

    assert "Truong" in result["messages"][0]
