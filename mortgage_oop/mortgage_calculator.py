"""Core mortgage calculation logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class PaymentBreakdown:
    """Represents a single amortization payment."""

    payment_number: int
    interest: float
    principal: float
    balance: float

    def as_dict(self) -> Dict[str, float]:
        return {
            "payment_number": self.payment_number,
            "interest": round(self.interest, 2),
            "principal": round(self.principal, 2),
            "balance": round(self.balance, 2),
        }


class MortgageCalculator:
    """Encapsulates mortgage computations."""

    def __init__(
        self,
        principal: float,
        annual_rate: float,
        years: int,
        payments_per_year: int = 12,
    ) -> None:
        self.principal = float(principal)
        self.annual_rate = float(annual_rate)
        self.years = int(years)
        self.payments_per_year = int(payments_per_year)
        self._validate()

    def _validate(self) -> None:
        if self.principal <= 0:
            raise ValueError("Principal must be greater than zero.")
        if self.annual_rate < 0:
            raise ValueError("Annual interest rate cannot be negative.")
        if self.years <= 0:
            raise ValueError("Term in years must be greater than zero.")
        if self.payments_per_year <= 0:
            raise ValueError("Payments per year must be greater than zero.")

    @property
    def periodic_rate(self) -> float:
        return (self.annual_rate / 100.0) / self.payments_per_year

    @property
    def total_payments(self) -> int:
        return self.years * self.payments_per_year

    def payment_amount(self) -> float:
        rate = self.periodic_rate
        n = self.total_payments
        if rate == 0:
            return self.principal / n
        numerator = rate * self.principal
        denominator = 1 - (1 + rate) ** -n
        return numerator / denominator

    def total_cost(self) -> float:
        return self.payment_amount() * self.total_payments

    def total_interest(self) -> float:
        return self.total_cost() - self.principal

    def amortization_schedule(self, limit: int | None = None) -> List[PaymentBreakdown]:
        """Return amortization rows up to `limit` (defaults to full schedule)."""
        payment = self.payment_amount()
        balance = self.principal
        rate = self.periodic_rate
        schedule: List[PaymentBreakdown] = []
        max_rows = self.total_payments if limit is None else min(limit, self.total_payments)
        for number in range(1, max_rows + 1):
            interest = balance * rate
            principal_paid = payment - interest
            balance = max(balance - principal_paid, 0.0)
            schedule.append(
                PaymentBreakdown(
                    payment_number=number,
                    interest=interest,
                    principal=principal_paid,
                    balance=balance,
                )
            )
            if balance <= 0:
                break
        return schedule

    def summary(self) -> Dict[str, float]:
        """Provide a formatted summary of the mortgage."""
        return {
            "principal": round(self.principal, 2),
            "annual_rate": round(self.annual_rate, 4),
            "years": self.years,
            "payments_per_year": self.payments_per_year,
            "payment_amount": round(self.payment_amount(), 2),
            "total_cost": round(self.total_cost(), 2),
            "total_interest": round(self.total_interest(), 2),
        }
