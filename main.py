import tkinter as tk
from tkinter import messagebox
import csv
from vision import plot_data

# Funktion zum Laden der Titel aus der CSV-Datei
def load_titles_from_csv(filename, max_titles=10000):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        titles = [row[0] for row in reader]
        return titles[:max_titles]

def on_listbox_select(event):
    widget = event.widget
    if widget.curselection():
        index = int(widget.curselection()[0])
        value = widget.get(index)
        entry.delete(0, tk.END)
        entry.insert(0, value)
        fetch_and_plot()

def fetch_and_plot():
    keyword = entry.get().strip()
    if not keyword:
        messagebox.showwarning("Warnung", "Bitte geben Sie ein gültiges Keyword ein.")
        return
    success = plot_data(keyword)
    if (success == True):
        print("close diagram")
    elif (success == - 1):
        messagebox.showinfo("Information", "Keine Daten gefunden. Bitte versuchen Sie einen anderen Begriff.")
    elif (success == -2):
        messagebox.showinfo("Warnung", "Google verweigert wieder den Zugriff auf diesen Begriff! Versuchen Sie einen")
    else:
        messagebox.showinfo("Warnung", "Hm...Schwierig!")


# Auto-Vervollständigungsfunktion
def autocomplete(event):
    text = entry.get()
    if text == '':
        listbox.delete(0, tk.END)
        return
    matches = [title for title in titles if title.lower().startswith(text.lower())]
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
entry = tk.Entry(main_frame, font=("Helvetica", 14), width=50, bg="#f0f0f0", fg="black")
entry.pack()

frame_for_listbox = tk.Frame(main_frame, bg="#dddddd", padx=5, pady=5)
frame_for_listbox.pack(padx=5, pady=5)

listbox = tk.Listbox(frame_for_listbox, width=50, bg="#ffffff", fg="black", selectbackground="#a0a0a0", font=("Helvetica", 12))
listbox.pack()

# Laden der Titel
titles = load_titles_from_csv('title.csv')

# Event-Bindung für Auto-Vervollständigung
entry.bind('<KeyRelease>', autocomplete)

# Bindung der Listbox-Selektion an die on_listbox_select Funktion
listbox.bind('<<ListboxSelect>>', on_listbox_select)

# Tkinter-Schleife starten
root.mainloop()
