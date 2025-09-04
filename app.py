import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="F&O & Equity Gap Down Green Candle Screener",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verified F&O Stock List (only working symbols)
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

# Additional verified F&O stocks
additional_fno_stocks = [
    'ACC.NS'
]

# Combine all F&O stocks
all_fno_stocks = list(set(fno_stocks + additional_fno_stocks))

# Equity Stock List
equity_stocks = ['360ONE.NS', '3MINDIA.NS', 'ABB.NS', 'ACC.NS', 'ACMESOLAR.NS', 'AIAENG.NS', 'APLAPOLLO.NS', 'AUBANK.NS', 'AWL.NS', 'AADHARHFC.NS', 'AARTIIND.NS', 'AAVAS.NS', 'ABBOTINDIA.NS', 'ACE.NS', 'ADANIENSOL.NS', 'ADANIENT.NS', 'ADANIGREEN.NS', 'ADANIPORTS.NS', 'ADANIPOWER.NS', 'ATGL.NS', 'ABCAPITAL.NS', 'ABFRL.NS', 'ABREL.NS', 'ABSLAMC.NS', 'AEGISLOG.NS', 'AFCONS.NS', 'AFFLE.NS', 'AJANTPHARM.NS', 'AKUMS.NS', 'APLLTD.NS', 'ALIVUS.NS', 'ALKEM.NS', 'ALKYLAMINE.NS', 'ALOKINDS.NS', 'ARE&M.NS', 'AMBER.NS', 'AMBUJACEM.NS', 'ANANDRATHI.NS', 'ANANTRAJ.NS', 'ANGELONE.NS', 'APARINDS.NS', 'APOLLOHOSP.NS', 'APOLLOTYRE.NS', 'APTUS.NS', 'ASAHIINDIA.NS', 'ASHOKLEY.NS', 'ASIANPAINT.NS', 'ASTERDM.NS', 'ASTRAZEN.NS', 'ASTRAL.NS', 'ATUL.NS', 'AUROPHARMA.NS', 'AIIL.NS', 'DMART.NS', 'AXISBANK.NS', 'BASF.NS', 'BEML.NS', 'BLS.NS', 'BSE.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BAJAJHLDNG.NS', 'BAJAJHFL.NS', 'BALKRISIND.NS', 'BALRAMCHIN.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', 'BANKINDIA.NS', 'MAHABANK.NS', 'BATAINDIA.NS', 'BAYERCROP.NS', 'BERGEPAINT.NS', 'BDL.NS', 'BEL.NS', 'BHARATFORG.NS', 'BHEL.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'BHARTIHEXA.NS', 'BIKAJI.NS', 'BIOCON.NS', 'BSOFT.NS', 'BLUEDART.NS', 'BLUESTARCO.NS', 'BBTC.NS', 'BOSCHLTD.NS', 'FIRSTCRY.NS', 'BRIGADE.NS', 'BRITANNIA.NS', 'MAPMYINDIA.NS', 'CCL.NS', 'CESC.NS', 'CGPOWER.NS', 'CRISIL.NS', 'CAMPUS.NS', 'CANFINHOME.NS', 'CANBK.NS', 'CAPLIPOINT.NS', 'CGCL.NS', 'CARBORUNIV.NS', 'CASTROLIND.NS', 'CEATLTD.NS', 'CENTRALBK.NS', 'CDSL.NS', 'CENTURYPLY.NS', 'CERA.NS', 'CHALET.NS', 'CHAMBLFERT.NS', 'CHENNPETRO.NS', 'CHOLAHLDNG.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 'CUB.NS', 'CLEAN.NS', 'COALINDIA.NS', 'COCHINSHIP.NS', 'COFORGE.NS', 'COHANCE.NS', 'COLPAL.NS', 'CAMS.NS', 'CONCORDBIO.NS', 'CONCOR.NS', 'COROMANDEL.NS', 'CRAFTSMAN.NS', 'CREDITACC.NS', 'CROMPTON.NS', 'CUMMINSIND.NS', 'CYIENT.NS', 'DCMSHRIRAM.NS', 'DLF.NS', 'DOMS.NS', 'DABUR.NS', 'DALBHARAT.NS', 'DATAPATTNS.NS', 'DEEPAKFERT.NS', 'DEEPAKNTR.NS', 'DELHIVERY.NS', 'DEVYANI.NS', 'DIVISLAB.NS', 'DIXON.NS', 'LALPATHLAB.NS', 'DRREDDY.NS', 'DUMMYDBRLT.NS', 'EIDPARRY.NS', 'EIHOTEL.NS', 'EICHERMOT.NS', 'ELECON.NS', 'ELGIEQUIP.NS', 'EMAMILTD.NS', 'EMCURE.NS', 'ENDURANCE.NS', 'ENGINERSIN.NS', 'ERIS.NS', 'ESCORTS.NS', 'ETERNAL.NS', 'EXIDEIND.NS', 'NYKAA.NS', 'FEDERALBNK.NS', 'FACT.NS', 'FINCABLES.NS', 'FINPIPE.NS', 'FSL.NS', 'FIVESTAR.NS', 'FORTIS.NS', 'GAIL.NS', 'GVT&D.NS', 'GMRAIRPORT.NS', 'GRSE.NS', 'GICRE.NS', 'GILLETTE.NS', 'GLAND.NS', 'GLAXO.NS', 'GLENMARK.NS', 'MEDANTA.NS', 'GODIGIT.NS', 'GPIL.NS', 'GODFRYPHLP.NS', 'GODREJAGRO.NS', 'GODREJCP.NS', 'GODREJIND.NS', 'GODREJPROP.NS', 'GRANULES.NS', 'GRAPHITE.NS', 'GRASIM.NS', 'GRAVITA.NS', 'GESHIP.NS', 'FLUOROCHEM.NS', 'GUJGASLTD.NS', 'GMDCLTD.NS', 'GNFC.NS', 'GPPL.NS', 'GSPL.NS', 'HEG.NS', 'HBLENGINE.NS', 'HCLTECH.NS', 'HDFCAMC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HFCL.NS', 'HAPPSTMNDS.NS', 'HAVELLS.NS', 'HEROMOTOCO.NS', 'HSCL.NS', 'HINDALCO.NS', 'HAL.NS', 'HINDCOPPER.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS', 'HINDZINC.NS', 'POWERINDIA.NS', 'HOMEFIRST.NS', 'HONASA.NS', 'HONAUT.NS', 'HUDCO.NS', 'HYUNDAI.NS', 'ICICIBANK.NS', 'ICICIGI.NS', 'ICICIPRULI.NS', 'IDBI.NS', 'IDFCFIRSTB.NS', 'IFCI.NS', 'IIFL.NS', 'INOXINDIA.NS', 'IRB.NS', 'IRCON.NS', 'ITC.NS', 'ITI.NS', 'INDGN.NS', 'INDIACEM.NS', 'INDIAMART.NS', 'INDIANB.NS', 'IEX.NS', 'INDHOTEL.NS', 'IOC.NS', 'IOB.NS', 'IRCTC.NS', 'IRFC.NS', 'IREDA.NS', 'IGL.NS', 'INDUSTOWER.NS', 'INDUSINDBK.NS', 'NAUKRI.NS', 'INFY.NS', 'INOXWIND.NS', 'INTELLECT.NS', 'INDIGO.NS', 'IGIL.NS', 'IKS.NS', 'IPCALAB.NS', 'JBCHEPHARM.NS', 'JKCEMENT.NS', 'JBMA.NS', 'JKTYRE.NS', 'JMFINANCIL.NS', 'JSWENERGY.NS', 'JSWHL.NS', 'JSWINFRA.NS', 'JSWSTEEL.NS', 'JPPOWER.NS', 'J&KBANK.NS', 'JINDALSAW.NS', 'JSL.NS', 'JINDALSTEL.NS', 'JIOFIN.NS', 'JUBLFOOD.NS', 'JUBLINGREA.NS', 'JUBLPHARMA.NS', 'JWL.NS', 'JUSTDIAL.NS', 'JYOTHYLAB.NS', 'JYOTICNC.NS', 'KPRMILL.NS', 'KEI.NS', 'KNRCON.NS', 'KPITTECH.NS', 'KAJARIACER.NS', 'KPIL.NS', 'KALYANKJIL.NS', 'KANSAINER.NS', 'KARURVYSYA.NS', 'KAYNES.NS', 'KEC.NS', 'KFINTECH.NS', 'KIRLOSBROS.NS', 'KIRLOSENG.NS', 'KOTAKBANK.NS', 'KIMS.NS', 'LTF.NS', 'LTTS.NS', 'LICHSGFIN.NS', 'LTFOODS.NS', 'LTIM.NS', 'LT.NS', 'LATENTVIEW.NS', 'LAURUSLABS.NS', 'LEMONTREE.NS', 'LICI.NS', 'LINDEINDIA.NS', 'LLOYDSME.NS', 'LODHA.NS', 'LUPIN.NS', 'MMTC.NS', 'MRF.NS', 'MGL.NS', 'MAHSEAMLES.NS', 'M&MFIN.NS', 'M&M.NS', 'MANAPPURAM.NS', 'MRPL.NS', 'MANKIND.NS', 'MARICO.NS', 'MARUTI.NS', 'MASTEK.NS', 'MFSL.NS', 'MAXHEALTH.NS', 'MAZDOCK.NS', 'METROPOLIS.NS', 'MINDACORP.NS', 'MSUMI.NS', 'MOTILALOFS.NS', 'MPHASIS.NS', 'MCX.NS', 'MUTHOOTFIN.NS', 'NATCOPHARM.NS', 'NBCC.NS', 'NCC.NS', 'NHPC.NS', 'NLCINDIA.NS', 'NMDC.NS', 'NSLNISP.NS', 'NTPCGREEN.NS', 'NTPC.NS', 'NH.NS', 'NATIONALUM.NS', 'NAVA.NS', 'NAVINFLUOR.NS', 'NESTLEIND.NS', 'NETWEB.NS', 'NETWORK18.NS', 'NEULANDLAB.NS', 'NEWGEN.NS', 'NAM-INDIA.NS', 'NIVABUPA.NS', 'NUVAMA.NS', 'OBEROIRLTY.NS', 'ONGC.NS', 'OIL.NS', 'OLAELEC.NS', 'OLECTRA.NS', 'PAYTM.NS', 'OFSS.NS', 'POLICYBZR.NS', 'PCBL.NS', 'PGEL.NS', 'PIIND.NS', 'PNBHOUSING.NS', 'PNCINFRA.NS', 'PTCIL.NS', 'PVRINOX.NS', 'PAGEIND.NS', 'PATANJALI.NS', 'PERSISTENT.NS', 'PETRONET.NS', 'PFIZER.NS', 'PHOENIXLTD.NS', 'PIDILITIND.NS', 'PEL.NS', 'PPLPHARMA.NS', 'POLYMED.NS', 'POLYCAB.NS', 'POONAWALLA.NS', 'PFC.NS', 'POWERGRID.NS', 'PRAJIND.NS', 'PREMIERENE.NS', 'PRESTIGE.NS', 'PNB.NS', 'RRKABEL.NS', 'RBLBANK.NS', 'RECLTD.NS', 'RHIM.NS', 'RITES.NS', 'RADICO.NS', 'RVNL.NS', 'RAILTEL.NS', 'RAINBOW.NS', 'RKFORGE.NS', 'RCF.NS', 'RTNINDIA.NS', 'RAYMONDLSL.NS', 'RAYMOND.NS', 'REDINGTON.NS', 'RELIANCE.NS', 'RPOWER.NS', 'ROUTE.NS', 'SBFC.NS', 'SBICARD.NS', 'SBILIFE.NS', 'SJVN.NS', 'SKFINDIA.NS', 'SRF.NS', 'SAGILITY.NS', 'SAILIFE.NS', 'SAMMAANCAP.NS', 'MOTHERSON.NS', 'SAPPHIRE.NS', 'SARDAEN.NS', 'SAREGAMA.NS', 'SCHAEFFLER.NS', 'SCHNEIDER.NS', 'SCI.NS', 'SHREECEM.NS', 'RENUKA.NS', 'SHRIRAMFIN.NS', 'SHYAMMETL.NS', 'SIEMENS.NS', 'SIGNATURE.NS', 'SOBHA.NS', 'SOLARINDS.NS', 'SONACOMS.NS', 'SONATSOFTW.NS', 'STARHEALTH.NS', 'SBIN.NS', 'SAIL.NS', 'SWSOLAR.NS', 'SUMICHEM.NS', 'SUNPHARMA.NS', 'SUNTV.NS', 'SUNDARMFIN.NS', 'SUNDRMFAST.NS', 'SUPREMEIND.NS', 'SUZLON.NS', 'SWANENERGY.NS', 'SWIGGY.NS', 'SYNGENE.NS', 'SYRMA.NS', 'TBOTEK.NS', 'TVSMOTOR.NS', 'TANLA.NS', 'TATACHEM.NS', 'TATACOMM.NS', 'TCS.NS', 'TATACONSUM.NS', 'TATAELXSI.NS', 'TATAINVEST.NS', 'TATAMOTORS.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TATATECH.NS', 'TTML.NS', 'TECHM.NS', 'TECHNOE.NS', 'TEJASNET.NS', 'NIACL.NS', 'RAMCOCEM.NS', 'THERMAX.NS', 'TIMKEN.NS', 'TITAGARH.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TORNTPOWER.NS', 'TARIL.NS', 'TRENT.NS', 'TRIDENT.NS', 'TRIVENI.NS', 'TRITURBINE.NS', 'TIINDIA.NS', 'UCOBANK.NS', 'UNOMINDA.NS', 'UPL.NS', 'UTIAMC.NS', 'ULTRACEMCO.NS', 'UNIONBANK.NS', 'UBL.NS', 'UNITDSPR.NS', 'USHAMART.NS', 'VGUARD.NS', 'DBREALTY.NS', 'VTL.NS', 'VBL.NS', 'MANYAVAR.NS', 'VEDL.NS', 'VIJAYA.NS', 'VMM.NS', 'IDEA.NS', 'VOLTAS.NS', 'WAAREEENER.NS', 'WELCORP.NS', 'WELSPUNLIV.NS', 'WESTLIFE.NS', 'WHIRLPOOL.NS', 'WIPRO.NS', 'WOCKPHARMA.NS', 'YESBANK.NS', 'ZFCVINDIA.NS', 'ZEEL.NS', 'ZENTEC.NS', 'ZENSARTECH.NS', 'ZYDUSLIFE.NS', 'ECLERX.NS']
@st.cache_data(ttl=300)  # Cache for 5 minutes
def screen_gap_down_green(stocks, gap_threshold, max_stocks=None, stock_type="F&O"):
    """Screen stocks for gap down with green candles with better error handling"""
    results = []
    failed_stocks = []
    processed_count = 0
    
    # Limit number of stocks if specified
    if max_stocks:
        stocks = stocks[:max_stocks]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, ticker in enumerate(stocks):
        try:
            status_text.text(f'Processing {ticker.replace(".NS", "")} ({stock_type})... ({i+1}/{len(stocks)})')
            progress_bar.progress((i + 1) / len(stocks))
            
            # Download data with error handling
            data = yf.download(ticker, period="5d", interval="1d", progress=False, auto_adjust=False)
            
            if data.empty:
                failed_stocks.append(ticker)
                continue
                
            data.dropna(inplace=True)

            # Group by date in case of index issues
            if len(data.index.names) > 1 or data.index.duplicated().any():
                data = data.groupby(data.index.date).last()

            if len(data) < 2:
                continue

            # Get last two trading days
            yesterday = data.iloc[-2]
            today = data.iloc[-1]

            # Extract values safely
            def safe_extract(series_or_value):
                if hasattr(series_or_value, 'iloc'):
                    return float(series_or_value.iloc[0])
                else:
                    return float(series_or_value)

            y_close = safe_extract(yesterday['Close'])
            t_open = safe_extract(today['Open'])
            t_close = safe_extract(today['Close'])
            t_high = safe_extract(today['High'])
            t_low = safe_extract(today['Low'])
            t_volume = safe_extract(today['Volume'])

            # Calculate metrics
            gap_down_pct = ((t_open - y_close) / y_close) * 100
            candle_green = t_close > t_open
            recovery_pct = ((t_close - t_open) / t_open) * 100 if t_open != 0 else 0

            # Apply filters
            if gap_down_pct <= gap_threshold and candle_green:
                results.append({
                    'Ticker': ticker.replace('.NS', ''),
                    'Type': stock_type,
                    'Yesterday Close': round(y_close, 2),
                    'Today Open': round(t_open, 2),
                    'Today Close': round(t_close, 2),
                    'Today High': round(t_high, 2),
                    'Today Low': round(t_low, 2),
                    'Volume': int(t_volume) if t_volume > 0 else 0,
                    'Gap Down %': round(gap_down_pct, 2),
                    'Recovery %': round(recovery_pct, 2),
                    'Green Candle': candle_green
                })
                
            processed_count += 1

        except Exception as e:
            failed_stocks.append(f"{ticker}: {str(e)}")
            continue
    
    progress_bar.empty()
    status_text.empty()
    
    # Show processing summary
    if failed_stocks:
        with st.expander(f"⚠️ Processing Issues ({len(failed_stocks)} {stock_type} stocks)", expanded=False):
            st.write(f"Some {stock_type} stocks couldn't be processed (possibly delisted or data unavailable):")
            for stock in failed_stocks[:10]:  # Show only first 10
                st.text(f"• {stock}")
            if len(failed_stocks) > 10:
                st.text(f"... and {len(failed_stocks) - 10} more")
    
    st.success(f"✅ Successfully processed {processed_count} {stock_type} stocks out of {len(stocks)}")
    
    return pd.DataFrame(results)

