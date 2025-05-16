import gradio as gr
import pandas as pd
from utils.data_loader import load_inventory

def load_data(filter_text="", page=1, page_size=15):
    inventory_data = load_inventory()
    df = pd.DataFrame(inventory_data)
    # Filter
    if filter_text:
        df = df[df["material"].str.contains(filter_text, case=False) | df["type"].str.contains(filter_text, case=False)]
    # Pagination
    total = len(df)
    max_page = max(1, -(-total // page_size))
    start = (page - 1) * page_size
    end = start + page_size
    df_page = df.iloc[start:end]
    return df_page, total, max_page

def inventory_list_content():
    with gr.Row():
        with gr.Column(scale=3):
            filter_box = gr.Textbox(label="Filter by Material or Type", placeholder="Type to filter...")
        with gr.Column(scale=1):
            page_number = gr.Number(value=1, label="Page", precision=0, minimum=1)
    data_table = gr.Dataframe(
        value=load_data()[0],
        interactive=False,
        label="Inventory Table",
        render=True
    )
    refresh_btn = gr.Button("🔄 Refresh Data")

    def update_table(filter_text, page):
        try:
            page = int(page)
        except Exception:
            page = 1
        df_page, total, max_page = load_data(filter_text, page)
        # Clamp page to valid range
        page = min(max(1, page), max_page)
        return df_page, gr.update(minimum=1, maximum=max_page, value=page)

    filter_box.change(
        lambda filter_text, page: update_table(filter_text, 1),  # Reset to page 1 on filter
        [filter_box, page_number],
        [data_table, page_number]
    )
    page_number.change(update_table, [filter_box, page_number], [data_table, page_number])
    refresh_btn.click(lambda: update_table(filter_box.value, page_number.value), [], [data_table, page_number])

    data_table
    refresh_btn