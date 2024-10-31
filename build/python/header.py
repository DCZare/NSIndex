# header.py

import pandas as pd
from tkinter import Tk, filedialog, messagebox

def main():
    root = Tk()
    root.withdraw()  # Hide the root window

    # Ask for the CSV file to open
    file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        print("No file selected.")
        return

    # Read the CSV file
    try:
        df = pd.read_csv(file_path)
        headers = df.columns.tolist()

        # Display the headers in a message box
        messagebox.showinfo("CSV Headers", f"Headers: {', '.join(headers)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the file:\n{e}")

if __name__ == "__main__":
    main()

