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
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(4, 3))
    wedges, texts, autotexts = ax.pie(
        top_items["quantity_sold"],
        labels=top_items["menuitem"],
        autopct='%1.1f%%',
        startangle=140,
        textprops=dict(color="white")
    )
    ax.set_title("Most Purchased Items (by Quantity)", color="white")
    for text in texts:
        text.set_color("white")
    for autotext in autotexts:
        autotext.set_color("white")
    fig.patch.set_facecolor("#222")
    return fig

def plot_bar(top5):
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(top5["menuitem"], top5["quantity_sold"], color="skyblue")
    ax.set_title("Top 5 Items by Quantity Sold", color="white")
    ax.set_xlabel("Menu Item", color="white")
    ax.set_ylabel("Quantity Sold", color="white")
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.xticks(rotation=30, ha="right", color="white")
    plt.yticks(color="white")
    fig.patch.set_facecolor("#222")
    return fig

def plot_trending_day(df_trend):
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(df_trend["date"].dt.strftime("%Y-%m-%d"), df_trend["total_sales_gbp"], color="orange")
    ax.set_title("Trending Sales Day", color="white")
    ax.set_xlabel("Date", color="white")
    ax.set_ylabel("Total Sales (GBP)", color="white")
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.xticks(rotation=30, ha="right", color="white")
    plt.yticks(color="white")
    fig.patch.set_facecolor("#222")
    return fig

def sales_trend_content():
    # Load sales trend and items data
    df_trend, df_items = load_sales_trend()
    # Create a row for the daily sales trend title
    with gr.Row():
        gr.Markdown("### Daily Sales Trend (Last 7 Days)")
    # Display a line plot of total sales per day
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
    # Create a row for the three plots
    with gr.Row():
        with gr.Column():
            # Group items by menuitem and sum quantity sold
            top_items = df_items.groupby("menuitem")["quantity_sold"].sum().reset_index()
            # Display pie chart of most purchased items
            gr.Plot(plot_pie(top_items))
        with gr.Column():
            # Get top 5 items by quantity sold
            top5 = top_items.sort_values("quantity_sold", ascending=False).head(5)
            # Display bar chart of top 5 items
            gr.Plot(plot_bar(top5))
        with gr.Column():
            # Display bar chart of daily sales trend
            gr.Plot(plot_trending_day(df_trend))
