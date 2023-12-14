import tkinter as tk
from tkinter import messagebox
import csv

# Funktion zum Laden der Titel aus der CSV-Datei
from vision import plot_data


def load_titles_from_csv(filename, max_titles=10000):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        titles = [row[0] for row in reader]
        return titles[:max_titles]

def on_listbox_select(event):
    # Holt den ausgewählten Text aus der Listbox
    widget = event.widget
    if widget.curselection():
        index = int(widget.curselection()[0])
        value = widget.get(index)
        entry.delete(0, tk.END)
        entry.insert(0, value)
        fetch_and_plot()  # Führt die Suchfunktion aus mit dem ausgewählten Titel

def fetch_and_plot():
    keyword = entry.get().strip()  # Entfernt führende und abschließende Leerzeichen
    if not keyword:  # Überprüft, ob das Eingabefeld leer ist
        messagebox.showwarning("Warnung", "Bitte geben Sie ein gültiges Keyword ein.")
        return
    success = plot_data(keyword)
    if not success:
        messagebox.showinfo("Information", "Keine Daten gefunden. Bitte versuchen Sie einen anderen Begriff.")


# Auto-Vervollständigungsfunktion
def autocomplete(entry_widget, titles_list, listbox):
    text = entry_widget.get()
    if text == '':
        listbox.delete(0, tk.END)
        return
    matches = [title for title in titles_list if title.lower().startswith(text.lower())]
    listbox.delete(0, tk.END)
    for match in matches:
        listbox.insert(tk.END, match)



# Initialisieren des Tkinter-Fensters
root = tk.Tk()
root.title("Data Visualizer")
root.state('zoomed')

# Haupt-Frame
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(padx=10, pady=10)

# Beschriftung
label = tk.Label(main_frame, text="Geben Sie ein Keyword ein:", font=("Arial", 14))
label.pack(pady=(0, 10))

# Eingabefeld und Listbox
entry = tk.Entry(main_frame, font=("Arial", 12), width=50)
entry.pack()

listbox = tk.Listbox(main_frame, width=50)
listbox.pack()

# Laden der Titel
titles = load_titles_from_csv('title.csv')

# Event-Bindung für Auto-Vervollständigung
entry.bind('<KeyRelease>', lambda event: autocomplete(entry, titles, listbox))

# Bindung der Listbox-Selektion an die on_listbox_select Funktion
listbox.bind('<<ListboxSelect>>', on_listbox_select)

# Tkinter-Schleife starten
root.mainloop()
