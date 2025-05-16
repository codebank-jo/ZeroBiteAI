# Inventory Dashboard

This project is a real-time dashboard for visualizing inventory data using Gradio and Pandas. It allows users to monitor inventory levels, track expiry dates, and manage stock efficiently.

## Project Structure

```
ZeroBite AI
├── app.py                # Main entry point for the Gradio application
├── data
│   └── inventory.json    # JSON file containing inventory data
├── utils
│   └── data_loader.py    # Utility functions for loading inventory data
├── layout.py             # Layout components for navbar, sidebar, and footer
├── requirements.txt      # List of dependencies for the project
└── README.md             # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd ZeroBite\ AI
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the application:
   ```sh
   python app.py
   ```

## Usage Guidelines

- Once the application is running, open your web browser and navigate to the provided local URL to access the dashboard.
- Use the filter box to search by material or type.
- Use the page number control to navigate through paginated inventory data.
- Click "Refresh Data" to reload the latest inventory from the JSON file.

## Features

- Real-time visualization of inventory data.
- Filtering and pagination for easy navigation.
- User-friendly interface powered by Gradio.
- Modular layout with navbar, sidebar, and footer.

## License

This project is licensed under the MIT License.