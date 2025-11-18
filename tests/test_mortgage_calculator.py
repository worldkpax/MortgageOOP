import math

import pytest

from mortgage_oop.mortgage_calculator import MortgageCalculator


def test_payment_amount_matches_known_value():
    calc = MortgageCalculator(principal=300_000, annual_rate=3.5, years=30)
    assert math.isclose(calc.payment_amount(), 1347.13, rel_tol=1e-4, abs_tol=1e-2)


def test_total_interest_zero_rate_matches_principal_difference():
    calc = MortgageCalculator(principal=120_000, annual_rate=0.0, years=15)
    assert math.isclose(calc.payment_amount(), 666.67, abs_tol=1e-2)
    assert math.isclose(calc.total_interest(), 0.0, abs_tol=1e-6)


def test_invalid_inputs_raise_value_error():
    with pytest.raises(ValueError):
        MortgageCalculator(principal=-10, annual_rate=5, years=10)
    with pytest.raises(ValueError):
        MortgageCalculator(principal=100_000, annual_rate=-1, years=10)
    with pytest.raises(ValueError):
        MortgageCalculator(principal=100_000, annual_rate=5, years=0)
