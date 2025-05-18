import gradio as gr  # Import Gradio for UI components
import pandas as pd  # Import pandas for data manipulation
import json  # Import json for reading JSON files
import os  # Import os for file path operations
import matplotlib.pyplot as plt  # Import matplotlib for plotting

def load_leftover(filter_text="", date_filter=None, page=1, page_size=10):
    # Build the path to the leftover.json data file
    json_path = os.path.join(os.path.dirname(__file__), "data", "leftover.json")
    # Open and load the JSON data
    with open(json_path, "r", encoding="utf-8") as f:
        waste_data = json.load(f)["food_waste"]
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(waste_data)
    # Filter by menu item or waste reason if filter_text is provided
    if filter_text:
        df = df[df["menuitem"].str.contains(filter_text, case=False) | df["waste_reason"].str.contains(filter_text, case=False)]
    # Filter by date if date_filter is provided
    if date_filter:
        df = df[df["date"] == date_filter]
    # Calculate total number of filtered rows
    total = len(df)
    # Calculate the maximum number of pages
    max_page = max(1, -(-total // page_size))
    # Calculate start and end indices for pagination
    start = (page - 1) * page_size
    end = start + page_size
    # Get the current page of data
    df_page = df.iloc[start:end].copy()
    # Return the page, total count, max page, and the full filtered DataFrame
    return df_page, total, max_page, df

def plot_loss_per_item(df):
    plt.style.use("dark_background")  # Use dark background for the plot
    fig, ax = plt.subplots(figsize=(8, 3))  # Create a figure and axis
    # Group by menuitem and sum estimated loss, sort descending
    per_item = df.groupby("menuitem")["estimated_loss_gbp"].sum().sort_values(ascending=False)
    # If no data, display a message
    if per_item.empty:
        ax.text(0.5, 0.5, "No data to display", ha="center", va="center", fontsize=12, color="white")
        ax.set_axis_off()
        plt.close(fig)
        return fig
    # Plot the bar chart
    per_item.plot(kind="bar", ax=ax, color="#FFA500")  # orange bars
    ax.set_ylabel("GBP", color="white")  # Set y-axis label
    ax.set_title("Loss per Item", color="white")  # Set plot title
    ax.tick_params(axis='x', colors='white')  # Set x-axis tick color
    ax.tick_params(axis='y', colors='white')  # Set y-axis tick color
    plt.xticks(rotation=30, ha="right", fontsize=10, color="white")  # Rotate x-ticks
    plt.yticks(color="white")  # Set y-tick color
    # Annotate each bar with its value
    for i, v in enumerate(per_item):
        ax.text(i, v + 0.5, f"£{v:.2f}", ha="center", fontsize=9, color="white")
    plt.tight_layout()  # Adjust layout
    plt.close(fig)  # Close the figure to prevent duplicate display
    return fig  # Return the figure

def plot_loss_by_date(df):
    plt.style.use("dark_background")  # Use dark background for the plot
    fig, ax = plt.subplots(figsize=(8, 3))  # Create a figure and axis
    # Group by date and sum estimated loss, sort by date
    per_date = df.groupby("date")["estimated_loss_gbp"].sum().sort_index()
    # If no data, display a message
    if per_date.empty:
        ax.text(0.5, 0.5, "No data to display", ha="center", va="center", fontsize=12, color="white")
        ax.set_axis_off()
        plt.close(fig)
        return fig
    # Plot the line chart
    per_date.plot(kind="line", ax=ax, color="#00FF88", marker="o")
    ax.set_ylabel("GBP", color="white")  # Set y-axis label
    ax.set_title("Loss by Date", color="white")  # Set plot title
    ax.tick_params(axis='x', colors='white')  # Set x-axis tick color
    ax.tick_params(axis='y', colors='white')  # Set y-axis tick color
    plt.xticks(rotation=30, ha="right", fontsize=10, color="white")  # Rotate x-ticks
    plt.yticks(color="white")  # Set y-tick color
    # Annotate each point with its value
    for i, (date, v) in enumerate(per_date.items()):
        ax.text(i, v, f"£{v:.2f}", ha="center", va="bottom", fontsize=9, color="white")
    plt.tight_layout()  # Adjust layout
    plt.close(fig)  # Close the figure to prevent duplicate display
    return fig  # Return the figure

def leftover_report_content():
    # Create a Gradio Blocks interface with custom CSS
    with gr.Blocks(css=".gradio-container {max-width: 100vw !important; padding: 0;}") as demo:
        # Title markdown
        gr.Markdown("### Food Waste / Leftover Report", elem_id="title", elem_classes="full-width")
        with gr.Row():
            # Textbox for filtering by menu item or reason
            filter_box = gr.Textbox(label="Filter by Menu Item or Reason", placeholder="Type to filter...", scale=3)
            # Dropdown for filtering by date
            date_filter = gr.Dropdown(
                choices=[""] + sorted(list({row["date"] for row in json.load(open(os.path.join(os.path.dirname(__file__), "data", "leftover.json"), encoding="utf-8"))["food_waste"]})),
                label="Filter by Date",
                value="",
                scale=1
            )
            # Number input for page number
            page_number = gr.Number(value=1, label="Page", precision=0, minimum=1, scale=1)
            # Button to refresh data
            refresh_btn = gr.Button("🔄 Refresh Data", scale=1)
        # Dataframe to display the leftover table
        data_table = gr.Dataframe(
            value=load_leftover()[0],
            interactive=False,
            label="Leftover Table",
            render=True,
            datatype=["str"] * 7,
            elem_classes="full-width"
        )
        with gr.Row():
            # Plot for loss per item
            per_item_graph = gr.Plot(plot_loss_per_item(load_leftover()[3]), elem_classes="full-width")
            # Plot for loss by date
            per_date_graph = gr.Plot(plot_loss_by_date(load_leftover()[3]), elem_classes="full-width")

        # Function to update the table and plots based on filters and pagination
        def update_table(filter_text, date_filter_val, page):
            try:
                page = int(page)  # Ensure page is an integer
            except Exception:
                page = 1
            date_val = date_filter_val if date_filter_val else None  # Handle empty date filter
            # Load filtered and paginated data
            df_page, total, max_page, df_all = load_leftover(filter_text, date_val, page)
            page = min(max(1, page), max_page)  # Clamp page number within valid range
            # Return updated table, page number, and plots
            return (
                df_page,
                gr.update(minimum=1, maximum=max_page, value=page),
                plot_loss_per_item(df_all),
                plot_loss_by_date(df_all)
            )

        # Update table and plots when filter text changes (reset to page 1)
        filter_box.change(
            lambda filter_text, date_filter_val, page: update_table(filter_text, date_filter_val, 1),
            [filter_box, date_filter, page_number],
            [data_table, page_number, per_item_graph, per_date_graph]
        )
        # Update table and plots when date filter changes (reset to page 1)
        date_filter.change(
            lambda date_filter_val, filter_text, page: update_table(filter_text, date_filter_val, 1),
            [date_filter, filter_box, page_number],
            [data_table, page_number, per_item_graph, per_date_graph]
        )
        # Update table and plots when page number changes
        page_number.change(
            update_table,
            [filter_box, date_filter, page_number],
            [data_table, page_number, per_item_graph, per_date_graph]
        )
        # Refresh data when refresh button is clicked
        refresh_btn.click(
            lambda: update_table(filter_box.value, date_filter.value, page_number.value),
            [],
            [data_table, page_number, per_item_graph, per_date_graph]
        )
    return demo  # Return the Gradio Blocks interface