import gradio as gr
from layout import layout
from inventorylist import inventory_list_content
from menuitems import menu_list_content
from salesreport import sales_trend_content
import uvicorn
from fastapi import FastAPI

app = FastAPI()

inventory_app = layout(inventory_list_content, selected="inventory")
menu_app = layout(menu_list_content, selected="menu")
sales_app = layout(sales_trend_content, selected="sales")

app = gr.mount_gradio_app(app, inventory_app, path="/inventory")
app = gr.mount_gradio_app(app, menu_app, path="/menu")
app = gr.mount_gradio_app(app, sales_app, path="/sales")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7860)