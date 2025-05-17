import gradio as gr  # Import the Gradio library for UI components

def navbar():
    # Returns a Gradio HTML component for the top navigation bar
    return gr.HTML(
        """
        <div style='width:100%;background:#222;color:#fff;padding:18px 32px;font-size:1.5em;font-weight:bold;letter-spacing:1px;'>
            ZeroBite AI Inventory Dashboard
        </div>
        """
    )

def sidenav(selected="inventory"):
    # Set styles for each menu item based on which is selected
    inventory_style = "color:#fff;font-weight:bold;" if selected == "inventory" else "color:#bbb;"
    menu_style = "color:#fff;font-weight:bold;" if selected == "menu" else "color:#bbb;"
    sales_style = "color:#fff;font-weight:bold;" if selected == "sales" else "color:#bbb;"
    leftover_style = "color:#fff;font-weight:bold;" if selected == "leftover" else "color:#bbb;"
    # Returns a Gradio HTML component for the side navigation menu
    return gr.HTML(
        f"""
        <div style='background:#222;color:#fff;padding:24px 0 24px 24px;height:80vh;min-width:150px;'>
            <h3 style='margin-top:0;color:#fff;'>Navigation</h3>
            <ul style='list-style:none;padding-left:0;font-size:1.1em;line-height:2;'>
                <li style="{inventory_style}"><a href='/inventory' style='text-decoration:none;{inventory_style}'>📦 Inventory List</a></li>
                <li style="{menu_style}"><a href='/menu' style='text-decoration:none;{menu_style}'>🍽️ Menu List</a></li>
                <li style="{sales_style}"><a href='/sales' style='text-decoration:none;{sales_style}'>📈 Sales Report</a></li>
                <li style="{leftover_style}"><a href='/leftover' style='text-decoration:none;{leftover_style}'>🥗 Leftover Report</a></li>
            </ul>
        </div>
        """
    )

def footer():
    # Returns a Gradio HTML component for the footer
    return gr.HTML(
        """
        <div style='width:100%;background:#222;color:#fff;padding:10px 0;text-align:center;font-size:1em;letter-spacing:1px;'>
            &copy; 2025 ZeroBite AI. All rights reserved.
        </div>
        """
    )

def layout(main_content_fn, selected="inventory"):
    # Defines the overall page layout using Gradio Blocks
    with gr.Blocks() as page:
        navbar()  # Add the navbar at the top
        with gr.Row():  # Create a horizontal row for sidebar and main content
            with gr.Column(scale=1, min_width=180):  # Sidebar column
                sidenav(selected)  # Add the side navigation
            with gr.Column(scale=5):  # Main content column
                main_content_fn()  # Call the function to add main content
        footer()  # Add the footer at the bottom
    return page  # Return the complete page layout