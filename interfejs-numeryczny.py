import tkinter as tk
from tkinter import ttk
import pandasql as psql
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tkinter import scrolledtext


df = pd.read_csv('lepsze_dane_klimatyczne_inter.csv')
df = df.drop(columns=["Unnamed: 0", "Kod stacji", "Data"])
df
df['Nazwa stacji'].unique()

# Nowe nazwy stacji do zamiany
nowe_stacje = {
    'KO£UDA WIELKA': 'Kołuda Wielka',
    'PU£TUSK': 'Pułtusk',
    'WIELICHOWO': 'Wielichowo',
    'KRAKÓW-OBSERWATORIUM': 'Kraków-obserwatorium',
    'LEGIONOWO': 'Legionowo',
    'WARSZAWA-BIELANY': "Warszawa-Bielany",
    'LIDZBARK WARMIÑSKI': "Lidzbark Warmiński",
    'SZEPIETOWO': "Szepietowo",
    'PUCZNIEW': "Puczniew",
    'PU£AWY': "Puławy",
    'DYNÓW': "Dynów",
    'SKIERNIEWICE': "Skierniewice"   
}

# Zamiana nazw stacji w ramce danych
df['Nazwa stacji'] = df['Nazwa stacji'].replace(nowe_stacje)

df_result = pd.DataFrame()

#print(df)

def build_query():
    selected_year = year_combobox.get()
    selected_month = month_combobox.get()
    selected_stations = station_combobox.get()
    
    query = "SELECT `Nazwa stacji`, Rok, `Miesiąc`, AVG(`Absolutna temperatura maksymalna (C)`) AS `Średnia absolutna temperatura maksymalna (C)`, \
                    AVG(`Średnia temperatura maksymalna (C)`) AS `Średnia temperatura maksymalna (C)`, \
                    AVG(`Absolutna temperatura minimalna`) AS `Średnia absolutna temperatura minimalna`, \
                    AVG(`Średnia temperatura minimalna`) AS `Średnia temperatura minimalna`, \
                    AVG(`Średnia temperatura miesięczna`) AS `Średnia temperatura miesięczna` FROM df WHERE 1=1"

    if selected_year != "Wszystkie":
        query += f" AND Rok = '{selected_year}'"
        
    if selected_month != "Wszystkie":
        month_mapping = {
            "Styczeń": 1, "Luty": 2, "Marzec": 3, "Kwiecień": 4,
            "Maj": 5, "Czerwiec": 6, "Lipiec": 7, "Sierpień": 8,
            "Wrzesień": 9, "Październik": 10, "Listopad": 11, "Grudzień": 12
        }
        selected_month_num = month_mapping[selected_month]
        query += f" AND Miesiąc = {selected_month_num}"
    
    if selected_stations != "Wszystkie":
        selected_stations_list = selected_stations.split(", ")
        if len(selected_stations_list) == 1:
            query += f" AND `Nazwa stacji` = '{selected_stations_list[0]}'"
        else:
            stations_str = "', '".join(selected_stations_list)
            query += f" AND `Nazwa stacji` IN ('{stations_str}')"
    
    query_text.delete(1.0, tk.END)  # Clear previous query text
    query_text.insert(tk.END, query)  # Insert new SQL query into text widget

def run_query():
    global df_result
    query = query_text.get(1.0, tk.END)  # Get SQL query from text widget
    df_result = psql.sqldf(query)
    # Update widoku treeview
    update_treeview()
    #print(df_result)


def update_treeview():
    print(df_result)
    # Tworzenie widżetu Treeview
    tree.delete(*tree.get_children())

    # Definiowanie kolumn
    tree["columns"] = list(df_result.columns)
    tree["show"] = "headings"

    # Dodawanie kolumn
    for column in df_result.columns:
        tree.heading(column, text=column)

    # Dodawanie wierszy
    for index, row in df_result.iterrows():
        tree.insert("", "end", values=list(row))

    # # Tworzenie suwaka pionowego
    # vsb = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
    # tree.configure(yscrollcommand=vsb.set)
    # vsb.pack(side=tk.RIGHT, fill=tk.Y)

    # # Tworzenie suwaka poziomego
    # hsb = ttk.Scrollbar(tree, orient="horizontal", command=tree.xview)
    # tree.configure(xscrollcommand=hsb.set)
    # hsb.pack(side=tk.BOTTOM, fill=tk.X)

    # Ustawianie widżetu Treeview na ekranie
    tree.pack(padx=10, pady=10, fill="both", expand=True)


# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Interfejs lokalnej stacji pogodowej")
root.geometry("1500x600")  # Zwiększenie rozmiaru okna

# Ustawianie stylu i kolorów
bg_color = "#FFFFFF"  # Jasny kolor tła
fg_color = "#01579B"  # Ciemny kolor tekstu
button_color = "#0288D1"  # Zielony kolor przycisku
button_fg_color = "#FFFFFF"  # Biały kolor tekstu przycisku
root.configure(bg=bg_color)

