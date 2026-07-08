import pytest

from ofks.workflows.combine_records import combine_record_sets


def test_combine_record_sets_preserves_order():
    combined = combine_record_sets(
        [
            [{"structure_id": "a", "value": 1}],
            [{"structure_id": "b", "value": 2}],
        ]
    )

    assert [record["structure_id"] for record in combined] == ["a", "b"]


def test_combine_record_sets_rejects_duplicate_ids():
    with pytest.raises(ValueError, match="Duplicate structure_id: a"):
        combine_record_sets(
            [
                [{"structure_id": "a", "value": 1}],
                [{"structure_id": "a", "value": 2}],
            ]
        )
