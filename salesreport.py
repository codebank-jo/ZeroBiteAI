import gradio as gr                # Import Gradio for UI components
import pandas as pd                # Import pandas for data manipulation
import json                        # Import json for reading JSON files
import os                          # Import os for file path operations
import matplotlib.pyplot as plt    # Import matplotlib for plotting

def load_sales_trend():
    # Build the path to the sales.json file in the data directory
    json_path = os.path.join(os.path.dirname(__file__), "data", "sales.json")
    # Open and load the JSON data
    with open(json_path, "r", encoding="utf-8") as f:
        sales_data = json.load(f)["daily_sales"]
    # Create a DataFrame for daily sales trend
    df_trend = pd.DataFrame([
        {"date": day["date"], "total_sales_gbp": day["total_sales_gbp"]}
        for day in sales_data
    ])
    # Convert date column to datetime
    df_trend["date"] = pd.to_datetime(df_trend["date"])
    # Sort the DataFrame by date
    df_trend = df_trend.sort_values("date")

    # Flatten all items_sold for all days into a list of dicts
    items = []
    for day in sales_data:
        for item in day["items_sold"]:
            items.append({
                "date": day["date"],
                "menuitem": item["menuitem"],
                "quantity_sold": item["quantity_sold"],
                "total_sales_gbp": item["total_sales_gbp"]
            })
    # Create a DataFrame for items sold
    df_items = pd.DataFrame(items)
    # Convert date column to datetime
    df_items["date"] = pd.to_datetime(df_items["date"])
    return df_trend, df_items

def plot_pie(top_items):
    plt.style.use("dark_background")  # Use dark background style for plot
    fig, ax = plt.subplots(figsize=(4, 2))  # Create a figure and axis
    wedges, texts, autotexts = ax.pie(
        top_items["quantity_sold"],         # Data for pie slices
        labels=top_items["menuitem"],       # Labels for each slice
        autopct='%1.1f%%',                  # Display percentage on slices
        startangle=140,                     # Start angle for pie chart
        textprops=dict(color="white")       # Text color for labels
    )
    ax.set_title("Most Purchased Items (by Quantity)", color="white")  # Set plot title
    for text in texts:
        text.set_color("white")             # Set label color to white
    for autotext in autotexts:
        autotext.set_color("white")         # Set percentage text color to white
    fig.patch.set_facecolor("#222")         # Set figure background color
    return fig

def plot_bar(top5):
    plt.style.use("dark_background")        # Use dark background style
    fig, ax = plt.subplots(figsize=(4, 2))  # Create a figure and axis
    ax.bar(top5["menuitem"], top5["quantity_sold"], color="skyblue")  # Bar plot
    ax.set_title("Top 5 Items by Quantity Sold", color="white")        # Set plot title
    ax.set_xlabel("Menu Item", color="white")                         # X-axis label
    ax.set_ylabel("Quantity Sold", color="white")                     # Y-axis label
    ax.tick_params(axis='x', colors='white')                          # X-axis tick color
    ax.tick_params(axis='y', colors='white')                          # Y-axis tick color
    plt.xticks(rotation=30, ha="right", color="white")                # Rotate x-ticks
    plt.yticks(color="white")                                         # Y-tick color
    fig.patch.set_facecolor("#222")                                   # Set figure background color
    return fig

def plot_trending_day(df_trend):
    plt.style.use("dark_background")        # Use dark background style
    fig, ax = plt.subplots(figsize=(4, 2))  # Create a figure and axis
    ax.bar(df_trend["date"].dt.strftime("%Y-%m-%d"), df_trend["total_sales_gbp"], color="orange")  # Bar plot
    ax.set_title("Trending Sales Day", color="white")                # Set plot title
    ax.set_xlabel("Date", color="white")                             # X-axis label
    ax.set_ylabel("Total Sales (GBP)", color="white")                # Y-axis label
    ax.tick_params(axis='x', colors='white')                         # X-axis tick color
    ax.tick_params(axis='y', colors='white')                         # Y-axis tick color
    plt.xticks(rotation=30, ha="right", color="white")               # Rotate x-ticks
    plt.yticks(color="white")                                        # Y-tick color
    fig.patch.set_facecolor("#222")                                  # Set figure background color
    return fig

def sales_trend_content():
    df_trend, df_items = load_sales_trend()
    with gr.Blocks() as demo:
        with gr.Row():
            gr.Markdown("### Daily Sales Trend (Last 7 Days)")
        with gr.Row():
            gr.LinePlot(
                value=df_trend,
                x="date",
                y="total_sales_gbp",
                title="Total Sales (GBP) per Day",
                x_title="Date",
                y_title="Total Sales (GBP)",
                tooltip=["date", "total_sales_gbp"],
                width=900,
                height=350,
            )
        with gr.Row():
            with gr.Column():
                top_items = df_items.groupby("menuitem")["quantity_sold"].sum().reset_index()
                gr.Plot(plot_pie(top_items))
            with gr.Column():
                top5 = top_items.sort_values("quantity_sold", ascending=False).head(5)
                gr.Plot(plot_bar(top5))
            with gr.Column():
                gr.Plot(plot_trending_day(df_trend))
    return demo
