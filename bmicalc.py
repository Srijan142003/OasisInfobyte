import tkinter as tk
from tkinter import messagebox
import sqlite3
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")

        self.create_widgets()
        self.create_database()

    def create_widgets(self):
        self.weight_label = tk.Label(self.root, text="Weight (kg):")
        self.weight_label.grid(row=0, column=0, padx=10, pady=5)
        self.weight_entry = tk.Entry(self.root)
        self.weight_entry.grid(row=0, column=1, padx=10, pady=5)

        self.height_label = tk.Label(self.root, text="Height (cm):")
        self.height_label.grid(row=1, column=0, padx=10, pady=5)
        self.height_entry = tk.Entry(self.root)
        self.height_entry.grid(row=1, column=1, padx=10, pady=5)

        self.calculate_button = tk.Button(self.root, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.history_button = tk.Button(self.root, text="View History", command=self.view_history)
        self.history_button.grid(row=4, column=0, columnspan=2, pady=10)

    def create_database(self):
        self.conn = sqlite3.connect('bmi_data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                weight REAL,
                                height REAL,
                                bmi REAL,
                                category TEXT,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get()) / 100  # Convert cm to meters

            if weight <= 0 or height <= 0:
                raise ValueError("Weight and height must be positive numbers.")

            bmi = weight / (height ** 2)
            category = self.categorize_bmi(bmi)

            self.result_label.config(text=f"BMI: {bmi:.2f} ({category})")
            self.save_bmi_record(weight, height, bmi, category)
        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))

    def categorize_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

    def save_bmi_record(self, weight, height, bmi, category):
        self.cursor.execute('''INSERT INTO bmi_records (weight, height, bmi, category)
                               VALUES (?, ?, ?, ?)''', (weight, height, bmi, category))
        self.conn.commit()

    def view_history(self):
        self.cursor.execute('SELECT timestamp, weight, height, bmi, category FROM bmi_records')
        records = self.cursor.fetchall()
        
        history_window = tk.Toplevel(self.root)
        history_window.title("BMI History")

        for i, (timestamp, weight, height, bmi, category) in enumerate(records):
            tk.Label(history_window, text=f"{timestamp}: Weight: {weight} kg, Height: {height * 100} cm, BMI: {bmi:.2f}, Category: {category}").grid(row=i, column=0, padx=10, pady=5)

        self.plot_bmi_trend(records, history_window)

    def plot_bmi_trend(self, records, window):
        timestamps = [record[0] for record in records]
        bmis = [record[3] for record in records]

        figure = Figure(figsize=(6, 4), dpi=100)
        plot = figure.add_subplot(1, 1, 1)
        plot.plot(timestamps, bmis, marker='o')
        plot.set_title('BMI Trend')
        plot.set_xlabel('Timestamp')
        plot.set_ylabel('BMI')

        canvas = FigureCanvasTkAgg(figure, window)
        canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=5)
        canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()
