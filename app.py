import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="F&O Gap Down Green Candle Screener",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# F&O Stock List
fno_stocks = [
    '360ONE.NS', 'AARTIIND.NS', 'ABB.NS', 'ABCAPITAL.NS', 'ABFRL.NS', 'ACC.NS', 
    'ADANIENSOL.NS', 'ADANIENT.NS', 'ADANIGREEN.NS', 'ADANIPORTS.NS', 'ALKEM.NS', 
    'AMBER.NS', 'AMBUJACEM.NS', 'ANGELONE.NS', 'APLAPOLLO.NS', 'APOLLOHOSP.NS', 
    'ASHOKLEY.NS', 'ASIANPAINT.NS', 'ASTRAL.NS', 'ATGL.NS', 'AUBANK.NS', 
    'AUROPHARMA.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 
    'BALKRISIND.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', 'BANKINDIA.NS', 'BDL.NS', 
    'BEL.NS', 'BHARATFORG.NS', 'BHARTIARTL.NS', 'BHEL.NS', 'BIOCON.NS', 
    'BLUESTARCO.NS', 'BOSCHLTD.NS', 'BPCL.NS', 'BRITANNIA.NS', 'BSE.NS', 'BSOFT.NS', 
    'CAMS.NS', 'CANBK.NS', 'CDSL.NS', 'CESC.NS', 'CGPOWER.NS', 'CHAMBLFERT.NS', 
    'CHOLAFIN.NS', 'CIPLA.NS', 'COALINDIA.NS', 'COFORGE.NS', 'COLPAL.NS', 'CONCOR.NS', 
    'CROMPTON.NS', 'CUMMINSIND.NS', 'CYIENT.NS', 'DABUR.NS', 'DALBHARAT.NS', 
    'DELHIVERY.NS', 'DIVISLAB.NS', 'DIXON.NS', 'DLF.NS', 'DMART.NS', 'DRREDDY.NS', 
    'EICHERMOT.NS', 'ETERNAL.NS', 'EXIDEIND.NS', 'FEDERALBNK.NS', 'FORTIS.NS', 
    'GAIL.NS', 'GLENMARK.NS', 'GMRAIRPORT.NS', 'GODREJCP.NS', 'GODREJPROP.NS', 
    'GRANULES.NS', 'GRASIM.NS', 'HAL.NS', 'HAVELLS.NS', 'HCLTECH.NS', 'HDFCAMC.NS', 
    'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HFCL.NS', 'HINDALCO.NS', 
    'HINDCOPPER.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS', 'HINDZINC.NS', 'HUDCO.NS', 
    'ICICIBANK.NS', 'ICICIGI.NS', 'ICICIPRULI.NS', 'IDEA.NS', 'IDFCFIRSTB.NS', 
    'IEX.NS', 'IGL.NS', 'IIFL.NS', 'INDHOTEL.NS', 'INDIANB.NS', 'INDIGO.NS', 
    'INDUSINDBK.NS', 'INDUSTOWER.NS', 'INFY.NS', 'INOXWIND.NS', 'IOC.NS', 'IRB.NS', 
    'IRCTC.NS', 'IREDA.NS', 'IRFC.NS', 'ITC.NS', 'JINDALSTEL.NS', 'JIOFIN.NS', 
    'JSL.NS', 'JSWENERGY.NS', 'JSWSTEEL.NS', 'JUBLFOOD.NS', 'KALYANKJIL.NS', 
    'KAYNES.NS', 'KEI.NS', 'KFINTECH.NS', 'KOTAKBANK.NS', 'KPITTECH.NS', 
    'LAURUSLABS.NS', 'LICHSGFIN.NS', 'LICI.NS', 'LODHA.NS', 'LT.NS', 'LTF.NS', 
    'LTIM.NS', 'LUPIN.NS', 'M&M.NS', 'M&MFIN.NS', 'MANAPPURAM.NS', 'MANKIND.NS', 
    'MARICO.NS', 'MARUTI.NS', 'MAXHEALTH.NS', 'MAZDOCK.NS', 'MCX.NS', 'MFSL.NS', 
    'MGL.NS', 'MOTHERSON.NS', 'MPHASIS.NS', 'MUTHOOTFIN.NS', 'NATIONALUM.NS', 
    'NAUKRI.NS', 'NBCC.NS', 'NCC.NS', 'NESTLEIND.NS', 'NHPC.NS', 'NMDC.NS', 
    'NTPC.NS', 'NYKAA.NS', 'OBEROIRLTY.NS', 'OFSS.NS', 'OIL.NS', 'ONGC.NS', 
    'PAGEIND.NS', 'PATANJALI.NS', 'PAYTM.NS', 'PEL.NS', 'PERSISTENT.NS', 
    'PETRONET.NS', 'PFC.NS', 'PGEL.NS', 'PHOENIXLTD.NS', 'PIDILITIND.NS', 
    'PIIND.NS', 'PNB.NS', 'PNBHOUSING.NS', 'POLICYBZR.NS', 'POLYCAB.NS', 
    'POONAWALLA.NS', 'POWERGRID.NS', 'PPLPHARMA.NS', 'PRESTIGE.NS', 'RBLBANK.NS', 
    'RECLTD.NS', 'RELIANCE.NS', 'RVNL.NS', 'SAIL.NS', 'SBICARD.NS', 'SBILIFE.NS', 
    'SBIN.NS', 'SHREECEM.NS', 'SHRIRAMFIN.NS', 'SIEMENS.NS', 'SJVN.NS', 
    'SOLARINDS.NS', 'SONACOMS.NS', 'SRF.NS', 'SUNPHARMA.NS', 'SUPREMEIND.NS', 
    'SYNGENE.NS', 'TATACHEM.NS', 'TATACOMM.NS', 'TATACONSUM.NS', 'TATAELXSI.NS', 
    'TATAMOTORS.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TATATECH.NS', 'TCS.NS', 
    'TECHM.NS', 'TIINDIA.NS', 'TITAGARH.NS', 'TITAN.NS', 'TORNTPHARM.NS', 
    'TORNTPOWER.NS', 'TRENT.NS', 'TVSMOTOR.NS', 'ULTRACEMCO.NS', 'UNIONBANK.NS', 
    'UNITDSPR.NS', 'UNOMINDA.NS', 'UPL.NS', 'VBL.NS', 'VEDL.NS', 'VOLTAS.NS', 
    'WIPRO.NS', 'YESBANK.NS', 'ZYDUSLIFE.NS'
]

