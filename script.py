import os
import smtplib
from email.message import EmailMessage
import yfinance as yf    
import pandas as pd      
import warnings          
import logging           
from datetime import datetime 

logging.getLogger('yfinance').setLevel(logging.CRITICAL)
warnings.filterwarnings('ignore')

def advanced_stock_scanner(ticker_list):
    results = []
    today_date = datetime.now().strftime("%d-%m-%Y")
    
    print(f"{len(ticker_list)} scanning\n")
    
    for ticker in ticker_list:
        try:

            data = yf.download(ticker, period="2y", interval="1d", progress=False)
            if data.empty or len(data) < 200: 
                continue
            close_prices = data['Close'].squeeze()
            dma_30 = close_prices.rolling(window=30).mean().iloc[-1]
            dma_50 = close_prices.rolling(window=50).mean().iloc[-1]
            dma_200 = close_prices.rolling(window=200).mean().iloc[-1]
            
            cmp = close_prices.iloc[-1]
            dist_200_dma = ((cmp - dma_200) / dma_200) * 100
            last_1y_data = data.tail(252)
            high_date = last_1y_data['High'].squeeze().idxmax()
            car_data = close_prices.loc[high_date:]
            if len(car_data) < 10: 
                continue
            car_values = car_data.expanding().mean()
            last_10_car = car_values.tail(10)

            if last_10_car.is_monotonic_increasing:
                car_status = 'Positive' 
            else:
                car_status = 'Negative' 
            
            if (cmp > dma_30) and (cmp > dma_50) and (cmp > dma_200) and (car_status == 'Positive'):
                action = '🟢 Positive Breakout' 
            else:
                action = '🔴 Avoid/Hold' 

            if action == '🟢 Positive Breakout':
                results.append({
                    'Date': today_date,
                    'Stock': ticker.replace('.NS', ''), 
                    'CMP': round(cmp, 2), 
                    '30 DMA': round(dma_30, 2),
                    '50 DMA': round(dma_50, 2),
                    '200 DMA': round(dma_200, 2),
                    '200 DMA Dist %': round(dist_200_dma, 2),
                    'CAR Status': car_status,
                    'Action': action
                })
            
        except Exception as e:
            pass
            
    df_positive = pd.DataFrame(results)
    
    if not df_positive.empty:
        df_positive = df_positive.sort_values(by='200 DMA Dist %', ascending=True)
        
    return df_positive

my_stocks = [
    '360ONE.NS', 'ABB.NS', 'APLAPOLLO.NS', 'AUBANK.NS', 'ADANIENSOL.NS',
    'ADANIENT.NS', 'ADANIGREEN.NS', 'ADANIPORTS.NS', 'ADANIPOWER.NS', 'ABCAPITAL.NS',
    'ALKEM.NS', 'AMBER.NS', 'AMBUJACEM.NS', 'ANGELONE.NS', 'APOLLOHOSP.NS',
    'ASHOKLEY.NS', 'ASIANPAINT.NS', 'ASTRAL.NS', 'AUROPHARMA.NS', 'DMART.NS',
    'AXISBANK.NS', 'BSE.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS',
    'BAJAJHLDNG.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', 'BANKINDIA.NS', 'BDL.NS',
    'BEL.NS', 'BHARATFORG.NS', 'BHEL.NS', 'BPCL.NS', 'BHARTIARTL.NS',
    'BIOCON.NS', 'BLUESTARCO.NS', 'BOSCHLTD.NS', 'BRITANNIA.NS', 'CGPOWER.NS',
    'CANBK.NS', 'CDSL.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 'COALINDIA.NS',
    'COCHINSHIP.NS', 'COFORGE.NS', 'COLPAL.NS', 'CAMS.NS', 'CONCOR.NS',
    'CROMPTON.NS', 'CUMMINSIND.NS', 'DLF.NS', 'DABUR.NS', 'DALBHARAT.NS',
    'DELHIVERY.NS', 'DIVISLAB.NS', 'DIXON.NS', 'DRREDDY.NS', 'ETERNAL.NS',
    'EICHERMOT.NS', 'EXIDEIND.NS', 'FORCEMOT.NS', 'NYKAA.NS', 'FORTIS.NS',
    'GAIL.NS', 'GVT&D.NS', 'GMRAIRPORT.NS', 'GLENMARK.NS', 'GODFRYPHLP.NS',
    'GODREJCP.NS', 'GODREJPROP.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCAMC.NS',
    'HDFCBANK.NS', 'HDFCLIFE.NS', 'HAVELLS.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS',
    'HAL.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS', 'HINDZINC.NS', 'POWERINDIA.NS',
    'HYUNDAI.NS', 'ICICIBANK.NS', 'ICICIGI.NS', 'ICICIPRULI.NS', 'IDFCFIRSTB.NS',
    'ITC.NS', 'INDIANB.NS', 'IEX.NS', 'IOC.NS', 'IRFC.NS', 'IREDA.NS',
    'INDUSTOWER.NS', 'INDUSINDBK.NS', 'NAUKRI.NS', 'INFY.NS', 'INOXWIND.NS',
    'INDIGO.NS', 'JINDALSTEL.NS', 'JSWENERGY.NS', 'JSWSTEEL.NS', 'JIOFIN.NS',
    'JUBLFOOD.NS', 'KEI.NS', 'KPITTECH.NS', 'KALYANKJIL.NS', 'KAYNES.NS',
    'KFINTECH.NS', 'KOTAKBANK.NS', 'LTF.NS', 'LICHSGFIN.NS', 'LTM.NS',
    'LT.NS', 'LAURUSLABS.NS', 'LICI.NS', 'LODHA.NS', 'LUPIN.NS',
    'M&M.NS', 'MANAPPURAM.NS', 'MANKIND.NS', 'MARICO.NS', 'MARUTI.NS',
    'MFSL.NS', 'MAXHEALTH.NS', 'MAZDOCK.NS', 'MOTILALOFS.NS', 'MPHASIS.NS',
    'MCX.NS', 'MUTHOOTFIN.NS', 'NBCC.NS', 'NHPC.NS', 'NMDC.NS',
    'NTPC.NS', 'NATIONALUM.NS', 'NESTLEIND.NS', 'NAM-INDIA.NS', 'NUVAMA.NS',
    'OBEROIRLTY.NS', 'ONGC.NS', 'OIL.NS', 'PAYTM.NS', 'OFSS.NS',
    'POLICYBZR.NS', 'PGEL.NS', 'PIIND.NS', 'PNBHOUSING.NS', 'PAGEIND.NS',
    'PATANJALI.NS', 'PERSISTENT.NS', 'PETRONET.NS', 'PIDILITIND.NS', 'POLYCAB.NS',
    'PFC.NS', 'POWERGRID.NS', 'PREMIERENE.NS', 'PRESTIGE.NS', 'PNB.NS',
    'RBLBANK.NS', 'RECLTD.NS', 'RADICO.NS', 'RVNL.NS', 'RELIANCE.NS',
    'SBICARD.NS', 'SBILIFE.NS', 'SHREECEM.NS', 'SRF.NS', 'MOTHERSON.NS',
    'SHRIRAMFIN.NS', 'SIEMENS.NS', 'SOLARINDS.NS', 'SONACOMS.NS', 'SBIN.NS',
    'SAIL.NS', 'SUNPHARMA.NS', 'SUPREMEIND.NS', 'SUZLON.NS', 'SWIGGY.NS',
    'TATACONSUM.NS', 'TVSMOTOR.NS', 'TCS.NS', 'TATAELXSI.NS', 'TMPV.NS',
    'TATAPOWER.NS', 'TATASTEEL.NS', 'TECHM.NS', 'FEDERALBNK.NS', 'INDHOTEL.NS',
    'PHOENIXLTD.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TRENT.NS', 'TIINDIA.NS',
    'UNOMINDA.NS', 'UPL.NS', 'ULTRACEMCO.NS', 'UNIONBANK.NS', 'UNITDSPR.NS',
    'VBL.NS', 'VEDL.NS', 'VMM.NS', 'IDEA.NS', 'VOLTAS.NS',
    'WAAREEENER.NS', 'WIPRO.NS', 'YESBANK.NS', 'ZYDUSLIFE.NS'
]

