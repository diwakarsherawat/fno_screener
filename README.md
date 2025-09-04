📈 F&O & Equity Gap Down Green Candle Screener

A Streamlit-based stock screener that identifies F&O and Equity stocks which:

Open with a Gap Down (below previous day’s close)

End the day with a Green Candle (bullish recovery pattern)

This tool helps traders quickly filter potential bullish reversal setups in Indian markets (NSE).

🚀 Features

✅ Screen F&O Stocks, Equity Stocks, or Both

✅ Adjustable Gap Down Threshold (%)

✅ Multiple scanning modes:

Quick Scan (Top 50 F&O)

Full Scan (All available stocks)

Custom Selection

✅ Interactive Data Table with sorting & gradient highlights

✅ Download results as CSV

✅ Auto-refresh every 5 minutes (optional)

✅ Clear summary metrics:

Total Matches

Avg. Gap Down %

Avg. Recovery %

Best Recovery %

🛠️ Tech Stack

Streamlit
 – Interactive web app framework

yFinance
 – Stock market data

Pandas
 – Data manipulation

Plotly
 – Interactive charts

📦 Installation

Clone this repository:

git clone https://github.com/your-username/gap-down-green-candle-screener.git
cd gap-down-green-candle-screener


Create and activate a virtual environment (recommended):

python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows


Install dependencies:

pip install -r requirements.txt

▶️ Usage

Run the Streamlit app:

streamlit run app.py


Then open the app in your browser:
👉 http://localhost:8501


⚠️ Disclaimer

This tool is for educational purposes only.
It does not provide investment advice.
Trading and investing involve substantial risk — please do your own research before making any financial decisions.
