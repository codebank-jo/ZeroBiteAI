import gradio as gr
import json
import os
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

WEATHER_PATH = os.path.join(os.path.dirname(__file__), "data", "weather.json")
WEATHER_TYPES = ["Sunny", "Rain", "Cloudy", "Thunderstorm", "Snow", "Fog", "Windy"]

def generate_weather_data():
    today = datetime.now()
    weather_data = []
    for i in range(14):
        date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        for period in ["Forenoon", "Afternoon"]:
            weather = random.choice(WEATHER_TYPES)
            temp = round(random.uniform(10, 35), 1) if weather != "Snow" else round(random.uniform(-5, 5), 1)
            feels_like = temp + random.uniform(-2, 2)
            weather_data.append({
                "date": date,
                "period": period,
                "weather": weather,
                "temperature": temp,
                "feels_like": round(feels_like, 1)
            })
    with open(WEATHER_PATH, "w", encoding="utf-8") as f:
        json.dump({"weather": weather_data}, f, indent=2)
    return weather_data

def load_weather_data():
    if not os.path.exists(WEATHER_PATH):
        return generate_weather_data()
    with open(WEATHER_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["weather"]

def plot_weather_graph(weather_data):
    df = pd.DataFrame(weather_data)
    df["date_period"] = df["date"] + " " + df["period"].str[0]
    fig, ax1 = plt.subplots(figsize=(12, 5))
    # Plot temperature and feels_like as lines
    ax1.plot(df["date_period"], df["temperature"], label="Temperature (°C)", marker="o", color="#FFA500")
    ax1.plot(df["date_period"], df["feels_like"], label="Feels Like (°C)", marker="x", color="#00BFFF")
    ax1.set_ylabel("Temperature (°C)")
    ax1.set_xlabel("Date & Period")
    ax1.set_xticks(range(len(df["date_period"])))
    ax1.set_xticklabels(df["date_period"], rotation=45, ha="right", fontsize=9)
    # Show weather type as colored background bands
    for i, row in df.iterrows():
        color = {
            "Sunny": "#FFFACD",
            "Rain": "#87CEEB",
            "Cloudy": "#D3D3D3",
            "Thunderstorm": "#B0C4DE",
            "Snow": "#E0FFFF",
            "Fog": "#F5F5F5",
            "Windy": "#E6E6FA"
        }.get(row["weather"], "#FFFFFF")
        ax1.axvspan(i-0.5, i+0.5, color=color, alpha=0.2)
        ax1.text(i, df["temperature"].min() - 2, row["weather"], rotation=90, va="bottom", ha="center", fontsize=8)
    ax1.legend()
    plt.tight_layout()
    plt.close(fig)
    return fig

def weather_page():
    with gr.Blocks(title="Weather Forecast") as demo:
        gr.Markdown("## 14-Day Weather Forecast (Forenoon & Afternoon)")
        with gr.Row():
            generate_btn = gr.Button("Generate Random Weather Data")
            output = gr.Textbox(label="Status", interactive=False)
        weather_plot = gr.Plot(label="Weather Forecast Graph")
        def on_generate():
            data = generate_weather_data()
            return "Weather data generated for next 14 days.", plot_weather_graph(data)
        def on_load():
            data = load_weather_data()
            return plot_weather_graph(data)
        generate_btn.click(fn=on_generate, inputs=[], outputs=[output, weather_plot])
        demo.load(fn=on_load, inputs=[], outputs=weather_plot)
    return demo