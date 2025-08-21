import streamlit as st
import pandas as pd
from datetime import date
from energyquantified import EnergyQuantified
from energyquantified.metadata import Aggregation
from energyquantified.time import Frequency

st.set_page_config(page_title="⚡ 德国电价 Dashboard", layout="wide")
st.title("🇩🇪 DE Electricity Price Viewer")
st.caption("数据源：Energy Quantified (EPEX Spot)")

# 日期选择器
col1, col2 = st.columns(2)
with col1:
    begin_date = st.date_input("起始日期", date(2022, 1, 1))
with col2:
    end_date = st.date_input("结束日期", date.today())

# ✅ 改成函数中初始化 EQ
@st.cache_data(show_spinner=True)
def load_data(begin, end):
    eq = EnergyQuantified(api_key=st.secrets["eq_api_key"])  # ✅ 放在函数内！
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
    st.success(f"✅ 共加载 {len(df)} 行数据")
    st.dataframe(df.head())

    import plotly.express as px
    fig = px.line(df, x="start", y="value", title="DE Electricity Price (EUR/MWh)")
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"❌ 数据加载失败: {e}")
