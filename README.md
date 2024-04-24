# Payment Processing and Forex Prediction

This project provides a payment processing API and includes functionality for predicting stock prices based on historical data. It consists of an API for processing payments and estimating stock prices, as well as modules for input data validation, model training, and templates for user interfaces.

## Folder Structure

- **App**: Contains the API code and HTML templates.
  - **api.py**: Flask application for payment processing and stock price estimation.
  - **templates**: HTML templates for different pages of the web application.
  - **input_data_validation.py**: Module for validating input data such as credit card numbers, expiration dates, security codes, and payment amounts.
- **model_training.py**: Script for training machine learning models to predict stock prices.
- **DJ**: Directory containing raw data for Dow Jones index.
- **requirements.txt**: List of dependencies for the project.

## Usage

### Running the API

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Navigate to the `App` directory:
   ```bash
   cd App
   ```
3. Run the Flask application:
   ```bash
   python api.py
   ```
4. Access the API endpoints through the specified routes.

### Processing Payments

- Endpoint: `/process-payment`
- Methods: GET, POST
- Validates credit card details and processes payments using different payment gateways based on the payment amount.

### Estimating Stock Prices

- Endpoint: `/estimate-price`
- Methods: GET, POST
- Predicts stock prices based on historical data and user input.

## Templates

The `templates` folder contains the following HTML templates for user interfaces:

- **cheap-payment-gateway.html**: Template for the cheap payment gateway page.
- **error-page.html**: Template for displaying error messages.
- **expensive-payment-gateway.html**: Template for the expensive payment gateway page.
- **home.html**: Homepage template.
- **premium-payment-gateway.html**: Template for the premium payment gateway page.
- **stock-prediction.html**: Template for displaying stock price predictions.
- **succesful-payment.html**: Template for displaying successful payment confirmation.

## Model Training

The `model_training.py` script trains machine learning models to predict stock prices based on historical data from the Dow Jones index.

## Contributing

Contributions to this project are welcome! If you have any suggestions or improvements, feel free to open an issue or create a pull request.


[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner2-direct.svg)](https://stand-with-ukraine.pp.ua)
