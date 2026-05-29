# tkinter for GUI components and ttk for advanced widgets like Combobox and Treeview
import tkinter as tk
from tkinter import ttk

# pathlib to handle filesystem paths
from pathlib import Path
# json for loading ESG data from JSON files
import json

# matplotlib integration for displaying charts inside Tkinter frames 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# customtkinter for modern styled Tkinter widgets and UI components
import customtkinter as ctk


from analyzer import Company
from analyzer import Analyzer


# Read JSON file

FILE_NAME = "ESG_DATA.json"

path = Path.cwd() / FILE_NAME

try:
    with path.open(mode="r") as file:
        data = json.load(file)                # Convert JSON data to a Python object
        print("*** Data loaded successfully ***\n")
        print("Number of companies:", len(data))
except FileNotFoundError:
    print(f"{path} does not exist.")
except Exception as e:
    print(f"Unexpected error: {e}")


# Create company objects

company_list = []
for item in data:
    new_company = Company(item["company"], item["data"])
    company_list.append(new_company)

# pass company_list to analyzer
analyzer = Analyzer(company_list)


# Function to show Ranking

def show_ranking(selected_name):

    ranking_list = analyzer.ranking()

    # Delete old lines
    for item in ranking_table.get_children():
        ranking_table.delete(item)

    for i, (name, score) in enumerate(ranking_list, start=1):
        tag = "selected" if name == selected_name else ""
        # insert the new line as normal main line (without parent) at the end of ranking_tabel
        ranking_table.insert("", "end", values=(i, name, f"{score:.2f}"), tags=(tag,))  # insert the new line as normal main line (without parent) at the end of tabel


# Function to show Comparison Chart

def show_comparison_chart():

    company_names= []
    scores =[]

    for company in company_list:
        last_entry = company.data[-1]
        _, _, _, esg_score = Analyzer.calculate_esg_score(last_entry)
        company_names.append(company.name)
        scores.append(esg_score)
    
    # Initialize custom figure
    fig = Figure(figsize=(8,4), dpi=100)      #  Figure size and resolution

    # Adjust the left boundary
    fig.subplots_adjust(left=0.23)            # start at 23 % of the figure's total width, measured from the left margin     
    
    # create a single plotting area for the chart
    ax = fig.add_subplot(111)                         # (row, column, Diagramm) inside the figure

    ax.set_title("Company ESG Comparison", fontsize=9)
    ax.set_xlabel("ESG Score", fontsize=9)
    ax.set_xlim(0, 100)                               # limit for ESG score 0 - 100

    # create horizantal bar plot
    ax.barh(company_names, scores, height=0.40, color="#3BB96D")

    # Create transparent dashed lines
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    
    # Embedding the Matplotlib chart in Tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=comparison_frame)

    # Generate the chart
    canvas.draw()

    # Display the chart in frame  and allow it to resize with the frame
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(5,15))
        

# Show analized Company on Dashboard        

def show_selected_company():
    
    # Get selected company from dropdown
    selected_name = company_dropdown.get()

    for company in company_list:
        if company.name == selected_name:
            
            # Clear previous company details
            output_text.config(state="normal")
            output_text.delete("1.0", tk.END)           
            
            # Display company name as title
            output_text.insert(tk.END, f"{company.name}\n", "company")

            # Show last year ESG values in cards 
            last_entry = company.data[-1]
            
            year_label.config(text=f"Scores shown for: {last_entry['year']}")
            
            env, soc, gov, latest_esg_score = Analyzer.calculate_esg_score(last_entry)

            env_score.config(text=f"{env:.2f}%")
            soc_score.config(text=f"{soc:.2f}")
            gov_score.config(text=f"{gov:.2f}")
            total_score.config(text=f"{latest_esg_score:.2f}")  

            # Determine and display ESG trend
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

            # Display ESG details for each year                 
            for entry in company.data:
                env, soc, gov, esg_score = Analyzer.calculate_esg_score(entry)
                rating = Analyzer.get_rating(esg_score)

                # Apply color tags based on ESG rating
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

            # Update dashboard
            show_trend_chart(company)
            show_ranking(selected_name)
            show_comparison_chart()

            # Make company details read-only
            output_text.config(state="disabled")            

            break

# Show Trend Chart
def show_trend_chart(company):
    
    # Remove previous chart before drawing a new one
    for widget in chart_frame.winfo_children():
        widget.destroy()  

    years = []
    scores = []

    # collect ESG scores for each year
    for entry in company.data:
        _, _, _, esg_score = Analyzer.calculate_esg_score(entry)
        years.append(str(entry["year"]))
        scores.append(esg_score)
    
    # Create matplotlib figure and plotting area
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    # Create ESG trend line chart with circular marker for each data point
    ax.plot(years, scores, marker="o")

    # Configure chart labels and appearance
    ax.set_title(f"ESG Score over Years - {company.name}", fontsize=10)
    ax.set_xlabel("Year")
    ax.set_ylabel("ESG Score")
    ax.grid(True)
    
    # Embed the chart into the Tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)

    canvas.draw()

    # Display the chart in the frame
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(5,15))
    

