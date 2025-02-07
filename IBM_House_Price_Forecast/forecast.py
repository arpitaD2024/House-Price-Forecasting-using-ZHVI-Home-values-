import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from prettytable import PrettyTable
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NY:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['Lt'] = 0.000
        self.df['Tt'] = 0.00000
        self.df['Ft'] = 0.0000
        self.df['Error'] = 0.0000

    def initial_T_L(self):
        current = self.df['zhvi'][:23]
        next = self.df['zhvi'][:23].shift(-1)
        dif = next - current
        s = dif.sum()
        T0 = abs((self.df['zhvi'].iat[23] - self.df['zhvi'].iat[0]) / 23)
        L0 = self.df['zhvi'].iat[23]
        #print(f"Initial Trend of 1996 is: {T0}")
        #print(f"The starting level of Forecast is: {L0}")
        self.df['Lt'].iat[23] = L0
        self.df['Tt'].iat[23] = T0

    def Level(self, i):
        a = 0.9
        self.df['Lt'].iat[i] = ((a * self.df['zhvi'].iat[i]) + ((1-a) * (self.df['Lt'].iat[i-1] + self.df['Tt'].iat[i-1])))

    def Trend(self, i):
        b = 0.9
        self.df['Tt'].iat[i] = (b * ((self.df['Lt'].iat[i]) - (self.df['Lt'].iat[i-1])) + ((1-b) * (self.df['Tt'].iat[i-1])))

    def together(self):
        for i in range(24, len(self.df)):
            self.Level(i)
            self.Trend(i)

    def Forecast_train(self):
        for i in range(24, len(self.df)):
            self.df['Ft'].iat[i] = self.df['Lt'].iat[i-1] + self.df['Tt'].iat[i-1]

    def Forecast_test_future(self):
        j = 2
        last_date = self.df['date'].dropna().iloc[-1]
        future_dates = pd.date_range(start=last_date, end='2030-12-31', freq='MS')[1:]
        future_df = pd.DataFrame({'date': future_dates, 'New York zhvi': np.nan, 'Lt': np.nan, 'Tt': np.nan, 'Ft': np.nan, 'Error': np.nan})
        self.future_df_len = len(future_df)
        self.df = pd.concat([self.df, future_df], ignore_index=True)

        for i in range(len(self.df) - len(future_df), len(self.df)):
            self.df.at[i, 'Ft'] = self.df.at[len(self.df)-len(future_df)-1, 'Lt'] + (j * self.df.at[len(self.df)-len(future_df)-1, 'Tt'])
            j += 1

    def error(self):
        for i in range(24, len(self.df) - self.future_df_len):  # Only calculate error for the training period
            self.df.at[i, 'Error'] = abs(self.df.at[i,'zhvi'] - self.df.at[i, 'Ft'])

    def MAD(self):
        sum_error = self.df['Error'][24:len(self.df) - self.future_df_len].sum()
        #print(f"Sum of error: {sum_error}")
        mad = sum_error / (len(self.df) - 204)  # Adjusted for the training period length
        #print(f"Mean Absolute Deviation of the model is: {mad}")

    # GUI Integration Functions
    def plot_in_gui(self, city_name, window):
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(self.df['date'], self.df['zhvi'], '-', linewidth=1, color='b', label='Home Value')
        ax.plot(self.df['date'], self.df['Ft'], '-', linewidth=1, color='orange', label="Forecast")
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        ax.set_title(f"Forecasting Home value of {city_name} till 2030")

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0, columnspan=4)

    def display_budget_recommendations(self, upper, lower, window):
        results_frame = Frame(window)
        results_frame.grid(row=6, column=0, columnspan=4, sticky="nsew")
        
        table = PrettyTable(['Year', 'Price'])
        for i, j in zip(self.df["Ft"], self.df["date"]):
            if lower <= i <= upper:
                table.add_row([j.strftime('%Y-%m-%d'), f"${i:,.2f}"])

        recommendations_label = Label(results_frame, text=table.get_string(), font=("Courier", 10), justify=LEFT)
        recommendations_label.grid(row=0, column=0, padx=10, pady=10)
    
    def call(self):
        self.initial_T_L()
        self.together()
        self.Forecast_train()
        self.Forecast_test_future()
        self.error()
        self.MAD()

# Subclasses for each city
class LA(NY):
    def __init__(self, csv_file):
        super().__init__(csv_file)

class CH(NY):
    def __init__(self, csv_file):
        super().__init__(csv_file)

class HO(NY):
    def __init__(self, csv_file):
        super().__init__(csv_file)

class PH(NY):
    def __init__(self, csv_file):
        super().__init__(csv_file)

root = Tk()
root.title("HousePriceXpert - Home Value Forecaster")
root.geometry("800x600")

ny = NY('NY_ZHVI.csv')
la = LA('ZHVI_LA.csv')
ch = CH('ZHVI_Chicago.csv')
ho = HO('ZHVI_Houston.csv')
ph = PH('ZHVI_Phoenix.csv')
ny.call()
la.call()
ch.call()
ho.call()
ph.call()

city_instances = {'New York': ny, 'Los Angeles': la, 'Chicago': ch, 'Houston': ho, 'Phoenix': ph}

# Create canvas and scrollbar
canvas = Canvas(root)
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)

# Bind the canvas to the scrollbar
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Now add all widgets to scrollable_frame instead of root
Label(scrollable_frame, text="Select a City for Forecast", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
city_var = StringVar(scrollable_frame)
city_var.set("New York")  # default value
city_dropdown = ttk.Combobox(scrollable_frame, textvariable=city_var, values=list(city_instances.keys()))
city_dropdown.grid(row=0, column=1, padx=10, pady=10)

# Plot Button Function
def plot_forecast():
    city_name = city_var.get()
    city_instance = city_instances[city_name]
    city_instance.plot_in_gui(city_name, scrollable_frame)

plot_button = Button(scrollable_frame, text="Show Forecast", command=plot_forecast)
plot_button.grid(row=0, column=2, padx=10, pady=10)

# Widgets for budget recommendation
Label(scrollable_frame, text="Enter Budget Range", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
Label(scrollable_frame, text="Upper Limit:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
upper_limit = Entry(scrollable_frame)
upper_limit.grid(row=2, column=1, padx=10, pady=5)
Label(scrollable_frame, text="Lower Limit:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
lower_limit = Entry(scrollable_frame)
lower_limit.grid(row=3, column=1, padx=10, pady=5)

# Budget recommendation display function
def show_recommendations():
    try:
        upper = int(upper_limit.get())
        lower = int(lower_limit.get())
        city_name = city_var.get()
        city_instance = city_instances[city_name]
        city_instance.display_budget_recommendations(upper, lower, scrollable_frame)
    except ValueError:
        Label(scrollable_frame, text="Please enter valid numeric values.", fg="red").grid(row=5, column=0, columnspan=4)

# Button for budget recommendations
recommend_button = Button(scrollable_frame, text="Show Budget Recommendations", command=show_recommendations)
recommend_button.grid(row=3, column=2, padx=10, pady=5)

# Call the main loop

root.mainloop()