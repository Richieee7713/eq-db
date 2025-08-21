# app.py
import streamlit as st
import pandas as pd
from datetime import date
from energyquantified import EnergyQuantified
from energyquantified.metadata import Aggregation
from energyquantified.time import Frequency


# 读取 API 密钥（建议用 secrets）
API_KEY = st.secrets["eq_api_key"]

st.set_page_config(page_title="🇩🇪 DE Electricity Price Viewer", layout="wide")
st.title("⚡ DE DA Auction Dashboard")
st.caption("Resource: Energy Quantified (EPEX Spot)")

# 初始化 EQ 对象
eq = EnergyQuantified(api_key=API_KEY)

# 日期选择器（默认 2022-01-01 至今天）
col1, col2 = st.columns(2)
with col1:
    begin_date = st.date_input("Start Date", date(2022, 1, 1))
with col2:
    end_date = st.date_input("End Date", date.today())

# 加载数据
@st.cache_data(show_spinner=True)
def load_data(begin, end):
    ts = eq.timeseries.load(
        'DE Price Spot EUR/MWh EPEX H Actual',
        begin=begin,
        end=end,
        frequency=Frequency.PTHW,
        aggregation=Aggregation.MEAN,
        threshold=0
    ).to_pandas_dataframe()

    df = ts.copy()
    df.columns = [col[0] for col in df.columns]
    df.reset_index(inplace=True)
    return df

try:
    df = load_data(begin_date, end_date)
    st.success(f"✅ Loading {len(df)}")
    st.dataframe(df.head())

    # 可视化
    import plotly.express as px
    fig = px.line(df, x="start", y="value", title="DE Electricity Price (EUR/MWh)")
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"❌ Fail to load the data: {e}")
