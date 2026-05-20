import tkinter as tk
from tkinter import ttk

from pathlib import Path
import json

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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

# --------------------------------- functions to show results --------------------------
def show_ranking():
    output_text.delete("1.0", tk.END)
    result = analyzer.ranking()
    output_text.insert(tk.END, result)

def show_selected_company():
    selected_name = company_dropdown.get()

    for company in company_list:
        if company.name == selected_name:

            output_text.delete("1.0", tk.END)  # clear output

            output_text.insert(tk.END, f"{company.name}\n", "company")

            # show last year esg values in cards 
            last_entry = company.data[-1]
            
            env, soc, gov, latest_esg_score = Analyzer.calculate_esg_score(last_entry)

            env_score.config(text=f"{env:.2f}")
            soc_score.config(text=f"{soc:.2f}")
            gov_score.config(text=f"{gov:.2f}")
            total_score.config(text=f"{latest_esg_score:.2f}")  

            # Trend Card:
            if len(company.data) > 1:
                first_entry = company.data[0]
                _, _, _, first_score = Analyzer.calculate_esg_score(first_entry)

                trend = Analyzer.get_trend(company.data)

                if trend == "Improving":
                    trend_score.config(text=trend, fg="green")

                elif trend == "Declining":
                    trend_score.config(text=trend, fg="red")

                else:
                    trend_score.config(text=trend, fg="orange")
            # output for every year                 
            for entry in company.data:
                env, soc, gov, esg_score = Analyzer.calculate_esg_score(entry)
                rating = Analyzer.get_rating(esg_score)

                if rating == "Excellent":
                    tag = "excellent"
                elif rating == "Good":
                    tag = "good"
                elif rating == "Average":
                    tag = "average"
                else:
                    tag = "bad"

                output_text.insert(tk.END, f"\nYear: {entry['year']}\n", "year")
                output_text.insert(tk.END, "=" * 30 + "\n", "line")
                output_text.insert(tk.END, f"Environmental Score : {env:.2f}\n")
                output_text.insert(tk.END, f"Social Score        : {soc:.2f}\n")
                output_text.insert(tk.END, f"Governance Score    : {gov:.2f}\n")
                output_text.insert(tk.END, f"Overall ESG Score   : {esg_score:.2f}\n")
                output_text.insert(tk.END, f"Rating              : {rating}\n", tag)

                show_trend_chart(company)

            break

def show_trend_chart(company):
    for widget in chart_frame.winfo_children():
        widget.destroy()  # delete old chart
    years = []
    scores = []

    for entry in company.data:
        _, _, _, esg_score = Analyzer.calculate_esg_score(entry)
        years.append(str(entry["year"]))
        scores.append(esg_score)

    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    ax.plot(years, scores)
    ax.set_title(f"ESG Trend - {company.name}")
    ax.set_xlabel("Year")
    ax.set_ylabel("ESG Score")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

#-------------------------------------- GUI window --------

root = tk.Tk()  # initialize root widget
root.title("ESG Data Analyzer")
root.geometry("1200x700")
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
    bd=0,
    command=show_selected_company
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
    bd=0,
    command=show_ranking
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

# -------------------- left side ---------------------------------
main_frame = tk.Frame(root, bg="#ffffff")
main_frame.pack(side="right", fill="both", expand=True)

main_title = tk.Label(main_frame, text="Dashboard", bg="#ffffff", font=("Arial", 20, "bold"))
main_title.pack(pady=20)

company_names = [company.name for company in company_list]
company_dropdown = ttk.Combobox(
    main_frame,
    values=company_names,
    state="readonly",
    font=("Arial", 12),
    width=20
)
company_dropdown.pack(pady=10)
company_dropdown.current(0)

# -------------------------- Cards -----------------------
cards_frame = tk.Frame(main_frame, bg="#ffffff")
cards_frame.pack(pady=15)

# Environmental card:
env_card = tk.Frame(cards_frame, bg="white", width=170, height=100, relief="solid", borderwidth=1)
env_card.pack(side="left", padx=10)
env_card.pack_propagate(False)
env_title = tk.Label(env_card, text="Environmental", bg="white", font=("Arial", 12, "bold"))
env_title.pack(pady=10)
env_score = tk.Label(env_card, text="0.00", bg="white", fg="#2e7d32", font=("Arial", 24, "bold"))   
env_score.pack()

