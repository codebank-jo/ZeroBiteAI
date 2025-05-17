import gradio as gr                # Import Gradio for UI components
import pandas as pd                # Import pandas for data manipulation
import json                        # Import json for reading JSON files
import os                          # Import os for file path operations
import matplotlib.pyplot as plt    # Import matplotlib for plotting

def load_leftover(filter_text="", date_filter=None, page=1, page_size=10):
    # Construct the path to the leftover.json file
    json_path = os.path.join(os.path.dirname(__file__), "data", "leftover.json")
    # Open and load the JSON data
    with open(json_path, "r", encoding="utf-8") as f:
        waste_data = json.load(f)["food_waste"]
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(waste_data)
    # Filter by menuitem or waste_reason if filter_text is provided
    if filter_text:
        df = df[df["menuitem"].str.contains(filter_text, case=False) | df["waste_reason"].str.contains(filter_text, case=False)]
    # Filter by date if date_filter is provided
    if date_filter:
        df = df[df["date"] == date_filter]
    total = len(df)  # Total number of filtered rows
    max_page = max(1, -(-total // page_size))  # Calculate max number of pages (ceiling division)
    start = (page - 1) * page_size  # Start index for pagination
    end = start + page_size         # End index for pagination
    df_page = df.iloc[start:end].copy()  # Get the current page of data
    return df_page, total, max_page, df  # Return page, total, max_page, and all filtered data

def plot_total_loss(df):
    fig, ax = plt.subplots(figsize=(3, 2))  # Create a small figure
    total_loss = df["estimated_loss_gbp"].sum()  # Sum the estimated loss
    if df.empty:
        # If no data, show a message
        ax.text(0.5, 0.5, "No data to display", ha="center", va="center", fontsize=10)
        ax.set_axis_off()
        plt.close(fig)
        return fig
    # Plot a single bar for total loss
    ax.bar(["Total Loss"], [total_loss], color="red")
    ax.set_ylabel("GBP")
    ax.set_title("Total Loss")
    # Annotate the bar with the value
    for i, v in enumerate([total_loss]):
        ax.text(i, v + 1, f"£{v:.2f}", ha="center", fontweight="bold", fontsize=9)
    plt.close(fig)
    return fig

def plot_loss_per_item(df):
    fig, ax = plt.subplots(figsize=(6, 3))  # Create a wider figure
    # Group by menuitem and sum the losses, sort descending
    per_item = df.groupby("menuitem")["estimated_loss_gbp"].sum().sort_values(ascending=False)
    if per_item.empty:
        # If no data, show a message
        ax.text(0.5, 0.5, "No data to display", ha="center", va="center", fontsize=12)
        ax.set_axis_off()
        plt.close(fig)
        return fig
    # Plot a bar chart for each menu item
    per_item.plot(kind="bar", ax=ax, color="orange")
    ax.set_ylabel("GBP")
    ax.set_title("Loss per Item")
    plt.xticks(rotation=30, ha="right", fontsize=10)
    # Annotate each bar with the value
    for i, v in enumerate(per_item):
        ax.text(i, v + 0.5, f"£{v:.2f}", ha="center", fontsize=9)
    plt.close(fig)
    return fig

def plot_loss_by_date(df):
    fig, ax = plt.subplots(figsize=(6, 3))  # Create a wider figure
    # Group by date and sum the losses
    per_date = df.groupby("date")["estimated_loss_gbp"].sum().sort_index()
    if per_date.empty:
        # If no data, show a message
        ax.text(0.5, 0.5, "No data to display", ha="center", va="center", fontsize=12)
        ax.set_axis_off()
        plt.close(fig)
        return fig
    # Plot a line chart for loss by date
    per_date.plot(kind="line", ax=ax, color="green", marker="o")
    ax.set_ylabel("GBP")
    ax.set_title("Loss by Date")
    plt.xticks(rotation=30, ha="right", fontsize=10)
    # Annotate each point with the value
    for i, (date, v) in enumerate(per_date.items()):
        ax.text(i, v, f"£{v:.2f}", ha="center", va="bottom", fontsize=9)
    plt.close(fig)
    return fig

def leftover_report_content():
    # Row for the report title
    with gr.Row():
        gr.Markdown("### Food Waste / Leftover Report")
    # Row for filters and pagination controls
    with gr.Row():
        with gr.Column(scale=2):
            filter_box = gr.Textbox(label="Filter by Menu Item or Reason", placeholder="Type to filter...")
        with gr.Column(scale=1):
            # Dropdown for date filter, populated from JSON file
            date_filter = gr.Dropdown(
                choices=[""] + sorted(list({row["date"] for row in json.load(open(os.path.join(os.path.dirname(__file__), "data", "leftover.json"), encoding="utf-8"))["food_waste"]})),
                label="Filter by Date",
                value=""
            )
        with gr.Column(scale=1):
            # Number input for page number
            page_number = gr.Number(value=1, label="Page", precision=0, minimum=1)
    # Data table to display the leftovers
    data_table = gr.Dataframe(
        value=load_leftover()[0],
        interactive=False,
        label="Leftover Table",
        render=True,
        datatype=["str"] * 7
    )
    # Button to refresh data
    refresh_btn = gr.Button("🔄 Refresh Data")

    # Graphs for loss per item and by date
    per_item_graph = gr.Plot(plot_loss_per_item(load_leftover()[3]))
    per_date_graph = gr.Plot(plot_loss_by_date(load_leftover()[3]))

    # Function to update table and graphs based on filters and pagination
    def update_table(filter_text, date_filter_val, page):
        try:
            page = int(page)
        except Exception:
            page = 1
        date_val = date_filter_val if date_filter_val else None
        df_page, total, max_page, df_all = load_leftover(filter_text, date_val, page)
        page = min(max(1, page), max_page)
        return (
            df_page,
            gr.update(minimum=1, maximum=max_page, value=page),
            plot_loss_per_item(df_all),
            plot_loss_by_date(df_all)
        )

    # Update table and graphs when filter text changes (reset to page 1)
    filter_box.change(
        lambda filter_text, date_filter_val, page: update_table(filter_text, date_filter_val, 1),
        [filter_box, date_filter, page_number],
        [data_table, page_number, per_item_graph, per_date_graph]
    )
    # Update table and graphs when date filter changes (reset to page 1)
    date_filter.change(
        lambda date_filter_val, filter_text, page: update_table(filter_text, date_filter_val, 1),
        [date_filter, filter_box, page_number],
        [data_table, page_number, per_item_graph, per_date_graph]
    )
    # Update table and graphs when page number changes
    page_number.change(
        update_table,
        [filter_box, date_filter, page_number],
        [data_table, page_number, per_item_graph, per_date_graph]
    )
    # Refresh button reloads data with current filters and page
    refresh_btn.click(
        lambda: update_table(filter_box.value, date_filter.value, page_number.value),
        [],
        [data_table, page_number, per_item_graph, per_date_graph]
    )

    # Display both graphs in a single row with two columns
    with gr.Row():
        with gr.Column(scale=1.1):
            per_item_graph
        with gr.Column(scale=1.1):
            per_date_graph

    # Display the data table and refresh button
    data_table
    refresh_btn