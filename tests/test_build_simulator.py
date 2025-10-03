import pytest
from core.build_simulator import BuildSimulator

def test_build_with_one_ring():
    build = BuildSimulator()
    build.add_ring_with_chaos(chaos_cost=5)

    assert build.total_build_cost() == 5
    summary = build.summary()
    assert "Ring" in summary
    assert "TOTAL BUILD: 5c" in summary

def test_build_with_two_rings():
    build = BuildSimulator()
    build.add_ring_with_chaos(chaos_cost=5)
    build.add_ring_with_chaos(chaos_cost=7)

    assert build.total_build_cost() == 12
    summary = build.summary()
    assert "TOTAL BUILD: 12c" in summary
