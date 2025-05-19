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
from fastapi.responses import RedirectResponse, FileResponse, Response
import os
from testdatagen import test_data_gen_content
from salesdetails import sales_details_content
from weather import weather_page

# Create a FastAPI application instance
app = FastAPI()

# Serve the favicon.ico using the same app logo
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    path = os.path.join(os.path.dirname(__file__), "favicon.ico")
    if os.path.exists(path):
        return FileResponse(path)
    return Response(status_code=204)  # No Content if favicon is missing

# Add a start page route that redirects to /inventory
@app.get("/", include_in_schema=False)
async def startpage():
    return RedirectResponse(url="/inventory")

# Create the Gradio app for the inventory page
inventory_app = layout(inventory_list_content, selected="inventory")
# Create the Gradio app for the menu page
menu_app = layout(menu_list_content, selected="menu")
# Create the Gradio app for the sales report page
sales_app = layout(sales_trend_content, selected="sales")
# Create the Gradio app for the leftover report page
leftover_app = layout(leftover_report_content, selected="leftover")
# Create the Gradio app for the test data generator page
testdata_app = layout(test_data_gen_content, selected="testdata")
# Create the Gradio app for the sales details page
salesdetails_app = layout(sales_details_content, selected="salesdetails")
# Create the Gradio app for the weather page
weather_app = layout(weather_page, selected="weather")

# Mount the inventory Gradio app at the root (/) and /inventory path
app = gr.mount_gradio_app(app, inventory_app, path="/inventory")
app = gr.mount_gradio_app(app, menu_app, path="/menu")
app = gr.mount_gradio_app(app, sales_app, path="/sales")
app = gr.mount_gradio_app(app, leftover_app, path="/leftover")
app = gr.mount_gradio_app(app, testdata_app, path="/testdata")
app = gr.mount_gradio_app(app, salesdetails_app, path="/salesdetails")
app = gr.mount_gradio_app(app, weather_app, path="/weather")

# Run the FastAPI app with Uvicorn if this file is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7860)