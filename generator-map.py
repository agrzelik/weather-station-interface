from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

wojewodztwa = {
    'KO£UDA WIELKA': 'Kujawsko-Pomorskie',
    'PU£TUSK': 'Mazowieckie',
    'WIELICHOWO': 'Wielkopolskie',
    'KRAKÓW-OBSERWATORIUM': 'Małopolskie',
    'LEGIONOWO': 'Mazowieckie',
    'WARSZAWA-BIELANY': 'Mazowieckie',
    'LIDZBARK WARMIÑSKI': 'Warmińsko-Mazurskie',
    'SZEPIETOWO': 'Podlaskie',
    'PUCZNIEW': 'Łódzkie',
    'PU£AWY': 'Lubelskie',
    'DYNÓW': 'Podkarpackie',
    'SKIERNIEWICE': 'Łódzkie'
}

miasta = {
    'Kołuda Wielka': {'pos': (52.44, 18.08), 'ilosc': 3, 'symbol': 'bo'},
    'Pułtusk': {'pos': (52.42, 21.05), 'ilosc': 3, 'symbol': 'bo'},
    'Wielichowo': {'pos': (52.07, 16.20), 'ilosc': 3, 'symbol': 'bo'},
    'Kraków-obserwatorium': {'pos': (50.03, 19.49), 'ilosc': 3, 'symbol': 'bo'},
    'Legionowo': {'pos': (52.24, 20.56), 'ilosc': 3, 'symbol': 'bo'},
    'Warszawa-Bielany': {'pos': (52.1, 20.52), 'ilosc': 3, 'symbol': 'bo'},
    'Lidzbark Warmiński': {'pos': (54.07, 20.34), 'ilosc': 3, 'symbol': 'bo'},
    'Szepietowo': {'pos': (52.52, 22.32), 'ilosc': 3, 'symbol': 'bo'},
    'Puczniew': {'pos': (51.47, 19.05), 'ilosc': 3, 'symbol': 'bo'},
    'Puławy': {'pos': (51.24, 21.58), 'ilosc': 3, 'symbol': 'bo'},
    'Dynów': {'pos': (49.48, 22.13), 'ilosc': 3, 'symbol': 'bo'},
    'Skierniewice': {'pos': (51.57, 20.08), 'ilosc': 3, 'symbol': 'bo'}
}


def create_map():

    # zakres mapy (Polska)
    lat_min, lat_max = 48.8, 55.0
    lon_min, lon_max = 13.8, 24.4

    # wymiary rysunku
    fig = plt.figure(figsize=(8.4, 7.9))

    # marginesy
    plt.subplots_adjust(left=0.10, right=0.90, top=0.90, bottom=0.10, wspace=0.1, hspace=0.05)

    # tworzenie mapy dla Polski
    map = Basemap(resolution='i', projection='merc', llcrnrlat=lat_min, urcrnrlat=lat_max, llcrnrlon=lon_min, urcrnrlon=lon_max)

    # grubość granic i linii wybrzeży
    map.drawcountries(linewidth=0.5)
    map.drawcoastlines(linewidth=0.5)

    map.drawmapboundary(fill_color='#D8F4FC')
    map.fillcontinents(color='white', lake_color='#D8F4FC')

    map.drawparallels(np.arange(lat_min, lat_max, 1.), labels=[1,0,0,0], color='grey', dashes=[1,5], linewidth=0.2)
    map.drawmeridians(np.arange(lon_min, lon_max, 1.), labels=[0,0,0,1], color='grey', dashes=[1,5], linewidth=0.2)

    map.drawcountries()
    map.drawrivers(color='grey')

    # rysowanie danych
    for nazwa, dane in miasta.items():
        # współrzędne w odwrotnej kolejności
        x, y = map(dane['pos'][1], dane['pos'][0])

        # narysowanie symbolu
        map.plot(x, y, dane['symbol'], markersize=dane['ilosc'])

        # wypisanie etykiety (z przesunięciem)
        plt.text(x+(dane['ilosc']*1200), y+(dane['ilosc']*1100), nazwa)

    return fig


def update_map():
    for widgets in frame.winfo_children():
      widgets.destroy()
    try:
        lat = float(lat_spinbox.get())  # Konwersja na float
        lon = float(lon_spinbox.get())  # Konwersja na float
        miasta['Twoja stacja pogodowa'] = {'pos': (lat, lon), 'ilosc': 3, 'symbol': 'ro'}  # Dodanie stacji do słownika
        # coordinates_list.append((lat, lon))  # Dodawanie współrzędnych do listy
        # listbox.insert(tk.END, f"Szerokość: {lat}, Długość: {lon}")  # Dodanie współrzędnych do listboxa
        #frame = ttk.Frame(root)
        #frame.pack(fill=tk.BOTH, expand=1)
        fig = create_map()
        canvas1 = FigureCanvasTkAgg(fig, master=frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=1)
    except ValueError:
        messagebox.showerror("Błąd", "Proszę wpisać poprawne współrzędne (liczby).")

coordinates_list = []

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Interfejs lokalnej stacji pogodowej")
root.geometry("800x800")  # Zwiększenie rozmiaru okna

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
label2 = tk.Label(root, text="Ten interfejs pozwala na dodawanie i wyświetlanie lokalnych stacji pogodowych na mapie.", font=("Arial", 10), bg=bg_color, fg=fg_color)
label2.pack(pady=(0, 10))

# Tworzenie ramki na pola wejściowe
input_frame = ttk.Frame(root)
input_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

# Tworzenie pola wejściowego dla szerokości geograficznej
lat_label = ttk.Label(input_frame, text="Szerokość geograficzna:")
lat_label.pack(side=tk.LEFT, padx=(10, 5))
lat_spinbox = tk.Spinbox(input_frame, from_=-90.0, to=90.0, increment=0.1, format="%.2f")
lat_spinbox.delete(0,"end")
lat_spinbox.insert(0,52)
lat_spinbox.pack(side=tk.LEFT, padx=(0, 10))

# Tworzenie pola wejściowego dla długości geograficznej
lon_label = ttk.Label(input_frame, text="Długość geograficzna:")
lon_label.pack(side=tk.LEFT, padx=(10, 5))
lon_spinbox = tk.Spinbox(input_frame, from_=-180.0, to=180.0, increment=0.1, format="%.2f")
lon_spinbox.delete(0,"end")
lon_spinbox.insert(0,19.2)
lon_spinbox.pack(side=tk.LEFT, padx=(0, 10))

# Tworzenie przycisku do aktualizacji mapy
update_button = ttk.Button(input_frame, text="Zaktualizuj mapę", command=update_map)
update_button.pack(side=tk.LEFT, padx=(10, 10))

# Tworzenie ramki do osadzenia mapy
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=1)

# Tworzenie mapy i osadzenie jej w ramce
fig = create_map()
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

# Uruchamianie głównej pętli aplikacji
root.mainloop()


