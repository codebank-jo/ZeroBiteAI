import gradio as gr
import pandas as pd
import json
import os

def load_sales_trend():
    json_path = os.path.join(os.path.dirname(__file__), "data", "sales.json")
    with open(json_path, "r", encoding="utf-8") as f:
        sales_data = json.load(f)["daily_sales"]
    df = pd.DataFrame([
        {"date": day["date"], "total_sales_gbp": day["total_sales_gbp"]}
        for day in sales_data
    ])
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    return df

def sales_trend_content():
    df = load_sales_trend()
    with gr.Row():
        gr.Markdown("### Daily Sales Trend (Last 7 Days)")
    gr.LinePlot(
        value=df,
        x="date",
        y="total_sales_gbp",
        title="Total Sales (GBP) per Day",
        x_title="Date",
        y_title="Total Sales (GBP)",
        tooltip=["date", "total_sales_gbp"],
        width=600,
        height=350,
    )
