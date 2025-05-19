import gradio as gr
import json
import os
import random
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
INVENTORY_PATH = os.path.join(DATA_DIR, "inventory.json")
MENU_PATH = os.path.join(DATA_DIR, "menu.json")
SALES_PATH = os.path.join(DATA_DIR, "sales.json")
LEFTOVER_PATH = os.path.join(DATA_DIR, "leftover.json")

MATERIALS = [
    ("Flour", "Dry Goods", "kg"),
    ("Eggs", "Dairy", "pcs"),
    ("Butter", "Dairy", "kg"),
    ("Beef (Sirloin)", "Meat", "kg"),
    ("Potatoes", "Vegetables", "kg"),
    ("Milk", "Dairy", "L"),
    ("Bread", "Bakery", "loaves"),
    ("Cheese", "Dairy", "kg"),
    ("Fish (Cod)", "Seafood", "kg"),
    ("Vegetables", "Fresh Produce", "kg"),
    ("Chicken Breast", "Meat", "kg"),
    ("Carrots", "Vegetables", "kg"),
    ("Pasta", "Dry Goods", "kg"),
    ("Onions", "Vegetables", "kg"),
    ("Salt", "Seasoning", "kg"),
    ("Black Pepper", "Seasoning", "kg"),
    ("Lettuce", "Vegetables", "kg"),
    ("Tomatoes", "Vegetables", "kg"),
    ("Olive Oil", "Condiments", "L"),
    ("Sugar", "Dry Goods", "kg"),
    ("Bacon", "Meat", "kg"),
    ("Mushrooms", "Vegetables", "kg"),
    ("Coffee Beans", "Beverages", "kg"),
    ("Tea Leaves", "Beverages", "kg"),
    ("Strawberries", "Fruits", "kg"),
    ("Lemons", "Fruits", "kg"),
    ("Ketchup", "Condiments", "L"),
    ("Mayonnaise", "Condiments", "L"),
    ("Honey", "Condiments", "kg"),
    ("Garlic", "Vegetables", "kg"),
]

MENU_ITEMS_TEMPLATE = [
    {
        "menuitem": "Classic Omelette",
        "type": "veg",
        "ingredient": "Eggs, butter, salt, black pepper",
        "inventories_used": ["Eggs", "Butter", "Salt", "Black Pepper"]
    },
    {
        "menuitem": "Vegetable Pasta",
        "type": "veg",
        "ingredient": "Pasta, tomatoes, onions, carrots, olive oil",
        "inventories_used": ["Pasta", "Tomatoes", "Onions", "Carrots", "Olive Oil"]
    },
    {
        "menuitem": "Grilled Chicken Breast",
        "type": "nonveg",
        "ingredient": "Chicken breast, black pepper, salt, olive oil",
        "inventories_used": ["Chicken Breast", "Black Pepper", "Salt", "Olive Oil"]
    },
    {
        "menuitem": "Vegan Stir Fry",
        "type": "vegan",
        "ingredient": "Broccoli, carrots, onions, garlic, olive oil",
        "inventories_used": ["Carrots", "Onions", "Garlic", "Olive Oil"]
    },
    {
        "menuitem": "Beef Sirloin Steak",
        "type": "nonveg",
        "ingredient": "Beef (Sirloin), salt, black pepper",
        "inventories_used": ["Beef (Sirloin)", "Salt", "Black Pepper"]
    },
    {
        "menuitem": "Cheese Sandwich",
        "type": "veg",
        "ingredient": "Bread, cheese, butter",
        "inventories_used": ["Bread", "Cheese", "Butter"]
    },
    {
        "menuitem": "Fruit Salad",
        "type": "vegan",
        "ingredient": "Strawberries, lemons",
        "inventories_used": ["Strawberries", "Lemons"]
    },
    {
        "menuitem": "Fish and Chips",
        "type": "nonveg",
        "ingredient": "Fish (Cod), potatoes, salt",
        "inventories_used": ["Fish (Cod)", "Potatoes", "Salt"]
    }
]

