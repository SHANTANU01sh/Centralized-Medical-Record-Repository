import pandas as pd
import sqlite3
import plotly.express as px

def fetch_metrics(username, metric_name, db_path="data/user_data.db"):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(
        "SELECT date, metric_value FROM metrics WHERE username=? AND metric_name=? ORDER BY date ASC",
        conn, params=(username, metric_name)
    )
    conn.close()
    return df

def plot_metric_trend(df, metric_name):
    if df.empty:
        return None
    fig = px.line(df, x='date', y='metric_value', title=f"{metric_name} Trend Over Time")
    fig.update_xaxes(rangeslider_visible=True)
    return fig
