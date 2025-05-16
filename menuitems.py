import gradio as gr
import pandas as pd
import json
import os

def load_menu(filter_text="", page=1, page_size=15):
    # Load menu data from data/menu.json
    json_path = os.path.join(os.path.dirname(__file__), "data", "menu.json")
    with open(json_path, "r", encoding="utf-8") as f:
        menu_data = json.load(f)["menu"]
    df = pd.DataFrame(menu_data)
    # Filter by menuitem or type
    if filter_text:
        df = df[df["menuitem"].str.contains(filter_text, case=False) | df["type"].str.contains(filter_text, case=False)]
    # Pagination
    total = len(df)
    max_page = max(1, -(-total // page_size))
    start = (page - 1) * page_size
    end = start + page_size
    df_page = df.iloc[start:end].copy()
    # Move image_url to first column and convert to markdown for preview
    if "image_url" in df_page.columns:
        df_page.insert(0, "Image", df_page["image_url"].apply(lambda url: f"![img]({url})" if pd.notna(url) else ""))
        df_page = df_page.drop(columns=["image_url"])
    return df_page, total, max_page

def menu_list_content():
    with gr.Row():
        with gr.Column(scale=3):
            filter_box = gr.Textbox(label="Filter by Menu Item or Type", placeholder="Type to filter...")
        with gr.Column(scale=1):
            page_number = gr.Number(value=1, label="Page", precision=0, minimum=1)
    data_table = gr.Dataframe(
        value=load_menu()[0],
        interactive=False,
        label="Menu Table",
        render=True,
        datatype=["markdown"] + ["str"]*7  # First column is markdown for image
    )
    refresh_btn = gr.Button("🔄 Refresh Data")

    def update_table(filter_text, page):
        try:
            page = int(page)
        except Exception:
            page = 1
        df_page, total, max_page = load_menu(filter_text, page)
        page = min(max(1, page), max_page)
        return df_page, gr.update(minimum=1, maximum=max_page, value=page)

    filter_box.change(
        lambda filter_text, page: update_table(filter_text, 1),
        [filter_box, page_number],
        [data_table, page_number]
    )
    page_number.change(update_table, [filter_box, page_number], [data_table, page_number])
    refresh_btn.click(lambda: update_table(filter_box.value, page_number.value), [], [data_table, page_number])

    data_table
    refresh_btn