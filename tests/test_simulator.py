import pytest
from core.item_simulator import ItemSimulator

def test_simulate_swap_valid():
    current_res = {"fire": 75, "cold": 75, "lightning": 76, "chaos": 37}
    item_current = {"fire": 30, "cold": 20, "lightning": 25, "chaos": 0}
    item_candidate = {"fire": 30, "cold": 30, "lightning": 30, "chaos": 24}

    sim = ItemSimulator(current_res)
    new_res, valid = sim.simulate_swap(item_current, item_candidate)

    assert valid is True
    assert new_res["chaos"] >= 37
    assert new_res["fire"] >= 75
