# AlphaGenie

Welcome to AlphaGenie, a comprehensive stock data platform designed for tech stock enthusiasts and algorithmic traders. This application enables users to interact with real-time market data, utilize predictive modeling, and deploy algorithmic trading bots based on custom strategies.

## Features

### Account Management

- **User Accounts:** Securely create and manage your account to access personalized features.

### Dashboard

- **Tech Stocks Overview:** View real-time data for 10 select tech stocks, carefully chosen to represent the tech sector.
- **Market Data:** Each stock is displayed with up-to-date market information, including prices, volume, and more.

### Predictive Analytics

- **Stock Predictions:** Utilize predictions for the stock symbols using advanced machine learning models, such as Random Forest and LSTM.
- **Model Insights:** Understand potential future movements of stocks based on historical data analysis.

### Alphabots

- **Algorithmic Trading Bots:** Deploy automated trading bots on selected stock buckets.
- **Custom Strategies:** Choose from strategies like MACD and Renko for executing trades.
- **Portfolio Rebalancing:** Utilize sophisticated rebalancing techniques to backtest strategies and improve performance.
- **Performance Visualization:** Compare your bots' performance against standard index funds, visualizing effectiveness and strategy success.

## Getting Started

### Prerequisites

Before you set up your local development environment, ensure you have the following installed:

- Python (3.9 or newer)
- Django (4.2 or newer)
- Other dependencies listed in `requirements.txt`

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/alphagenie.git
   cd alphagenie
   ```
2. **Create and activate a Virtual Environment** (If provided zip file, venv is named venv3.9)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Initialize Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

## Project Structure

AlphaGenie is structured into several Django apps and utility folders, each serving a specific function within the application. Below is an overview of the key directories and their contents:

### Django Applications

- **core**

  - The main Django application containing configuration files such as `settings.py`. This folder acts as the central hub for project-wide configurations.

- **alphahome**

  - A Django app that manages the static frontend pages of the website, including the Home, About, and Services pages. It also handles user authentication views such as login.

- **alphamarket**

  - This app focuses on the user dashboard and related functionalities. It includes endpoints for dashboard access, market details, and stock predictions. The `utils` folder within this app contains the machine learning models used for stock predictions.

- **alphatrader**

  - Manages user/trader profiles and includes Django models for user accounts. It handles routes for user interactions such as login, signup, and profile editing.

- **alphabots**
  - Contains logic for the trading bots, managing routes for creating stock buckets and deploying trading bots. This app is essential for the algorithmic trading functionality of AlphaGenie. The `utils` folder within this app houses the scripts for the final trading bots used in the application, including essential functions and classes for executing trading strategies.

### Utility and Script Folders

- **scripts_ml**

  - Houses test scripts and Python notebooks for machine learning prediction algorithms. This folder is crucial for developing and testing the predictive models used in the application.

- **scripts_trading**
  - Includes test scripts and notebooks for trading strategies, KPIs, backtesting, and visualization. These scripts are key for developing and evaluating the trading bots.

## Setup and Configuration

For details on setting up and running the project, refer to the [Getting Started](#getting-started) section above. Ensure all dependencies are installed as per the `requirements.txt` file to avoid any issues during deployment or development.

## Contributions

Contributions to improve AlphaGenie are always welcome. Whether it's enhancing the predictive models, refining the trading algorithms, or improving the UI/UX, your input is valuable. Check out our [CONTRIBUTING.md](CONTRIBUTING.md) for more information on how to make your contributions count.
