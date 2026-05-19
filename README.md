# 💼 Financial Data Analysis & Expense Tracking System

> A complete end-to-end data analytics project using **Python · Excel · Power BI**  
> Internship/Placement-ready | Beginner-friendly | Production-quality code

---

## 📌 Project Overview

This project analyzes 2 years of personal/company financial data to:
- Track monthly and category-wise spending patterns
- Compare actual expenses against budgets
- Identify seasonal financial trends
- Simulate "What-If" scenarios (salary change, expense inflation)
- Generate automated Excel reports and Power BI dashboards

---

## 🗂 Folder Structure

```
financial_analysis/
│
├── data/
│   ├── financial_data.csv            ← Raw generated dataset (240 rows)
│   └── financial_data_clean.csv      ← Cleaned & enriched dataset
│
├── scripts/
│   ├── generate_data.py              ← Synthetic dataset generator
│   ├── data_cleaning.py              ← Data cleaning & preprocessing
│   ├── analysis.py                   ← All 5 analysis features
│   ├── visualizations.py             ← 9 charts (Matplotlib + Seaborn)
│   ├── excel_report.py               ← Multi-sheet Excel report builder
│   └── insights.py                   ← Automated text insights report
│
├── outputs/
│   ├── charts/                       ← 9 saved PNG chart files
│   │   ├── 01_monthly_trend.png
│   │   ├── 02_category_bar.png
│   │   ├── 03_expense_pie.png
│   │   ├── 04_budget_vs_actual.png
│   │   ├── 05_savings_rate.png
│   │   ├── 06_heatmap.png
│   │   ├── 07_payment_method.png
│   │   ├── 08_scenario_analysis.png
│   │   └── 09_quarterly_trend.png
│   ├── excel/
│   │   └── Financial_Analysis_Report.xlsx   ← 5-sheet Excel workbook
│   └── reports/
│       └── Business_Insights.txt            ← Auto-generated text report
│
├── powerbi/
│   └── PowerBI_Dashboard_Guide.md    ← Step-by-step Power BI setup
│
├── docs/
│   └── Viva_Questions_Answers.md     ← 32 Q&A for project defence
│
├── main.py                           ← Master pipeline (run this first!)
└── README.md                         ← You are here
```

---

## ⚙️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Core programming language |
| Pandas | 2.x | Data manipulation & analysis |
| NumPy | 1.x | Numerical computations |
| Matplotlib | 3.x | Base chart library |
| Seaborn | 0.x | Statistical visualizations |
| openpyxl | 3.x | Excel file generation |
| Excel | 2016+ | Financial reporting |
| Power BI Desktop | Latest | Interactive dashboards |

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

### 2. Run the full pipeline
```bash
python main.py
```

This runs all 6 steps automatically:
1. Generate synthetic dataset → `data/financial_data.csv`
2. Clean & preprocess data → `data/financial_data_clean.csv`
3. Run analysis (all 5 features)
4. Generate 9 charts → `outputs/charts/`
5. Build Excel report → `outputs/excel/`
6. Print business insights → `outputs/reports/`

### 3. Run individual scripts
```bash
python scripts/generate_data.py     # Step 1 only
python scripts/data_cleaning.py     # Step 2 only
python scripts/analysis.py          # Step 3 only
python scripts/visualizations.py    # Step 4 only
python scripts/excel_report.py      # Step 5 only
python scripts/insights.py          # Step 6 only
```

---

## 📊 Dataset Description

| Column | Type | Description |
|--------|------|-------------|
| `Date` | Date | Transaction date |
| `Month` | String | Year-Month (e.g., 2023-01) |
| `Expense_Category` | String | One of 10 categories |
| `Amount` | Float | Expense amount (₹) |
| `Income` | Float | Monthly take-home salary (₹) |
| `Budget` | Int | Planned budget for category (₹) |
| `Payment_Method` | String | Credit Card / UPI / Cash / etc. |

**Derived columns (added during cleaning):**
`Year`, `Month_Num`, `Month_Name`, `Quarter`, `Budget_Variance`, `Savings_Rate`

---

## 📈 Key Results (2023–2024)

| Metric | Value |
|--------|-------|
| Avg Monthly Income | ₹56,280 |
| Avg Monthly Expense | ₹41,778 |
| Avg Monthly Savings | ₹14,502 |
| Savings Rate | 25.6% |
| Largest Category | Housing (28.6%) |
| Over-Budget Categories | 6 out of 10 |

---

## 🔮 Scenario Analysis Results

| Scenario | New Savings | New Savings Rate |
|----------|-------------|-----------------|
| Baseline | ₹14,502 | 25.6% |
| +10% Salary | ₹20,130 | 32.3% |
| +20% Salary | ₹25,760 | 38.0% |
| +15% Expenses | ₹8,230 | 14.6% |
| +10% Salary, +10% Expenses | ₹15,680 | 25.2% |

---

## 📋 Excel Report Sheets

| Sheet | Content |
|-------|---------|
| Raw Data | Full cleaned dataset with auto-filter |
| Monthly Summary | Income / Expense / Savings per month + line chart |
| Category Analysis | Ranked category totals, budgets, and status |
| Budget vs Actual | Month × category comparison with conditional formatting |
| Scenario Analysis | 8 what-if scenarios with color-coded impact |

---

## 🖥 Power BI Dashboard Pages

1. **Executive Summary** — KPI cards (Income, Expense, Savings, Savings Rate)
2. **Monthly Trend** — Line chart + savings bar chart with year slicer
3. **Category Analysis** — Donut chart + ranked bar chart
4. **Budget vs Actual** — Matrix heatmap + gauge chart
5. **Payment Methods** — Pie + stacked bar
6. **Scenario Analysis** — What-If sliders with live-updating metrics

---

## 📄 Resume Description

```
Financial Data Analysis & Expense Tracking System | Python · Excel · Power BI
• Built an end-to-end financial analytics pipeline processing 240+ expense records 
  across 10 categories and 2 years using Python (Pandas, NumPy, Matplotlib, Seaborn)
• Designed automated data cleaning module handling missing values (median imputation),
  duplicates, and derived feature engineering (Budget Variance, Savings Rate)
• Developed 9 publication-quality visualizations including trend lines, heatmaps, 
  and scenario comparison charts
• Created a 5-sheet Excel workbook with dynamic formulas, conditional formatting, 
  and embedded charts using openpyxl
• Built a 6-page interactive Power BI dashboard with DAX measures, What-If 
  parameter sliders, and drill-through budget heatmaps
• Generated automated business insights identifying 6 over-budget categories and 
  seasonal spending patterns, with actionable recommendations
```

---

## 📚 References

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)
- [openpyxl Documentation](https://openpyxl.readthedocs.io/)
- [Power BI DAX Reference](https://docs.microsoft.com/en-us/dax/)
- [DAX Patterns — Financial](https://www.daxpatterns.com/)

---

## 👨‍💻 Author

Built as an internship/placement project demonstrating full data analytics pipeline.  
*Feel free to fork, extend, and adapt for your own financial dataset.*
