import streamlit as st
import investpy as inv
import datetime
import time
import history as hist
import bollinger_bands as bollinger

tickers = inv.get_stocks_list("brazil")
st.set_page_config(
    page_title="DataViz",
    page_icon=":bar_chart:",
    layout="wide"
)
#region Sidebar
with st.sidebar:
    ticker = st.selectbox(
        "Select the Action or Real Estate Fund",
        tickers
    )
    date_reference = st.date_input(
        "Select a init of period",
        datetime.datetime.today()
    )
    default_number_of_days = 30
    number_of_days = st.number_input("Inser a number of days", value=default_number_of_days)
    sleep_time = st.select_slider(
        "Select update time (seconds)",
        options=[5, 10, 15, 30, 60]
    )
    init_date = date_reference + datetime.timedelta(days=-(default_number_of_days + number_of_days))
    end_date = date_reference

    toggle_column1, toggle_column2 = st.columns([0.6,0.4])
    with toggle_column1:
        toggle = False
        toggle = st.toggle(f"Auto Refresh ({sleep_time})", value=False)
    with toggle_column2:
        if toggle:
            st.write("Activated!")
#endregion

#region Graph
def prepare_history_visualization():
    history, instance = hist.get(ticker, init_date, end_date)
    print("Current price ->", history['Close'].iat[-1])
    bollinger_figure = bollinger.get(ticker, history)
    current_value.metric("Current Value", f"R$ {round(history['Close'][history.index.max()], 2)}", f"{round((history['Close'][history.index.max()] / history['Close'][history.index[-2]] - 1) * 100,2)}")
    min_value.metric("Min Value", f"R$ {round(history['Close'].min(), 2)}", f"{round((history['Close'].min() / history['Close'][history.index.max()] - 1) * 100,2)}%")
    max_value.metric("Min Value", f"R$ {round(history['Close'].max(), 2)}", f"{round((history['Close'].max() / history['Close'][history.index.min()] - 1) * 100,2)}%")
    graph.plotly_chart(bollinger_figure, use_container_width=True, sharing="streamlit")

if ticker and sleep_time:
    col1, col2, col3 = st.columns(3)
    with col1:
        current_value = st.empty()
    with col2:
        min_value = st.empty()
    with col3:
        max_value = st.empty()
    graph = st.empty()

    while toggle:
        prepare_history_visualization()
        time.sleep(sleep_time)
    else:
        prepare_history_visualization()
#endregion