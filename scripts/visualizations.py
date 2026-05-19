"""
visualizations.py
-----------------
Generates and saves all project charts to outputs/charts/.

Run standalone:
    python scripts/visualizations.py
"""

import os, sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

sys.path.insert(0, os.path.dirname(__file__))
from data_cleaning import load_and_clean, CLEAN_PATH
from analysis import (
    monthly_spending_trend,
    category_analysis,
    budget_vs_actual,
    financial_trend,
    scenario_analysis,
)

# ── Style ─────────────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
plt.rcParams.update({
    "figure.facecolor" : "#F8F9FA",
    "axes.facecolor"   : "#FFFFFF",
    "axes.edgecolor"   : "#CCCCCC",
    "font.family"      : "DejaVu Sans",
})

CHART_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "charts")
os.makedirs(CHART_DIR, exist_ok=True)

CURRENCY = "₹"   # swap to "$" if needed


def _save(fig, name: str):
    path = os.path.join(CHART_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved → {path}")


# ══════════════════════════════════════════════════════════════════════════════
# Chart 1 – Monthly Spending Trend (line chart)
# ══════════════════════════════════════════════════════════════════════════════
def plot_monthly_trend(df):
    monthly = monthly_spending_trend(df)

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(monthly["Month"], monthly["Income"],       color="#2ECC71", lw=2.5, marker="o", ms=5, label="Income")
    ax.plot(monthly["Month"], monthly["Total_Expense"],color="#E74C3C", lw=2.5, marker="s", ms=5, label="Total Expense")
    ax.fill_between(monthly["Month"],
                    monthly["Total_Expense"], monthly["Income"],
                    alpha=0.12, color="#2ECC71", label="Savings Zone")
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator(interval=2))
    plt.xticks(rotation=30)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{CURRENCY}{x:,.0f}"))
    ax.set_title("📈 Monthly Income vs Expense Trend", fontsize=16, fontweight="bold", pad=14)
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    ax.legend()
    _save(fig, "01_monthly_trend.png")


# ══════════════════════════════════════════════════════════════════════════════
# Chart 2 – Category-wise Expense (horizontal bar)
# ══════════════════════════════════════════════════════════════════════════════
def plot_category_bar(df):
    cat = category_analysis(df).sort_values("Total_Spent")

    colors = ["#E74C3C" if "Over" in s else "#2ECC71" for s in cat["Status"]]
    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.barh(cat["Expense_Category"], cat["Total_Spent"], color=colors, edgecolor="white", height=0.6)
    ax.bar_label(bars, fmt=lambda x: f"{CURRENCY}{x:,.0f}", padding=4, fontsize=9)
    ax.set_title("🛒 Category-wise Total Expense (2023–2024)", fontsize=15, fontweight="bold")
    ax.set_xlabel("Total Amount")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{CURRENCY}{x/1000:.0f}K"))
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#2ECC71", label="Under Budget"),
                        Patch(color="#E74C3C", label="Over Budget")], loc="lower right")
    _save(fig, "02_category_bar.png")


# ══════════════════════════════════════════════════════════════════════════════
# Chart 3 – Expense Share (pie / donut)
# ══════════════════════════════════════════════════════════════════════════════
def plot_expense_pie(df):
    cat = category_analysis(df)
    palette = sns.color_palette("Set2", len(cat))

    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(
        cat["Total_Spent"],
        labels=cat["Expense_Category"],
        autopct="%1.1f%%",
        colors=palette,
        startangle=140,
        wedgeprops=dict(width=0.55, edgecolor="white"),
        pctdistance=0.78,
    )
    for t in autotexts:
        t.set_fontsize(8)
    ax.set_title("🥧 Expense Distribution by Category", fontsize=15, fontweight="bold")
    _save(fig, "03_expense_pie.png")


