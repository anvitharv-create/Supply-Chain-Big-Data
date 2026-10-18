# Supply Chain and Inventory Analysis Using Big Data Analytics

> A PySpark and Spark SQL pipeline for analyzing products, warehouses, suppliers, regional performance, and inventory reorder requirements, supported by an interactive Streamlit dashboard.

**Live Demo:** [Open the Streamlit Dashboard](https://supply-chain-big-data-o9gobhu445vgvrbn2wvou5.streamlit.app/)

**GitHub Repository:** [Supply-Chain-Big-Data](https://github.com/anvitharv-create/Supply-Chain-Big-Data)

## Business Problem

Supply chain operations require effective monitoring of product sales, inventory levels, supplier activity, and replenishment needs. Analyzing these areas can help identify records requiring reordering and reveal differences in product, warehouse, and regional performance.

This project uses PySpark, Spark SQL, and Streamlit to process supply chain inventory data, create analytical features, perform business-focused analysis, and present results through an interactive dashboard.

## Key Insights

- **Records requiring reorder:** 5,041 records classified as `REORDER_REQUIRED`.
- **Records with sufficient stock:** 86,209 records classified as `STOCK_SUFFICIENT`.
- **Top-revenue product:** SKU_38, with revenue of ₹1,057,641.51 and profit of ₹368,630.97.
- **Top-revenue warehouse:** WH_2, with revenue of ₹7,395,653.40.
- **Supplier with the highest order quantity:** SUP_7, with an order quantity of 239,283, an average lead time of 7.56 days, and associated profit of ₹1,547,508.63.
- **Top-revenue region:** North, with revenue of ₹8,411,171.01.

**Recommendation:** Use reorder classifications to review replenishment requirements and examine high-revenue products and regions when planning inventory allocation.

*These findings are based on the supplied synthetic dataset. The dataset contains no positive stockout events, so this project does not claim to measure actual stockout reduction.*

## Dashboard

The interactive Streamlit dashboard provides the following sections:

- **Dashboard:** Key performance indicators and an overview of supply chain data.
- **Product Analysis:** Product-level revenue and profitability.
- **Regional Analysis:** Regional revenue and performance comparisons.
- **Warehouse Analysis:** Warehouse-level performance analysis.
- **Supplier Analysis:** Supplier order quantities, lead times, and related metrics.
- **Reorder Analysis:** Inventory records grouped by reorder status.
- **Data Explorer:** Interactive exploration of processed data.

## Dashboard Screenshots

The following screenshots are stored in the repository under `screenshots/supply_chain_readme_images/`.

### Dashboard Overview

![Supply Chain Dashboard Overview](screenshots/supply_chain_readme_images/dashboard-overview.png)

### Product Analysis

![Product Analysis](screenshots/supply_chain_readme_images/product-analysis.png)

### Regional Analysis

![Regional Analysis](screenshots/supply_chain_readme_images/regional-analysis.png)

### Warehouse Analysis

![Warehouse Analysis](screenshots/supply_chain_readme_images/warehouse-analysis.png)

### Supplier Analysis

![Supplier Analysis](screenshots/supply_chain_readme_images/supplier-analysis.png)

### Reorder Analysis

![Reorder Analysis](screenshots/supply_chain_readme_images/reorder-analysis.png)

**[Explore the Live Dashboard](https://supply-chain-big-data-o9gobhu445vgvrbn2wvou5.streamlit.app/)**

## What This Project Delivers

- **Data ingestion:** Loads raw CSV data into PySpark DataFrames.
- **Data validation:** Checks missing values, duplicate records, and invalid data.
- **Feature engineering:** Creates `Revenue`, `Total_Cost`, `Profit`, `Inventory_Value`, `Demand_Variance`, `Reorder_Status`, and `Stock_Level_Category`.
- **Parquet storage:** Saves processed data in Parquet format.
- **Product analysis:** Examines product-level revenue and profitability.
- **Warehouse analysis:** Compares warehouse performance.
- **Supplier analysis:** Examines supplier order quantities, lead times, and associated metrics.
- **Regional analysis:** Compares regional revenue.
- **Reorder analysis:** Classifies inventory records according to reorder requirements.
- **Spark SQL:** Performs SQL-based analytical queries.
- **Dashboard development:** Presents analytical results through Streamlit and Plotly.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Core programming language |
| PySpark 4.2.0 | Data processing and transformation |
| Spark SQL | Analytical queries |
| Parquet | Processed data storage |
| Pandas | Dashboard data handling |
| Streamlit 1.64.0 | Interactive dashboard |
| Plotly 6.5.0 | Interactive charts |
| Git and GitHub | Version control and project hosting |

**Development environment:** Python 3.12 and Java 25.0.2 were used. Local Windows execution may require Hadoop native utilities configured for Spark.

## Dataset

- **Source:** [High-Dimensional Supply Chain Inventory Dataset – Kaggle](https://www.kaggle.com/datasets/ziya07/high-dimensional-supply-chain-inventory-dataset)
- **Raw file:** `supply_chain_dataset1.csv`
- **Records:** 91,250
- **Original columns:** 15
- **Missing values:** 0
- **Duplicate records:** 0
- **Invalid records identified during validation:** 0
- **Data type:** Synthetic supply chain and inventory data.

Key fields include `Date`, `SKU_ID`, `Warehouse_ID`, `Supplier_ID`, `Region`, `Units_Sold`, `Inventory_Level`, `Supplier_Lead_Time_Days`, `Reorder_Point`, `Order_Quantity`, `Unit_Cost`, `Unit_Price`, `Promotion_Flag`, `Stockout_Flag`, and `Demand_Forecast`.

The dataset is medium-sized. The project demonstrates a Spark-based data-processing workflow that can be adapted to larger datasets, although large-scale performance has not been benchmarked.

## Project Workflow

```text
Raw CSV Dataset
       ↓
Data Ingestion Using PySpark
       ↓
Data Validation
       ↓
Feature Engineering
       ↓
Processed Data in Parquet Format
       ↓
PySpark Analysis
       ↓
Spark SQL Analysis
       ↓
Dashboard Data Preparation
       ↓
Interactive Streamlit Dashboard
```

### Why Parquet?

Parquet is a columnar storage format that supports compression and efficient column-based data access. The project uses Parquet to store processed data for subsequent analytical operations.

## Sample Spark SQL Queries

The following examples assume that the processed dataset has been registered as a Spark SQL temporary view named `supply_chain` and contains the referenced columns.

### Records Requiring Reorder

```sql
SELECT SKU_ID,
       Warehouse_ID,
       Inventory_Level,
       Reorder_Point,
       Reorder_Status
FROM supply_chain
WHERE Reorder_Status = 'REORDER_REQUIRED'
ORDER BY Inventory_Level ASC;
```

### Supplier Performance Summary

```sql
SELECT Supplier_ID,
       SUM(Order_Quantity) AS Total_Order_Quantity,
       AVG(Supplier_Lead_Time_Days) AS Average_Lead_Time,
       SUM(Profit) AS Total_Profit
FROM supply_chain
GROUP BY Supplier_ID
ORDER BY Average_Lead_Time DESC;
```

These queries illustrate how processed data can be explored with Spark SQL. The temporary view must be registered before executing them.

## Project Structure

```text
Supply-Chain-Big-Data/
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   │   └── supply_chain_dataset1.csv
│   ├── processed/
│   │   └── supply_chain_processed/
│   └── dashboard/
├── docs/
├── notebooks/
├── output/
├── screenshots/
│   └── supply_chain_readme_images/
│       ├── dashboard-overview.png
│       ├── product-analysis.png
│       ├── regional-analysis.png
│       ├── warehouse-analysis.png
│       ├── supplier-analysis.png
│       └── reorder-analysis.png
├── sql/
│   ├── product_analysis.sql
│   ├── warehouse_analysis.sql
│   ├── supplier_analysis.sql
│   └── regional_analysis.sql
├── src/
│   ├── spark_test.py
│   ├── data_ingestion.py
│   ├── data_validation.py
│   ├── feature_engineering.py
│   ├── analytics.py
│   ├── sql_analysis.py
│   └── export_dashboard_data.py
├── requirements.txt
├── .gitignore
└── README.md
```

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/anvitharv-create/Supply-Chain-Big-Data.git
cd Supply-Chain-Big-Data
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the Processing Pipeline

From the project root, run the scripts in the order required by their input and output dependencies:

```bash
python src/spark_test.py
python src/data_ingestion.py
python src/data_validation.py
python src/feature_engineering.py
python src/analytics.py
python src/sql_analysis.py
python src/export_dashboard_data.py
```

### 6. Launch the Dashboard

```bash
streamlit run dashboard/app.py
```

Ensure Java is installed and correctly configured for PySpark. On Windows, configure any required Hadoop native utilities according to your local Spark environment.

## Limitations

- The dataset is synthetic and contains 91,250 records; it does not represent a massive production-scale dataset.
- The analysis is descriptive and does not include a trained demand forecasting model.
- `Stockout_Flag` has no positive cases, limiting analysis of actual stockout events.
- Reorder classifications depend on the rules and fields implemented in the project.
- The findings describe the supplied dataset and are not independently verified real-world business results.

## Future Improvements

- Develop and evaluate demand forecasting models.
- Add inventory optimization and automated reorder recommendations.
- Test the pipeline on larger datasets and distributed environments.
- Extend supplier reliability analysis when additional suitable data is available.
- Introduce automated data quality tests and scheduled data refreshes.

## Conclusion

This project demonstrates a supply chain analytics workflow using PySpark, Spark SQL, Parquet, and Streamlit. It transforms raw inventory data into analytical features, examines product and operational performance, identifies records requiring reordering, and presents results through an interactive dashboard.

The project provides practical experience in big data processing, data validation, feature engineering, SQL analytics, and data visualization.

## Author

**Anvitha R V**  
Final-Year Student, Information Science and Engineering

GitHub: [anvitharv-create](https://github.com/anvitharv-create)