# GUI window

# Initialize root widget
root = tk.Tk()  
root.title("ESG Data Analyzer")
root.geometry("1400x800")
root.configure(background="#f4f7f5")

# Right Sidebar

sidebar = tk.Frame(root, bg="#ffffff", width=260)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)           # Disable automatic resizing 

title = tk.Label(sidebar, text="ESG Analyzer", bg="#ffffff", font=("Arial", 18, "bold"))
title.pack(pady=30)

# Create ComboBox with Company names

company_names = [company.name for company in company_list]

company_dropdown = ttk.Combobox(sidebar, values=company_names, state="readonly", font=("Arial", 12), width=20)
company_dropdown.pack(pady=10)
company_dropdown.current(0)               # Show first entry in Company_names

# Buttons
analyze_button = tk.Button(sidebar, text="Analyze Company", width=18, height=1, font=("Arial", 11, "bold"), bg="#2673D9", fg="white",
                 activebackground="#b0c1e7", activeforeground="white", relief="flat", bd=0, command=show_selected_company)
analyze_button.pack(pady=10)

analyze_all_button = tk.Button(sidebar, text="Analyze all Companies", width=18, height=1, font=("Arial", 11, "bold"), bg="#2BA664",
                     fg="white", activebackground="#b0c1e7", activeforeground="white", relief="flat", bd=0)
analyze_all_button.pack(pady=10)

show_ranking_button = tk.Button(sidebar, text="Show Ranking", width=18, height=1, font=("Arial", 11, "bold"), bg="#8E67D8", fg="white",
                      activebackground="#b0c1e7", activeforeground="white", relief="flat", bd=0, command=show_ranking)
show_ranking_button.pack(pady=10)

show_trends_button = tk.Button(sidebar, text="Show Trends", width=18, height=1, font=("Arial", 11, "bold"), bg="#03A1AE", fg="white",
                     activebackground="#b0c1e7", activeforeground="white", relief="flat", bd=0)
show_trends_button.pack(pady=10)

refresh_data_button = tk.Button(sidebar, text="Refresh Data", width=18, height=1, font=("Arial", 11, "bold"), bg="#718193", fg="white",
                     activebackground="#b0c1e7", activeforeground="white", relief="flat", bd=0)
refresh_data_button.pack(pady=10)

# Main frame left

main_frame = tk.Frame(root, bg="#ffffff")
main_frame.pack(fill="both", expand=True)

main_title = tk.Label(main_frame, text="Dashboard", bg="#ffffff", font=("Arial", 20, "bold"))
main_title.pack(pady=20)

year_label = tk.Label(main_frame, bg="#ffffff", font=("Arial", 11, "bold"))
year_label.pack(pady=5)

# Cards:
cards_frame = tk.Frame(main_frame, bg="#ffffff")
cards_frame.pack(pady=15)

# Environmental card:
env_card = ctk.CTkFrame(cards_frame, width=170, height=100, fg_color="white", border_width=1, border_color="#eceef3", corner_radius=10)
env_card.pack(side="left", padx=5)
env_card.pack_propagate(False)
env_title = tk.Label(env_card, text="Environmental", bg="white", font=("Arial", 12, "bold"))
env_title.pack(pady=10)
env_score = tk.Label(env_card, text="0.00", bg="white", fg="#3BB96D", font=("Arial", 24, "bold"))   
env_score.pack()

# social card:
soc_card = ctk.CTkFrame(cards_frame, width=170, height=100, fg_color="white", border_width=1, border_color="#e0e2e6", corner_radius=10)
soc_card.pack(side="left", padx=10)
soc_card.pack_propagate(False)
soc_title = tk.Label(soc_card, text="Social", bg="white", font=("Arial", 12, "bold"))
soc_title.pack(pady=10)
soc_score = tk.Label(soc_card, text="0.00", bg="white", fg="#764EC9", font=("Arial", 24, "bold"))
soc_score.pack()

# Governance card:
gov_card = ctk.CTkFrame(cards_frame, width=170, height=100, fg_color="white", border_width=1, border_color="#e0e2e6", corner_radius=10)
gov_card.pack(side="left", padx=10)
gov_card.pack_propagate(False)
gov_title = tk.Label(gov_card, text="Governance", bg="white", font=("Arial", 12, "bold"))
gov_title.pack(pady=10)
gov_score = tk.Label(gov_card, text="0.00", bg="white", fg="#2670DA", font=("Arial", 24, "bold"))
gov_score.pack()

