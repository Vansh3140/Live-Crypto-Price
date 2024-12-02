import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import logging
from update_sheet import update_google_sheet
import time

# Logging Initialization
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=logging.StreamHandler()
)

def fetch_data():
    """Fetch the top 50 cryptocurrencies from CoinGecko API."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        logging.info("Data fetched successfully")
        return pd.DataFrame(response.json())
    else:
        logging.error(f"Failed to fetch data: {response.status_code}")
        raise Exception(f"API request failed with status code {response.status_code}")

def analyze_top_cryptos(df):
    """Identify the top 5 cryptocurrencies by market cap."""
    logging.info("Identifying top 5 cryptocurrencies by market cap")
    return df.nlargest(5, 'market_cap')[['name', 'market_cap']]

def calculate_average_price(df):
    """Calculate the average price of the top 50 cryptocurrencies."""
    logging.info("Calculating average price of top 50 cryptocurrencies")
    return df['current_price'].mean()

def analyze_price_changes(df):
    """Analyze the highest and lowest 24-hour percentage price change."""
    logging.info("Analyzing highest and lowest 24-hour percentage price changes")
    highest = df.loc[df['price_change_percentage_24h'].idxmax()]
    lowest = df.loc[df['price_change_percentage_24h'].idxmin()]
    return highest, lowest

def generate_pie_chart(df):
    """Create and save a market share distribution pie chart."""
    logging.info("Generating market share pie chart")
    top_10_market_share = df.nlargest(10, 'market_cap')
    others_market_cap = df.nsmallest(len(df) - 10, 'market_cap')['market_cap'].sum()
    labels = list(top_10_market_share['name']) + ['Others']
    sizes = list(top_10_market_share['market_cap']) + [others_market_cap]
    explode = [0.1 if i == 0 else 0 for i in range(len(labels))]
    plt.figure(figsize=(16, 10))
    wedges, _, autotexts = plt.pie(
        sizes,
        autopct='%1.1f%%',
        startangle=140,
        explode=explode,
        colors=plt.cm.tab20.colors[:len(labels)],
        textprops={'fontsize': 10}
    )
    plt.legend(
        wedges, labels,
        title="Cryptocurrencies",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )
    plt.title('Market Cap Distribution (Top 10 + Others)', fontsize=16)
    chart_filename = "market_share_pie_with_legend.png"
    plt.savefig(chart_filename)
    plt.close()
    logging.info(f"Pie chart saved as '{chart_filename}'")
    return chart_filename

def generate_pdf_report(top_5, avg_price, highest, lowest, chart_filename):
    """Generate a PDF report summarizing the analysis."""
    logging.info("Generating PDF report")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, "Cryptocurrency Market Analysis", ln=True, align="C")
    pdf.ln(10)

    # Top 5 Cryptos
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, "Top 5 Cryptocurrencies by Market Cap", ln=True)
    pdf.set_font("Arial", size=10)
    for index, row in top_5.iterrows():
        pdf.cell(0, 10, f"{row['name']}: ${row['market_cap']:,}", ln=True)
    pdf.ln(5)

    # Average Price
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, "Average Price of Top 50 Cryptocurrencies", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"The average price is ${avg_price:,.2f}.", ln=True)
    pdf.ln(5)

    # Price Changes
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, "24-Hour Price Change Analysis", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Highest: {highest['name']} ({highest['price_change_percentage_24h']:.2f}%).", ln=True)
    pdf.cell(0, 10, f"Lowest: {lowest['name']} ({lowest['price_change_percentage_24h']:.2f}%).", ln=True)
    pdf.ln(5)

    # Pie Chart
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, "Market Share Distribution", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.image(chart_filename, x=10, y=None, w=190)
    pdf.output("Cryptocurrency_Analysis.pdf")
    logging.info("PDF report saved as 'Cryptocurrency_Analysis.pdf'")

def main():
    try:
        while True:
            df = fetch_data()
            update_google_sheet(df)
            top_5 = analyze_top_cryptos(df)
            avg_price = calculate_average_price(df)
            highest, lowest = analyze_price_changes(df)
            chart_filename = generate_pie_chart(df)
            generate_pdf_report(top_5, avg_price, highest, lowest, chart_filename)
    
            if os.path.exists(chart_filename):
                os.remove(chart_filename)
                logging.info(f"Temporary file '{chart_filename}' deleted.")
            times.sleep(5)
    except Exception as e:
        logging.exception(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
