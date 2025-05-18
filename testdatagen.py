import gradio as gr
import json
import os
import random
from datetime import datetime, timedelta

SALES_PATH = os.path.join(os.path.dirname(__file__), "data", "sales.json")
MENU_PATH = os.path.join(os.path.dirname(__file__), "data", "menu.json")

def generate_sales_data(days):
    # Read menu items and their available_stock and price from menu.json
    with open(MENU_PATH, "r", encoding="utf-8") as f:
        menu_data = json.load(f)
    menu_items = []
    for item in menu_data.get("menu", []):
        menu_items.append({
            "menuitem": item["menuitem"],
            "price": float(item.get("price", 5.0)),
            "available_stock": int(item.get("available_stock", 20))
        })

    today = datetime.now()
    daily_sales = []
    for i in range(days):
        date = (today - timedelta(days=days - i - 1)).strftime("%Y-%m-%d")
        items_sold = []
        total_sales_gbp = 0
        for item in menu_items:
            # For each day, sold quantity cannot exceed available_stock
            max_qty = item["available_stock"]
            qty = random.randint(0, max_qty) if max_qty > 0 else 0
            if qty > 0:
                item_total = qty * item["price"]
                items_sold.append({
                    "menuitem": item["menuitem"],
                    "quantity_sold": qty,
                    "total_sales_gbp": round(item_total, 2)
                })
                total_sales_gbp += item_total
        daily_sales.append({
            "date": date,
            "total_sales_gbp": round(total_sales_gbp, 2),
            "items_sold": items_sold
        })
    # Save to sales.json
    with open(SALES_PATH, "w", encoding="utf-8") as f:
        json.dump({"daily_sales": daily_sales}, f, indent=2)
    return f"Generated sales data for last {days} days and saved to data/sales.json (using menu.json for items and stock)."

def test_data_gen_content():
    with gr.Blocks(title="Test Data Generator") as demo:
        gr.Markdown("## Generate Test Sales Data")
        days_slider = gr.Slider(1, 90, value=30, step=1, label="Number of Days")
        generate_btn = gr.Button("Generate Data")
        output = gr.Textbox(label="Status", interactive=False)
        generate_btn.click(
            fn=generate_sales_data,
            inputs=days_slider,
            outputs=output
        )
    return demo