# social card:
soc_card = tk.Frame(cards_frame, bg="white", width=170, height=100, relief="solid", borderwidth=1)
soc_card.pack(side="left", padx=10)
soc_card.pack_propagate(False)
soc_title = tk.Label(soc_card, text="Social", bg="white", font=("Arial", 12, "bold"))
soc_title.pack(pady=10)
soc_score = tk.Label(soc_card, text="0.00", bg="white", fg="#2e7d32", font=("Arial", 24, "bold"))
soc_score.pack()

# Governance card:
gov_card = tk.Frame(cards_frame, bg="white", width=170, height=100, relief="solid", borderwidth=1)
gov_card.pack(side="left", padx=10)
gov_card.pack_propagate(False)
gov_title = tk.Label(gov_card, text="Governance", bg="white", font=("Arial", 12, "bold"))
gov_title.pack(pady=10)
gov_score = tk.Label(gov_card, text="0.00", bg="white", fg="#2e7d32", font=("Arial", 24, "bold"))
gov_score.pack()

# ESG Total card:
total_card = tk.Frame(cards_frame, bg="white", width=170, height=100, relief="solid", borderwidth=1)
total_card.pack(side="left", padx=10)
total_card.pack_propagate(False)
total_title = tk.Label(total_card, text="ESG Total", bg="white", font=("Arial", 12, "bold"))
total_title.pack(pady=10)
total_score = tk.Label(total_card, bg="white", fg="#2e7d32", font=("Arial", 24, "bold"))
total_score.pack()

# Trend card:
trend_card = tk.Frame(cards_frame, bg="white", width=170, height=100, relief="solid", borderwidth=1)
trend_card.pack(side="left", padx=10)
trend_card.pack_propagate(False)
trend_title = tk.Label(trend_card, text="Trend", bg="white", font=("Arial", 12, "bold"))
trend_title.pack(pady=10)
trend_score = tk.Label(trend_card, bg="white", fg="#2e7d32", font=("Arial", 18, "bold"))
trend_score.pack()

# ------------------------------------------------------------------------------------------------

content_frame = tk.Frame(main_frame, bg="#ffffff")
content_frame.pack(fill="both", expand=True, padx=20, pady=20)

company_details_frame = tk.Frame(content_frame, bg="white", width=340, relief="solid", borderwidth=1)
company_details_frame.pack(side="left", fill="y", padx=(0, 10))
company_details_frame.pack_propagate(False)
company_details_title = tk.Label(company_details_frame, text="Company Details", bg="white", font=("Arial", 14, "bold"))
company_details_title.pack(anchor="w", padx=10, pady=10)

""" company_ranking_frame = tk.Frame(content_frame, bg="white", width=320, relief="solid", borderwidth=1)
company_ranking_frame.pack(side="left", fill="y", padx=(0, 10))
company_ranking_frame.pack_propagate(False) """

# --------------- Chart Frame -------------------

chart_frame = tk.Frame(content_frame, bg="white", relief="solid", borderwidth=1)
chart_frame.pack(side="right", fill="both", expand=True)

chart_title = tk.Label(chart_frame, text="Charts / Comparison", bg="white", font=("Arial", 14, "bold"))
chart_title.pack(pady=10)

# ---------------------- output tags ---------------------------------------------------------------------

output_text = tk.Text(
    company_details_frame,
    height=20,
    width=70,
    font=("Consolas", 11),
    bg="white",
    fg="#1f2933"
)

output_text.tag_configure(
    "company",
    font=("Arial", 16, "bold"),
    foreground="#2e7d32"
)
output_text.pack(pady=20)

output_text.tag_configure(
    "year",
    font=("Arial", 12, "bold")
)

output_text.tag_configure(
    "rating_good",
    foreground="green",
    font=("Arial", 11, "bold")
)

output_text.tag_configure(
    "trend",
    foreground="#1565c0",
    font=("Arial", 11, "bold")
)

output_text.tag_configure(
    "line",
    foreground="grey"
)
output_text.tag_configure(
    "excellent",
    foreground="dark green",
    font=("Arial", 11, "bold")
)

output_text.tag_configure(
    "good",
    foreground="green",
    font=("Arial", 11, "bold")
)
output_text.tag_configure(
    "average",
    foreground="orange",
    font=("Arial", 11, "bold")
)

output_text.tag_configure(
    "bad",
    foreground="red",
    font=("Arial", 11, "bold")
)


# ------------------------------------------------------------



















root.mainloop()

