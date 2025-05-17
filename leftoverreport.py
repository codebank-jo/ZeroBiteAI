import gradio as gr
import pandas as pd
import json
import os
import matplotlib.pyplot as plt

def load_leftover(filter_text="", date_filter=None, page=1, page_size=10):
    json_path = os.path.join(os.path.dirname(__file__), "data", "leftover.json")
    with open(json_path, "r", encoding="utf-8") as f:
        waste_data = json.load(f)["food_waste"]
    df = pd.DataFrame(waste_data)
    if filter_text:
        df = df[df["menuitem"].str.contains(filter_text, case=False) | df["waste_reason"].str.contains(filter_text, case=False)]
    if date_filter:
        df = df[df["date"] == date_filter]
    total = len(df)
    max_page = max(1, -(-total // page_size))
    start = (page - 1) * page_size
    end = start + page_size
    df_page = df.iloc[start:end].copy()
    return df_page, total, max_page, df

def plot_loss_per_item(df):
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(8, 3))
    per_item = df.groupby("menuitem")["estimated_loss_gbp"].sum().sort_values(ascending=False)
    if per_item.empty:
        ax.text(0.5, 0.5, "No data to display", ha="center", va="center", fontsize=12, color="white")
        ax.set_axis_off()
        plt.close(fig)
        return fig
    per_item.plot(kind="bar", ax=ax, color="#FFA500")  # orange
    ax.set_ylabel("GBP", color="white")
    ax.set_title("Loss per Item", color="white")
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.xticks(rotation=30, ha="right", fontsize=10, color="white")
    plt.yticks(color="white")
    for i, v in enumerate(per_item):
        ax.text(i, v + 0.5, f"£{v:.2f}", ha="center", fontsize=9, color="white")
    plt.tight_layout()
    plt.close(fig)
    return fig

def plot_loss_by_date(df):
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(8, 3))
    per_date = df.groupby("date")["estimated_loss_gbp"].sum().sort_index()
    if per_date.empty:
        ax.text(0.5, 0.5, "No data to display", ha="center", va="center", fontsize=12, color="white")
        ax.set_axis_off()
        plt.close(fig)
        return fig
    per_date.plot(kind="line", ax=ax, color="#00FF88", marker="o")
    ax.set_ylabel("GBP", color="white")
    ax.set_title("Loss by Date", color="white")
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.xticks(rotation=30, ha="right", fontsize=10, color="white")
    plt.yticks(color="white")
    for i, (date, v) in enumerate(per_date.items()):
        ax.text(i, v, f"£{v:.2f}", ha="center", va="bottom", fontsize=9, color="white")
    plt.tight_layout()
    plt.close(fig)
    return fig

def leftover_report_content():
    with gr.Blocks(css=".gradio-container {max-width: 100vw !important; padding: 0;}") as demo:
        gr.Markdown("### Food Waste / Leftover Report", elem_id="title", elem_classes="full-width")
        with gr.Row():
            filter_box = gr.Textbox(label="Filter by Menu Item or Reason", placeholder="Type to filter...", scale=3)
            date_filter = gr.Dropdown(
                choices=[""] + sorted(list({row["date"] for row in json.load(open(os.path.join(os.path.dirname(__file__), "data", "leftover.json"), encoding="utf-8"))["food_waste"]})),
                label="Filter by Date",
                value="",
                scale=1
            )
            page_number = gr.Number(value=1, label="Page", precision=0, minimum=1, scale=1)
            refresh_btn = gr.Button("🔄 Refresh Data", scale=1)
        data_table = gr.Dataframe(
            value=load_leftover()[0],
            interactive=False,
            label="Leftover Table",
            render=True,
            datatype=["str"] * 7,
            elem_classes="full-width"
        )
        with gr.Row():
            per_item_graph = gr.Plot(plot_loss_per_item(load_leftover()[3]), elem_classes="full-width")
            per_date_graph = gr.Plot(plot_loss_by_date(load_leftover()[3]), elem_classes="full-width")

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

        filter_box.change(
            lambda filter_text, date_filter_val, page: update_table(filter_text, date_filter_val, 1),
            [filter_box, date_filter, page_number],
            [data_table, page_number, per_item_graph, per_date_graph]
        )
        date_filter.change(
            lambda date_filter_val, filter_text, page: update_table(filter_text, date_filter_val, 1),
            [date_filter, filter_box, page_number],
            [data_table, page_number, per_item_graph, per_date_graph]
        )
        page_number.change(
            update_table,
            [filter_box, date_filter, page_number],
            [data_table, page_number, per_item_graph, per_date_graph]
        )
        refresh_btn.click(
            lambda: update_table(filter_box.value, date_filter.value, page_number.value),
            [],
            [data_table, page_number, per_item_graph, per_date_graph]
        )
    return demo