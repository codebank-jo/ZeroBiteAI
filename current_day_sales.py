import gradio as gr
import pandas as pd
import os
import json
from datetime import datetime

MENU_PATH = os.path.join(os.path.dirname(__file__), "data", "menu.json")
SALES_PATH = os.path.join(os.path.dirname(__file__), "data", "sales.json")

def load_json(path, key):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f).get(key, [])

def calculate_remaining_items(menu, sales):
    # Map menu items
    menu_map = {item["menuitem"]: item for item in menu}

    # Calculate total sold quantities for each menu item
    sold_quantities = {}
    for day in sales:
        for sold_item in day.get("items_sold", []):
            menuitem = sold_item["menuitem"]
            sold_quantities[menuitem] = sold_quantities.get(menuitem, 0) + sold_item["quantity_sold"]

    # Calculate remaining stock
    remaining_items = []
    for menuitem, details in menu_map.items():
        available_stock = details.get("available_stock", 0)
        sold_quantity = sold_quantities.get(menuitem, 0)
        remaining_stock = max(available_stock - sold_quantity, 0)
        remaining_items.append({
            "MenuItem": menuitem,
            "Price": details.get("price", 0),
            "RemainingStock": remaining_stock,
            "Reason": "Normal"
        })

    return pd.DataFrame(remaining_items)

def apply_discount(df, discount, time):
    # Apply discount to each item
    df["DiscountedPrice"] = df["Price"] * (1 - discount / 100)
    if discount == 100:
        df["Reason"] = f"Free to go items after {time}"
    else:   
        df["Reason"] = f"Discount of {discount}% applicable from {time}"
    return df

def current_day_sales_page():
    with gr.Blocks(title="Current Day Sales") as demo:
        gr.Markdown("## Current Day Sales and Remaining Items")
        
        # Slider for discount percentage
        discount_slider = gr.Slider(25, 100, value=0, step=5, label="Discount Percentage (%)")
        
        # Dropdown for time selection
        time_dropdown = gr.Dropdown(
            ["12PM", "3PM", "5PM", "7PM", "9PM"],
            value="5PM",
            label="Discount Start Time"
        )
        
        # Button to apply discount
        apply_discount_btn = gr.Button("Apply Discount")
        
        # Output table
        output_table = gr.Dataframe(label="Remaining Items with Discounts", interactive=False)

        # Load menu and sales data
        menu = load_json(MENU_PATH, "menu")
        sales = load_json(SALES_PATH, "daily_sales")
        remaining_items_df = calculate_remaining_items(menu, sales)

        # Function to handle discount application
        def on_apply_discount(discount, time):
            return apply_discount(remaining_items_df.copy(), discount, time)

        # Set up button click event
        apply_discount_btn.click(
            fn=on_apply_discount,
            inputs=[discount_slider, time_dropdown],
            outputs=output_table
        )

        # Load the initial table without discounts
        demo.load(fn=lambda: remaining_items_df, inputs=[], outputs=output_table)

    return demo