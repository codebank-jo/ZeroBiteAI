import gradio as gr
from layout import layout
from inventorylist import inventory_list_content
from menuitems import menu_list_content
import uvicorn
from fastapi import FastAPI

app = FastAPI()

# Create Gradio Blocks for each page
inventory_app = layout(inventory_list_content, selected="inventory")
menu_app = layout(menu_list_content, selected="menu")

app = FastAPI()
app = gr.mount_gradio_app(app, inventory_app, path="/inventory")
app = gr.mount_gradio_app(app, menu_app, path="/menu")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7860)