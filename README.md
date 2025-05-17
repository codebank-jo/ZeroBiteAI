# ZeroBite AI Inventory, Menu & Food Waste Dashboard

This project is a real-time dashboard for visualizing and managing inventory, menu, sales, and food waste data using Gradio and Pandas. It allows users to monitor inventory levels, track expiry dates, manage stock efficiently, view menu items with images and pricing, and analyze food waste/loss trends.

## Project Structure

```
ZeroBite AI
├── app.py                # Main entry point for the Gradio/FastAPI application
├── data
│   ├── inventory.json    # JSON file containing inventory data
│   ├── menu.json         # JSON file containing menu data
│   ├── sales.json        # JSON file containing sales data
│   └── leftover.json     # JSON file containing food waste/leftover data
├── utils
│   └── data_loader.py    # Utility functions for loading inventory data
├── layout.py             # Layout components for navbar, sidebar, and footer
├── inventorylist.py      # Inventory list page logic
├── menuitems.py          # Menu list page logic
├── salesreport.py        # Sales report page logic
├── leftoverreport.py     # Leftover/waste report page logic
├── requirements.txt      # List of dependencies for the project
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd "ZeroBite AI"
   ```

2. **Install the required dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```sh
   python app.py
   ```

## Usage Guidelines

- Open your web browser and navigate to the provided local URL (e.g., `http://127.0.0.1:7860/inventory`, `/menu`, `/sales`, or `/leftover`) to access the dashboard.
- Use the sidebar to switch between Inventory List, Menu List, Sales Report, and Leftover Report.
- Use the filter box to search by material/type (inventory), menu item/type (menu), or menu item/reason (leftover).
- Use the date filter and page number control to navigate through paginated data.
- Click "Refresh Data" to reload the latest data from the JSON files.
- Menu items display image thumbnails and prices in GBP.
- The Leftover Report page provides:
  - A table of food waste/leftover items with pagination and filtering.
  - Graphs for loss per menu item (bar chart) and loss by date (line chart), displayed side by side and using the full width of the page.

## Features

- Real-time visualization of inventory, menu, sales, and food waste data.
- Filtering and pagination for easy navigation.
- Image preview for menu items.
- Food waste analytics with interactive graphs.
- User-friendly interface powered by Gradio.
- Modular layout with navbar, sidebar, and footer.
- Clean navigation URLs (`/inventory`, `/menu`, `/sales`, `/leftover`).

## License

This project is licensed under the MIT License.
