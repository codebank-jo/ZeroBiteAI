import gradio as gr

def navbar():
    return gr.HTML(
        """
        <div style='width:100%;background:#222;color:#fff;padding:18px 32px;font-size:1.5em;font-weight:bold;letter-spacing:1px;'>
            ZeroBite AI Inventory Dashboard
        </div>
        """
    )

def sidenav(selected="inventory"):
    inventory_style = "color:#fff;font-weight:bold;" if selected == "inventory" else "color:#bbb;"
    menu_style = "color:#fff;font-weight:bold;" if selected == "menu" else "color:#bbb;"
    sales_style = "color:#fff;font-weight:bold;" if selected == "sales" else "color:#bbb;"
    return gr.HTML(
        f"""
        <div style='background:#222;color:#fff;padding:24px 0 24px 24px;height:80vh;min-width:150px;'>
            <h3 style='margin-top:0;color:#fff;'>Navigation</h3>
            <ul style='list-style:none;padding-left:0;font-size:1.1em;line-height:2;'>
                <li style="{inventory_style}"><a href='/inventory' style='text-decoration:none;{inventory_style}'>📦 Inventory List</a></li>
                <li style="{menu_style}"><a href='/menu' style='text-decoration:none;{menu_style}'>🍽️ Menu List</a></li>
                <li style="{sales_style}"><a href='/sales' style='text-decoration:none;{sales_style}'>📈 Sales Report</a></li>
            </ul>
        </div>
        """
    )

def footer():
    return gr.HTML(
        """
        <div style='width:100%;background:#222;color:#fff;padding:10px 0;text-align:center;font-size:1em;letter-spacing:1px;'>
            &copy; 2025 ZeroBite AI. All rights reserved.
        </div>
        """
    )

def layout(main_content_fn, selected="inventory"):
    with gr.Blocks() as page:
        navbar()
        with gr.Row():
            with gr.Column(scale=1, min_width=180):
                sidenav(selected)
            with gr.Column(scale=5):
                main_content_fn()  # <-- call the function!
        footer()
    return page