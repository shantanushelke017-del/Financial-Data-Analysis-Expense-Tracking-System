"""
analysis.py
-----------
Core analysis module. Returns DataFrames / Series for all five features:
  1. Monthly spending trend
  2. Category-wise expense analysis
  3. Budget vs actual comparison
  4. Financial trend (income, savings)
  5. Scenario ("what-if") analysis

Run standalone:
    python scripts/analysis.py
"""

import pandas as pd
import numpy as np
import os, sys

sys.path.insert(0, os.path.dirname(__file__))
from data_cleaning import load_and_clean, CLEAN_PATH

CLEAN = CLEAN_PATH


# ── helpers ───────────────────────────────────────────────────────────────────
def _load(path: str = CLEAN) -> pd.DataFrame:
    if os.path.exists(path):
        df = pd.read_csv(path, parse_dates=["Date"])
    else:
        df = load_and_clean()
    return df


# ══════════════════════════════════════════════════════════════════════════════
# 1.  Monthly Spending Trend
# ══════════════════════════════════════════════════════════════════════════════
def monthly_spending_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a DataFrame indexed by Year-Month with columns:
    Total_Expense, Income, Savings, Savings_Rate (%)
    """
    monthly = (
        df.groupby("Month")
        .agg(
            Total_Expense=("Amount", "sum"),
            Income=("Income", "mean"),       # income is the same within a month
        )
        .reset_index()
    )
    monthly["Savings"]      = monthly["Income"] - monthly["Total_Expense"]
    monthly["Savings_Rate"] = (monthly["Savings"] / monthly["Income"] * 100).round(2)
    monthly["Month"]        = pd.to_datetime(monthly["Month"])
    monthly = monthly.sort_values("Month")
    return monthly


# ══════════════════════════════════════════════════════════════════════════════
# 2.  Category-wise Expense Analysis
# ══════════════════════════════════════════════════════════════════════════════
def category_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns category totals, averages, budget, variance, and % of total spend.
    """
    cat = (
        df.groupby("Expense_Category")
        .agg(
            Total_Spent=("Amount", "sum"),
            Avg_Monthly=("Amount", "mean"),
            Budget=("Budget", "first"),
            Transaction_Count=("Amount", "count"),
        )
        .reset_index()
    )
    cat["Pct_of_Total"]    = (cat["Total_Spent"] / cat["Total_Spent"].sum() * 100).round(2)
    cat["Budget_Variance"] = cat["Budget"] - cat["Avg_Monthly"]
    cat["Status"]          = cat["Budget_Variance"].apply(
        lambda x: "✅ Under Budget" if x >= 0 else "⚠️ Over Budget"
    )
    return cat.sort_values("Total_Spent", ascending=False).reset_index(drop=True)


# ══════════════════════════════════════════════════════════════════════════════
# 3.  Budget vs Actual Comparison
# ══════════════════════════════════════════════════════════════════════════════
def budget_vs_actual(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly budget adherence per category."""
    bva = (
        df.groupby(["Month", "Expense_Category"])
        .agg(
            Actual=("Amount", "sum"),
            Budget=("Budget", "first"),
        )
        .reset_index()
    )
    bva["Variance"]    = bva["Budget"] - bva["Actual"]
    bva["Pct_Used"]    = (bva["Actual"] / bva["Budget"] * 100).round(2)
    bva["Over_Budget"] = bva["Variance"] < 0
    return bva


# ══════════════════════════════════════════════════════════════════════════════
# 4.  Financial Trend Analysis (quarterly roll-up)
# ══════════════════════════════════════════════════════════════════════════════
def financial_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Quarterly income, expense, savings, and 3-month rolling avg expense."""
    quarterly = (
        df.groupby(["Year", "Quarter"])
        .agg(
            Total_Expense=("Amount", "sum"),
            Avg_Income=("Income", "mean"),
        )
        .reset_index()
    )
    quarterly["Savings"]       = quarterly["Avg_Income"] - quarterly["Total_Expense"]
    quarterly["Period"]        = quarterly["Year"].astype(str) + "-" + quarterly["Quarter"]
    quarterly["Rolling_Exp"]   = quarterly["Total_Expense"].rolling(2, min_periods=1).mean().round(2)
    return quarterly


# ══════════════════════════════════════════════════════════════════════════════
# 5.  Scenario / What-If Analysis
# ══════════════════════════════════════════════════════════════════════════════
def scenario_analysis(
    df: pd.DataFrame,
    salary_change_pct: float = 0.0,   # e.g. +10 for 10 % raise
    expense_change_pct: float = 0.0,  # e.g. +15 for 15 % cost increase
) -> dict:
    """
    Applies hypothetical % changes to income and/or expenses.
    Returns a dict with baseline and scenario summary statistics.
    """
    monthly = monthly_spending_trend(df)
    baseline_income  = monthly["Income"].mean()
    baseline_expense = monthly["Total_Expense"].mean()
    baseline_savings = baseline_income - baseline_expense
    baseline_rate    = baseline_savings / baseline_income * 100

    new_income  = baseline_income  * (1 + salary_change_pct  / 100)
    new_expense = baseline_expense * (1 + expense_change_pct / 100)
    new_savings = new_income - new_expense
    new_rate    = new_savings / new_income * 100 if new_income else 0

    return {
        "baseline": {
            "avg_monthly_income" : round(baseline_income, 2),
            "avg_monthly_expense": round(baseline_expense, 2),
            "avg_monthly_savings": round(baseline_savings, 2),
            "savings_rate_pct"   : round(baseline_rate, 2),
        },
        "scenario": {
            "salary_change_pct"  : salary_change_pct,
            "expense_change_pct" : expense_change_pct,
            "new_income"         : round(new_income, 2),
            "new_expense"        : round(new_expense, 2),
            "new_savings"        : round(new_savings, 2),
            "new_savings_rate"   : round(new_rate, 2),
            "impact"             : "Positive ✅" if new_savings > baseline_savings else "Negative ⚠️",
        },
    }


# ── CLI demo ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = _load()

    print("\n── 1. Monthly Spending Trend ──")
    print(monthly_spending_trend(df).to_string(index=False))

    print("\n── 2. Category Analysis ──")
    print(category_analysis(df).to_string(index=False))

    print("\n── 3. Budget vs Actual (first 12 rows) ──")
    print(budget_vs_actual(df).head(12).to_string(index=False))

    print("\n── 4. Financial Trend (Quarterly) ──")
    print(financial_trend(df).to_string(index=False))

    print("\n── 5a. Scenario: +10% salary ──")
    result = scenario_analysis(df, salary_change_pct=10)
    for section, vals in result.items():
        print(f"  [{section}]")
        for k, v in vals.items():
            print(f"    {k}: {v}")

    print("\n── 5b. Scenario: +20% expenses ──")
    result2 = scenario_analysis(df, expense_change_pct=20)
    for section, vals in result2.items():
        print(f"  [{section}]")
        for k, v in vals.items():
            print(f"    {k}: {v}")
