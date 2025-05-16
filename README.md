# ZeroBite AI Inventory & Menu Dashboard

This project is a real-time dashboard for visualizing and managing inventory and menu data using Gradio and Pandas. It allows users to monitor inventory levels, track expiry dates, manage stock efficiently, and view menu items with images and pricing.

## Project Structure

```
ZeroBite AI
├── app.py                # Main entry point for the Gradio/FastAPI application
├── data
│   ├── inventory.json    # JSON file containing inventory data
│   └── menu.json         # JSON file containing menu data
├── utils
│   └── data_loader.py    # Utility functions for loading inventory data
├── layout.py             # Layout components for navbar, sidebar, and footer
├── inventorylist.py      # Inventory list page logic
├── menuitems.py          # Menu list page logic
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

- Open your web browser and navigate to the provided local URL (e.g., `http://127.0.0.1:7860/inventory` or `/menu`) to access the dashboard.
- Use the sidebar to switch between the Inventory List and Menu List.
- Use the filter box to search by material/type (inventory) or menu item/type (menu).
- Use the page number control to navigate through paginated data.
- Click "Refresh Data" to reload the latest data from the JSON files.
- Menu items display image thumbnails and prices in GBP.

## Features

- Real-time visualization of inventory and menu data.
- Filtering and pagination for easy navigation.
- Image preview for menu items.
- User-friendly interface powered by Gradio.
- Modular layout with navbar, sidebar, and footer.
- Clean navigation URLs (`/inventory`, `/menu`).

## License

This project is licensed under the MIT License.
