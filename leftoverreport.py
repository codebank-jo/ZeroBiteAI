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
        waste_data = json.load(f)["leftover"]  # <-- FIXED KEY HERE
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

def add_estimated_loss_gbp(df):
    if df.empty or "menuitem" not in df.columns or "wasted_quantity" not in df.columns:
        return df
    # Load menu price map here to avoid NameError
    menu_path = os.path.join(os.path.dirname(__file__), "data", "menu.json")
    with open(menu_path, "r", encoding="utf-8") as f:
        menu_price_map = {item["menuitem"]: float(item["price"]) for item in json.load(f)["menu"]}
    df = df.copy()
    df["estimated_loss_gbp"] = df.apply(
        lambda row: menu_price_map.get(row["menuitem"], 0) * row.get("wasted_quantity", 0), axis=1
    )
    return df

def plot_loss_per_item(df):
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(8, 4))
    # Check for empty DataFrame or missing columns
    if df.empty or "menuitem" not in df.columns or "sold_quantity" not in df.columns or "wasted_quantity" not in df.columns:
        ax.text(0.5, 0.5, "No data to display", ha="center", va="center", fontsize=12, color="white")
        ax.set_axis_off()
        plt.close(fig)
        return fig
    grouped = df.groupby("menuitem")[["sold_quantity", "wasted_quantity"]].sum()
    if grouped.empty:
        ax.text(0.5, 0.5, "No data to display", ha="center", va="center", fontsize=12, color="white")
        ax.set_axis_off()
        plt.close(fig)
        return fig
    grouped.plot(kind="bar", ax=ax, color=["#00FF88", "#FFA500"])
    ax.set_ylabel("Quantity", color="white")
    ax.set_title("Sold vs Wasted Quantity per Menu Item", color="white")
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.xticks(rotation=30, ha="right", fontsize=10, color="white")
    plt.yticks(color="white")
    plt.tight_layout()
    plt.close(fig)
    return fig

def plot_loss_by_date(df):
    import matplotlib.pyplot as plt
    import os
    import json

    # Load menu prices
    menu_path = os.path.join(os.path.dirname(__file__), "data", "menu.json")
    with open(menu_path, "r", encoding="utf-8") as f:
        menu_price_map = {item["menuitem"]: float(item["price"]) for item in json.load(f)["menu"]}

    # If df is empty, reload from leftover.json to ensure we have all data
    if df.empty or "menuitem" not in df.columns or "date" not in df.columns or "wasted_quantity" not in df.columns:
        leftover_path = os.path.join(os.path.dirname(__file__), "data", "leftover.json")
        with open(leftover_path, "r", encoding="utf-8") as f:
            waste_data = json.load(f)["leftover"]
        df = pd.DataFrame(waste_data)
        if df.empty or "menuitem" not in df.columns or "date" not in df.columns or "wasted_quantity" not in df.columns:
            # Still empty, show no data
            plt.style.use("dark_background")
            fig, ax = plt.subplots(figsize=(8, 3))
            ax.text(0.5, 0.5, "No data to display", ha="center", va="center", fontsize=12, color="white")
            ax.set_axis_off()
            plt.close(fig)
            return fig

    # Calculate estimated loss per row
    df = df.copy()
    df["estimated_loss_gbp"] = df.apply(
        lambda row: menu_price_map.get(row["menuitem"], 0) * row.get("wasted_quantity", 0), axis=1
    )

    # Group by date and menuitem
    grouped = df.groupby(["date", "menuitem"])["estimated_loss_gbp"].sum().reset_index()

    if grouped.empty:
        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.text(0.5, 0.5, "No data to display", ha="center", va="center", fontsize=12, color="white")
        ax.set_axis_off()
        plt.close(fig)
        return fig

    # Pivot for plotting: dates as x, menuitems as lines/bars
    pivot = grouped.pivot(index="date", columns="menuitem", values="estimated_loss_gbp").fillna(0)

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(10, 5))
    pivot.plot(ax=ax, kind="bar", stacked=True, colormap="tab20")

    ax.set_ylabel("Estimated Loss (GBP)", color="white")
    ax.set_title("Estimated Loss by Item and Date", color="white")
    ax.tick_params(axis='x', colors='white', rotation=30)
    ax.tick_params(axis='y', colors='white')
    plt.xticks(fontsize=10, color="white")
    plt.yticks(color="white")
    plt.tight_layout()
    plt.close(fig)
    return fig

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
                choices=[""] + sorted(list({row["date"] for row in json.load(open(os.path.join(os.path.dirname(__file__), "data", "leftover.json"), encoding="utf-8"))["leftover"]})),
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