# ══════════════════════════════════════════════════════════════════════════════
# Chart 4 – Budget vs Actual (grouped bar, annual totals)
# ══════════════════════════════════════════════════════════════════════════════
def plot_budget_vs_actual(df):
    cat = category_analysis(df)
    x = np.arange(len(cat))
    width = 0.38

    fig, ax = plt.subplots(figsize=(14, 6))
    b1 = ax.bar(x - width/2, cat["Budget"] * 24,    width, label="Budget (24 mo)", color="#3498DB", alpha=0.85)
    b2 = ax.bar(x + width/2, cat["Total_Spent"],     width, label="Actual Spent",   color="#E74C3C", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(cat["Expense_Category"], rotation=30, ha="right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{CURRENCY}{v/1000:.0f}K"))
    ax.set_title("📊 Budget vs Actual Expense by Category", fontsize=15, fontweight="bold")
    ax.set_ylabel("Amount (2-year total)")
    ax.legend()
    _save(fig, "04_budget_vs_actual.png")


# ══════════════════════════════════════════════════════════════════════════════
# Chart 5 – Monthly Savings Rate
# ══════════════════════════════════════════════════════════════════════════════
def plot_savings_rate(df):
    monthly = monthly_spending_trend(df)
    colors  = ["#2ECC71" if r >= 0 else "#E74C3C" for r in monthly["Savings_Rate"]]

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(monthly["Month"], monthly["Savings_Rate"], color=colors, width=20, edgecolor="white")
    ax.axhline(0, color="black", lw=1.2)
    ax.axhline(monthly["Savings_Rate"].mean(), color="#F39C12", lw=1.8, ls="--", label=f"Avg: {monthly['Savings_Rate'].mean():.1f}%")
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator(interval=2))
    plt.xticks(rotation=30)
    ax.set_title("💰 Monthly Savings Rate (%)", fontsize=15, fontweight="bold")
    ax.set_ylabel("Savings Rate (%)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.legend()
    _save(fig, "05_savings_rate.png")


# ══════════════════════════════════════════════════════════════════════════════
# Chart 6 – Heatmap: Category spend by Month
# ══════════════════════════════════════════════════════════════════════════════
def plot_heatmap(df):
    pivot = df.pivot_table(values="Amount", index="Expense_Category",
                           columns="Month_Name", aggfunc="sum", fill_value=0)
    # Order months Jan→Dec
    month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    pivot = pivot[[m for m in month_order if m in pivot.columns]]

    fig, ax = plt.subplots(figsize=(16, 7))
    sns.heatmap(pivot, ax=ax, cmap="YlOrRd", fmt=".0f",
                annot=True, annot_kws={"size": 7.5},
                linewidths=0.4, cbar_kws={"label": f"Amount ({CURRENCY})"})
    ax.set_title("🔥 Expense Heatmap: Category × Month", fontsize=15, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Category")
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    _save(fig, "06_heatmap.png")


# ══════════════════════════════════════════════════════════════════════════════
# Chart 7 – Payment Method Distribution
# ══════════════════════════════════════════════════════════════════════════════
def plot_payment_method(df):
    pm = df.groupby("Payment_Method")["Amount"].sum().sort_values(ascending=False)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    palette = sns.color_palette("pastel", len(pm))

    # Bar
    ax1.bar(pm.index, pm.values, color=palette, edgecolor="white")
    ax1.set_title("Total Spend by Payment Method", fontweight="bold")
    ax1.set_ylabel(f"Amount ({CURRENCY})")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v/1000:.0f}K"))
    plt.setp(ax1.get_xticklabels(), rotation=20)

    # Pie
    ax2.pie(pm.values, labels=pm.index, autopct="%1.1f%%",
            colors=palette, startangle=90,
            wedgeprops=dict(edgecolor="white"))
    ax2.set_title("Share by Payment Method", fontweight="bold")
    fig.suptitle("💳 Payment Method Analysis", fontsize=15, fontweight="bold")
    _save(fig, "07_payment_method.png")


# ══════════════════════════════════════════════════════════════════════════════
# Chart 8 – Scenario / What-If Analysis
# ══════════════════════════════════════════════════════════════════════════════
def plot_scenario(df):
    scenarios = [
        ("Baseline",        scenario_analysis(df,  0,   0)),
        ("+10% Salary",     scenario_analysis(df, 10,   0)),
        ("+20% Salary",     scenario_analysis(df, 20,   0)),
        ("+15% Expenses",   scenario_analysis(df,  0,  15)),
        ("+10% Sal\n+10% Exp", scenario_analysis(df, 10, 10)),
    ]

    labels   = [s[0] for s in scenarios]
    savings  = [s[1]["scenario"]["new_savings"]      if "new_savings" in s[1]["scenario"]
                else s[1]["baseline"]["avg_monthly_savings"]
                for s in scenarios]

    # Use baseline for the first entry
    savings[0] = scenarios[0][1]["baseline"]["avg_monthly_savings"]
    rates    = [s[1]["scenario"].get("new_savings_rate",
                s[1]["baseline"]["savings_rate_pct"]) for s in scenarios]
    rates[0] = scenarios[0][1]["baseline"]["savings_rate_pct"]

    colors = ["#3498DB" if s >= savings[0] else "#E74C3C" for s in savings]
    colors[0] = "#95A5A6"

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.bar(labels, savings, color=colors, edgecolor="white")
    ax1.set_title("Monthly Savings", fontweight="bold")
    ax1.set_ylabel(f"Avg Monthly Savings ({CURRENCY})")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{CURRENCY}{v:,.0f}"))
    plt.setp(ax1.get_xticklabels(), rotation=15)

    ax2.bar(labels, rates, color=colors, edgecolor="white")
    ax2.set_title("Savings Rate (%)", fontweight="bold")
    ax2.set_ylabel("Savings Rate (%)")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.1f}%"))
    plt.setp(ax2.get_xticklabels(), rotation=15)

    fig.suptitle("🔮 What-If Scenario Analysis", fontsize=15, fontweight="bold")
    _save(fig, "08_scenario_analysis.png")


