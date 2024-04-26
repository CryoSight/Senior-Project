# Budget App 
# Python
#    Requirments: tkinter
#                 csv
#                 re
# 
# 04/21/2024 Initial Development   Austin Hallman
#################################################

#Import the dependencies 
import tkinter as tk
from tkinter import ttk, filedialog
import csv
import re

# Main class for the application
class ExpenseTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Expense Tracker") # Set the title
        self.master.configure(bg="white") # Set the background color

        self.data = []

        # Set the default look of the application
        style = ttk.Style()
        style.configure("TLabel", background="white", font=("Helvetica", 12))
        style.configure("TEntry", font=("Helvetica", 12))

        # Create the amount lable
        self.amount_label = ttk.Label(master, text="Amount:")
        self.amount_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Call the validator amount when a key is pressed
        self.amount_entry = ttk.Entry(master, validate="key")
        self.amount_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.amount_entry['validatecommand'] = (self.amount_entry.register(self.validate_amount), '%P')

        # Create the date lable
        self.date_label = ttk.Label(master, text="Date (MM/DD/YYYY):")
        self.date_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Create the date entry
        self.date_entry = tk.Entry(master)
        self.date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.date_entry.bind('<KeyRelease>', self.validate_date)

        # Create the category lable
        self.category_label = ttk.Label(master, text="Category:")
        self.category_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # Create the category options
        categories = ["Housing", "Transportation", "Food", "Utilities", "Insurance",
                      "Medical & Healthcare", r"Savings\Investment", "Personal Spending", "Fun", "Miscellaneous"]
        self.category_var = tk.StringVar(master)
        self.category_var.set("Select Category")
        self.category_dropdown = ttk.OptionMenu(master, self.category_var, *categories)
        self.category_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Create the button to save the data
        self.save_button = ttk.Button(master, text="Add", command=self.save_data)
        self.save_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        # Create the button to delete last entry
        self.delete_last_button = ttk.Button(master, text="Delete Last", command=self.delete_last_entry)
        self.delete_last_button.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Create the element to display the list entries
        self.listbox = tk.Listbox(master, font=("Helvetica", 12), bg="white", selectbackground="lightgray", selectmode="extended")
        self.listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.master.rowconfigure(4, weight=1)
        self.master.columnconfigure([0, 1], weight=1)

        # Create the improt button
        self.import_button = ttk.Button(master, text="Import", command=self.import_csv)
        self.import_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        # Create the export button
        self.export_button = ttk.Button(master, text="Export", command=self.export_csv)
        self.export_button.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        # Create the default pie chart
        self.canvas_pie = tk.Canvas(master, bg="white", bd=0, highlightthickness=0)
        self.canvas_pie.grid(row=0, rowspan=5, column=2, padx=10, pady=5, sticky="nsew")
        self.master.columnconfigure(2, weight=1)

        # Create the default ledgend
        self.legend_canvas = tk.Canvas(master, bg="white", bd=0, highlightthickness=0)
        self.legend_canvas.grid(row=0, rowspan=5, column=3, padx=10, pady=5, sticky="nsew")
        self.master.columnconfigure(3, weight=1)

        # Default the pie chart to be a full circle with green color
        self.draw_pie_chart()
        self.draw_legend()

        # Bind canvas resizing to window resize event
        self.master.bind("<Configure>", self.redraw_pie_chart)

    #Validate the amount entry
    def validate_amount(self, new_value):
        if new_value == '':
            return True
        try:
            amount = float(new_value)
            # Check if the entered amount is between 0 and 1000000 and has no more than 2 decimals
            return 0.00 <= amount <= 1000000.00 and re.match(r'^\d+(\.\d{0,2})?$', new_value) is not None
        except ValueError:
            return False
        
    # Validate that the date is in the correct format
    def validate_date(self, event):
        date_pattern = r'^(0[1-9]|1[0-2])/(0[1-9]|[1-2]\d|3[01])/\d{4}$'
        entered_date = self.date_entry.get()
        match_result = re.match(date_pattern, entered_date)
        if match_result:
            self.date_entry.config(bg="white")
            return True  # Return True if date format is valid
        else:
            self.date_entry.config(bg="red")
            return False  # Return False if date format is invalid

    # Validate and save data if correct
    def save_data(self):
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        category = self.category_var.get()

        # Validate amount and date
        if not self.validate_amount(amount):
            print("Invalid amount. Please enter a valid amount.")
            return
        if not self.validate_date(date):
            print("Invalid date format. Please enter a date in MM/DD/YYYY format.")
            return
        
        # Check if a valid category is selected
        if amount and date and category != "Select Category":
            self.data.append([amount, date, category])
            self.update_listbox()
            self.draw_pie_chart()
            print("Data saved successfully.")
        else:
            print("Please fill in all fields.")

    # Delete the last entry in the list
    def delete_last_entry(self):
        if self.data:
            self.data.pop()
            self.update_listbox()
            self.draw_pie_chart()
            print("Last entry deleted successfully.")
        else:
            print("No entries to delete.")

    # Update the List box with data from the list
    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for entry in self.data:
            self.listbox.insert(tk.END, f"Amount: ${entry[0]}, Date: {entry[1]}, Category: {entry[2]}")

    # Create the pie chart
    def draw_pie_chart(self):
        self.canvas_pie.delete("all")

        if not self.data:
            self.draw_full_pie_chart()
            return

        # Set the location of the pie chart
        padding = 20
        canvas_width = min(self.canvas_pie.winfo_width(), self.canvas_pie.winfo_height())
        self.canvas_pie.create_oval(padding, padding, canvas_width - padding - 10, canvas_width - padding, fill="green", outline="black")

        # Calculate proportions of each category's expenditure
        category_amounts = {}
        total_amount = 0
        for entry in self.data:
            category = entry[2]
            amount = float(entry[0])
            total_amount += amount
            if category in category_amounts:
                category_amounts[category] += amount
            else:
                category_amounts[category] = amount

        # Check if "Others" category exists
        if "Others" not in category_amounts:
            category_amounts["Others"] = 0

        # Draw pie slices
        start_angle = 0
        for category, amount in category_amounts.items():
            proportion = amount / total_amount
            extent = proportion * 360
            color = self.get_category_color().get(category, "black")  # Retrieve color for the category
            self.canvas_pie.create_arc(padding, padding, canvas_width - padding - 10, canvas_width - padding, start=start_angle, extent=extent, fill=color, outline="black", style=tk.PIESLICE)
            start_angle += extent

    # Crete the full pie chart
    def draw_full_pie_chart(self):
        padding = 20
        canvas_width = min(self.canvas_pie.winfo_width(), self.canvas_pie.winfo_height())
        self.canvas_pie.create_oval(padding, padding, canvas_width - padding - 10, canvas_width - padding, fill="green", outline="black")

    # Create the category ledgend next to the pie chart
    def draw_legend(self):
        legend_height = len(self.get_category_color()) * 20
        legend_width = 120
        padding = 5

        for i, (category, color) in enumerate(self.get_category_color().items()):
            y_start = i * 20 + padding
            y_end = (i + 1) * 20 + padding
            self.legend_canvas.create_rectangle(padding, y_start, padding + 15, y_end, fill=color, outline="")
            self.legend_canvas.create_text(padding + 20, (y_start + y_end) / 2, text=category, anchor="w")

        self.legend_canvas.config(width=legend_width, height=legend_height)

    # Set the color for each category
    def get_category_color(self):
        # Assign a color to each category
        return {"Housing": "#ff9999", "Transportation": "#66b3ff", "Food": "#99ff99", "Utilities": "#ffcc99",
                "Insurance": "#ffff99", "Medical & Healthcare": "#cc99ff", r"Savings\Investment": "#ff6666",
                "Personal Spending": "#66ff66", "Fun": "#3399ff", "Miscellaneous": "#9999ff"}

    # Refresh the pie chart
    def redraw_pie_chart(self, event):
        self.draw_pie_chart()
        self.draw_legend()

    # Function to import the csv and load the data into the list
    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    self.data.append(row)
        self.update_listbox()
        self.draw_pie_chart()  # Add this line to update the pie chart
        self.draw_legend()  # Add this line to update the legend
        print("CSV file imported successfully.")

    # Function to save the data in the list to a csv file
    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for entry in self.data:
                    writer.writerow(entry)
            print("Data exported successfully.")

# Main body of the application
def main():
    root = tk.Tk()
    app = ExpenseTrackerApp(root)

    # Get the current width and height of the window
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()

    # Set the width and height of the window to be tripled
    window_width *= 7
    window_height *= 3

    # Set the size of the window
    root.geometry(f"{window_width}x{window_height}")

    root.mainloop()

if __name__ == "__main__":
    main()
