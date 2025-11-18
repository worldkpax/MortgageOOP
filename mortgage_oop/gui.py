"""Tkinter GUI for the mortgage calculator."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from mortgage_oop.mortgage_calculator import MortgageCalculator


class MortgageGUI:
    """Simple Tkinter GUI wrapper around the MortgageCalculator."""

    def __init__(self, root: tk.Tk | None = None) -> None:
        self.root = root or tk.Tk()
        self.root.title("Mortgage OOP Calculator")
        self._init_vars()
        self._build_layout()

    def _init_vars(self) -> None:
        self.principal_var = tk.StringVar(value="300000")
        self.rate_var = tk.StringVar(value="3.5")
        self.years_var = tk.StringVar(value="30")
        self.ppy_var = tk.StringVar(value="12")
        self.schedule_rows_var = tk.StringVar(value="12")
        self.summary_var = tk.StringVar(value="")

    def _build_layout(self) -> None:
        container = ttk.Frame(self.root, padding="12 12 12 12")
        container.grid(column=0, row=0, sticky="NSEW")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        fields = [
            ("Principal", self.principal_var),
            ("Annual rate (%)", self.rate_var),
            ("Term (years)", self.years_var),
            ("Payments per year", self.ppy_var),
            ("Schedule rows", self.schedule_rows_var),
        ]
        for idx, (label, var) in enumerate(fields):
            ttk.Label(container, text=label).grid(column=0, row=idx, sticky="W", pady=2)
            ttk.Entry(container, textvariable=var, width=25).grid(
                column=1,
                row=idx,
                sticky="EW",
                pady=2,
            )

        ttk.Button(container, text="Calculate", command=self._on_calculate).grid(
            column=0,
            row=len(fields),
            columnspan=2,
            pady=(10, 5),
            sticky="EW",
        )

        summary_frame = ttk.LabelFrame(container, text="Summary", padding="8 8 8 8")
        summary_frame.grid(column=0, row=len(fields) + 1, columnspan=2, sticky="NSEW")
        ttk.Label(summary_frame, textvariable=self.summary_var, justify="left").grid(
            column=0,
            row=0,
            sticky="W",
        )

        schedule_frame = ttk.LabelFrame(container, text="Amortization (preview)", padding="8 8 8 8")
        schedule_frame.grid(
            column=0,
            row=len(fields) + 2,
            columnspan=2,
            sticky="NSEW",
            pady=(10, 0),
        )

        columns = ("#", "Interest", "Principal", "Balance")
        self.schedule_tree = ttk.Treeview(
            schedule_frame,
            columns=columns,
            show="headings",
            height=8,
        )
        for col in columns:
            self.schedule_tree.heading(col, text=col)
            anchor = "center" if col == "#" else "e"
            width = 60 if col == "#" else 110
            self.schedule_tree.column(col, anchor=anchor, width=width, stretch=False)
        self.schedule_tree.grid(column=0, row=0, sticky="NSEW")
        scrollbar = ttk.Scrollbar(
            schedule_frame,
            orient="vertical",
            command=self.schedule_tree.yview,
        )
        scrollbar.grid(column=1, row=0, sticky="NS")
        self.schedule_tree.configure(yscrollcommand=scrollbar.set)

        for child in container.winfo_children():
            child.grid_configure(padx=5, pady=3)

        container.columnconfigure(1, weight=1)
        schedule_frame.columnconfigure(0, weight=1)
        schedule_frame.rowconfigure(0, weight=1)

    def _parse_float(self, value: str, label: str, positive: bool = False) -> float:
        try:
            parsed = float(value)
        except ValueError as exc:
            raise ValueError(f"{label} must be a number.") from exc
        if positive and parsed <= 0:
            raise ValueError(f"{label} must be greater than zero.")
        return parsed

    def _parse_int(self, value: str, label: str, positive: bool = False) -> int:
        try:
            parsed = int(value)
        except ValueError as exc:
            raise ValueError(f"{label} must be an integer.") from exc
        if positive and parsed <= 0:
            raise ValueError(f"{label} must be greater than zero.")
        return parsed

    def _on_calculate(self) -> None:
        try:
            principal = self._parse_float(self.principal_var.get(), "Principal", positive=True)
            rate = self._parse_float(self.rate_var.get(), "Annual rate")
            years = self._parse_int(self.years_var.get(), "Term", positive=True)
            payments_per_year = self._parse_int(
                self.ppy_var.get(),
                "Payments per year",
                positive=True,
            )
            schedule_rows = self._parse_int(
                self.schedule_rows_var.get(),
                "Schedule rows",
                positive=True,
            )
        except ValueError as exc:
            messagebox.showerror("Validation error", str(exc), parent=self.root)
            return

        try:
            calculator = MortgageCalculator(
                principal=principal,
                annual_rate=rate,
                years=years,
                payments_per_year=payments_per_year,
            )
        except ValueError as exc:
            messagebox.showerror("Mortgage error", str(exc), parent=self.root)
            return

        self._update_summary(calculator)
        self._populate_schedule(calculator, schedule_rows)

    def _update_summary(self, calculator: MortgageCalculator) -> None:
        summary = calculator.summary()
        summary_lines = [
            f"Principal:      {summary['principal']}",
            f"Annual rate:    {summary['annual_rate']}%",
            f"Term (years):   {summary['years']}",
            f"Payments/Year:  {summary['payments_per_year']}",
            f"Payment amount: {summary['payment_amount']}",
            f"Total cost:     {summary['total_cost']}",
            f"Total interest: {summary['total_interest']}",
        ]
        self.summary_var.set("\n".join(summary_lines))

    def _populate_schedule(self, calculator: MortgageCalculator, rows: int) -> None:
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)
        schedule = calculator.amortization_schedule(limit=rows)
        for entry in schedule:
            self.schedule_tree.insert(
                "",
                "end",
                values=(
                    entry.payment_number,
                    f"{entry.interest:.2f}",
                    f"{entry.principal:.2f}",
                    f"{entry.balance:.2f}",
                ),
            )

    def run(self) -> None:
        """Start the Tkinter main loop."""
        self.root.mainloop()


if __name__ == "__main__":
    MortgageGUI().run()