def generate_test_data(days):
    try:
        today = datetime.now()
        # 1. Generate Inventory Data (unchanged)
        inventory = []
        for material, mat_type, unit in MATERIALS:
            purchase_days_ago = random.randint(10, days)
            purchase_date = today - timedelta(days=purchase_days_ago)
            purchase_date_str = purchase_date.strftime("%Y-%m-%d")
            next_purchase_date = purchase_date + timedelta(days=30)
            next_purchase_date_str = next_purchase_date.strftime("%Y-%m-%d")
            expiry_date = next_purchase_date + timedelta(days=random.randint(1, 90))
            expiry_date_str = expiry_date.strftime("%Y-%m-%d")
            qty = random.randint(100, 200)
            remaining = random.randint(1, qty)
            quantity = f"{qty} {unit}"
            remaining_stock = f"{remaining} {unit}"
            inventory.append({
                "material": material,
                "type": mat_type,
                "quantity": quantity,
                "purchase_date": purchase_date_str,
                "remaining_stock": remaining_stock,
                "next_purchase_tentative_date": next_purchase_date_str,
                "expiry_date": expiry_date_str
            })
        for item in inventory:
            pd = datetime.strptime(item["purchase_date"], "%Y-%m-%d")
            nptd = datetime.strptime(item["next_purchase_tentative_date"], "%Y-%m-%d")
            expd = datetime.strptime(item["expiry_date"], "%Y-%m-%d")
            if not (expd > nptd and nptd == pd + timedelta(days=30)):
                raise Exception("Inventory date rules violated.")

        with open(INVENTORY_PATH, "w", encoding="utf-8") as f:
            json.dump({"inventory": inventory}, f, indent=2)

        # 2. Generate Menu Data (cycle menu items across all days)
        menu_items = []
        menu_dates = []
        for i in range(days):
            template = MENU_ITEMS_TEMPLATE[i % len(MENU_ITEMS_TEMPLATE)]
            available_stock = random.randint(50, 150)
            price = round(random.uniform(5, 30), 2)
            prepared_date = (today - timedelta(days=(days - i - 1))).strftime("%Y-%m-%d")
            menu_dates.append(prepared_date)
            menuitem_text = template["menuitem"].replace(" ", "+")
            image_url = f"https://placehold.co/120x120?text={menuitem_text}"
            menu_items.append({
                "menuitem": template["menuitem"],
                "type": template.get("type", ""),
                "ingredient": template["ingredient"],
                "inventories_used": template["inventories_used"],
                "price": price,
                "available_stock": available_stock,
                "prepared_date": prepared_date,
                "image_url": image_url
            })

        with open(MENU_PATH, "w", encoding="utf-8") as f:
            json.dump({"menu": menu_items}, f, indent=2)

        # 3. Generate Sales Data (sales date matches menu prepared_date)
        daily_sales = []
        for i in range(days):
            date = (today - timedelta(days=days - i - 1)).strftime("%Y-%m-%d")
            items_sold = []
            total_sales_gbp = 0
            for item in menu_items:
                if date == item["prepared_date"]:
                    max_qty = item["available_stock"]
                    qty = random.randint(0, max_qty)
                    if qty > 0:
                        item_total = qty * float(item.get("price", 5.0))
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
        with open(SALES_PATH, "w", encoding="utf-8") as f:
            json.dump({"daily_sales": daily_sales}, f, indent=2)

        # 4. Generate Leftover Data (date matches prepared_date)
        leftover_records = []
        for i in range(days):
            date = (today - timedelta(days=days - i - 1)).strftime("%Y-%m-%d")
            for item in menu_items:
                if date == item["prepared_date"]:
                    sold_quantity = 0
                    for sale in daily_sales:
                        if sale["date"] == date:
                            for sold in sale["items_sold"]:
                                if sold["menuitem"] == item["menuitem"]:
                                    sold_quantity = sold["quantity_sold"]
                    max_leftover = item["available_stock"] - sold_quantity
                    if max_leftover > 0 and random.random() < 0.3:
                        wasted_quantity = random.randint(1, max_leftover)
                        reason = random.choice(["Overproduction", "Spoilage", "Customer Return"])
                        leftover_records.append({
                            "date": date,
                            "menuitem": item["menuitem"],
                            "sold_quantity": sold_quantity,
                            "wasted_quantity": wasted_quantity,
                            "reason": reason
                        })
        with open(LEFTOVER_PATH, "w", encoding="utf-8") as f:
            json.dump({"leftover": leftover_records}, f, indent=2)

        return "Test data generated successfully for inventory, menu, sales, and leftover."
    except Exception as e:
        return f"Error: {str(e)}"

def test_data_gen_content():
    with gr.Blocks(title="Test Data Generator") as demo:
        gr.Markdown("## Generate Test Data for Inventory, Menu, Sales, and Leftover")
        days_slider = gr.Slider(7, 180, value=30, step=1, label="Generate data for last N days")
        output = gr.Textbox(label="Status", interactive=False, lines=3)
        generate_btn = gr.Button("Generate Test Data")
        generate_btn.click(
            fn=generate_test_data,
            inputs=days_slider,
            outputs=output
        )
    return demo