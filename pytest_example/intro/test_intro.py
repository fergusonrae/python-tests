"""Tests for file intro.py"""

import intro

def test_update_with_id():
    """Tests for update_with_id(lists: List[list], run_id: str) -> None"""
    run_id = 'run_id'

    # Test no sublists, does not fail
    lists = []
    intro.update_with_id(lists, run_id)
    assert lists == []

    # Test when multiple sublists
    lists = [['device_1', 'type'], ['device_2', 'type']]
    intro.update_with_id(lists, run_id)
    assert len(lists) == 2
    for sublist in lists:
        assert len(sublist) == 3
        assert sublist[0] == run_id
        assert sublist[-1] == 'type'