from app.llm.parsing import extract_json_array


def test_plain_array():
    assert extract_json_array('[{"a": 1}]') == [{"a": 1}]


def test_array_wrapped_in_prose_and_fences():
    text = 'Sure, here you go:\n```json\n[{"id": 1}]\n```\nHope that helps!'
    assert extract_json_array(text) == [{"id": 1}]


def test_no_brackets_returns_empty():
    assert extract_json_array("no array here") == []


def test_malformed_json_returns_empty():
    assert extract_json_array('[{"id": }]') == []


def test_realistic_batch_preserves_order():
    text = '[{"id": 1, "category": "Health"}, {"id": 2, "category": "Transport"}]'
    result = extract_json_array(text)
    assert [item["id"] for item in result] == [1, 2]
