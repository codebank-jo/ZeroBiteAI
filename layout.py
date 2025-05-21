import gradio as gr  # Import the Gradio library for UI components

def navbar():
    # Returns a Gradio HTML component for the top navigation bar with logo, anonymous profile, and logout
    return gr.HTML(
        """
        <div style='width:100%;background:#222;color:#fff;padding:18px 32px;font-size:2em;font-weight:bold;letter-spacing:1px;display:flex;align-items:center;justify-content:space-between;'>
            <span style="display:flex;align-items:center;gap:16px;">
                <img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png" alt="Zero Waste Ninjas Logo" style="width:38px;height:38px;border-radius:50%;background:#fff;padding:2px;">
                Zero Waste Ninjas
            </span>
            <div style='display:flex;align-items:center;gap:18px;'>
                <span style='display:flex;align-items:center;gap:8px;font-size:1em;'>
                    <img src="https://cdn-icons-png.flaticon.com/512/149/149071.png" alt="Anonymous Profile" style="background:#444;border-radius:50%;width:32px;height:32px;display:inline-flex;align-items:center;justify-content:center;object-fit:cover;">
                    <span style="font-size:0.9em;color:#ccc;">Hive Kitchen</span>
                </span>
                <a href="/logout" style='color:#fff;text-decoration:none;font-size:1em;padding:6px 16px;background:#e74c3c;border-radius:5px;font-weight:500;'>Logout</a>
            </div>
        </div>
        """
    )

def sidenav(selected="inventory"):
    inventory_style = "color:#fff;font-weight:bold;" if selected == "inventory" else "color:#bbb;"
    menu_style = "color:#fff;font-weight:bold;" if selected == "menu" else "color:#bbb;"
    sales_style = "color:#fff;font-weight:bold;" if selected == "sales" else "color:#bbb;"
    salesdetails_style = "color:#fff;font-weight:bold;" if selected == "salesdetails" else "color:#bbb;"
    leftover_style = "color:#fff;font-weight:bold;" if selected == "leftover" else "color:#bbb;"
    testdata_style = "color:#fff;font-weight:bold;" if selected == "testdata" else "color:#bbb;"
    weather_style = "color:#fff;font-weight:bold;" if selected == "weather" else "color:#bbb;"
    trends_style = "color:#fff;font-weight:bold;" if selected == "trends" else "color:#bbb;"
    prediction_style = "color:#fff;font-weight:bold;" if selected == "prediction" else "color:#bbb;"
    current_day_sales_style = "color:#fff;font-weight:bold;" if selected == "current_day_sales" else "color:#bbb;"

    return gr.HTML(
        f"""
        <div style='background:#222;color:#fff;padding:24px 0 24px 24px;height:80vh;min-width:150px;margin-top:-10px'>
            <h3 style='margin-top:0;color:#fff;'>Navigation</h3>
            <ul style='list-style:none;padding-left:0;font-size:1.1em;line-height:2;'>
                <li style="{inventory_style}"><a href='/inventory' style='text-decoration:none;{inventory_style}'>📦 Inventory List</a></li>
                <li style="{menu_style}"><a href='/menu' style='text-decoration:none;{menu_style}'>🍽️ Menu List</a></li>
                <li style="{sales_style}"><a href='/sales' style='text-decoration:none;{sales_style}'>📈 Sales Report</a></li>
                <li style="{salesdetails_style}"><a href='/salesdetails' style='text-decoration:none;{salesdetails_style}'>🧾 Sales Details</a></li>
                <li style="{leftover_style}"><a href='/leftover' style='text-decoration:none;{leftover_style}'>🥗 Leftover Report</a></li>
                <li style="{weather_style}"><a href='/weather' style='text-decoration:none;{weather_style}'>🌤️ Weather</a></li>
                <li style="{trends_style}"><a href='/trends' style='text-decoration:none;{trends_style}'>📊 Social Trends</a></li>
                <li style="{prediction_style}"><a href='/prediction' style='text-decoration:none;{prediction_style}'>🔮 Food Demand Prediction</a></li>
                <li style="{testdata_style}"><a href='/testdata' style='text-decoration:none;{testdata_style}'>🧪 Test Data Generator</a></li>
                <li style="{current_day_sales_style}"><a href='/current_day_sales' style='text-decoration:none;{current_day_sales_style}'>🛒 Current Day Sales</a></li>
            </ul>
        </div>
        """
    )

def footer():
    # Returns a Gradio HTML component for the footer
    return gr.HTML(
        """
        <div style='width:100%;background:#222;color:#fff;padding:10px 0;text-align:center;font-size:1em;letter-spacing:1px;'>
            &copy; 2025 Zero Waste Ninjas. All rights reserved.
        </div>
        """
    )

def layout(main_content_fn, selected="inventory"):
    # Example inside your layout function or main Gradio Blocks
    with gr.Blocks(title="Zero Waste Ninjas") as demo:
        navbar()  # Add the navbar at the top
        with gr.Row():  # Create a horizontal row for sidebar and main content
            with gr.Column(scale=1, min_width=180):  # Sidebar column
                sidenav(selected)  # Add the side navigation
            with gr.Column(scale=5):  # Main content column
                main_content_fn()  # Call the function to add main content
        footer()  # Add the footer at the bottom
    return demo  # Return the complete page layout