from ofks.io import read_jsonl, write_jsonl


def test_jsonl_roundtrip(tmp_path):
    path = tmp_path / "records.jsonl"
    count = write_jsonl(path, [{"b": 1, "a": "x"}, {"b": 2, "a": "y"}])

    assert count == 2
    assert read_jsonl(path) == [{"a": "x", "b": 1}, {"a": "y", "b": 2}]
