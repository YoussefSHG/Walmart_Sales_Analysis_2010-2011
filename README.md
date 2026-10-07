# walmart_Sales_analysis_2010-2012

## Executive Summary

**Context & Goal:** 
This project analyzes multi-store retail performance by shifting focus from broad macroeconomic factors to actionable, internal seasonality patterns. Using historical Walmart weekly sales data from February 2010 to October 2012, the objective was to identify core revenue drivers, optimize inventory cycles, and evaluate store performance tiers.

**Key Findings:** 
* **Total Sales Analyzed:** $6.74 B across all store locations.
* **Average Weekly Sales:** $1.01 M per store.
* **Tier Performance Distribution:**
  * **Outperformers:** Accounted for 35.97% of total sales revenue.
  * **Average Performers:** Accounted for 34.55% of total sales revenue.
  * **Underperformers:** Accounted for 29.48% of total sales revenue.
* **Seasonal Drivers:** Core weekly sales experience a distinct pre-holiday surge peaking the week before Christmas followed by a major decline in sales with the exception of Thanksgiving which had a less significant surge peaking during thanksgiving week. In contrast, Python correlation analysis confirmed that external macroeconomic metrics (such as CPI, Fuel Price, and Unemployment) exhibited minimal direct correlation with short-term sales volume.

**Strategic Impact:** 
Prioritizing inventory procurement and staffing adjustments around internal seasonal demand spikes—rather than macroeconomic shifts—provides a reliable framework for reducing stockouts and optimizing labor costs during peak revenue windows.

---

## 1. Data Architecture & Setup

* **Database Engine:** MySQL (Hosted locally).
* **Data Modeling:** Transformed raw relational tables into a Star Schema (`fact_weekly_sales`, `dim_store`, `dim_date`) for enhanced DAX performance and time-series aggregation.
* **Analytics Stack:** 
  * **SQL:** Extracted, cleaned, and aggregated tier classifications and historical sales metrics.
  * **Power BI:** Built time-series dashboards featuring DAX measures for Tier Contribution %, Total Weekly Sales, and Tier-based performance tracking.
  * **Python:** Executed exploratory data analysis (EDA) and built correlation matrices to evaluate macroeconomic variables against weekly sales volume.

---

## 2. Interactive Dashboard & Key Visuals

> *Insert high-resolution screenshots or short animated GIFs of your Power BI dashboard views below.*

![Power BI Dashboard Overview](assets/dashboard_overview.png)

### Core Visual Breakdown
1. **Tier Performance Matrix:** Highlights revenue contribution across *Outperformer*, *Average*, and *Underperformer* store categories.
2. **Weekly Sales Trend (Time-Series):** Visualizes the pre-holiday volume spikes and weekly variance across departments.
3. **Correlation Heatmap (EDA):** Demonstrates weak correlation coefficients between macroeconomic metrics and weekly revenue performance.

---

## 3. Strategic Recommendations

1. **Pre-Holiday Inventory Ramp-Up:** Shift inventory allocation schedules **X weeks prior** to the identified peak seasonal windows to prevent stockouts in high-performing store tiers.
2. **Tier-Based Resource Allocation:** Reallocate marketing budget and premium supply chain bandwidth toward *Outperformer* tier stores to maximize return on investment.
3. **Labor Scheduling Optimization:** Align store staffing levels strictly with historical weekly sales volume surges rather than maintaining uniform, year-round scheduling models.
4. **Further Analysis on Tier 3 Stores:** Due to macroeconomics have no to little effect on store sales further investigation on tier 3 (Focus area underperformers) is advised to further understand the underlying factors.   

---

## 4. Technical Artifacts & Repository Navigation

All underlying scripts and data models are available in the repository:

* **Power BI Workbook:** [`Walmart_Sales_Analysis.pbix`](./Walmart_Sales_Analysis.pbix) *(Requires local MySQL connection setup)*
* **SQL Queries & Schema:** [`scripts/data_extraction_and_schema.sql`](./scripts/data_extraction_and_schema.sql)
* **Python Correlation Analysis:** [`scripts/eda_correlation.py`](./scripts/eda_correlation.py)
* **Database Setup Guide:** [`docs/database_setup.md`](./docs/database_setup.md)
