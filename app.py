# Import the Gradio library for building web UIs
import gradio as gr
# Import the custom layout function
from layout import layout
# Import the content for the inventory list page
from inventorylist import inventory_list_content
# Import the content for the menu items page
from menuitems import menu_list_content
# Import the content for the sales report page
from salesreport import sales_trend_content
# Import the content for the leftover report page
from leftoverreport import leftover_report_content
# Import Uvicorn for running the FastAPI app
import uvicorn
# Import FastAPI for creating the backend API
from fastapi import FastAPI

# Create a FastAPI application instance
app = FastAPI()

# Create the Gradio app for the inventory page
inventory_app = layout(inventory_list_content, selected="inventory")
# Create the Gradio app for the menu page
menu_app = layout(menu_list_content, selected="menu")
# Create the Gradio app for the sales report page
sales_app = layout(sales_trend_content, selected="sales")
# Create the Gradio app for the leftover report page
leftover_app = layout(leftover_report_content, selected="leftover")

# Mount the inventory Gradio app at the /inventory path
app = gr.mount_gradio_app(app, inventory_app, path="/inventory")
# Mount the menu Gradio app at the /menu path
app = gr.mount_gradio_app(app, menu_app, path="/menu")
# Mount the sales Gradio app at the /sales path
app = gr.mount_gradio_app(app, sales_app, path="/sales")
# Mount the leftover Gradio app at the /leftover path
app = gr.mount_gradio_app(app, leftover_app, path="/leftover")

# Run the FastAPI app with Uvicorn if this file is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7860)