def create_candlestick_chart(ticker):
    """Create candlestick chart for a specific ticker with error handling"""
    try:
        data = yf.download(f"{ticker}.NS", period="10d", interval="1d", progress=False)
        
        if data.empty:
            st.error(f"No data available for {ticker}")
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
            showlegend=False,
            xaxis_rangeslider_visible=False
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating chart for {ticker}: {str(e)}")
        return None

# Streamlit App Layout
def main():
    st.title("📈 F&O & Equity Gap Down Green Candle Screener")
    st.markdown("**Find F&O and Equity stocks that gapped down but closed green (bullish reversal pattern)**")
    
    # Sidebar for controls
    st.sidebar.header("⚙️ Screening Parameters")
    
    # Market selection
    market_type = st.sidebar.radio(
        "Select Market:",
        ["F&O Stocks", "Equity Stocks", "Both Markets"]
    )
    
    gap_threshold = st.sidebar.slider(
        "Gap Down Threshold (%)", 
        min_value=-10.0, 
        max_value=-0.5, 
        value=-2.0, 
        step=0.1,
        help="Minimum gap down percentage required"
    )
    
    # Stock selection based on market type
    if market_type == "F&O Stocks":
        st.sidebar.markdown("**F&O Screening Options:**")
        fno_screening_mode = st.sidebar.radio(
            "F&O Screening Mode:",
            ["Quick Scan (Top 50)", "Full Scan (All F&O stocks)", "Custom Selection"],
            key="fno_mode"
        )
        
        if fno_screening_mode == "Custom Selection":
            max_fno_stocks = st.sidebar.number_input(
                "Number of F&O stocks to screen:", 
                min_value=10, 
                max_value=len(all_fno_stocks), 
                value=100,
                key="fno_custom"
            )
        elif fno_screening_mode == "Quick Scan (Top 50)":
            max_fno_stocks = 50
        else:
            max_fno_stocks = None
            
        max_equity_stocks = 0
        equity_screening_mode = None
        
    elif market_type == "Equity Stocks":
        st.sidebar.markdown("**Equity Screening Options:**")
        equity_screening_mode = st.sidebar.radio(
            "Equity Screening Mode:",
            ["Full Scan (All Equity stocks)", "Custom Selection"],
            key="equity_mode"
        )
        
        if equity_screening_mode == "Custom Selection":
            max_equity_stocks = st.sidebar.number_input(
                "Number of Equity stocks to screen:", 
                min_value=1, 
                max_value=len(equity_stocks), 
                value=len(equity_stocks),
                key="equity_custom"
            )
        else:
            max_equity_stocks = None
            
        max_fno_stocks = 0
        fno_screening_mode = None
        
    else:  # Both Markets
        st.sidebar.markdown("**F&O Screening Options:**")
        fno_screening_mode = st.sidebar.radio(
            "F&O Screening Mode:",
            ["Quick Scan (Top 50)", "Full Scan (All F&O stocks)", "Custom Selection"],
            key="fno_mode_both"
        )
        
        if fno_screening_mode == "Custom Selection":
            max_fno_stocks = st.sidebar.number_input(
                "Number of F&O stocks to screen:", 
                min_value=10, 
                max_value=len(all_fno_stocks), 
                value=100,
                key="fno_custom_both"
            )
        elif fno_screening_mode == "Quick Scan (Top 50)":
            max_fno_stocks = 50
        else:
            max_fno_stocks = None
            
        st.sidebar.markdown("**Equity Screening Options:**")
        equity_screening_mode = st.sidebar.radio(
            "Equity Screening Mode:",
            ["Full Scan (All Equity stocks)", "Custom Selection"],
            key="equity_mode_both"
        )
        
        if equity_screening_mode == "Custom Selection":
            max_equity_stocks = st.sidebar.number_input(
                "Number of Equity stocks to screen:", 
                min_value=1, 
                max_value=len(equity_stocks), 
                value=len(equity_stocks),
                key="equity_custom_both"
            )
        else:
            max_equity_stocks = None
    
    auto_refresh = st.sidebar.checkbox("Auto Refresh (5 min)", value=False)
    
    if st.sidebar.button("🔄 Run Screener", type="primary"):
        st.session_state.run_screener = True
    
    # Info section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if market_type == "F&O Stocks":
            total_stocks = max_fno_stocks if max_fno_stocks else len(all_fno_stocks)
            st.info(f"Screening {total_stocks} F&O stocks for gap down ≤ {gap_threshold}% with green candles")
        elif market_type == "Equity Stocks":
            total_stocks = max_equity_stocks if max_equity_stocks else len(equity_stocks)
            st.info(f"Screening {total_stocks} Equity stocks for gap down ≤ {gap_threshold}% with green candles")
        else:
            total_fno = max_fno_stocks if max_fno_stocks else len(all_fno_stocks)
            total_equity = max_equity_stocks if max_equity_stocks else len(equity_stocks)
            st.info(f"Screening {total_fno} F&O + {total_equity} Equity stocks for gap down ≤ {gap_threshold}% with green candles")
    
    # Show current time
    st.sidebar.markdown(f"**Last Update:** {datetime.now().strftime('%H:%M:%S IST')}")
    
    # Run screener
    if st.session_state.get('run_screener', False) or auto_refresh:
        with st.spinner("🔍 Screening stocks... Please wait"):
            all_results = []
            
            # Screen F&O stocks if selected
            if market_type in ["F&O Stocks", "Both Markets"]:
                df_fno = screen_gap_down_green(all_fno_stocks, gap_threshold, max_fno_stocks, "F&O")
                if not df_fno.empty:
                    all_results.append(df_fno)
            
            # Screen Equity stocks if selected
            if market_type in ["Equity Stocks", "Both Markets"]:
                df_equity = screen_gap_down_green(equity_stocks, gap_threshold, max_equity_stocks, "Equity")
                if not df_equity.empty:
                    all_results.append(df_equity)
            
            # Combine results
            if all_results:
                df_result = pd.concat(all_results, ignore_index=True)
            else:
                df_result = pd.DataFrame()
        
        st.session_state.df_result = df_result
        st.session_state.run_screener = False
    
    # Display results
    if 'df_result' in st.session_state:
        df_result = st.session_state.df_result
        
        if not df_result.empty:
            st.success(f"🎯 Found {len(df_result)} stocks matching criteria!")
            
            # Summary metrics by type
            if 'Type' in df_result.columns and market_type == "Both Markets":
                col1, col2, col3, col4 = st.columns(4)
                
                fno_count = len(df_result[df_result['Type'] == 'F&O'])
                equity_count = len(df_result[df_result['Type'] == 'Equity'])
                
                with col1:
                    st.metric("F&O Matches", fno_count)
                with col2:
                    st.metric("Equity Matches", equity_count)
                with col3:
                    avg_gap = df_result['Gap Down %'].mean()
                    st.metric("Avg Gap Down", f"{avg_gap:.1f}%")
                with col4:
                    avg_recovery = df_result['Recovery %'].mean()
                    st.metric("Avg Recovery", f"{avg_recovery:.1f}%")
            else:
                # Original metrics for single market
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
                ["Recovery %", "Gap Down %", "Volume", "Ticker", "Type"],
                index=0
            )
            
            ascending = sort_by in ["Gap Down %", "Ticker", "Type"]
            df_sorted = df_result.sort_values(sort_by, ascending=ascending)
            
            # Display table with formatting
            if 'Type' in df_result.columns:
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
            else:
                st.dataframe(
                    df_sorted.drop(columns=['Type'], errors='ignore').style.format({
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
                file_name=f"gap_down_green_{market_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
            
            # Chart section
            if len(df_result) > 0:
                st.subheader("📈 Stock Charts")
                
                selected_stocks = st.multiselect(
                    "Select stocks to view charts:",
                    df_result['Ticker'].tolist(),
                    default=df_result['Ticker'].head(min(3, len(df_result))).tolist()
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
            st.info("💡 **Suggestions:**\n- Try adjusting the gap down threshold\n- Check during market hours for better results\n- Some stocks might be delisted or have data issues")
    
    # Market timing info
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📅 Market Hours**")
    st.sidebar.markdown("NSE: 9:15 AM - 3:30 PM IST")
    st.sidebar.markdown("Best results during market hours")
    
    # Stock count info
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📊 Stock Universe**")
    st.sidebar.markdown(f"F&O Stocks: {len(all_fno_stocks)}")
    st.sidebar.markdown(f"Equity Stocks: {len(equity_stocks)}")
    st.sidebar.markdown(f"Total: {len(all_fno_stocks) + len(equity_stocks)}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**⚠️ Disclaimer:** This screener is for educational purposes only. "
        "Always do your own research before making investment decisions. "
        "Stock trading involves substantial risk of loss."
    )
    
    # Auto refresh
    if auto_refresh:
        time.sleep(300)  # 5 minutes
        st.rerun()

if __name__ == "__main__":
    main()
