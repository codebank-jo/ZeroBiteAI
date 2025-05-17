import gradio as gr                # Import Gradio for UI components
import pandas as pd                # Import pandas for data manipulation
from utils.data_loader import load_inventory   # Import custom function to load inventory data

def load_data(filter_text="", page=1, page_size=15):
    inventory_data = load_inventory()          # Load inventory data from external source
    df = pd.DataFrame(inventory_data)          # Convert data to pandas DataFrame
    # Filter
    if filter_text:
        # Filter rows where 'material' or 'type' contains the filter text (case-insensitive)
        df = df[df["material"].str.contains(filter_text, case=False) | df["type"].str.contains(filter_text, case=False)]
    # Pagination
    total = len(df)                            # Total number of filtered rows
    max_page = max(1, -(-total // page_size))  # Calculate max number of pages (ceiling division)
    start = (page - 1) * page_size             # Start index for current page
    end = start + page_size                    # End index for current page
    df_page = df.iloc[start:end]               # Slice DataFrame for current page
    return df_page, total, max_page            # Return page data, total rows, and max page

def inventory_list_content():
    with gr.Row():                            # Create a horizontal row layout
        with gr.Column(scale=3):              # First column (wider)
            filter_box = gr.Textbox(          # Textbox for filtering
                label="Filter by Material or Type", 
                placeholder="Type to filter..."
            )
        with gr.Column(scale=1):              # Second column (narrower)
            page_number = gr.Number(          # Number input for page selection
                value=1, 
                label="Page", 
                precision=0, 
                minimum=1
            )
    data_table = gr.Dataframe(                # Dataframe to display inventory data
        value=load_data()[0],                 # Initial value: first page of data
        interactive=False,                    # Table is not editable
        label="Inventory Table", 
        render=True
    )
    refresh_btn = gr.Button("🔄 Refresh Data") # Button to refresh data

    def update_table(filter_text, page):
        try:
            page = int(page)                  # Ensure page is integer
        except Exception:
            page = 1                          # Default to page 1 if conversion fails
        df_page, total, max_page = load_data(filter_text, page) # Load filtered, paginated data
        # Clamp page to valid range
        page = min(max(1, page), max_page)    # Ensure page is within valid range
        return df_page, gr.update(minimum=1, maximum=max_page, value=page) # Return updated data and page control

    filter_box.change(
        lambda filter_text, page: update_table(filter_text, 1),  # Reset to page 1 on filter change
        [filter_box, page_number],                               # Inputs: filter text and page number
        [data_table, page_number]                                # Outputs: update table and page number
    )
    page_number.change(
        update_table, 
        [filter_box, page_number], 
        [data_table, page_number]
    )
    refresh_btn.click(
        lambda: update_table(filter_box.value, page_number.value), 
        [], 
        [data_table, page_number]
    )

    data_table    # Return or display the data table
    refresh_btn   # Return or display the refresh button