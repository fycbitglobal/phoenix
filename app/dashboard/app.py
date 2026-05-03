# app/dashboard/app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import numpy as np

st.set_page_config(
    page_title="MTO Trading OS", 
    page_icon="🚀", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0b0e11;
        color: #ffffff;
    }
    [data-testid="stSidebar"] {
        background-color: #131722;
        border-right: 1px solid #2d313d;
    }
    .strategy-card {
        background-color: #1e222d;
        border: 1px solid #363a45;
        border-radius: 12px;
        padding: 20px;
        margin: 10px;
        transition: transform 0.3s ease;
        cursor: pointer;
    }
    .strategy-card:hover {
        transform: translateY(-5px);
        border-color: #00ffcc;
    }
    .metric-label { color: #808a9d; font-size: 12px; text-transform: uppercase; }
    .metric-value { color: #ffffff; font-size: 20px; font-weight: bold; }
    .roi-positive { color: #00ffcc; font-weight: bold; }
    .roi-negative { color: #ff4d4d; font-weight: bold; }
    .stButton>button {
        background-color: #222222;
        color: white;
        border-radius: 8px;
        border: 1px solid #363a45;
    }
    </style>
    """, unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000"

def fetch_data(endpoint):
    try:
        r = requests.get(f"{API_URL}/{endpoint}", timeout=1)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

with st.sidebar:
    st.markdown("### 🚀 MTO OS")
    st.markdown("---")
    st.markdown("🏠 **Dashboard**")
    st.markdown("💼 My Portfolio")
    st.markdown("📡 Signal Bot")
    st.markdown("📉 DCA Bot")
    st.markdown("⛓️ Grid Bot")
    st.markdown("🖥️ Terminal")
    st.markdown("---")
    st.markdown("👥 Invite Friends")
    st.markdown("📜 Subscriptions")

top_col1, top_col2, top_col3, top_col4 = st.columns(4)
pnl_data = fetch_data("pnl")
total_pnl = pnl_data['total_pnl'] if pnl_data else 0.0

with top_col1:
    st.markdown('<div class="metric-label">Sanal Bakiye</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">10,000.00 USDT</div>', unsafe_allow_html=True) # DÜZELTME: unsafe_allow_html=True olmalı

# Yukarıdaki satırdaki hatayı hemen düzeltiyorum:
with top_col1:
    st.markdown('<div class="metric-label">Sanal Bakiye</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">10,000.00 USDT</div>', unsafe_allow_html=True)

with top_col2:
    st.markdown('<div class="metric-label">Toplam Kar/Zarar</div>', unsafe_allow_html=True)
    color = "roi-positive" if total_pnl >= 0 else "roi-negative"
    st.markdown(f'<div class="metric-value {color}">{total_pnl:.2f} USDT</div>', unsafe_allow_html=True)

with top_col3:
    st.markdown('<div class="metric-label">Sistem Durumu</div>', unsafe_allow_html=True)
    api_status = fetch_data("/")
    status_text = "Aktif ✅" if api_status else "Kesik ❌"
    st.markdown(f'<div class="metric-value">{status_text}</div>', unsafe_allow_html=True)

with top_col4:
    st.markdown('<div class="metric-label">Aktif Pozisyonlar</div>', unsafe_allow_html=True)
    # Düzeltme:
    st.markdown('<div class="metric-label">Aktif Pozisyonlar</div>', unsafe_allow_html=True)
    pos_data = fetch_data("positions")
    pos_count = len(pos_data) if pos_data else 0
    st.markdown(f'<div class="metric-value">{pos_count} Adet</div>', unsafe_allow_html=True)

st.markdown("---")
st.subheader("Top Strategies")
st.markdown("Sistem tarafından otomatik optimize edilen en iyi stratejiler.")

strategies = [
    {"name": "SMC_BOS_Sinyal", "symbol": "SOL/USDT", "roi": "149.45%", "drawdown": "-18.99%", "type": "LONG SPOT"},
    {"name": "Trend_EMA_Follow", "symbol": "BTC/USDT", "roi": "70.73%", "drawdown": "-9.52%", "type": "LONG SPOT"},
    {"name": "Volatility_Squeeze", "symbol": "ETH/USDT", "roi": "65.5%", "drawdown": "-11.79%", "type": "LONG SPOT"},
]

cols = st.columns(3)
for i, strat in enumerate(strategies):
    with cols[i]:
        st.markdown(f"""
            <div class="strategy-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #808a9d; font-size: 14px;">{strat['type']}</span>
                    <span style="color: #00ffcc; font-weight: bold;">{strat['roi']}</span>
                </div>
                <div style="font-size: 18px; font-weight: bold; margin: 10px 0;">{strat['symbol']}</div>
                <div style="color: #808a9d; font-size: 12px; margin-bottom: 15px;">
                    Max Drawdown: <span style="color: #ff4d4d;">{strat['drawdown']}</span>
                </div>
                <button style="width: 100%; background: #363a45; color: white; border: none; padding: 8px; border-radius: 5px; cursor: pointer;">
                    Copy Bot
                </button>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")
col_main, col_side = st.columns([2, 1])

with col_main:
    st.subheader("Canli Analiz ve Grafik")
    symbol = st.selectbox("Sembol Secin", ["BTCUSDT", "ETHUSDT", "SOLUSDT"], index=0)
    price_data = fetch_data(f"price/{symbol}")
    if price_data:
        st.markdown(f"### {symbol} Guncel Fiyat: `{price_data['price']:.2f} USDT`")
        dates = pd.date_range(start="2023-01-01", periods=30, freq='D')
        df = pd.DataFrame({
            'Date': dates,
            'Open': np.random.uniform(60000, 61000, 30),
            'High': np.random.uniform(61000, 62000, 30),
            'Low': np.random.uniform(59000, 60000, 30),
            'Close': np.random.uniform(60000, 61000, 30)
        })
        fig = go.Figure(data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Fiyat verisi alinamadi.")

with col_side:
    st.subheader("Acik Pozisyonlar")
    pos_data = fetch_data("positions")
    if pos_data:
        df_pos = pd.DataFrame(pos_data)
        st.dataframe(df_pos, hide_index=True, use_container_width=True)
    else:
        st.info("Aktif pozisyon bulunmuyor.")
