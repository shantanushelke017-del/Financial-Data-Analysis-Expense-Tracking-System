"""
data_cleaning.py
----------------
Step 1 of the pipeline: load raw CSV, clean it, and return a tidy DataFrame.

Run standalone:
    python scripts/data_cleaning.py
"""

import pandas as pd
import numpy as np
import os

RAW_PATH    = os.path.join(os.path.dirname(__file__), "..", "data", "financial_data.csv")
CLEAN_PATH  = os.path.join(os.path.dirname(__file__), "..", "data", "financial_data_clean.csv")


def load_and_clean(path: str = RAW_PATH) -> pd.DataFrame:
    """Load raw CSV, clean it, and return a tidy DataFrame."""

    # ── 1. Load ───────────────────────────────────────────────────────────────
    df = pd.read_csv(path)
    print(f"Loaded  : {len(df)} rows, {df.shape[1]} columns")
    print(f"Columns : {list(df.columns)}\n")

    # ── 2. Inspect before cleaning ────────────────────────────────────────────
    print("=== Missing values (before) ===")
    print(df.isnull().sum())
    print()

    # ── 3. Parse dates ────────────────────────────────────────────────────────
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    invalid_dates = df["Date"].isna().sum()
    if invalid_dates:
        print(f"⚠  Dropped {invalid_dates} rows with un-parseable dates.")
        df = df.dropna(subset=["Date"])

    # ── 4. Handle missing Amount  (impute with category median) ───────────────
    cat_medians = df.groupby("Expense_Category")["Amount"].transform("median")
    missing_amt = df["Amount"].isna().sum()
    df["Amount"] = df["Amount"].fillna(cat_medians).round(2)
    print(f"✔  Imputed {missing_amt} missing Amount values with category median.")

    # ── 5. Fix Payment_Method unknowns ────────────────────────────────────────
    bad_pm = (df["Payment_Method"] == "Unknown") | df["Payment_Method"].isna()
    df.loc[bad_pm, "Payment_Method"] = "Other"
    print(f"✔  Replaced {bad_pm.sum()} unknown Payment_Method entries with 'Other'.")

    # ── 6. Remove duplicates ──────────────────────────────────────────────────
    before = len(df)
    df = df.drop_duplicates()
    print(f"✔  Removed {before - len(df)} duplicate rows.")

    # ── 7. Remove negative amounts ────────────────────────────────────────────
    neg = (df["Amount"] < 0).sum()
    df = df[df["Amount"] >= 0]
    print(f"✔  Removed {neg} rows with negative Amount.")

    # ── 8. Derived columns ────────────────────────────────────────────────────
    df["Year"]          = df["Date"].dt.year
    df["Month_Num"]     = df["Date"].dt.month
    df["Month_Name"]    = df["Date"].dt.strftime("%b")
    df["Quarter"]       = df["Date"].dt.quarter.map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"})
    df["Budget_Variance"] = df["Budget"] - df["Amount"]          # positive = under budget
    df["Savings_Rate"]  = ((df["Income"] - df["Amount"]) / df["Income"] * 100).round(2)

    # ── 9. Post-clean summary ─────────────────────────────────────────────────
    print("\n=== Missing values (after) ===")
    print(df.isnull().sum())
    print(f"\nFinal dataset: {len(df)} rows, {df.shape[1]} columns")
    print(df.dtypes)

    return df


def save_clean(df: pd.DataFrame, path: str = CLEAN_PATH) -> None:
    df.to_csv(path, index=False)
    print(f"\n✅  Clean data saved → {os.path.abspath(path)}")


if __name__ == "__main__":
    df = load_and_clean()
    save_clean(df)
    print("\nSample rows:")
    print(df.head(10).to_string())
