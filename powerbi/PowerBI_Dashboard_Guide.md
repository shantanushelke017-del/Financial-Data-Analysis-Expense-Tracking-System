# Power BI Dashboard Setup Guide
## Financial Data Analysis & Expense Tracking System

---

## Prerequisites
- Power BI Desktop (free download from microsoft.com/power-bi)
- The cleaned CSV file: `data/financial_data_clean.csv`
- OR the Excel file: `outputs/excel/Financial_Analysis_Report.xlsx`

---

## Step 1: Load Data into Power BI

1. Open **Power BI Desktop**
2. Click **Home → Get Data → Text/CSV**
3. Browse to `data/financial_data_clean.csv` → Click **Load**
4. *(Alternatively)* Use **Excel** source and load the Excel report

---

## Step 2: Data Transformation (Power Query)

Go to **Home → Transform Data** to open Power Query Editor.

### Apply these transformations:
| Column | Transformation |
|--------|---------------|
| Date | Change type → Date |
| Amount | Change type → Decimal Number |
| Income | Change type → Decimal Number |
| Budget | Change type → Whole Number |
| Year | Change type → Whole Number |
| Month_Num | Change type → Whole Number |

Click **Close & Apply** when done.

---

## Step 3: Create DAX Measures

In the **Data** pane, right-click the table → **New Measure**. 
Create each of the following:

```dax
-- 1. Total Expense
Total Expense = SUM(financial_data_clean[Amount])

-- 2. Average Monthly Expense
Avg Monthly Expense = AVERAGEX(
    VALUES(financial_data_clean[Month]),
    CALCULATE(SUM(financial_data_clean[Amount]))
)

-- 3. Total Income (monthly, not summed)
Monthly Income = AVERAGE(financial_data_clean[Income])

-- 4. Net Savings
Net Savings = [Monthly Income] - [Avg Monthly Expense]

-- 5. Savings Rate %
Savings Rate % = DIVIDE([Net Savings], [Monthly Income], 0) * 100

-- 6. Budget Utilization %
Budget Utilization % = DIVIDE(
    SUM(financial_data_clean[Amount]),
    SUM(financial_data_clean[Budget]),
    0
) * 100

-- 7. Over Budget Flag
Over Budget Count = 
COUNTROWS(
    FILTER(financial_data_clean, 
    financial_data_clean[Amount] > financial_data_clean[Budget])
)

-- 8. YoY Expense Growth
YoY Growth % = 
VAR CurrentYear = CALCULATE(SUM(financial_data_clean[Amount]), 
                             financial_data_clean[Year] = MAX(financial_data_clean[Year]))
VAR PrevYear    = CALCULATE(SUM(financial_data_clean[Amount]), 
                             financial_data_clean[Year] = MAX(financial_data_clean[Year])-1)
RETURN DIVIDE(CurrentYear - PrevYear, PrevYear, 0) * 100
```

---

## Step 4: Build the Dashboard (Page Layout)

### Page 1 – Executive Summary (KPI Cards)

**Add 5 Card Visuals** (Insert → Card):
1. Total Expense → `[Total Expense]`
2. Avg Monthly Income → `[Monthly Income]`
3. Net Savings → `[Net Savings]`
4. Savings Rate → `[Savings Rate %]` (format as %)
5. Budget Utilization → `[Budget Utilization %]` (format as %)

