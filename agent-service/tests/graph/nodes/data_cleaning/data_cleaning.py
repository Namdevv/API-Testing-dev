from src.graph.nodes.data_cleaning.data_cleaning import DataCleaning


def test_data_cleaning():
    state = type(
        "State",
        (object,),
        {"data": "Tôi là một học sinh ở trường trung học.!!!@@@", "lang": "vi"},
    )()
    data_cleaning = DataCleaning()
    result = data_cleaning(state)
    assert result == {"cleaned_data": ["học sinh trường trung học"]}
