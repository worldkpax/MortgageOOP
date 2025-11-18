"""Simple CLI for mortgage calculations."""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict

from mortgage_oop.mortgage_calculator import MortgageCalculator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Mortgage OOP calculator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch Tkinter GUI instead of CLI calculations.",
    )
    parser.add_argument("principal", type=float, nargs="?", help="Loan principal amount.")
    parser.add_argument(
        "annual_rate",
        type=float,
        nargs="?",
        help="Annual interest rate (percent).",
    )
    parser.add_argument("years", type=int, nargs="?", help="Loan term in years.")
    parser.add_argument(
        "--payments-per-year",
        type=int,
        default=12,
        help="Number of payments per year.",
    )
    parser.add_argument(
        "--schedule",
        type=int,
        default=0,
        help="Show amortization schedule limited to this many rows (0 disables).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of human friendly text.",
    )
    return parser


def format_summary(summary: Dict[str, Any]) -> str:
    if summary:
        lines = [
            "Mortgage Summary:",
            f"  Principal:        {summary['principal']}",
            f"  Annual Rate (%):  {summary['annual_rate']}",
            f"  Years:            {summary['years']}",
            f"  Payments/Year:    {summary['payments_per_year']}",
            f"  Payment Amount:   {summary['payment_amount']}",
            f"  Total Cost:       {summary['total_cost']}",
            f"  Total Interest:   {summary['total_interest']}",
        ]
        return "\n".join(lines)
    return ""


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.gui:
        from mortgage_oop.gui import MortgageGUI

        MortgageGUI().run()
        return

    missing = [
        name
        for name in ("principal", "annual_rate", "years")
        if getattr(args, name) is None
    ]
    if missing:
        parser.error("principal, annual_rate, and years are required unless --gui is used.")

    calculator = MortgageCalculator(
        principal=args.principal,
        annual_rate=args.annual_rate,
        years=args.years,
        payments_per_year=args.payments_per_year,
    )
    summary = calculator.summary()

    if args.json:
        payload: Dict[str, Any] = {"summary": summary}
        if args.schedule > 0:
            schedule = calculator.amortization_schedule(limit=args.schedule)
            payload["schedule"] = [row.as_dict() for row in schedule]
        print(json.dumps(payload, indent=2))
        return

    print(format_summary(summary))
    if args.schedule > 0:
        print("\nAmortization Schedule:")
        cols = ("#".ljust(4), "Interest".rjust(12), "Principal".rjust(12), "Balance".rjust(14))
        print("".join(cols))
        print("-" * 44)
        for row in calculator.amortization_schedule(limit=args.schedule):
            print(
                f"{row.payment_number:<4}"
                f"{row.interest:>12.2f}"
                f"{row.principal:>12.2f}"
                f"{row.balance:>14.2f}"
            )


if __name__ == "__main__":
    main()