@st.cache_data(ttl=300)  # Cache for 5 minutes
def screen_gap_down_green(stocks, gap_threshold):
    """Screen stocks for gap down with green candles"""
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, ticker in enumerate(stocks):
        try:
            status_text.text(f'Processing {ticker}... ({i+1}/{len(stocks)})')
            progress_bar.progress((i + 1) / len(stocks))
            
            data = yf.download(ticker, period="5d", interval="1d", progress=False, auto_adjust=False)
            data.dropna(inplace=True)

            # Group by date in case of index issues
            data = data.groupby(data.index.date).last()

            if len(data) < 2:
                continue

            # Get last two trading days
            yesterday = data.iloc[-2]
            today = data.iloc[-1]

            # Extract values as float (avoid Series ambiguity)
            y_close = yesterday['Close'].iloc[0] if hasattr(yesterday['Close'], 'iloc') else yesterday['Close']
            t_open = today['Open'].iloc[0] if hasattr(today['Open'], 'iloc') else today['Open']
            t_close = today['Close'].iloc[0] if hasattr(today['Close'], 'iloc') else today['Close']
            t_high = today['High'].iloc[0] if hasattr(today['High'], 'iloc') else today['High']
            t_low = today['Low'].iloc[0] if hasattr(today['Low'], 'iloc') else today['Low']
            t_volume = today['Volume'].iloc[0] if hasattr(today['Volume'], 'iloc') else today['Volume']

            gap_down_pct = ((t_open - y_close) / y_close) * 100
            candle_green = t_close > t_open
            recovery_pct = ((t_close - t_open) / t_open) * 100

            if gap_down_pct <= gap_threshold and candle_green:
                results.append({
                    'Ticker': ticker.replace('.NS', ''),
                    'Yesterday Close': round(y_close, 2),
                    'Today Open': round(t_open, 2),
                    'Today Close': round(t_close, 2),
                    'Today High': round(t_high, 2),
                    'Today Low': round(t_low, 2),
                    'Volume': int(t_volume),
                    'Gap Down %': round(gap_down_pct, 2),
                    'Recovery %': round(recovery_pct, 2),
                    'Green Candle': candle_green
                })

        except Exception as e:
            st.warning(f"Error processing {ticker}: {str(e)}")
            continue
    
    progress_bar.empty()
    status_text.empty()
    return pd.DataFrame(results)

