# Interactive Executive Sales Dashboard

A beginner-friendly interactive dashboard built with **Python, Streamlit, Pandas, and Plotly**. It presents sales KPIs, monthly trends, and performance comparisons with filters for date, region, product category, customer segment, and sales channel.

> **Dataset note:** `data/retail_sales.csv` is a synthetic dataset generated for educational and portfolio demonstration. It is not real company data.

## Dashboard features

- KPI cards for total sales, total profit, orders, units sold, and profit margin
- Average order value and filtered record count
- Monthly sales and profit trend line charts
- Horizontal bar charts for sales by category and region
- Interactive sidebar filters
- Filtered order details table
- Download filtered data as CSV
- Basic duplicate removal and missing-value handling

## Tech stack

- Python
- Streamlit
- Pandas
- Plotly

## Run the dashboard locally

### 1. Install Python

Install Python 3.10 or newer from [python.org](https://www.python.org/downloads/).

During installation on Windows, select **Add Python to PATH** if the installer offers that option.

### 2. Download or clone this repository

If you have Git installed, open a terminal and run:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd interactive-executive-sales-dashboard
```

Alternatively, download the repository as a ZIP from GitHub and extract it.

### 3. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

### 4. Install the packages

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Launch the app

```bash
streamlit run app.py
```

Streamlit will show a local address, usually `http://localhost:8501`. Open it in your browser.

To stop the dashboard, return to the terminal and press `Ctrl+C`.

## Project structure

```text
interactive-executive-sales-dashboard/
├── app.py
├── data/
│   └── retail_sales.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## Metrics and definitions

- **Sales:** unit price × quantity × (1 − discount), in USD.
- **Profit:** simulated sales minus simulated product cost.
- **Orders:** number of unique order IDs after filters.
- **Units sold:** sum of quantity after filters.
- **Profit margin:** total profit divided by total sales.
- **Average order value:** total sales divided by unique orders.

Because the dataset is synthetic, these metrics are examples for demonstrating dashboard functionality, not business findings about a real company.

## Applying the tutorial's 12 dashboard design principles

1. **Know the purpose:** focus on sales performance and support quick business review.
2. **Include only important content:** lead with five KPIs, then trends and breakdowns.
3. **Reduce visual noise:** use a clean layout and avoid decorative elements that do not explain the data.
4. **Round numbers:** KPI values are formatted for quick scanning.
5. **Choose efficient visualizations:** line charts show trends; horizontal bars compare categories and regions.
6. **Group related metrics:** sales and profit trends sit together; category and regional comparisons sit together.
7. **Be consistent:** charts share a visual style, labels, and currency formatting.
8. **Show hierarchy:** KPI cards appear near the top before detailed charts and records.
9. **Give numbers context:** date and category filters allow users to compare different slices of the data.
10. **Use clear labels:** charts identify the metric and units; the date filter states its purpose.
11. **Remember it's for people:** users can interact with filters and inspect detailed records.
12. **Keep evolving:** test the dashboard with users and improve it based on feedback.

## Suggested next improvements

- Add month-over-month percentage changes to KPI cards.
- Add a target sales value and compare actual performance with the target.
- Add automated data-quality checks and tests.
- Deploy the app so reviewers can access it without running Python locally.

## Limitations

- Data is synthetic and intended for learning.
- Profit is simulated using generated cost assumptions.
- The dashboard does not connect to a live database or external data source.
