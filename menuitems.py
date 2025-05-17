import gradio as gr                # Import Gradio for UI components
import pandas as pd                # Import pandas for data manipulation
import json                        # Import json for reading JSON files
import os                          # Import os for file path operations

def load_menu(filter_text="", page=1, page_size=15):
    # Construct the path to the menu.json file in the data directory
    json_path = os.path.join(os.path.dirname(__file__), "data", "menu.json")
    # Open and load the JSON file containing menu data
    with open(json_path, "r", encoding="utf-8") as f:
        menu_data = json.load(f)["menu"]
    # Convert the menu data to a pandas DataFrame
    df = pd.DataFrame(menu_data)
    # If a filter is provided, filter rows by menuitem or type columns (case-insensitive)
    if filter_text:
        df = df[df["menuitem"].str.contains(filter_text, case=False) | df["type"].str.contains(filter_text, case=False)]
    # Calculate total number of filtered rows
    total = len(df)
    # Calculate the maximum number of pages based on page size
    max_page = max(1, -(-total // page_size))
    # Determine the start and end indices for the current page
    start = (page - 1) * page_size
    end = start + page_size
    # Select the rows for the current page
    df_page = df.iloc[start:end].copy()
    # If image_url column exists, move it to the first column and convert to markdown for image preview
    if "image_url" in df_page.columns:
        df_page.insert(0, "Image", df_page["image_url"].apply(lambda url: f"![img]({url})" if pd.notna(url) else ""))
        df_page = df_page.drop(columns=["image_url"])
    # Return the current page DataFrame, total rows, and max page number
    return df_page, total, max_page

def menu_list_content():
    # Create a row layout for filter and page number inputs
    with gr.Row():
        # Left column: filter textbox
        with gr.Column(scale=3):
            filter_box = gr.Textbox(label="Filter by Menu Item or Type", placeholder="Type to filter...")
        # Right column: page number input
        with gr.Column(scale=1):
            page_number = gr.Number(value=1, label="Page", precision=0, minimum=1)
    # Create a data table to display the menu, with the first column as markdown for images
    data_table = gr.Dataframe(
        value=load_menu()[0],
        interactive=False,
        label="Menu Table",
        render=True,
        datatype=["markdown"] + ["str"]*7  # First column is markdown for image
    )
    # Add a refresh button to reload data
    refresh_btn = gr.Button("🔄 Refresh Data")

    # Define a function to update the table based on filter and page number
    def update_table(filter_text, page):
        try:
            page = int(page)  # Ensure page is an integer
        except Exception:
            page = 1          # Default to page 1 if conversion fails
        df_page, total, max_page = load_menu(filter_text, page)  # Load filtered and paginated data
        page = min(max(1, page), max_page)                      # Clamp page number within valid range
        return df_page, gr.update(minimum=1, maximum=max_page, value=page)  # Return updated data and page control

    # When filter changes, update table and reset to page 1
    filter_box.change(
        lambda filter_text, page: update_table(filter_text, 1),
        [filter_box, page_number],
        [data_table, page_number]
    )
    # When page number changes, update table
    page_number.change(update_table, [filter_box, page_number], [data_table, page_number])
    # When refresh button is clicked, update table with current filter and page
    refresh_btn.click(lambda: update_table(filter_box.value, page_number.value), [], [data_table, page_number])

    # Return the data table and refresh button (for Gradio Blocks API)
    data_table
    refresh_btn