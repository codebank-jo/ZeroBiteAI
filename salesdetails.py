import gradio as gr  # Import Gradio for building the UI
import pandas as pd  # Import pandas for data manipulation
import json  # Import json for reading JSON files
import os  # Import os for file path operations

def load_sales_details(filter_text="", date_filter=None, page=1, page_size=10):
    # Construct the path to the sales.json file
    json_path = os.path.join(os.path.dirname(__file__), "data", "sales.json")
    # Open and load the JSON data
    with open(json_path, "r", encoding="utf-8") as f:
        sales_data = json.load(f)["daily_sales"]

    # Flatten sales data into a list of rows for DataFrame
    rows = []
    for day in sales_data:
        for item in day["items_sold"]:
            rows.append({
                "date": day["date"],  # Date of sale
                "menuitem": item["menuitem"],  # Name of menu item
                "quantity_sold": item["quantity_sold"],  # Quantity sold
                "total_sales_gbp": item["total_sales_gbp"]  # Total sales in GBP
            })
    df = pd.DataFrame(rows)  # Create DataFrame from rows

    # Filter by menu item text if provided
    if filter_text:
        df = df[df["menuitem"].str.contains(filter_text, case=False)]
    # Filter by date if provided
    if date_filter:
        df = df[df["date"] == date_filter]

    total = len(df)  # Total number of filtered rows
    max_page = max(1, -(-total // page_size))  # Calculate max number of pages (ceiling division)
    start = (page - 1) * page_size  # Start index for pagination
    end = start + page_size  # End index for pagination
    df_page = df.iloc[start:end].copy()  # Get the current page of data
    return df_page, total, max_page, df  # Return page, total, max_page, and full filtered DataFrame

def plot_quantity_trend(df):
    import matplotlib.pyplot as plt  # Import matplotlib for plotting
    plt.style.use("dark_background")  # Use dark background style
    if df.empty:
        # If DataFrame is empty, show "No data to display"
        fig, ax = plt.subplots(figsize=(12, 3))  # Set figure size
        ax.text(0.5, 0.5, "No data to display", ha="center", va="center", fontsize=12, color="white")
        ax.set_axis_off()
        plt.close(fig)
        return fig
    # Group by date and menuitem, sum quantity sold
    df_trend = df.groupby(["date", "menuitem"])["quantity_sold"].sum().reset_index()
    # Pivot for plotting: dates as index, menuitems as columns
    pivot = df_trend.pivot(index="date", columns="menuitem", values="quantity_sold").fillna(0)
    fig, ax = plt.subplots(figsize=(12, 3))  # Set figure size
    pivot.plot(ax=ax, marker="o")  # Plot the trend lines
    ax.set_title("Quantity Sold per Item by Date", color="white")  # Set plot title
    ax.set_xlabel("Date", color="white")  # Set x-axis label
    ax.set_ylabel("Quantity Sold", color="white")  # Set y-axis label
    ax.tick_params(axis='x', colors='white', rotation=30)  # Style x-axis ticks
    ax.tick_params(axis='y', colors='white')  # Style y-axis ticks
    plt.legend(title="Menu Item", loc="upper left", fontsize=8)  # Add legend
    plt.tight_layout()  # Adjust layout
    plt.close(fig)  # Close figure to prevent duplicate display
    return fig  # Return the figure

def sales_details_content():
    # Construct the path to the sales.json file
    json_path = os.path.join(os.path.dirname(__file__), "data", "sales.json")
    # Open and load the JSON data
    with open(json_path, "r", encoding="utf-8") as f:
        sales_data = json.load(f)["daily_sales"]
    # Get all unique dates for the dropdown filter
    all_dates = sorted({day["date"] for day in sales_data})

    # Start building the Gradio Blocks UI
    with gr.Blocks(title="Sales Details") as demo:
        gr.Markdown("### Sales Details")  # Section title
        with gr.Row():
            # Textbox for filtering by menu item
            filter_box = gr.Textbox(label="Search by Menu Item", placeholder="Type to filter...", scale=3)
            # Dropdown for filtering by date
            date_filter = gr.Dropdown(
                choices=[""] + all_dates,  # Empty string for no filter
                label="Filter by Date",
                value="",
                scale=1
            )
            # Number input for page navigation
            page_number = gr.Number(value=1, label="Page", precision=0, minimum=1, scale=1)
            # Button to refresh data
            refresh_btn = gr.Button("🔄 Refresh Data", scale=1)
        # Dataframe to display sales details
        data_table = gr.Dataframe(
            value=load_sales_details()[0],  # Initial data
            interactive=False,
            label="Sales Details Table",
            render=True,
            datatype=["str", "str", "int", "float"],
            elem_classes="full-width"
        )
        # Plot to display quantity trend
        trend_graph = gr.Plot(plot_quantity_trend(load_sales_details()[3]), elem_classes="full-width")

        # Function to update table and plot based on filters and page
        def update_table(filter_text, date_filter_val, page):
            try:
                page = int(page)  # Ensure page is integer
            except Exception:
                page = 1
            date_val = date_filter_val if date_filter_val else None  # Handle empty date filter
            df_page, total, max_page, df_all = load_sales_details(filter_text, date_val, page)
            page = min(max(1, page), max_page)  # Clamp page number to valid range
            return (
                df_page,  # Updated page of data
                gr.update(minimum=1, maximum=max_page, value=page),  # Update page number control
                plot_quantity_trend(df_all)  # Updated plot
            )

        # Update table and plot when filter text changes (reset to page 1)
        filter_box.change(
            lambda filter_text, date_filter_val, page: update_table(filter_text, date_filter_val, 1),
            [filter_box, date_filter, page_number],
            [data_table, page_number, trend_graph]
        )
        # Update table and plot when date filter changes (reset to page 1)
        date_filter.change(
            lambda date_filter_val, filter_text, page: update_table(filter_text, date_filter_val, 1),
            [date_filter, filter_box, page_number],
            [data_table, page_number, trend_graph]
        )
        # Update table and plot when page number changes
        page_number.change(
            update_table,
            [filter_box, date_filter, page_number],
            [data_table, page_number, trend_graph]
        )
        # Refresh button reloads data with current filters and page
        refresh_btn.click(
            lambda: update_table(filter_box.value, date_filter.value, page_number.value),
            [],
            [data_table, page_number, trend_graph]
        )
    return demo  # Return the Gradio Blocks app