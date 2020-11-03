"""Simple functions that are easy to test."""

from typing import List

def update_with_id(lists: List[list], run_id: str) -> None:
    """Add the run_id as the first element of each of the lists."""
    for sublist in lists:
        sublist.insert(0, run_id)