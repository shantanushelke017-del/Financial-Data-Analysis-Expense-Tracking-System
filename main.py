"""
main.py
-------
Master pipeline — runs all steps in sequence:
  Step 1: Generate synthetic dataset
  Step 2: Clean & preprocess data
  Step 3: Run analysis
  Step 4: Generate charts
  Step 5: Build Excel report
  Step 6: Print business insights

Usage:
    python main.py
"""

import os, sys, time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))

DIVIDER = "─" * 60

def step(n, title):
    print(f"\n{DIVIDER}")
    print(f"  STEP {n}: {title}")
    print(DIVIDER)


def main():
    print("\n" + "="*60)
    print("  💼 FINANCIAL DATA ANALYSIS & EXPENSE TRACKING SYSTEM")
    print("  Pipeline starting …")
    print("="*60)

    t0 = time.time()

    # ── Step 1: Generate data ─────────────────────────────────────────────────
    step(1, "Generate Synthetic Dataset")
    from generate_data import RAW_PATH
    import generate_data  # runs on import? No — just import then call
    # re-run as module
    os.system(f"python {os.path.join(PROJECT_ROOT, 'scripts', 'generate_data.py')}")

    # ── Step 2: Clean data ────────────────────────────────────────────────────
    step(2, "Data Cleaning & Preprocessing")
    from data_cleaning import load_and_clean, save_clean
    df = load_and_clean()
    save_clean(df)

    # ── Step 3: Analysis ──────────────────────────────────────────────────────
    step(3, "Run Financial Analysis")
    from analysis import (monthly_spending_trend, category_analysis,
                           budget_vs_actual, scenario_analysis)
    monthly = monthly_spending_trend(df)
    cat     = category_analysis(df)
    print(f"  Monthly records    : {len(monthly)}")
    print(f"  Categories tracked : {len(cat)}")
    print(f"  Date range         : {df['Date'].min().date()} → {df['Date'].max().date()}")

    # ── Step 4: Visualizations ────────────────────────────────────────────────
    step(4, "Generate Charts (9 charts)")
    from visualizations import generate_all_charts
    generate_all_charts(df)

    # ── Step 5: Excel report ──────────────────────────────────────────────────
    step(5, "Build Excel Report")
    from excel_report import build_excel_report
    build_excel_report(df)

    # ── Step 6: Insights ──────────────────────────────────────────────────────
    step(6, "Business Insights Report")
    from insights import generate_insights, REPORT_PATH
    report = generate_insights(df)
    print(report)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  Insights saved → {REPORT_PATH}")

    # ── Done ──────────────────────────────────────────────────────────────────
    elapsed = time.time() - t0
    print(f"\n{'='*60}")
    print(f"  ✅  PIPELINE COMPLETE in {elapsed:.1f}s")
    print(f"  📁  Outputs in:  {os.path.join(PROJECT_ROOT, 'outputs')}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
