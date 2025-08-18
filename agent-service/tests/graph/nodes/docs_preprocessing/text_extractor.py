from src.registry.nodes import NODE_REGISTRY


def test_text_extractor_pdf_vn():
    source = "assents/test_extractor/test_vn.pdf"

    extractor = NODE_REGISTRY.get("docs_preprocessing.text_extractor")()
    result = extractor(type("State", (object,), {"data": [source], "lang": "vi"})())

    assert "Trường" in result["data"][0]


def test_text_extractor_pdf_en():
    source = "assents/test_extractor/test_en.pdf"

    extractor = NODE_REGISTRY.get("docs_preprocessing.text_extractor")()
    result = extractor(type("State", (object,), {"data": [source], "lang": "en"})())

    assert "Truong" in result["data"][0]


def test_text_extractor_via_link():
    source = "http://example.com"

    extractor = NODE_REGISTRY.get("docs_preprocessing.text_extractor")()
    result = extractor(type("State", (object,), {"data": [source], "lang": "vi"})())

    assert "Example Domain" in result["data"][0]
