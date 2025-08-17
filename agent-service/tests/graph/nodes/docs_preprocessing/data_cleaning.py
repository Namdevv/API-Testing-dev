# tests/graph/nodes/docs_preprocessing/data_cleaning.py
from src.registry.nodes import NODE_REGISTRY


def test_data_cleaning_vn():
    state = type(
        "State",
        (object,),
        {"data": "Tôi là một học sinh ở trường trung học.!!!@@@", "lang": "vi"},
    )()
    data_cleaning = NODE_REGISTRY.get("docs_preprocessing.data_cleaning")()
    result = data_cleaning(state)
    assert result == {"cleaned_data": ["học sinh trường trung học"]}


def test_data_cleaning_en():
    state = type(
        "State",
        (object,),
        {"data": "I am a student at the high school.!!!@@@", "lang": "en"},
    )()
    data_cleaning = NODE_REGISTRY.get("docs_preprocessing.data_cleaning")()
    result = data_cleaning(state)
    assert result == {"cleaned_data": ["student high school"]}
