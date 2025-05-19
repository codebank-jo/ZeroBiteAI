import gradio as gr
import json
import os
import random
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

TRENDS_PATH = os.path.join(os.path.dirname(__file__), "data", "trends.json")
MENU_PATH = os.path.join(os.path.dirname(__file__), "data", "menu.json")
SOCIAL_MEDIA = ["Facebook", "Instagram", "TikTok", "Twitter"]
TREND_STATUS = ["Trending", "Non-Trending", "Similar"]

def generate_trends_data():
    # Load menu items
    with open(MENU_PATH, "r", encoding="utf-8") as f:
        menu_items = [item["menuitem"] for item in json.load(f)["menu"]]
    trends_data = []
    for item in menu_items:
        trend = {
            "menuitem": item,
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        for platform in SOCIAL_MEDIA:
            # Randomly assign a trend status and a score
            status = random.choices(TREND_STATUS, weights=[0.4, 0.4, 0.2])[0]
            score = random.randint(10, 100) if status == "Trending" else random.randint(0, 40)
            trend[f"{platform.lower()}_status"] = status
            trend[f"{platform.lower()}_score"] = score
        trends_data.append(trend)
    with open(TRENDS_PATH, "w", encoding="utf-8") as f:
        json.dump({"trends": trends_data}, f, indent=2)
    return trends_data

def load_trends_data():
    if not os.path.exists(TRENDS_PATH):
        return generate_trends_data()
    with open(TRENDS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["trends"]

def plot_trend_graph(trends_data, platform):
    df = pd.DataFrame(trends_data)
    status_col = f"{platform.lower()}_status"
    score_col = f"{platform.lower()}_score"
    fig, ax = plt.subplots(figsize=(8, 4))
    # Social media logos (Unicode or emoji for simplicity)
    logos = {
        "Facebook": "📘",
        "Instagram": "📸",
        "TikTok": "🎵",
        "Twitter": "🐦"
    }
    bars = ax.bar(df["menuitem"], df[score_col], color=[
        "#00FF88" if s == "Trending" else "#FFA500" if s == "Similar" else "#888" for s in df[status_col]
    ])
    for bar, status in zip(bars, df[status_col]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, status, ha="center", va="bottom", fontsize=9)
    # Add the logo to the title
    logo = logos.get(platform, "")
    ax.set_title(f"{logo} {platform} Trends")
    ax.set_ylabel("Trend Score")
    ax.set_xlabel("Menu Item")
    plt.xticks(rotation=30, ha="right", fontsize=10)
    plt.tight_layout()
    plt.close(fig)
    return fig

def social_trends_page():
    with gr.Blocks(title="Social Media Trends") as demo:
        gr.Markdown("## Social Media Trends for Menu Items")
        with gr.Row():
            generate_btn = gr.Button("Generate Random Trends Data")
            output = gr.Textbox(label="Status", interactive=False)
        with gr.Row():
            facebook_plot = gr.Plot(label="Facebook Trends")
            instagram_plot = gr.Plot(label="Instagram Trends")
        with gr.Row():
            tiktok_plot = gr.Plot(label="TikTok Trends")
            twitter_plot = gr.Plot(label="Twitter Trends")
        def on_generate():
            data = generate_trends_data()
            return (
                "Trends data generated.",
                plot_trend_graph(data, "Facebook"),
                plot_trend_graph(data, "Instagram"),
                plot_trend_graph(data, "TikTok"),
                plot_trend_graph(data, "Twitter"),
            )
        def on_load():
            data = load_trends_data()
            return (
                plot_trend_graph(data, "Facebook"),
                plot_trend_graph(data, "Instagram"),
                plot_trend_graph(data, "TikTok"),
                plot_trend_graph(data, "Twitter"),
            )
        generate_btn.click(
            fn=on_generate,
            inputs=[],
            outputs=[output, facebook_plot, instagram_plot, tiktok_plot, twitter_plot]
        )
        demo.load(
            fn=on_load,
            inputs=[],
            outputs=[facebook_plot, instagram_plot, tiktok_plot, twitter_plot]
        )
    return demo