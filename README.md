# HousePriceXpert - House Price Forecast System

## Overview

HousePriceXpert is a Python application designed to forecast home values using historical data. The application utilizes various libraries such as Pandas for data manipulation, NumPy for numerical operations, Matplotlib for plotting, and Tkinter for creating a graphical user interface (GUI).

## Features

*   **Data Import:** The application reads historical home value data from CSV files.
*   **Forecasting:** It implements a forecasting model to predict future home values based on historical trends.
*   **GUI:** A user-friendly interface allows users to select cities and view forecasts and budget recommendations.
*   **Visualization:** The application plots historical and forecasted home values for better understanding.

## Requirements

To run this application, ensure you have the following Python packages installed:

*   `pandas`: For data manipulation and analysis.
*   `numpy`: For numerical operations.
*   `matplotlib`: For plotting graphs and visualizations.
*   `prettytable`: For displaying tabular data in a readable format.
*   `tkinter`: For creating the GUI (usually included with Python installations).

You can install the required packages using:

```bash
pip install pandas numpy matplotlib prettytable
```
## Data Files

## The application uses the following CSV files:

*    NY_ZHVI.csv: Contains historical home value data for New York.
*    ZHVI_LA.csv: Contains historical home value data for Los Angeles.
*    ZHVI_Chicago.csv: Contains historical home value data for Chicago.
*    ZHVI_Houston.csv: Contains historical home value data for Houston.
*    ZHVI_Phoenix.csv: Contains historical home value data for Phoenix.

## Application Logic

1. Class Structure
*    NY Class: This class handles the data processing and forecasting for New York. It includes methods for:
*    Initializing the data and setting up columns for trends and forecasts.
*    Calculating levels and trends based on historical data.
*    Forecasting future values and calculating errors.
*    Plotting data in the GUI.

2. Subclasses:
   
The application defines subclasses for other cities (LA, CH, HO, PH) that inherit from the NY class, allowing for similar functionality with different datasets.

3. GUI Integration:
   
The application uses Tkinter to create a GUI that allows users to:
*	Select a city from a dropdown menu.
*	View the forecasted home values plotted on a graph.
*	Enter a budget range to receive recommendations based on the forecasted values.

4. Main Loop:
   
The main loop of the application initializes the GUI and keeps it running, allowing users to interact with the application.  It handles user events (like city selection and budget input) and updates the display accordingly.

5. Running the Application:
   
To run the application, execute the following command in your terminal:

```Bash
python forecast.py
```
This will open the GUI where you can select a city and view forecasts.

## Conclusion
HousePriceXpert provides a comprehensive tool for forecasting home values based on historical data. The combination of data analysis, forecasting, and visualization makes it a valuable resource for potential homebuyers and real estate professionals.
