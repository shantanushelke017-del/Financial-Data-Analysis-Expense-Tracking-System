"""
generate_data.py
----------------
Generates a realistic 2-year financial dataset and saves it to
data/financial_data.csv
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)

# ── Configuration ─────────────────────────────────────────────────────────────
START_DATE   = "2023-01-01"
END_DATE     = "2024-12-31"
MONTHLY_INC  = 55_000          # monthly take-home salary (₹)

CATEGORIES = {
    "Housing"      : {"mean": 12_000, "std": 500,   "budget": 12_500},
    "Food"         : {"mean":  6_500, "std": 1_000,  "budget":  6_000},
    "Transport"    : {"mean":  3_200, "std": 600,   "budget":  3_000},
    "Healthcare"   : {"mean":  1_800, "std": 800,   "budget":  2_000},
    "Entertainment": {"mean":  2_500, "std": 700,   "budget":  2_000},
    "Education"    : {"mean":  2_000, "std": 400,   "budget":  2_500},
    "Shopping"     : {"mean":  4_000, "std": 1_200,  "budget":  3_500},
    "Utilities"    : {"mean":  2_200, "std": 300,   "budget":  2_000},
    "Savings"      : {"mean":  5_000, "std": 800,   "budget":  6_000},
    "Miscellaneous": {"mean":  1_500, "std": 500,   "budget":  1_500},
}

PAYMENT_METHODS = ["Credit Card", "Debit Card", "Cash", "UPI", "Net Banking"]
PAYMENT_WEIGHTS = [0.30, 0.25, 0.15, 0.20, 0.10]

# ── Build rows ─────────────────────────────────────────────────────────────────
months = pd.date_range(START_DATE, END_DATE, freq="MS")   # month-start dates
rows = []

for month_start in months:
    month_label = month_start.strftime("%Y-%m")

    # Income: slight raise mid-2024
    if month_start >= pd.Timestamp("2024-07-01"):
        income = MONTHLY_INC * 1.10
    else:
        income = MONTHLY_INC + np.random.uniform(-500, 500)

    for category, cfg in CATEGORIES.items():
        # Seasonal bump for Food/Entertainment in summer & December
        seasonal = 1.0
        if month_start.month in [6, 7, 8, 12]:
            if category in ["Food", "Entertainment", "Shopping"]:
                seasonal = 1.15

        amount = max(0, np.random.normal(cfg["mean"] * seasonal, cfg["std"]))
        amount = round(amount, 2)

        # Random transaction date within the month
        days_in_month = (month_start + pd.offsets.MonthEnd(0)).day
        day = np.random.randint(1, days_in_month + 1)
        date = month_start.replace(day=day)

        payment = np.random.choice(PAYMENT_METHODS, p=PAYMENT_WEIGHTS)

        rows.append({
            "Date"            : date.strftime("%Y-%m-%d"),
            "Month"           : month_label,
            "Expense_Category": category,
            "Amount"          : amount,
            "Income"          : round(income, 2),
            "Budget"          : cfg["budget"],
            "Payment_Method"  : payment,
        })

df = pd.DataFrame(rows)

# Inject ~3 % missing / noisy values for data-cleaning demo
noise_idx = np.random.choice(df.index, size=int(len(df) * 0.03), replace=False)
df.loc[noise_idx[:len(noise_idx)//2], "Amount"] = np.nan
df.loc[noise_idx[len(noise_idx)//2:], "Payment_Method"] = "Unknown"

out_path = os.path.join(os.path.dirname(__file__), "..", "data", "financial_data.csv")
df.to_csv(out_path, index=False)
print(f"✅  Dataset saved → {os.path.abspath(out_path)}  ({len(df)} rows)")