def create_candlestick_chart(ticker):
    """Create candlestick chart for a specific ticker"""
    try:
        data = yf.download(f"{ticker}.NS", period="10d", interval="1d", progress=False)
        
        if data.empty:
            return None
            
        fig = go.Figure(data=go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name=ticker
        ))
        
        fig.update_layout(
            title=f"{ticker} - Last 10 Days",
            yaxis_title="Price (₹)",
            xaxis_title="Date",
            height=400,
            showlegend=False
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating chart for {ticker}: {str(e)}")
        return None

# Streamlit App Layout
def main():
    st.title("📈 F&O Gap Down Green Candle Screener")
    st.markdown("**Find F&O stocks that gapped down but closed green (bullish reversal pattern)**")
    
    # Sidebar for controls
    st.sidebar.header("⚙️ Screening Parameters")
    
    gap_threshold = st.sidebar.slider(
        "Gap Down Threshold (%)", 
        min_value=-10.0, 
        max_value=-0.5, 
        value=-2.0, 
        step=0.1,
        help="Minimum gap down percentage required"
    )
    
    auto_refresh = st.sidebar.checkbox("Auto Refresh (5 min)", value=False)
    
    if st.sidebar.button("🔄 Run Screener", type="primary"):
        st.session_state.run_screener = True
    
    # Main content area
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info(f"Screening {len(fno_stocks)} F&O stocks for gap down ≤ {gap_threshold}% with green candles")
    
    # Run screener
    if st.session_state.get('run_screener', False) or auto_refresh:
        with st.spinner("🔍 Screening stocks... This may take a few minutes"):
            df_result = screen_gap_down_green(fno_stocks, gap_threshold)
        
        st.session_state.df_result = df_result
        st.session_state.run_screener = False
    
    # Display results
    if 'df_result' in st.session_state:
        df_result = st.session_state.df_result
        
        if not df_result.empty:
            st.success(f"✅ Found {len(df_result)} stocks matching criteria!")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Matches", len(df_result))
            with col2:
                avg_gap = df_result['Gap Down %'].mean()
                st.metric("Avg Gap Down", f"{avg_gap:.1f}%")
            with col3:
                avg_recovery = df_result['Recovery %'].mean()
                st.metric("Avg Recovery", f"{avg_recovery:.1f}%")
            with col4:
                best_recovery = df_result['Recovery %'].max()
                st.metric("Best Recovery", f"{best_recovery:.1f}%")
            
            # Results table
            st.subheader("📊 Screening Results")
            
            # Sort options
            sort_by = st.selectbox(
                "Sort by:", 
                ["Gap Down %", "Recovery %", "Volume", "Ticker"],
                index=1
            )
            
            ascending = sort_by in ["Gap Down %", "Ticker"]
            df_sorted = df_result.sort_values(sort_by, ascending=ascending)
            
            # Display table with formatting
            st.dataframe(
                df_sorted.style.format({
                    'Yesterday Close': '₹{:.2f}',
                    'Today Open': '₹{:.2f}',
                    'Today Close': '₹{:.2f}',
                    'Today High': '₹{:.2f}',
                    'Today Low': '₹{:.2f}',
                    'Volume': '{:,}',
                    'Gap Down %': '{:.2f}%',
                    'Recovery %': '{:.2f}%'
                }).background_gradient(subset=['Recovery %'], cmap='RdYlGn'),
                use_container_width=True
            )
            
            # Download button
            csv = df_result.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name=f"fno_gap_down_green_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
            
            # Chart section
            st.subheader("📈 Stock Charts")
            
            selected_stocks = st.multiselect(
                "Select stocks to view charts:",
                df_result['Ticker'].tolist(),
                default=df_result['Ticker'].head(3).tolist() if len(df_result) >= 3 else df_result['Ticker'].tolist()
            )
            
            if selected_stocks:
                chart_cols = st.columns(min(2, len(selected_stocks)))
                
                for i, ticker in enumerate(selected_stocks):
                    with chart_cols[i % 2]:
                        fig = create_candlestick_chart(ticker)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.warning("📉 No stocks matched the criteria today.")
            st.info("Try adjusting the gap down threshold or check back later.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Note:** This screener is for educational purposes only. "
        "Always do your own research before making investment decisions."
    )
    
    # Auto refresh
    if auto_refresh:
        time.sleep(300)  # 5 minutes
        st.rerun()

if __name__ == "__main__":
    main()