# ══════════════════════════════════════════════════════════════════════════════
# Chart 9 – Quarterly Financial Trend
# ══════════════════════════════════════════════════════════════════════════════
def plot_quarterly_trend(df):
    qt = financial_trend(df)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(qt["Period"], qt["Avg_Income"],     marker="o", lw=2.5, color="#2ECC71", label="Avg Income")
    ax.plot(qt["Period"], qt["Total_Expense"],  marker="s", lw=2.5, color="#E74C3C", label="Total Expense")
    ax.plot(qt["Period"], qt["Savings"],        marker="^", lw=2.5, color="#3498DB", label="Net Savings")
    ax.plot(qt["Period"], qt["Rolling_Exp"],    ls="--", lw=1.5,  color="#F39C12",  label="2-Qtr Rolling Exp")
    ax.fill_between(qt["Period"], qt["Savings"], alpha=0.10, color="#3498DB")
    plt.xticks(rotation=30)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{CURRENCY}{v:,.0f}"))
    ax.set_title("📉 Quarterly Financial Trend", fontsize=15, fontweight="bold")
    ax.set_ylabel("Amount")
    ax.legend()
    _save(fig, "09_quarterly_trend.png")


# ── main ──────────────────────────────────────────────────────────────────────
def generate_all_charts(df: pd.DataFrame = None):
    if df is None:
        if os.path.exists(CLEAN_PATH):
            df = pd.read_csv(CLEAN_PATH, parse_dates=["Date"])
        else:
            df = load_and_clean()

    print("Generating charts …")
    import matplotlib.dates        # needed inside plot functions

    plot_monthly_trend(df)
    plot_category_bar(df)
    plot_expense_pie(df)
    plot_budget_vs_actual(df)
    plot_savings_rate(df)
    plot_heatmap(df)
    plot_payment_method(df)
    plot_scenario(df)
    plot_quarterly_trend(df)
    print("✅  All 9 charts saved to outputs/charts/")


if __name__ == "__main__":
    generate_all_charts()
