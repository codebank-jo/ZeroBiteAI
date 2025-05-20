import gradio as gr
import json
import os
import random
from datetime import datetime, timedelta
import pandas as pd

MENU_PATH = os.path.join(os.path.dirname(__file__), "data", "menu.json")
SALES_PATH = os.path.join(os.path.dirname(__file__), "data", "sales.json")
LEFTOVER_PATH = os.path.join(os.path.dirname(__file__), "data", "leftover.json")
TRENDS_PATH = os.path.join(os.path.dirname(__file__), "data", "trends.json")
WEATHER_PATH = os.path.join(os.path.dirname(__file__), "data", "weather.json")

def load_json(path, key):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f).get(key, [])

def sample_prediction_model(days):
    # Load data
    menu = load_json(MENU_PATH, "menu")
    sales = load_json(SALES_PATH, "daily_sales")
    leftover = load_json(LEFTOVER_PATH, "leftover")
    trends = load_json(TRENDS_PATH, "trends")
    weather = load_json(WEATHER_PATH, "weather")

    today = datetime.now()
    prediction = []
    menu_map = {item["menuitem"]: item for item in menu}
    trends_map = {item["menuitem"]: item for item in trends}
    # Build weather map by date and period
    weather_map = {(w["date"], w["period"]): w for w in weather}

    for i in range(days):
        date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        for menuitem in menu_map:
            # --- AI logic: base demand on past sales, leftover, trends, weather ---
            # Get last 7 days sales for this item
            past_sales = [
                sold["quantity_sold"]
                for day in sales[-7:]
                for sold in day.get("items_sold", [])
                if sold["menuitem"] == menuitem
            ]
            avg_sales = sum(past_sales) / len(past_sales) if past_sales else random.randint(5, 15)
            # Add trend boost
            trend_status = trends_map.get(menuitem, {}).get("facebook_status", "Non-Trending")
            trend_boost = 1.2 if trend_status == "Trending" else 1.0
            # Add weather boost (forenoon/afternoon)
            weather_forenoon = weather_map.get((date, "Forenoon"), {})
            weather_afternoon = weather_map.get((date, "Afternoon"), {})
            weather_reason = []
            weather_boost = 1.0
            for w in [weather_forenoon, weather_afternoon]:
                if w.get("weather") == "Rain":
                    weather_boost += 0.1
                    weather_reason.append("Rainy")
                elif w.get("weather") == "Sunny":
                    weather_boost += 0.05
                    weather_reason.append("Sunny")
            # Estimate demand
            quantity_in_demand = int(avg_sales * trend_boost * weather_boost + random.uniform(-2, 2))
            actual_quantity = menu_map[menuitem].get("available_stock", 0)
            demand_status = "High" if quantity_in_demand > actual_quantity else "Normal"
            # Cost saved: if demand < actual, cost saved is (actual - demand) * price
            price = float(menu_map[menuitem].get("price", 0))
            cost_saved = round(max(actual_quantity - quantity_in_demand, 0) * price, 2)
            # Reason
            reason = []
            # Social trend
            trend = trends_map.get(menuitem, {})
            for platform in ["facebook", "instagram", "tiktok", "twitter"]:
                status = trend.get(f"{platform}_status", "")
                if status == "Trending":
                    reason.append(f"{platform.capitalize()} Trending")
            # Weather
            if weather_reason:
                reason.append("Weather: " + ", ".join(set(weather_reason)))
            prediction.append({
                "Date": date,
                "MenuItem": menuitem,
                "QuantityInDemand": quantity_in_demand,
                "ActualQuantity": actual_quantity,
                "Demand": demand_status,
                "CostSaved": f"£{cost_saved:.2f}",  # <-- Show as GBP
                "Reason": "; ".join(reason) if reason else "Normal"
            })
    df = pd.DataFrame(prediction)
    print("Prediction DataFrame:")
    print(df)
    return df

def food_demand_prediction_page():
    with gr.Blocks(title="Food Demand Prediction") as demo:
        gr.Markdown("## Food Demand Prediction (Next 14 Days)")
        days_slider = gr.Slider(1, 14, value=7, step=1, label="Forecast Days")
        predict_btn = gr.Button("Predict Demand")
        output_table = gr.Dataframe(label="Prediction Table", interactive=False)
        def on_predict(days):
            df = sample_prediction_model(days)
            return df
        predict_btn.click(fn=on_predict, inputs=days_slider, outputs=output_table)
        demo.load(fn=lambda: sample_prediction_model(7), inputs=[], outputs=output_table)
    return demo