# ESG Total card:
total_card = ctk.CTkFrame(cards_frame, width=170, height=100, fg_color="white", border_width=1, border_color="#e0e2e6", corner_radius=10)
total_card.pack(side="left", padx=10)
total_card.pack_propagate(False)
total_title = tk.Label(total_card, text="ESG Total", bg="white", font=("Arial", 12, "bold"))
total_title.pack(pady=10)
total_score = tk.Label(total_card, text="0.00", bg="white", fg="#708192", font=("Arial", 24, "bold"))
total_score.pack()

# Trend card:
trend_card = ctk.CTkFrame(cards_frame, width=170, height=100, fg_color="white", border_width=1, border_color="#e0e2e6", corner_radius=10)
trend_card.pack(side="left", padx=10)
trend_card.pack_propagate(False)
trend_title = tk.Label(trend_card, text="Trend", bg="white", font=("Arial", 12, "bold"))
trend_title.pack(pady=10)
trend_score = tk.Label(trend_card, bg="white", fg="#E3791D", font=("Arial", 18, "bold"))
trend_score.pack()

# Content Frame (output)

content_frame = tk.Frame(main_frame, bg="#ffffff")
content_frame.pack(fill="both", expand=True, padx=20, pady=20)

for i in range(2):
    content_frame.grid_rowconfigure(i, weight=1, uniform="row")
    content_frame.grid_columnconfigure(i, weight=1, uniform="cols")

# Company details frame
details_frame = ctk.CTkFrame(content_frame, fg_color="white", border_width=1, border_color="#e0e2e6", corner_radius=10)
details_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
details_title =ctk.CTkLabel(details_frame, text="Company Details", font=("Arial", 14, "bold"))
details_title.pack(pady=10)

# Ranking frame
ranking_frame = ctk.CTkFrame(content_frame,fg_color="white", border_width=1, border_color="#e0e2e6", corner_radius=10)
ranking_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
ranking_title = ctk.CTkLabel(ranking_frame, text="Company Ranking", font=("Arial", 14, "bold"))
ranking_title.pack(pady=10)

# Comparison frame
comparison_frame = ctk.CTkFrame(content_frame,fg_color="white", border_width=1, border_color="#e0e2e6", corner_radius=10)
comparison_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
comparison_frame_title = ctk.CTkLabel(comparison_frame, text="Comparisons", font=("Arial", 14, "bold"))
comparison_frame_title.pack(pady=10)

# Trend chart frame
chart_frame= ctk.CTkFrame(content_frame,fg_color="white", border_width=1, border_color="#e0e2e6", corner_radius=10)
chart_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
chart_title = ctk.CTkLabel(chart_frame, text="Charts", font=("Arial", 14, "bold"))
chart_title.pack(pady=10)

# Company Details Output:
output_text = tk.Text(details_frame, font=("Consolas", 11), bg="white", fg="#1f2933", relief="flat", borderwidth=0)

# Text formatting tags
output_text.tag_configure("company", font=("Arial", 16, "bold"), foreground="#2e7d32")
output_text.tag_configure("year", font=("Arial", 12, "bold"))
output_text.tag_configure("rating_good", foreground="green", font=("Arial", 11, "bold"))
output_text.tag_configure("trend", foreground="#1565c0", font=("Arial", 11, "bold"))
output_text.tag_configure("line", foreground="grey")

# ESG rating color tags
output_text.tag_configure("excellent", foreground="dark green", font=("Arial", 11, "bold"))
output_text.tag_configure("good", foreground="green", font=("Arial", 11, "bold"))
output_text.tag_configure("average", foreground="orange", font=("Arial", 11, "bold"))
output_text.tag_configure("bad", foreground="red", font=("Arial", 11, "bold"))

output_text.pack(fill="both", expand=True, padx=12, pady=(0, 12))

# Ranking table:
# Configure Treeview style
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", borderwidth=0, relief="flat", rowheight=30)

# Remove default Treeview border
style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

# Configure table header style
style.configure("Treeview.Heading", background="white", foreground="#1f2933", font=("Arial", 10, "bold"), relief="flat")

# Ranking table displaying company ESG scores
ranking_table = ttk.Treeview(ranking_frame, columns=("rank", "company", "score"), show="headings", height=5)

# Define table column headings
ranking_table.heading("rank", text="Rank")
ranking_table.heading("company", text="Company")
ranking_table.heading("score", text="ESG Score")

# Configure column width and alignment
ranking_table.column("rank", width=60, anchor="center")
ranking_table.column("company", width=220)
ranking_table.column("score", width=100, anchor="center")

# Highlight the selected company in the ranking
ranking_table.tag_configure("selected", background="#d8f3dc", foreground="#1b7f35")

ranking_table.pack(fill="both", expand=True, padx=10, pady=10)


root.mainloop()


