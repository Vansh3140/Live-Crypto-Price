# Cryptocurrency Market Analysis Application

This repository contains Python scripts for fetching, analyzing, visualizing, and reporting on cryptocurrency data using the CoinGecko API. The results are also synced with Google Sheets for live updates.

## Features

1. **Data Fetching**: Retrieves data of the top 50 cryptocurrencies by market capitalization.
2. **Analysis**:
   - Identifies the top 5 cryptocurrencies by market cap.
   - Calculates the average price of the top 50 cryptocurrencies.
   - Analyzes the highest and lowest percentage price changes over the past 24 hours.
3. **Visualization**: Generates a pie chart showing the market share distribution of the top 10 cryptocurrencies.
4. **Reporting**: Creates a detailed PDF report summarizing the analysis and visualizations.
5. **Google Sheets Integration**: Updates a Google Sheet with the latest cryptocurrency data.

---

## Installation

### Prerequisites
- Python 3.8 or above
- Required Python packages (install via `pip install -r requirements.txt`):
  - `requests`
  - `pandas`
  - `matplotlib`
  - `fpdf`
  - `gspread`
  - `oauth2client`
  - `gspread-formatting`

### Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

---

## Setup

### CoinGecko API
No authentication is needed for CoinGecko API. The application fetches data from the following endpoint:
- **Endpoint**: `https://api.coingecko.com/api/v3/coins/markets`
- **Parameters**:
  - `vs_currency=usd`
  - `order=market_cap_desc`
  - `per_page=50`
  - `page=1`

### Google Sheets Integration
1. Create a Google Cloud Project and enable the Google Sheets API.
2. Generate a service account and download the credentials JSON file.
3. Replace the `CREDS_FILE` dictionary in the code with your service account credentials.
4. Share your Google Sheet with the service account email.

---

## Files

### `main.py`
This script orchestrates the entire workflow:
1. Fetches data from the CoinGecko API.
2. Analyzes and visualizes the data.
3. Updates the data on Google Sheets.
4. Generates a detailed PDF report.

### `update_sheet.py`
This module contains functions for updating Google Sheets with cryptocurrency data. It formats headers, clears the sheet, and appends new data.

### `requirements.txt`
List of all dependencies required to run the application.

---

## Usage

1. Run the main script:
   ```bash
   python main.py
   ```
2. View the results:
   - PDF Report: `Cryptocurrency_Analysis.pdf`
   - Pie Chart: Temporary file `market_share_pie_with_legend.png` (deleted after use).
   - Google Sheet: Updated with the latest data.

---

## Outputs

### PDF Report
The report includes:
- Top 5 cryptocurrencies by market cap.
- Average price of the top 50 cryptocurrencies.
- Analysis of the highest and lowest price changes in the last 24 hours.
- A market share pie chart.

### Google Sheet
Columns:
- **Cryptocurrency Name**
- **Symbol**
- **Current Price (USD)**
- **Market Capitalization (USD)**
- **24h Trading Volume (USD)**
- **Price Change (24h %)**

---

## Logging
Logs are generated at each step, making it easy to track the process and debug issues:
- INFO: Successful steps.
- ERROR: Failures during API requests or other errors.

---

## License
This project is licensed under the MIT License.

--- 

For any questions or issues, feel free to open an issue in the repository!