**Formatting Tips:**
- Background: Dark Navy (#1F4E79) or White
- Font: Segoe UI, Bold
- Add conditional formatting: Green if Savings Rate > 10%, Red if < 0%

---

### Page 2 – Monthly Trend Analysis

**Visual 1: Line Chart**
- X-axis: `Month` (sorted by Month_Num)
- Y-axis: `Total Expense`, `Monthly Income`
- Legend: Series names
- Title: "Monthly Income vs Expense Trend"

**Visual 2: Clustered Bar Chart**
- X-axis: `Month`
- Y-axis: `Net Savings`
- Conditional color: Green (positive) / Red (negative)
- Title: "Monthly Net Savings"

**Add Slicer:** Year (2023 / 2024)

---

### Page 3 – Category Analysis

**Visual 1: Donut Chart**
- Values: `Total Expense`
- Legend: `Expense_Category`
- Title: "Expense Share by Category"

**Visual 2: Horizontal Bar Chart**
- Y-axis: `Expense_Category`
- X-axis: `Total Expense`, `Budget` (clustered)
- Title: "Category: Budget vs Actual"

**Visual 3: Table**
Columns: Category | Total Spent | Budget | Variance | Status
Apply conditional formatting on Variance column.

---

### Page 4 – Budget vs Actual Heatmap

**Visual 1: Matrix Visual**
- Rows: `Expense_Category`
- Columns: `Month`
- Values: `Budget Utilization %`
- Apply color scale: Green (≤80%) → Yellow (80–100%) → Red (>100%)

**Visual 2: Gauge Chart**
- Value: `[Budget Utilization %]`
- Min: 0, Target: 100, Max: 150
- Title: "Overall Budget Utilization"

---

### Page 5 – Payment Method Analysis

**Visual 1: Pie Chart**
- Values: `Total Expense`
- Legend: `Payment_Method`

**Visual 2: Stacked Bar**
- X-axis: `Payment_Method`
- Y-axis: `Total Expense`
- Legend: `Expense_Category`

---

### Page 6 – Scenario Analysis (What-If Parameters)

**Step A: Create What-If Parameters**
1. Go to **Modeling → New Parameter**
2. Create "Salary Change %" : Min -20, Max 50, Default 0, Increment 1
3. Create "Expense Change %" : Min -20, Max 50, Default 0, Increment 1

**Step B: Create Scenario Measures**
```dax
Scenario Income = [Monthly Income] * (1 + 'Salary Change %'[Salary Change % Value] / 100)

Scenario Expense = [Avg Monthly Expense] * (1 + 'Expense Change %'[Expense Change % Value] / 100)

Scenario Savings = [Scenario Income] - [Scenario Expense]

Scenario Savings Rate = DIVIDE([Scenario Savings], [Scenario Income], 0) * 100
```

**Step C: Add Scenario Cards**
- Scenario Income, Scenario Expense, Scenario Savings, Scenario Savings Rate
- Add sliders for both What-If parameters

---

## Step 5: Add Filters & Slicers

Place these slicers on every page (use **Sync Slicers**):
- **Year** slicer (2023 / 2024)
- **Quarter** slicer (Q1 / Q2 / Q3 / Q4)
- **Expense Category** slicer (multi-select)
- **Payment Method** slicer

---

## Step 6: Theme & Formatting

Apply a consistent theme:
1. **View → Themes → Browse for themes**
2. Or manually set:
   - Primary color: `#1F4E79` (navy blue)
   - Accent: `#2ECC71` (green for positive), `#E74C3C` (red for negative)
   - Background: `#F8F9FA` (light gray)
   - Font: Segoe UI

---

## Step 7: Publish (Optional)

1. Save file as `Financial_Dashboard.pbix`
2. Click **Home → Publish**
3. Sign in with Microsoft account
4. Select your workspace → Publish
5. Access at app.powerbi.com

---

## Dashboard Screenshot Description

```
┌─────────────────────────────────────────────────────────────────┐
│  💼 FINANCIAL EXPENSE TRACKING DASHBOARD                        │
│  [Year: 2023 ✓ 2024 ✓]  [Quarter: All]  [Category: All]       │
├──────────┬──────────┬──────────┬──────────┬────────────────────┤
│ Income   │ Expense  │ Savings  │ Sav.Rate │ Budget Util.       │
│ ₹56,280  │ ₹41,778  │ ₹14,502  │  25.6%   │   88.4%           │
├──────────┴──────────┴──────────┴──────────┴────────────────────┤
│  [Monthly Trend Line Chart]    │  [Category Donut Chart]       │
│                                │                               │
├────────────────────────────────┼───────────────────────────────┤
│  [Budget vs Actual Bar Chart]  │  [Payment Method Pie]         │
│                                │                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tips for Viva / Presentation
- Mention that Power BI connects directly to Python outputs via CSV
- The What-If parameters use DAX to simulate real-time scenarios
- Explain how drill-through works (click category → see monthly breakdown)
- Highlight the use of conditional formatting for budget alerts