# Dodawanie etykiety
label = tk.Label(root, text="Witaj w interfejsie dla lokalnych stacji pogodowych. ", font=("Arial", 12), bg=bg_color, fg=fg_color)
label.pack(pady=20)

# Dodawanie dodatkowych etykiet
label2 = tk.Label(root, text="Ten interfejs pozwala na wyświetlanie średnich wartości parametrów pogodowych dla wybranych stacji, lat i miesięcy.", font=("Arial", 10), bg=bg_color, fg=fg_color)
label2.pack(pady=(0, 10))

# Tworzenie ramki na pola wejściowe
input_frame = ttk.Frame(root)
input_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

# Tworzenie pola wejściowego dla roku
year_label = ttk.Label(input_frame, text="Wybierz rok:")
year_label.pack(side=tk.LEFT, padx=(10, 5))

# Lista lat od 1951 do 2023 z opcją "All"
years = ["Wszystkie"] + [str(year) for year in range(1951, 2023 + 1)]

# Tworzenie listy rozwijanej dla wyboru roku
year_combobox = ttk.Combobox(input_frame, values=years)
year_combobox.current(0)  # Ustawienie domyślnej wartości na "All"
year_combobox.pack(side=tk.LEFT, padx=(0, 10))

# Dodanie zdarzenia na zmianę wyboru
# year_combobox.bind("<<ComboboxSelected>>", build_query)

# Tworzenie pola wejściowego dla miesiąca
month_label = ttk.Label(input_frame, text="Wybierz miesiąc:")
month_label.pack(side=tk.LEFT, padx=(10, 5))

# Lista miesięcy po polsku z opcją "Wszystkie"
months = ["Wszystkie", "Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec",
          "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"]

# Tworzenie listy rozwijanej dla wyboru miesiąca
month_combobox = ttk.Combobox(input_frame, values=months)
month_combobox.current(0)  # Ustawienie domyślnej wartości na "Wszystkie"
month_combobox.pack(side=tk.LEFT, padx=(0, 10))

# Dodanie zdarzenia na zmianę wyboru
# month_combobox.bind("<<ComboboxSelected>>", build_query)

# Tworzenie etykiety dla wyboru stacji
station_label = ttk.Label(input_frame, text="Wybierz stacje:")
station_label.pack(side=tk.LEFT, padx=(10, 5))

# Lista stacji z opcją "Wszystkie"
stations = ["Kołuda Wielka", "Pułtusk", "Wielichowo", "Kraków-obserwatorium", 
            "Legionowo", "Warszawa-Bielany", "Lidzbark Warmiński", "Szepietowo", "Puczniew", 
            "Puławy", "Dynów", "Skierniewice", "Wszystkie"]

# Tworzenie listy rozwijanej dla wyboru stacji z możliwością wielokrotnego wyboru
station_combobox = ttk.Combobox(input_frame, values=stations)
station_combobox.set("Wszystkie")  # Ustawienie domyślnej wartości na "Wszystkie"
station_combobox.pack(side=tk.LEFT, padx=(0, 10))

# Dodanie zdarzenia na zmianę wyboru
# month_combobox.bind("<<ComboboxSelected>>", build_query)

# Tworzenie pola tekstowego dla zapytania SQL
query_text = tk.Text(root, height=4, width=100)
query_text.pack(pady=(10, 20))

# Tworzenie przycisku do budowania zapytania SQL
build_query_button = ttk.Button(input_frame, text="Zbuduj Query", command=build_query)
build_query_button.pack(side=tk.LEFT, padx=(0, 10))

# Tworzenie przycisku do wyszukania zapytania SQL
build_query_button = ttk.Button(input_frame, text="Zastosuj Query", command=run_query)
build_query_button.pack(side=tk.LEFT, padx=(0, 10))

# Tworzenie widżetu Treeview
tree = ttk.Treeview(root)

# Definiowanie kolumn
tree["columns"] = list(df.columns)
tree["show"] = "headings"

# Dodawanie kolumn
for column in df.columns:
    tree.heading(column, text=column)

# Dodawanie wierszy
for index, row in df.iterrows():
    tree.insert("", "end", values=list(row))

# Tworzenie suwaka pionowego
vsb = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.pack(side=tk.RIGHT, fill=tk.Y)

# Tworzenie suwaka poziomego
hsb = ttk.Scrollbar(tree, orient="horizontal", command=tree.xview)
tree.configure(xscrollcommand=hsb.set)
hsb.pack(side=tk.BOTTOM, fill=tk.X)

# Ustawianie widżetu Treeview na ekranie
tree.pack(padx=10, pady=10, fill="both", expand=True)

# Uruchamianie głównej pętli aplikacji
root.mainloop()