# ZeroBite AI Inventory, Menu & Food Waste Dashboard

ZeroBite AI is a real-time dashboard for visualizing and managing inventory, menu, sales, and food waste data. Built with **Gradio**, **FastAPI**, and **Pandas**, it enables users to:

- Monitor inventory levels and expiry dates
- Manage stock efficiently
- View menu items with images and pricing
- Analyze food waste and loss trends

## Project Structure

```
ZeroBite AI
├── app.py                # Main application entry point
├── data
│   ├── inventory.json    # Inventory data
│   ├── menu.json         # Menu data
│   ├── sales.json        # Sales data
│   └── leftover.json     # Food waste/leftover data
├── utils
│   └── data_loader.py    # Data loading utilities
├── layout.py             # UI layout components
├── inventorylist.py      # Inventory page logic
├── menuitems.py          # Menu page logic
├── salesreport.py        # Sales report logic
├── leftoverreport.py     # Waste report logic
├── salesdetails.py       # Sales details (filter, search, trends)
├── testdatagen.py        # Test data generator for sales
├── requirements.txt      # Project dependencies
└── README.md             # Documentation
```

## Requirements

- **Python 3.10+** (recommended for compatibility)
- **pip** (Python package manager)

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd "ZeroBite AI"
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```sh
   python app.py
   ```

4. **Access the dashboard:**
   Open your browser and navigate to the local URL displayed in the terminal (e.g., `http://127.0.0.1:7860`).

## Usage

- **Navigation:** Use the sidebar to switch between Inventory, Menu, Sales, Sales Details, Leftover, and Test Data Generator pages.
- **Filtering & Search:** Filter and search by material/type, menu item/type, reason, or date as appropriate.
- **Pagination & Date Filters:** Browse data using pagination and date filters.
- **Refresh Data:** Click "Refresh Data" to reload from JSON files.
- **Menu Items:** View image thumbnails and GBP prices for menu items.
- **Leftover Report:** Analyze food waste with tables, bar charts, and line charts.
- **Sales Details:** View sales trends with tables, filters, and trend graphs.
- **Test Data Generator:** Generate random sales data for 1–90 days based on menu and stock.

## Key Features

- **Real-Time Data Visualization:** Monitor inventory, menu, sales, and food waste in real time.
- **Interactive Analytics:** Use filtering, pagination, and search for detailed insights.
- **Graphical Reports:** Visualize food waste and sales trends with interactive charts.
- **Test Data Generation:** Simulate sales data for testing and analysis.
- **User-Friendly Interface:** Built with Gradio and FastAPI for a seamless experience.
- **Modular Design:** Includes a navbar, sidebar, and footer for easy navigation.
- **Custom Branding:** Features a custom favicon and clean URLs for all pages.

## Public Access

To share your dashboard publicly, use a tunneling tool such as [ngrok](https://ngrok.com/) or [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/):

```sh
ngrok http 7860
# or
cloudflared tunnel --url http://localhost:7860
```

## Troubleshooting

- **Dependency Issues:** Ensure all dependencies in `requirements.txt` are installed.
- **Port Conflicts:** If port `7860` is in use, specify a different port when running the app:
  ```sh
  python app.py --server.port <new-port>
  ```
- **Data Loading Errors:** Verify the JSON files in the `data` directory are correctly formatted.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

## Screenshots
### Inventory Page
![Inventory Image](https://github.com/codebank-jo/ZeroBiteAI/blob/main/screenshots/inventory.jpg)
### Menu Page
![Menu Image](https://github.com/codebank-jo/ZeroBiteAI/blob/main/screenshots/menu.jpg)
### Sales reReport
![Sales Image](https://github.com/codebank-jo/ZeroBiteAI/blob/main/screenshots/salesreport.jpg)
### Sales Details Page
![Sales Details Image](https://github.com/codebank-jo/ZeroBiteAI/blob/main/screenshots/salesdetails.jpg)
### Leftover Page
![Leftover Image](https://github.com/codebank-jo/ZeroBiteAI/blob/main/screenshots/leftovers.jpg)
### Weather Page
![Weather Image](https://github.com/codebank-jo/ZeroBiteAI/blob/main/screenshot/weather.jpg)
### Social Media Trends Page
![Trends Image](https://github.com/codebank-jo/ZeroBiteAI/blob/main/screenshot/trends.jpg)
### Prediction Page
![Prediction Image](https://github.com/codebank-jo/ZeroBiteAI/blob/main/screenshots/prediction.jpg)
### Test Data Generator Page
![Test Data Image](https://github.com/codebank-jo/ZeroBiteAI/blob/main/screenshots/testdata.jpg)
### Current day sales
![Current day stock Image](https://github.com/codebank-jo/ZeroBiteAI/blob/main/screenshots/currentday.jpg)