positive_breakout_data = advanced_stock_scanner(my_stocks)

print("\n--- 🟢 final list: only POSITIVE BREAKOUT stocks ---")
if positive_breakout_data.empty:
    print("no new breakouts")
else:
    print(positive_breakout_data.to_string(index=False))
    
    # positive_breakout_data.to_excel("Final_Breakout_List.xlsx", index=False)
    # print("\nsaved")
    
    # from google.colab import files
    # files.download("Final_Breakout_List.xlsx")

EMAIL = os.environ["EMAIL"]
APP_PASSWORD = os.environ["APP_PASSWORD"]

RECIPIENTS = [
    EMAIL,
    "studypoint.gulati@gmail.com"
]

today = datetime.now().strftime("%d-%m-%Y")

msg = EmailMessage()

msg["Subject"] = f"📈 Daily Breakout Scan | {len(positive_breakout_data)} Stocks"
msg["From"] = EMAIL
msg["To"] = ", ".join(RECIPIENTS)

if positive_breakout_data.empty:

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">

        <h2>📈 Daily Positive Breakout Report</h2>

        <p><b>Date:</b> {today}</p>

        <p style="font-size:16px;color:red;">
            No new positive breakout stocks today.
        </p>

        <hr>

        <p style="color:gray;font-size:12px;">
            Generated automatically via GitHub Actions
        </p>

    </body>
    </html>
    """

else:

    table_html = positive_breakout_data.round(2).to_html(
        index=False,
        border=0,
        classes="stock-table"
    )

    html = f"""
    <html>

    <head>

    <style>

    body {{
        font-family: Arial, sans-serif;
        margin: 25px;
        font-size: 14px;
    }}

    h2 {{
        color: #0d6efd;
    }}

    table.stock-table {{
        border-collapse: collapse;
        width: 100%;
    }}

    table.stock-table th {{
        background-color: #0d6efd;
        color: white;
        padding: 10px;
        border: 1px solid #ddd;
    }}

    table.stock-table td {{
        padding: 8px;
        border: 1px solid #ddd;
        text-align: center;
    }}

    table.stock-table tr:nth-child(even) {{
        background-color: #f8f8f8;
    }}

    </style>

    </head>

    <body>

        <h2>📈 Daily Positive Breakout Report</h2>

        <p><b>Date:</b> {today}</p>

        <p>
            <b>Total Positive Breakouts:</b> {len(positive_breakout_data)}
        </p>

        {table_html}

        <br>

        <hr>

        <p style="color:gray;font-size:12px;">
            Generated automatically via GitHub Actions
        </p>

    </body>

    </html>
    """

# Plain-text fallback
msg.set_content(
    f"Daily Positive Breakout Report\n"
    f"Date: {today}\n"
    f"Total Breakouts: {len(positive_breakout_data)}"
)

# HTML version
msg.add_alternative(html, subtype="html")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL, APP_PASSWORD)
    smtp.send_message(msg)

print("✅ Email sent successfully!")