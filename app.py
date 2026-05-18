import tkinter as tk

from pathlib import Path
import json

from analyzer import Company
from analyzer import Analyzer

# ---------------------------- read json file .....

FILE_NAME = "ESG_DATA.json"

path = Path.cwd() / FILE_NAME

try:
    with path.open(mode="r") as file:
        data = json.load(file)  # Convert JSON data to a Python object
        print("*** Data loaded successfully ***\n")
        print("Number of companies:", len(data))
except FileNotFoundError:
    print(f"{path} does not exist.")
except Exception as e:
    print(f"Unexpected error: {e}")

print()

# --------------------------create company objects ------

company_list = []
for item in data:
    new_company = Company(item["company"], item["data"])
    company_list.append(new_company)

analyzer = Analyzer(company_list)


#-------------------------------------- GUI window --------
root = tk.Tk()  # initialize root widget
root.title("ESG Data Analyzer")
root.geometry("1000x600")
root.configure(background="#f4f7f5")

# ------------ sidebar right -------------------------
sidebar = tk.Frame(root, bg="#ffffff", width=260)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)  # don't ignore

title = tk.Label(sidebar, text="ESG Analyzer", bg="#ffffff", font=("Arial", 18, "bold"))
title.pack(pady=30)

analyze_button = tk.Button(sidebar,
    text="Analyze Company",
    width=18,
    height=1,
    font=("Arial", 11, "bold"),
    bg="#2673D9",
    fg="white",
    activebackground="#b0c1e7",
    activeforeground="white",
    relief="flat",
    bd=0
)
analyze_button.pack(pady=10)

analyze_all_button = tk.Button(sidebar,
    text="Analyze all Companies",
    width=18,
    height=1,
    font=("Arial", 11, "bold"),
    bg="#2BA664",
    fg="white",
    activebackground="#b0c1e7",
    activeforeground="white",
    relief="flat",
    bd=0
)
analyze_all_button.pack(pady=10)

show_ranking_button = tk.Button(sidebar,
    text="Show Ranking",
    width=18,
    height=1,
    font=("Arial", 11, "bold"),
    bg="#8E67D8",
    fg="white",
    activebackground="#b0c1e7",
    activeforeground="white",
    relief="flat",
    bd=0
)
show_ranking_button.pack(pady=10)

show_trends_button = tk.Button(sidebar,
    text="Show Trends",
    width=18,
    height=1,
    font=("Arial", 11, "bold"),
    bg="#03A1AE",
    fg="white",
    activebackground="#b0c1e7",
    activeforeground="white",
    relief="flat",
    bd=0
)
show_trends_button.pack(pady=10)

refresh_data_button = tk.Button(sidebar,
    text="Refresh Data",
    width=18,
    height=1,
    font=("Arial", 11, "bold"),
    bg="#718193",
    fg="white",
    activebackground="#b0c1e7",
    activeforeground="white",
    relief="flat",
    bd=0
)
refresh_data_button.pack(pady=10)

# -----------------------------------------------------
main_frame = tk.Frame(root, bg="#d2eddb")
main_frame.pack(side="right", fill="both", expand=True)




















root.mainloop()

