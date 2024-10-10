import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

from src.task3.statistics_calculator import calculate_statistics


def get_yesterday():
    return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')


def make_colourful(val):
    if (val == 0): return
    color = 'red' if val < 0 else 'green'
    return f'color: {color}'


def display_statistics(hourly_stats):

    hourly_data = {
        "Hour": [],
        "Number of Trades": [],
        "Total Buy [MW]": [],
        "Total Sell [MW]": [],
        "PnL [Eur]": []
    }

    for hour, stat in hourly_stats.items():
        if hour != "Total":
            hourly_data["Hour"].append(stat.current_hour)
            hourly_data["Number of Trades"].append(stat.num_trades)
            hourly_data["Total Buy [MW]"].append(stat.num_buy)
            hourly_data["Total Sell [MW]"].append(stat.num_sell)
            hourly_data["PnL [Eur]"].append(stat.pnl)

    df_hourly = pd.DataFrame(hourly_data)

    styled_df = df_hourly.style.applymap(make_colourful, subset=['PnL [Eur]'])

    st.write("### Hourly Statistics")
    st.dataframe(styled_df)  # Display styled dataframe

    total_stat = hourly_stats["Total"]
    st.write("### Total Statistics")
    st.write(f"Total Trades: {total_stat.num_trades}")
    st.write(f"Total Buy [MW]: {total_stat.num_buy}")
    st.write(f"Total Sell [MW]: {total_stat.num_sell}")
    st.write(f"Total PnL [Eur]: {total_stat.pnl}")


def display():

    st.title("Trader Statistics Dashboard")

    trader_id = st.text_input("Enter Trader ID", value="trader_1")
    date = st.date_input("Select Date", value=datetime.now() - timedelta(days=1))

    formatted_date = date.strftime('%Y-%m-%d')

    if st.button("Get Statistics"):
        hourly_stats, daily_stats = calculate_statistics(trader_id, formatted_date, formatted_date)
        display_statistics(hourly_stats)


display()